# Templates (4.3)

Todas as notas: frontmatter conforme `formato-obsidian.md`, corpo gerado entre
`<!-- gerado:inicio -->` e `<!-- gerado:fim -->`, `[[wikilinks]]` entre tudo que se relaciona
(tela ↔ coleção ↔ API ↔ fluxo ↔ componente ↔ serviço) e uma seção final `## Relacionadas`.
Seção sem conteúdo aplicável: "Não se aplica — <busca que comprova>" (nunca vazia, nunca inventada).
Exemplos JSON sempre sintéticos e rotulados "exemplo ilustrativo".

## TELA / MODAL (03 Telas)

```markdown
---
tipo: "tela"                       # ou "modal"
rota: "/customers/:id"             # modal: abertoPor: ["[[Tela - Clientes - Lista]]"]
arquivo: "src/app/customers/customer-detail.component.ts"
modulo: "Clientes"
acesso: "autenticado; guard authGuard"
commit: "a1b2c3d"
fontes: ["src/app/customers/customer-detail.component.ts", "src/app/customers/customer-detail.component.html"]
status: "completo"                 # "parcial" se houver qualquer ⚠️
tags: [tela, clientes]
aliases: ["/customers/:id", "CustomerDetailComponent"]
---
<!-- gerado:inicio -->
# Tela - Clientes - Detalhe

## Objetivo
## Acesso
Rota, guards, perfis, resolvers, de onde se chega, query params/deep links.
## Estrutura/layout
Seções na ordem em que aparecem.
## Elementos interativos
| Elemento (texto visível) | Ação | Handler (arquivo → símbolo, Lx) | Efeito final |
|---|---|---|---|

Interações no código: N | documentadas: N
## Formulários
| Rótulo visível | Chave no payload | Tipo | Obrigatório | Validações | Máscara | Padrão |
|---|---|---|---|---|---|---|

Payload enviado (exemplo ilustrativo), destino, comportamento em sucesso e em erro (texto exato da
mensagem, ou "mensagem dinâmica de <origem> (variável X)" quando não for literal no código).
## Modos / Abas / Passos
Uma subseção por modo, aba ou passo, cada uma com suas próprias tabelas.
## Dados carregados
Fonte, filtros/ordenação, quando carrega, cache, tempo real.
## Chamadas
| Operação | Endpoint/Coleção | Payload | Resposta | Tratamento de erro |
|---|---|---|---|---|
## Estados
Loading, vazio, erro, sucesso, sem permissão — cada um com evidência ou "—" + motivo.
## Regras de negócio
## Navegação de saída
## Componentes usados
## Pontos de atenção
## Evidências
## Relacionadas
<!-- gerado:fim -->
```

**Contagem obrigatória antes de fechar a nota**: conte no template os bindings de evento (`(click)`,
`(ngSubmit)`, `(change)`, `(input)`, `onClick=`, `onSubmit=`, `routerLink`, `[mat-dialog-close]`,
drag/drop) e controles de formulário. Conte ocorrências no CÓDIGO-FONTE (não instâncias renderizadas
por `*ngFor`/`@for`/`.map`). Cada ocorrência aparece numa linha de Interações ou de Formulários;
diferença só com justificativa por item. Exemplo:
```bash
rg -n -o "\((click|ngSubmit|change|input)\)=|routerLink|mat-dialog-close|formControlName" src/app/customers/customer-detail.component.html | wc -l
```

## COMPONENTE COMPARTILHADO (04 Componentes)

```markdown
# Componente - <Nome>
## Responsabilidade
## Localização
## API
| Input/prop | Tipo | Padrão | Propósito |  + outputs/eventos
## Variantes e estados visuais
## Estado interno e comportamento
## Serviços injetados e chamadas
## Acessibilidade
## Usado em
Links para cada tela/componente que o usa (com a busca que comprova).
## Pontos de atenção
## Relacionadas
```

## CATALOGO UI (04 Componentes/Catalogo UI)

| Componente | Arquivo → símbolo | Propósito (1 linha) | Inputs principais | Usado em (nº + links) |

## COLEÇÃO / TABELA (06 Dados)

```markdown
---
tipo: "colecao"
caminho: "customers/{id}/orders"
aliases: ["customers/{id}/orders"]
...
---
# Coleção - customers › (id) › orders
## Campos
| Campo | Tipo | Fonte do tipo | Obrigatório | Quem grava | Obs. |
|---|---|---|---|---|---|
## Exemplo ilustrativo
## Índices
Declarados × queries que os exigem.
## Regras de segurança aplicáveis
## Quem lê
## Quem escreve
## Relacionamentos
## Relacionadas
```

- Fontes de tipo, em ordem: migrations / `database.types` / Zod / DTOs / interfaces de modelo /
  campos escritos em `add|set|update|insert` / campos lidos em templates. Registre a fonte de cada campo.
- "Obrigatório" (Firestore/NoSQL) = "sempre escrito na criação: [pontos de criação]" ou "desconhecido"
  (updates parciais não contam). Em SQL, vem da constraint.
- Sem escrita no código: "Origem externa/desconhecida (nenhuma escrita encontrada; busca: ...)" —
  nunca atribua escrita a uma tela.

## API / FUNCTION (07 APIs)

```markdown
# API - <Nome>
## Tipo
HTTP, callable, trigger, cron.
## Rota/gatilho
## Autenticação
## Request
Schema + exemplo ilustrativo.
## Response
Schema + exemplo ilustrativo.
## Erros
## Efeitos colaterais
O que grava, dispara, envia.
## Quem chama
## Evidências
## Relacionadas
```

## SERVIÇO / STORE (08 Serviços e Estado)

```markdown
# Serviço - <Nome>
## Responsabilidade
## Localização
## Estado mantido
Signals/subjects/store: quem escreve, quem lê, persistência, sincronização com servidor, invalidação de cache.
## Operações
| Operação | Entrada | Saída | O que chama (coleção/API/integração) | Tratamento de erro |
## Chamadas
| Operação | Endpoint/Coleção | Payload | Resposta | Tratamento de erro |
## Dependências
## Consumidores
## Pontos de atenção
## Relacionadas
```

## INTEGRAÇÃO (09 Integrações)

```markdown
# Integração - <Nome>
## Propósito
## Configuração
Arquivos de config e NOMES de env vars. Sem valores.
## Cliente/SDK e autenticação
## Onde é usada
## Dados enviados
## Dados recebidos
## Tratamento de erro, retries, rate limit, webhooks
## Riscos
## Relacionadas
```

`09 Integrações/Links externos`: | URL (domínio + caminho, sem tokens) | Texto visível | Onde (arquivo → símbolo, Lx) |

## FLUXO (05 Fluxos)

```markdown
# Fluxo - <Nome>
## Objetivo
## Ator
## Pré-condições
## Passos
1. Tela → ação → chamada → dado gravado → próxima tela (cada passo com evidência)
## Caminhos alternativos e de erro
## Diagrama
sequenceDiagram
## Relacionadas
```

Obrigatórios: cada modo de autenticação existente (cadastro, login, logout, recuperação), cada CRUD
e cada jornada de negócio.

## Notas gerais (`tipo: "meta"`)

`01 Visão Geral`, `02 Arquitetura`, `10 Segurança e Acesso`, `11 Infra e Deploy`, `12 Qualidade`,
`13 Pendências e Riscos`, `Glossário`: conteúdo mínimo em `fase-2-documentacao.md` §Cobertura por área.

`13 Pendências e Riscos`:
```markdown
| ID | Item | Tipo | Severidade | Evidência | Impacto |
|---|---|---|---|---|---|
| P-001 | Config commitada | segurança | Alta | `src/environments/environment.ts` → `environment.firebaseConfig` (L3) | ... |
```
Tipo: bug aparente | segurança | inconsistência | dívida técnica | TODO/FIXME | risco | não confirmado.

## Home (bloco gerado acrescentado ao Home.md existente)

```markdown
<!-- gerado:inicio -->
## Documentação do projeto (raio-x)
Commit documentado: `a1b2c3d` · Status: COMPLETO|PARCIAL
- [[01 Visão Geral]] · [[02 Arquitetura]]
- Telas: [[...]] (índice por módulo)
- ... um link para cada seção 01–14, Glossário e _meta
<!-- gerado:fim -->
```

## Inventário (_meta/Inventario.md)

```markdown
---
tipo: "meta"
commit: "a1b2c3d"
fontes: []
status: "parcial"
---
<!-- gerado:inicio -->
# Inventario

- Commit documentado: `a1b2c3d` (árvore limpa | com alterações locais: <arquivos>)
- Apps/pacotes: ...
- Exclusões: node_modules, dist, ... ; não inventariados: src/app/database.types.ts (gerado)

## Totais
| Categoria | Total | Comando |
|---|---|---|
| Rotas | 23 | `rg -n "path:" src/app --glob "*routes.ts" \| wc -l` (2 descartadas: redirect vazio) |

## Triagem das buscas
| Padrão | Ocorrências | Descartadas | Motivo |

## Lote 1 — Dados
- [x] D-001 `src/app/core/customer.service.ts` → `CustomerService.list()` → [[Coleção - customers]]
- [~] D-002 ... → [[Coleção - orders]] (parcial: regras não versionadas)
- [!] D-003 ... (buscou `rg "invoices"` em src/ e functions/: nenhuma escrita)
- [ ] T-001 `src/app/customers/customer-detail.component.ts` → `CustomerDetailComponent` → Tela - Clientes - Detalhe
<!-- gerado:fim -->
```

## Mapa Codigo-Notas (_meta/Mapa Codigo-Notas.md)

| arquivo | notas que o documentam |

## Relatório de Cobertura (_meta/Relatorio de Cobertura.md)

Totais inventariados × documentados (com comandos), itens `[~]` e `[!]`, resultado dos scripts da
Fase 4 (comandos e contagens), divergências encontradas na verificação independente e como foram
corrigidas, lacunas que exigem informação humana.
