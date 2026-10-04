#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza os dados do dashboard da AEFOS a partir do SIG do CREA-PR (ArcGIS REST).

Gera ../sig_data.js (window.SIG_DATA = {...}) com:
  - Profissionais (título Eng. Florestal): total + registro/visto + gênero,
    série histórica estratificada e por regional.
  - ARTs (modalidade florestal): total, por regional e top municípios.
  - Recorte AEFOS (Cascavel + Pato Branco) e produtividade.

Dependência:  pip install requests      |  Rode:  python update_sig.py
"""

import json, sys, time, datetime, os

try:
    import requests
except ImportError:
    sys.exit("Instale a dependência:  pip install requests")

BASE = "https://sig.crea-pr.org.br/arcgis/rest/services"
PROF = f"{BASE}/SIGCREA.Profissional/Profissionais_titulo/MapServer/0/query"
ART  = f"{BASE}/SIGCREA.ART/art_titulo/MapServer/0/query"

# Profissionais: título "Eng. Florestal" (bate com o Defis "engenheiros florestais").
PROF_WHERE = "TITULO='ENG. FLORESTAL' AND CODMOD<>0"
# ARTs: modalidade florestal (CODMOD=10), linha agregada por título.
ART_WHERE  = "CODMOD=10 AND TITULO='*TODOS'"
AEFOS = {"CASCAVEL", "PATO BRANCO"}

session = requests.Session()
session.headers.update({"User-Agent": "AEFOS-dashboard-updater/2.0"})


def q(url, where, stats=None, group=None, order=None):
    params = {"f": "json", "where": where, "returnGeometry": "false",
              "spatialRel": "esriSpatialRelIntersects", "outFields": "*"}
    if stats: params["outStatistics"] = json.dumps(stats)
    if group: params["groupByFieldsForStatistics"] = group
    if order: params["orderByFields"] = order
    last = None
    for i in range(6):
        try:
            r = session.get(url, params=params, timeout=40)
            if r.status_code == 200:
                d = r.json()
                if "error" not in d:
                    return d.get("features", [])
                last = d["error"]
            else:
                last = f"HTTP {r.status_code}"
        except Exception as e:
            last = str(e)
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"Falha ({where}) -> {last}")


def S(*fields):
    return [{"onStatisticField": f, "outStatisticFieldName": f.lower(), "statisticType": "sum"} for f in fields]


def titulo(n):
    return " ".join(w.capitalize() for w in n.split())


def main():
    log = lambda m: print(f"[SIG] {m}")

    ano = int(q(PROF, PROF_WHERE, stats=[{"onStatisticField": "ANO", "outStatisticFieldName": "v",
                                          "statisticType": "max"}])[0]["attributes"]["v"])
    log(f"Ano: {ano}")

    # --- Profissionais: série estratificada (últimos 6 anos) ---
    serie = []
    for f in q(PROF, PROF_WHERE, stats=S("TOTAL", "REGISTRO", "VISTO"), group="ANO", order="ANO asc"):
        a = f["attributes"]
        serie.append({"y": str(int(a["ANO"])), "total": int(a["total"] or 0),
                      "reg": int(a["registro"] or 0), "vis": int(a["visto"] or 0)})
    serie = [s for s in serie if int(s["y"]) >= ano - 5]

    # --- Profissionais por regional (ano atual): total/registro/visto/gênero ---
    preg = {}
    for f in q(PROF, PROF_WHERE + f" AND ANO={ano}", stats=S("TOTAL", "REGISTRO", "VISTO", "MASCULINO", "FEMININO"),
               group="REGIONAL", order="REGIONAL asc"):
        a = f["attributes"]
        preg[a["REGIONAL"]] = {"t": int(a["total"] or 0), "r": int(a["registro"] or 0), "v": int(a["visto"] or 0),
                               "m": int(a["masculino"] or 0), "f": int(a["feminino"] or 0)}

    prof_total = sum(x["t"] for x in preg.values())
    prof_reg = sum(x["r"] for x in preg.values())
    prof_vis = sum(x["v"] for x in preg.values())
    prof_m = sum(x["m"] for x in preg.values())
    prof_f = sum(x["f"] for x in preg.values())
    log(f"Profissionais {ano}: {prof_total} (reg {prof_reg} / visto {prof_vis}); M {prof_m} F {prof_f}")

    byRegional = sorted(
        [{"k": titulo(k), "t": x["t"], "r": x["r"], "v": x["v"], "a": (k.upper() in AEFOS)} for k, x in preg.items()],
        key=lambda d: -d["t"])

    # --- ARTs por regional + top municípios (ano atual) ---
    def art_group(dim):
        out = {}
        for f in q(ART, ART_WHERE + f" AND ANO={ano}", stats=S("TOTAL"), group=dim, order=f"{dim} asc"):
            a = f["attributes"]
            out[a[dim]] = int(a["total"] or 0)
        return out

    areg = art_group("REGIONAL")
    art_total = sum(areg.values())

    # Top municípios (com regional -> marca as cidades do raio AEFOS em "a")
    muns = []
    for f in q(ART, ART_WHERE + f" AND ANO={ano}", stats=S("TOTAL"),
               group="MUNICIPIO,REGIONAL", order="MUNICIPIO asc"):
        a = f["attributes"]
        muns.append({"k": titulo(a["MUNICIPIO"]), "v": int(a["total"] or 0),
                     "a": (str(a.get("REGIONAL") or "").upper() in AEFOS)})
    muns.sort(key=lambda d: -d["v"])
    top_mun = muns[:20]
    log(f"ARTs {ano}: {art_total}")

    art_by = sorted([{"k": titulo(k), "v": v, "a": (k.upper() in AEFOS)} for k, v in areg.items()], key=lambda d: -d["v"])

    # --- Recorte AEFOS ---
    aef = {k: v for k, v in preg.items() if k.upper() in AEFOS}
    a_prof = sum(x["t"] for x in aef.values())
    a_reg = sum(x["r"] for x in aef.values())
    a_vis = sum(x["v"] for x in aef.values())
    a_m = sum(x["m"] for x in aef.values())
    a_f = sum(x["f"] for x in aef.values())
    a_art = sum(v for k, v in areg.items() if k.upper() in AEFOS)

    prod = []
    for k, v in areg.items():
        p = preg.get(k, {}).get("t", 0)
        if p:
            prod.append({"k": titulo(k), "v": round(v / p, 1), "a": (k.upper() in AEFOS)})
    prod.sort(key=lambda d: -d["v"])

    data = {
        "ano": ano,
        "atualizadoEm": datetime.date.today().isoformat(),
        "prof": {
            "total": prof_total, "registro": prof_reg, "visto": prof_vis, "masc": prof_m, "fem": prof_f,
            "serie": serie, "byRegional": byRegional,
        },
        "art": {"total": art_total, "byRegional": art_by,
                "topMunicipios": top_mun},
        "aefos": {
            "prof": a_prof, "registro": a_reg, "visto": a_vis, "art": a_art, "masc": a_m, "fem": a_f,
            "pctProf": round(a_prof / prof_total * 100, 1) if prof_total else 0,
            "pctArt": round(a_art / art_total * 100, 1) if art_total else 0,
            "prod": prod,
            "aefosProd": round(a_art / a_prof, 1) if a_prof else 0,
            "estadualProd": round(art_total / prof_total, 1) if prof_total else 0,
            "cascavelProf": preg.get("CASCAVEL", {}).get("t", 0), "patoProf": preg.get("PATO BRANCO", {}).get("t", 0),
            "cascavelArt": areg.get("CASCAVEL", 0), "patoArt": areg.get("PATO BRANCO", 0),
        },
    }

    out = os.path.join(os.path.dirname(__file__), "..", "sig_data.js")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("/* Gerado automaticamente por automacao/update_sig.py a partir do SIG CREA-PR. Não editar à mão. */\n")
        fh.write("window.SIG_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
    log(f"Escrito: {os.path.abspath(out)}")
    log(f"AEFOS: {a_prof} prof (reg {a_reg}/visto {a_vis}) · {a_art} ARTs · {data['aefos']['aefosProd']} ARTs/prof")


if __name__ == "__main__":
    main()
