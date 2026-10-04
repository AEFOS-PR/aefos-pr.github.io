# Atualização automática dos dados (SIG do CREA-PR)

O dashboard puxa parte dos números **automaticamente** do SIG do CREA-PR
(serviços públicos ArcGIS), sem ninguém precisar mexer.

## O que atualiza sozinho (vem do SIG)
Modalidade **Engenharia Florestal**, ano mais recente disponível:
- Profissionais por Regional (gráfico) e total
- ARTs por Regional (gráfico) e total
- Produtividade (ARTs por profissional) por Regional
- Gênero (masculino/feminino) e Registro/Visto
- Recorte AEFOS: 156 / 899, 7,1% / 20,5%, 5,8 ARTs/prof — recalculados a cada atualização
- A data de "Atualizado em ..." no topo

## O que continua manual (dados internos do Defis)
Não têm API pública — só mudam quando o CREA reenvia os números:
- Fiscalização (ações, autos, regularizações, denúncias)
- Câmara Especializada (processos)
- Distribuição por tipo de ART e média de ARTs por profissional
- Ranking de serviços técnicos
- As séries históricas 2021–2026 de profissionais e ARTs (base "título" do Defis)
- Os totais-título 2.108 profissionais / 4.530 ARTs (base Defis)

Para atualizar esses, basta pedir ao Claude com os novos números.

## Como a automação funciona
1. `automacao/update_sig.py` consulta os serviços do SIG e gera o arquivo `sig_data.js`.
2. `dashboard.html` carrega `sig_data.js` e usa esses valores nos gráficos e KPIs.
3. O GitHub Action `.github/workflows/atualizar-dados.yml` roda o script
   **todo dia** (06h de Brasília), e se houver mudança, publica sozinho.

Endpoints usados (públicos, sem login):
- Profissionais: `sig.crea-pr.org.br/arcgis/rest/services/SIGCREA.Profissional/Profissionais_titulo/MapServer/0`
- ARTs: `sig.crea-pr.org.br/arcgis/rest/services/SIGCREA.ART/art_titulo/MapServer/0`
- Filtro da modalidade florestal: `CODMOD=10 AND TITULO='*TODOS'`

## Rodar manualmente (opcional, no seu PC)
```
pip install requests
python automacao/update_sig.py
```
Isso regenera `sig_data.js` com os dados do dia.

## Publicar o site com atualização automática (grátis) — GitHub Pages
1. Crie uma conta gratuita em github.com.
2. Crie um repositório novo (ex.: `site-aefos`), público.
3. Envie **todo o conteúdo desta pasta** para o repositório
   (index.html, dashboard.html, sig_data.js, assets/, automacao/, .github/).
4. No repositório: **Settings → Pages → Build and deployment → Deploy from a branch →
   Branch: main / (root) → Save.** O site fica no ar em poucos minutos
   (`https://SEU-USUARIO.github.io/site-aefos`).
5. A rotina de atualização roda sozinha todo dia. Para rodar na hora:
   aba **Actions → "Atualizar dados do SIG" → Run workflow**.
6. Domínio próprio: **Settings → Pages → Custom domain** (ex.: `aefos.org.br`).

> Dica: para mudar a frequência, edite a linha `cron:` em
> `.github/workflows/atualizar-dados.yml` (ex.: `0 9 * * 1` = só às segundas).
