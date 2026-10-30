# Vault configurado

Contrato para vaults que seguem a convenção do "segundo cérebro". Um vault é **configurado** quando
`<raiz do vault>/00 Sistema/projetos.yaml` existe. A raiz do vault é o primeiro diretório acima do
VAULT que contém `.obsidian/`. Sem esse arquivo, ignore este documento inteiro.

Num vault configurado, as regras abaixo **substituem** as convenções padrão de `SKILL.md`,
`formato-obsidian.md` e `templates.md` nos pontos que tratam. O resto (evidência, segredos, somente leitura,
fases, inventário, auditoria) continua igual.

Por que existe: o vault tem ferramentas próprias (`cerebro`) que leem as notas pelo `tipo`, pelo nome
da Home e pelo primeiro parágrafo. Notas fora dessa convenção somem da síntese
`11 Conhecimento/Conhecimento - <Projeto>.md` e da busca.

## Projeto e pasta

- O VAULT é `02 Projetos/<Projeto>/`, onde `<Projeto>` é o `nome` da entrada de `projetos.yaml` cuja
  `pasta_vault` é esse caminho (ou cujo `caminho_local` é a raiz do projeto).
- Projeto fora do `projetos.yaml`: PARE e pergunte. Ofereça registrar a entrada (`nome`, `pasta_vault`,
  `repo` do `git remote`, `caminho_local`, `aliases_cwd: []`). Só escreva no yaml com o OK do usuário.

## Home

- A Home é `<Projeto> Home.md` na raiz do VAULT, não `Home.md`. É ela que a regra 1.1 exige e onde
  entra o bloco gerado. Se o VAULT só tiver `Home.md`, use-a nesta rodada e registre no Relatório de
  Cobertura a recomendação de renomear (com o OK do usuário, renomeie e atualize os links por script).
- `tipo: "visao-geral"` na Home.
- Todos os links para a Home: `[[<Projeto> Home]]` ou `[[<Projeto> Home|texto]]`.

## Nomes de nota

- Nomes precisam ser únicos no vault inteiro, e outros projetos já usam `01 Visão Geral`,
  `Inventario`, `Glossário` etc. Por isso **toda** nota gerada recebe o prefixo `<Projeto> - `:
  `<Projeto> - 01 Visão Geral`, `<Projeto> - Serviço - escada`, `<Projeto> - Inventario`.
- Proibidos no nome: `| # ^ [ ] :` (além dos da regra 1.6).
- Link para alias é sempre `[[arquivo|texto]]`, nunca `[[alias]]`.

## Frontmatter

Além das chaves da skill (`tipo, commit, fontes, status, aliases, tags`), toda nota leva:

```yaml
projeto: "<Projeto>"        # exatamente o nome do projetos.yaml
data: "AAAA-MM-DD"          # dia da geração/atualização
caminho: "ram_a_x/modulo.py" # opcional: caminho técnico real (arquivo, rota, host)
```

### Valores de `tipo`

| Nota | Padrão da skill | Vault configurado |
|---|---|---|
| Home | — | `visao-geral` |
| `01 Visão Geral` | `meta` | `visao-geral` |
| `02 Arquitetura` | `meta` | `arquitetura` |
| `Serviço - …` (08 Serviços e Estado) | `servico` | `modulo` |
| Demais (`tela`, `modal`, `componente`, `colecao`, `api`, `fluxo`, `integracao`, `meta`) | iguais | iguais |

O gerador do Conhecimento só lê notas com `tipo` em `visao-geral`, `arquitetura`, `fluxo` ou `modulo`,
e usa a Home (`* Home`), a visão geral e a arquitetura como "Onde aprofundar". Por isso a tabela acima.

## Corpo da nota

Logo depois de `<!-- gerado:inicio -->`, a linha de navegação vai **como citação**, para não ser lida
como primeiro parágrafo:

```markdown
<!-- gerado:inicio -->
> Projeto: [[<Projeto> Home]] · Dia: [[AAAA-MM-DD]]

# <Projeto> - Serviço - escada

Uma ou duas frases dizendo o que é e por que existe.
```

O primeiro parágrafo de prosa depois do título é o trecho que entra no Conhecimento: ele precisa ser
um resumo autossuficiente da nota (máx. ~450 caracteres úteis), não uma tabela nem uma lista.

## Escritas permitidas fora do VAULT (exceção à regra 1.1)

Só estas, ao fim de cada execução:

1. **Diário:** em `01 Diário/AAAA-MM-DD.md` (hoje), sob `## Registro`, uma linha
   `- [[<Projeto> Home]]: raio-x <completo|parcial> (commit <hash>, <n> notas, validador <OK|FALHOU>)`.
   Arquivo ausente: crie com frontmatter `tipo: diario`, `projeto: geral`, `data: AAAA-MM-DD`,
   `tags: [diario]` e o cabeçalho `## Registro`.
2. **Conhecimento:** se `11 Conhecimento/Conhecimento - <Projeto>.md` existe, ponha
   `desatualizado: true` no frontmatter. Não crie nem reescreva essa nota; ofereça ao usuário rodar
   `cerebro conhecimento gerar --projeto "<Projeto>"`.
3. **Reindexação:** rode `cerebro reindexar` se `cerebro` estiver no PATH; senão, pule em silêncio.
4. **Aprendizados/decisões** que o `CLAUDE.md` do vault mande registrar (`06 Decisões`, `07 Aprendizados`),
   seguindo as regras de nome e frontmatter desse arquivo.

## Auditoria

Rode o validador com a Home do projeto e a raiz do vault:

```bash
python3 -I /tmp/validate_vault.py "<VAULT>" --vault-root "<raiz do vault>" --home "<Projeto> Home"
```

O validador aceita os tipos `visao-geral`, `arquitetura` e `modulo`. Sem `--home`, ele procura
`Home.md` e, se não houver, a única `* Home.md` na raiz do VAULT.

## Modo Atualização

Igual ao padrão, com duas regras a mais: notas de itens removidos ganham `status: "descontinuado"` e
vão para `12 Arquivo/` (não `_arquivo/`), sem apagar; e `data` é atualizada nas notas reprocessadas.
