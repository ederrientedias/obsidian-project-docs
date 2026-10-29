# Ferramentas externas (curadoria do inventário de repositórios)

Origem: inventário pessoal de repositórios do GitHub (`inventario-repos.pdf`, out/2026, ~450 repos em
16 temas). O próprio inventário avisa que os repos **não foram checados** e devem ser verificados
antes de qualquer uso. Abaixo estão só os que se relacionam com documentar/entender código.

## Regra de uso durante a execução da skill

**Nenhuma destas ferramentas é instalada, clonada, chamada pela rede ou executada durante um
raio-x.** A regra 1.2 proíbe instalar dependências, usar rede e rodar ferramentas fora de
`rg/grep/find/wc/git` + scripts próprios em `/tmp`. Elas servem como:
1. **ideias já incorporadas** nesta skill (coluna "O que a skill aproveita");
2. **complemento opcional que o usuário roda por conta própria**, fora da execução, se quiser.

Exceção única: se o usuário já tiver um MCP local de busca de código configurado na sessão, que só
lê o repositório e não usa rede, ele pode ajudar a LOCALIZAR candidatos. Nunca substitui `rg -n`
como evidência (a linha citada vem sempre de `rg`/`grep`/`cat -n`) e nunca justifica pular uma busca da 3.2.

## Inteligência de código

| Repo | O que é (segundo o inventário) | O que a skill aproveita |
|---|---|---|
| `zzet/gortex` | Motor de inteligência de código em grafo para agentes/IDEs, multi-repo, 257 linguagens | Ideia de tratar o código como grafo: o Mapa Codigo-Notas e as matrizes da Fase 3 são as arestas arquivo ↔ nota ↔ dado |
| `cocoindex-io/cocoindex-code` | Busca de código embutida baseada em AST para agentes | Reforça triagem: busca textual dá candidatos, a confirmação é pelo símbolo (âncora `arquivo → símbolo`) |
| `crisnahine/rails-ai-context` | MCP com "ground truth" de apps Rails: schema, models, routes, controllers, views | Mesmo princípio do inventário mecânico: schema, rotas e telas extraídos do código antes de qualquer prosa |
| `idosal/git-mcp` | MCP remoto que expõe qualquer repo do GitHub para reduzir alucinação | Não usar (rede). Princípio aplicado: toda afirmação cita o código |
| `upstash/context7` | Docs atualizadas de bibliotecas para agentes | Não usar durante o raio-x (rede). O comportamento do projeto vem do código, não da doc da lib |

## Explicação de codebases e diagramas

| Repo | O que é | O que a skill aproveita |
|---|---|---|
| `The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge` | Gera tutoriais de uma codebase a partir das abstrações centrais | `01 Visão Geral` começa pelas abstrações e módulos centrais e diz onde ler mais, para quem nunca viu o código |
| `ahmedkhaleel2004/gitdiagram` | Diagramas interativos de arquitetura a partir do repo | Diagrama de arquitetura e mapa de navegação derivados da árvore real e das rotas, um por módulo, ≤ ~40 nós |
| `cathrynlavery/diagram-design` | Design editorial de diagramas para agentes de código (44 tipos) | Mantemos só os 4 tipos Mermaid nativos do Obsidian, por compatibilidade |
| `drawdb-io/drawdb` | Editor de diagramas de banco e gerador de SQL | Complemento opcional do usuário para visualizar o ER; a skill gera `erDiagram` |

## Design system

| Repo | O que é | O que a skill aproveita |
|---|---|---|
| `VoltAgent/official-design-md`, `VoltAgent/awesome-design-md` | Arquivos `DESIGN.md` de design systems para agentes | Se o projeto tiver `DESIGN.md`, ele é fonte de tokens (a confirmar no código); a nota `04 Componentes/Design System` documenta só tokens reais |

## Memória e conhecimento para agentes

| Repo | O que é | O que a skill aproveita |
|---|---|---|
| `campfirein/byterover-cli` (arquivado) | Camada de memória portátil para agentes de código | O vault é essa memória: `commit` + `fontes` permitem saber quando uma nota ficou velha (Modo Atualização) |
| `gnekt/My-Brain-Is-Full-Crew`, `cocoindex-io/cocoindex`, `laurent22/joplin`, `outline/outline` | Bases de conhecimento / indexação | Nada a incorporar além do que o Obsidian já faz |

## Dívida técnica

| Repo | O que é | O que a skill aproveita |
|---|---|---|
| `azat-io/todoctor` | CLI que acompanha comentários TODO no repositório | `TODO`/`FIXME`/`HACK`/`XXX` entram no inventário e cada um vira linha em 13 Pendências |

Nomes de repositório foram transcritos do PDF (texto extraído com quebras); confirme o nome exato
no GitHub antes de usar qualquer um.
