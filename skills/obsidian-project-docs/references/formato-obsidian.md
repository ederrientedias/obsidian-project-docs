# Formato Obsidian, citações e preservação

Use só recursos nativos do Obsidian (wikilinks, propriedades, callouts, Mermaid). Nada de Dataview,
Templater ou plugins da comunidade.

## Canal de escrita
- MCP do Obsidian: só se `Home.md` lido pelo MCP e pelo sistema de arquivos for o mesmo (regra 1.1).
- Caso contrário: escreva `.md` direto no VAULT. Nunca toque em `.obsidian/`.
- Antes de reescrever uma nota existente, leia-a e preserve tudo fora dos marcadores gerados.

## Nomes de arquivo
- Únicos no vault inteiro (inclusive fora da pasta documentada). Antes de criar, confira a lista de
  nomes lida na Fase 0.
- Proibidos: `/ \ : * ? " < > | # ^ [ ]`.
- Convenção:
  - `Tela - <Módulo> - <Nome>` · `Modal - <Módulo> - <Nome>`
  - `Componente - <Nome>`
  - `Coleção - <caminho com / → " › " e {id} → "(id)">` (ex.: `customers/{id}/orders` →
    `Coleção - customers › (id) › orders`)
  - `API - <Nome>` · `Fluxo - <Nome>` · `Serviço - <Nome>` · `Integração - <Nome>`
- O caminho técnico real vai no frontmatter (`rota`, `arquivo`, `caminho`) e em `aliases`.
- Arquivos de `_meta` sem acento (`Inventario.md`, `Mapa Codigo-Notas.md`, `Relatorio de Cobertura.md`).

## Frontmatter
YAML válido. Todo valor string entre aspas duplas. Listas inline `[a, b]` ou em bloco.

```yaml
---
tipo: "tela"
rota: "/customers/:id"
arquivo: "src/app/customers/customer-detail.component.ts"
modulo: "Clientes"
acesso: "autenticado"
commit: "a1b2c3d"
fontes: ["src/app/customers/customer-detail.component.ts"]
status: "completo"
tags: [tela, clientes]
aliases: ["/customers/:id"]
---
```

- `tipo` só de: `tela | modal | componente | colecao | api | fluxo | integracao | servico | meta`.
- `tags` SEM `#`.
- `commit` e `fontes` obrigatórios em TODA nota gerada.
- `status`: `"completo"` ou `"parcial"`; nota com qualquer item ⚠️ → `"parcial"`.
- Chaves geridas pela skill: `tipo, commit, fontes, status, aliases, tags` (+ as específicas do
  template na criação). Qualquer outra chave existente é humana: preserve.
- Wikilink em frontmatter só entre aspas: `abertoPor: ["[[Tela - Clientes - Lista]]"]`.

## Marcadores de conteúdo gerado
```markdown
<!-- gerado:inicio -->
...conteúdo da skill...
<!-- gerado:fim -->
```
Tudo fora deles é humano e NUNCA é alterado. Em reexecução, substitua só o que está entre eles.
Na `Home.md`, acrescente um bloco gerado ao final sem tocar no texto existente.

## Evidência e confiança
- Sem rótulo = Confirmado (há citação).
- `Inferido`: cite o código e explique o raciocínio.
- `⚠️ Não confirmado #nao-confirmado`: diga exatamente o que buscou e onde.
- Citação: `` `src/app/x.service.ts` → `XService.save()` (L42) ``. Linha sempre de `rg -n`/`grep -n`/`cat -n`.
- Tabela sem evidência: "—" + motivo.

Callouts ajudam a destacar:
```markdown
> [!info] Inferido
> ... raciocínio + evidência

> [!warning] ⚠️ Não confirmado #nao-confirmado
> Buscou `rg "invoices" src functions` — sem escrita encontrada.
```

## Links
- `[[wikilinks]]` para toda relação; texto alternativo quando ajudar: `[[Coleção - customers|customers]]`.
- Linke só para notas que existem ou que estão no Inventário com nome fixado (a Fase 4 confere).
- Código é citado com caminho entre crases, nunca com wikilink.
- Cada nota termina em `## Relacionadas`.

## Mermaid
- Só `flowchart`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`.
- No máximo ~40 nós por diagrama; divida por módulo.
- IDs de nó em ASCII sem espaço; rótulos sempre entre aspas: `custDetail["Detalhe /customers/:id"]`.
- No `erDiagram`, nomes de atributo só `[A-Za-z0-9_]`; o nome real fica numa tabela logo abaixo.
- Todo nó corresponde a algo real no projeto. Nada decorativo.

## Estilo
- Português; nomes técnicos exatamente como no código.
- Comece cada nota com uma ou duas frases dizendo o que é e por que existe.
- Prosa para explicar, tabelas para fatos enumeráveis.
- Proibido "etc.", "entre outros", "o resto é parecido".
- Trechos curtos de código só quando forem a evidência de uma regra.
