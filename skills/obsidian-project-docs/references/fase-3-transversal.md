# Fase 3 — Visão transversal (`14 Visão Transversal/`)

Uma nota por item abaixo (`tipo: "meta"`), cada uma com `commit`, `fontes` e marcadores gerados.
Item sem aplicação → "Não se aplica — <busca que comprova>" na nota índice da pasta.

- **Mapa de navegação**: um diagrama-índice de módulos + um diagrama por módulo (`flowchart`, ≤ ~40 nós).
- **Arquitetura**: front ↔ backend ↔ banco ↔ terceiros (`flowchart`).
- **Diagrama ER**: um por domínio/módulo (`erDiagram`); nomes de campo fora de `[A-Za-z0-9_]` são
  normalizados no diagrama e o nome real fica numa tabela logo abaixo.
- **Matriz de permissões**: perfil × tela/ação (de guards, claims, regras, condicionais de template).
- **Matriz de dados**: | Coleção | Lê | Escreve | Functions |
- **Estados de entidades**: para cada campo status/enum, `stateDiagram-v2` com quem dispara cada transição.
- **Mensagens ao usuário**: | Texto exato (resolvido do i18n, com a chave) | Onde | Gatilho |
  (snackbars, toasts, alerts, `confirm()`, textos de erro de formulário).
- **Efeitos em cascata**: escrita → trigger → escritas/e-mails/chamadas seguintes.
- **Storage**: caminhos, quem sobe, quem lê, regras.
- **Ambientes**: | Config | dev | staging | prod | (só nomes e identificadores, nunca valores secretos).
- **PWA/SSR**: o que é cacheado, como atualiza, o que roda no servidor.
- **Linhagem de dados** dos dados principais: origem → serviço → estado → componente → tela,
  incluindo mappers, caches e onde o formato muda.

## Cruzamentos obrigatórios → `13 Pendências e Riscos`
- Cada query com filtro + ordenação × índice declarado (falta de índice = risco).
- Cada escrita × regra de segurança que a permite (escrita sem regra que permita = bug aparente;
  regra mais aberta que o uso = risco).
- Rules/índices ausentes do repositório = "⚠️ não versionados (podem existir só no console)" como RISCO.
- Contradições docs × código.

## `_meta/Mapa Codigo-Notas`
| arquivo | notas que o documentam | — gerado a partir das `fontes` de todas as notas (por script em /tmp).

## Código morto
É sempre "Suspeito de não uso", com a busca feita (incluindo templates, strings, rotas lazy e
injeção por token). Nunca afirme que está morto.
