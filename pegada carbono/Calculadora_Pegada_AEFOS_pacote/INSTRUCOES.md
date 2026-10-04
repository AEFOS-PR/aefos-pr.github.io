# Calculadora de pegada de carbono, instruções de publicação

Pacote para subir no repositório `AEFOS-PR/aefos-pr.github.io`.
Versão 2.0, 01/10/2026.

---

## O que vai no site

| Arquivo | Onde fica no repositório |
|---|---|
| `pegada-7k3m9x.html` | dentro da pasta `validacao/`, criar a pasta |
| `robots.txt` | na raiz do repositório |

Endereço final, depois de publicado:

**https://aefos.com.br/validacao/pegada-7k3m9x.html**

Esse é o link para mandar ao professor.

---

## Como a página fica oculta

Três camadas, todas já configuradas nos arquivos:

1. **Caminho não óbvio.** Pasta `validacao/` e nome com sufixo aleatório. Ninguém chega nela digitando um endereço provável.
2. **Bloqueio de buscadores.** A página traz `noindex, nofollow, noarchive, nosnippet` no cabeçalho, e o `robots.txt` bloqueia a pasta inteira.
3. **Sem link de entrada.** Nenhuma página do site aponta para ela. Conferido em `index.html`, `circuito.html` e no rodapé.

Quem tiver o link abre normalmente. Quem navegar pelo site não encontra.

**Ressalva honesta:** o repositório é público. Quem abrir o GitHub da AEFOS vê o arquivo lá na listagem. Isso é "não divulgado", não é "secreto". Para um material de validação técnica isso não é problema, mas convém você saber.

---

## Caminho A, pela interface web do GitHub

O mais rápido. Não precisa instalar nada.

### Passo 1, criar a página

1. Abra `https://github.com/AEFOS-PR/aefos-pr.github.io`
2. Botão **Add file**, depois **Create new file**
3. No campo do nome do arquivo, digite exatamente:
   ```
   validacao/pegada-7k3m9x.html
   ```
   Ao digitar a barra, o GitHub cria a pasta sozinho.
4. Abra o arquivo `pegada-7k3m9x.html` deste pacote num editor de texto, selecione tudo e copie
5. Cole no campo grande do GitHub
6. Role até o fim, botão **Commit changes**

### Passo 2, criar o robots.txt

1. Volte à raiz do repositório
2. **Add file**, **Create new file**
3. Nome do arquivo:
   ```
   robots.txt
   ```
4. Cole este conteúdo, são duas linhas:
   ```
   User-agent: *
   Disallow: /validacao/
   ```
5. **Commit changes**

### Passo 3, esperar a publicação

O GitHub Pages leva de um a três minutos. Acompanhe na aba **Actions** do repositório: quando o check ficar verde, está no ar.

Abra `https://aefos.com.br/validacao/pegada-7k3m9x.html` para conferir.

**Atenção ao copiar e colar:** use um editor de texto puro (Bloco de Notas, VS Code, Notepad++). Não use Word, que troca aspas retas por aspas curvas e quebra o código. Se preferir, no passo 1 use **Add file** e depois **Upload files**, arrastando o arquivo direto. Nesse caso crie a pasta antes, digitando `validacao/` no nome de um arquivo qualquer.

---

## Caminho B, pelo Git local

Se você já tem o repositório clonado na máquina:

```
cd caminho/do/aefos-pr.github.io
git pull
mkdir validacao
```

Copie `pegada-7k3m9x.html` para dentro de `validacao/` e `robots.txt` para a raiz. Depois:

```
git add validacao/ robots.txt
git commit -m "Adiciona protótipo da calculadora de pegada de carbono do Circuito"
git push
```

---

## Caminho C, liberar o acesso para eu publicar

Se quiser que eu passe a subir alterações direto, sem você mexer em arquivo:

1. Abra `https://github.com/apps/claude/installations/select_target`
2. Escolha a organização **AEFOS-PR**
3. Autorize o repositório `aefos-pr.github.io`

Alternativa: reconectar o GitHub em `https://claude.ai/customize/connectors`.

Feito isso, me avise. Daí em diante eu publico os ajustes direto no repositório.

---

## O que ainda precisa ser ajustado antes de valer como dado

A página está marcada como protótipo e isso aparece para quem abre. Dois itens pendentes:

### 1. Distâncias dos municípios

A tabela traz 32 municípios do Oeste e Sudoeste, com a distância rodoviária até Pato Branco e até Dois Vizinhos. **Os valores são aproximados e precisam ser conferidos um a um.**

No arquivo, procure por `var MUN = [`. O formato de cada linha é:

```
["Nome do Município", distância até Pato Branco, distância até Dois Vizinhos],
```

Exemplo:

```
["Francisco Beltrão",50,50],
```

Para corrigir, basta trocar os números. Para acrescentar um município, copie uma linha e ajuste. Mantenha a vírgula no fim de cada linha, menos na última.

### 2. Fatores provisórios

Na tabela da página, os fatores marcados em laranja com a etiqueta "provisório" vêm de base secundária e precisam ser travados contra a versão vigente da Ferramenta de Cálculo do Programa Brasileiro GHG Protocol (GVces/FGV):

- Etanol hidratado, parcela de CH₄ e N₂O
- Ônibus de linha
- Hospedagem
- Refeição e coffee break

No arquivo, procure por `var F = {`. Os valores estão todos ali, em um bloco só.

**Os fatores de combustível não são provisórios.** Gasolina C, diesel B e a fração biogênica foram derivados de parâmetros do IPCC 2006 e conferem com a nota metodológica. Não mexa neles sem refazer a derivação.

---

## Como o cálculo funciona, resumo

Tudo roda no navegador de quem responde. Não há servidor, não há banco, nenhuma resposta é gravada ou transmitida. O arquivo é autossuficiente: um único HTML, sem dependência externa além da logomarca em `../assets/logo.png`.

Dois pontos de método que o código respeita e que a maioria das calculadoras de internet erra:

- **Rateio por ocupantes.** A emissão do veículo é dividida pelo número de pessoas a bordo. Sem isso, um carro com três participantes seria contado três vezes.
- **Fração biogênica apartada.** O CO₂ do etanol anidro e do biodiesel das misturas obrigatórias sai do total antrópico e vai para linha própria.

A tela de resultado mostra a memória de cálculo completa, passo a passo, com os números da resposta. É o que permite ao professor auditar sem abrir o código.

---

## Para mandar ao professor

Sugestão de mensagem, depois que o link estiver no ar:

> Professor, montamos um instrumento para calcular a pegada de carbono do 1º Circuito da AEFOS, que vai servir de base para o plantio compensatório. Antes de aplicar em campo, gostaria da sua avaliação do método.
>
> A calculadora está em: https://aefos.com.br/validacao/pegada-7k3m9x.html
>
> A tela de resultado abre a memória de cálculo completa, para conferência. Em anexo vai a nota metodológica, com a derivação dos fatores, exemplos resolvidos e, na seção 14, os oito pontos sobre os quais gostaria especificamente da sua opinião.

Anexe o PDF `Nota_Metodologica_Pegada_Carbono_Circuito_AEFOS.pdf`.
