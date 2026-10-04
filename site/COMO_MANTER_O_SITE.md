# Como manter e organizar o site da AEFOS
*Manual de manutenção — leia isto primeiro. Qualquer pessoa consegue cuidar do site seguindo este guia.*
*Última atualização: 11/09/2026.*

---

## 1. O essencial (o que é e onde fica)
- **Site:** https://aefos.com.br — site institucional da AEFOS (Associação dos Engenheiros Florestais do Oeste e Sudoeste do Paraná).
- **Hospedagem:** GitHub Pages (grátis). Repositório: **AEFOS-PR/aefos-pr.github.io** → https://github.com/AEFOS-PR/aefos-pr.github.io
- **Domínio:** aefos.com.br (registrado no Registro.br, apontando pro GitHub). O arquivo `CNAME` guarda esse domínio — **não apague**.
- **Pasta de trabalho no computador:** `…/Documentos/Neofloresta/AEFOS/site`
  Essa pasta é a **cópia oficial** do site. É só ela que vira o site no ar.

> **Como funciona, em 1 frase:** você edita os arquivos da pasta `site/` → sobe eles no GitHub → em ~1 minuto o aefos.com.br atualiza sozinho.

---

## 2. O que tem dentro da pasta `site/`
- `index.html` → página inicial (Início, Sobre, Diretoria, Notícias, Documentos).
- `dashboard.html` → o **Painel de dados** (gráficos e números). O botão "Painel de dados" do site abre este arquivo — **o nome tem que ser exatamente `dashboard.html`**.
- `sig_data.js` → os **números** que aparecem no painel (profissionais, ARTs, etc.). É o arquivo que muda quando atualizamos os dados.
- `assets/` → logo, favicon, foto do evento, estatuto em PDF.
- `automacao/` → script e explicação de como os dados são coletados do SIG.
- `.github/workflows/` → o "robô" de atualização automática (hoje **desligado/quebrado**, ver seção 6).
- `CNAME` → o domínio aefos.com.br.
- `README.txt` / este manual.

---

## 3. Regra de ouro da organização
**A pasta `site/` contém SÓ o website.** Tudo que é material de evento, patrocínio, documentos, cartazes, listas etc. fica **FORA** dela — nas outras pastas da AEFOS (`2026/`, `Logomarcas/`, etc.). Nunca misturar. Assim o site fica sempre limpo e fácil de publicar.

Estrutura recomendada da pasta AEFOS:
- `site/` → o website (esta é a pasta que se vincula ao Claude e se publica).
- `_historico/` → versões antigas do site (só memória).
- `2026/`, `Logomarcas/`, PDFs, listas… → materiais de projeto (não entram no site).

---

## 4. Como PUBLICAR uma alteração (colocar no ar)
Sempre que algum arquivo da pasta `site/` mudar, faça isto:

1. Entre **logado** no GitHub e abra a tela de upload (link direto):
   **https://github.com/AEFOS-PR/aefos-pr.github.io/upload/main**
   (login com a conta do GitHub da AEFOS-PR).
2. Abra a pasta `site/` no computador e **arraste os arquivos que você mudou** para a área "Drag files here". Arquivos de mesmo nome são substituídos automaticamente.
3. Embaixo, escreva uma mensagem curta (ex.: "Atualiza dados set/2026"), deixe marcado **"Commit directly to the main branch"** e clique em **Commit changes / Confirmar alterações**.
4. Espere ~1 minuto, abra **aefos.com.br** e aperte **Ctrl+Shift+R** (atualização forçada) pra ver a mudança.

⚠️ **Atenção ao Google Tradutor:** se o navegador estiver traduzindo a página do GitHub, os nomes aparecem traduzidos **só na tela** — `dashboard.html` vira "painel.html", `assets` vira "ativos", `automacao` vira "autômato". **Isso é normal e não muda os arquivos.** Para ver os nomes reais, clique no ícone do tradutor → "Mostrar original".

---

## 5. Como ATUALIZAR OS DADOS do painel (números)
Os números do painel vêm de **duas fontes**:

**A) SIG CREA-PR** (dados públicos, atualizáveis) → profissionais, ARTs, por regional, série por ano, top municípios, recorte AEFOS, gênero, produtividade.
**B) Defis/CREA-PR** (relatório manual) → fiscalização, Câmara Especializada, tipos de ART, ranking de serviços, e o total "ARTs em 2026 (parcial)" do topo. **Só mudam com um novo relatório Defis.**

O robô que atualizaria o SIG sozinho **não funciona** (o servidor do SIG bloqueia os servidores do GitHub). Por isso a atualização é **sob demanda**, feita pelo Claude:

1. Vincule a pasta `site` (ou a pasta AEFOS) à sessão do Claude.
2. Peça: **"faz uma rodada de atualização dos dados"**.
3. O Claude puxa os números atuais do SIG, recalcula, e atualiza na pasta `site/` os arquivos **`sig_data.js`**, **`dashboard.html`** e **`index.html`**.
4. Você publica esses arquivos no GitHub (seção 4).

> Detalhes técnicos das consultas ao SIG (endpoints, filtros, campos) estão no documento do projeto **`automacao_sig_crea.md`** e no arquivo `automacao/COMO_FUNCIONA.md`.

---

## 6. Trabalhando com o Claude (para qualquer pessoa)
- No app do Claude no computador, **vincule a pasta `site`** (ou a pasta AEFOS) a este projeto. Pronto — o Claude lê e edita os arquivos direto.
- Fale em linguagem simples o que quer ("atualiza os dados", "adiciona uma seção de patrocinadores", "troca a foto do evento"). O Claude edita os arquivos na pasta; **você faz a publicação no GitHub** (seção 4).
- Este projeto do Claude ("SIte AEFOS") guarda a memória: estrutura, dados consolidados, histórico da AEFOS e como a automação funciona.

**Pendência opcional:** desligar o robô quebrado no GitHub para parar de acumular falhas — aba **Actions** → **"Atualizar dados do SIG"** → botão **"…"** → **Disable workflow**.

---

## 7. Estado atual dos dados (atualizar a cada rodada)
**Publicado em 11/09/2026:**
- Profissionais (Eng. Florestal no PR): **2.206**
- ARTs florestais no PR (2026): **5.794**
- Território AEFOS (Cascavel + Pato Branco): **158 profissionais · 1.166 ARTs · 7,2% dos profissionais · 20,1% das ARTs · 7,4 ARTs por profissional**
- Destaque: **Dois Vizinhos é o 4º município do PR** em ARTs florestais (171); 5 cidades do raio AEFOS no Top 20.

*(Quando fizer uma nova rodada, o Claude atualiza estes números aqui também.)*

---

## 8. Guia rápido de problemas
- **"O site não abre":** confira se digitou **aefos.com.br** por extenso (com o ponto). Digitar "aefospr" não funciona. Dica: use o QR code, que leva direto.
- **Nomes de arquivo estranhos no GitHub ("painel", "ativos", "autômato"):** é o Google Tradutor (seção 4). Ignore ou clique em "Mostrar original".
- **Publiquei e não mudou:** espere 1 min e recarregue com Ctrl+Shift+R (cache do navegador).
- **Dados do painel parados:** peça ao Claude "faz uma rodada de atualização" (seção 5).
