# Fase 2 — Documentação

## 4.1 Execução em lotes

- Divida o inventário em lotes por módulo/feature (~10–15 itens).
- Se puder usar subagentes, delegue cada lote a um subagente com contexto limpo. O briefing do
  subagente leva, por escrito (ele não vê esta conversa):
  - VAULT e raiz do PROJETO;
  - o texto das regras da seção 1 do SKILL.md, a tabela 3.3 (`fase-0-1-inventario.md`), as seções
    4.2 e 4.3 (este arquivo e `templates.md`) e `formato-obsidian.md`;
  - a lista exata de itens do lote, com `arquivo → símbolo` e o NOME DE NOTA já fixado;
  - a lista de nomes de nota de outros lotes que ele pode linkar;
  - o commit documentado.
- Cada subagente escreve SOMENTE as notas de item do seu lote. Linhas destinadas a notas
  compartilhadas (Coleção › Quem lê/escreve, Catalogo UI, 11 Infra, 13 Pendências, Mapa
  Codigo-Notas) e a marcação do Inventário são DEVOLVIDAS ao coordenador, que as grava em
  sequência. Se não puder garantir isso, rode um lote por vez.
- Atualize o Inventário AO FINAL DE CADA LOTE (nunca tudo no fim). É isso que permite retomar.
- Se contexto/tempo apertar: é PROIBIDO reduzir profundidade. Pare no limite de um lote, atualize o
  Inventário e reporte onde parou.

Ordem sugerida dos lotes: 1) Dados (coleções/tabelas, porque todo o resto linka nelas) →
2) APIs/functions → 3) Serviços e Estado → 4) Integrações → 5) Telas e Modais por módulo →
6) Componentes compartilhados + Catalogo UI → 7) Fluxos → 8) notas gerais (01, 02, 10–13, Glossário).
Notas de destino ainda não escritas podem ser linkadas pelo nome já fixado no Inventário; a Fase 4
pega o que ficar quebrado.

## 4.2 Rastreie até o destino final

Para cada ação, siga: handler → serviço → store/effect → chamada HTTP/DB, atravessando
`afterClosed()`/retorno de modal, `@Output()`/`output()`, signals/stores, interceptors, guards.
A coluna "Efeito" só fecha ao chegar numa leitura/escrita concreta ou numa navegação.
Modal que só devolve dados: documente quem recebe e o que grava.

Para cada coisa documentada, responda mais que "o que existe": o que é, onde vive, para que serve,
como funciona, o que a dispara, do que depende, quem depende dela, de onde vêm e para onde vão os
dados, que regras impõe e o que pode dar errado.

**Regras de negócio** são a parte mais valiosa e menos visível. Procure em schemas de validação,
condicionais em serviços e handlers, constraints e policies do banco, guards, valores computados,
regras de segurança. Escreva a regra em linguagem simples e cite onde vive.

## Cobertura por área (notas gerais)

Além das notas de item, as notas gerais precisam cobrir (cada tópico preenchido com evidência ou
"Não se aplica — <busca>"):

- **01 Visão Geral**: objetivo do produto e público (no máximo `Inferido` sem texto explícito), apps/pacotes,
  stack e versões, estrutura de pastas com o propósito de cada uma, como rodar/buildar localmente
  (de scripts e configs, sem executar), módulos e onde ler mais.
- **02 Arquitetura**: arquitetura real (não a de livro; se é metade feature-sliced e metade em camadas,
  diga), camadas e regras de dependência na prática (respeitadas e violadas), bootstrap/entry points,
  dependências principais por papel (UI, dados, estado, auth, teste, tooling) incluindo desatualizadas
  ou duplicadas, convenções observadas (nomes de arquivo, componentes, funções, tipos; organização de
  pastas; aliases de import; estilo de tratamento de erro; commits/branches pelo `git log`) com um
  exemplo real de cada e onde o código foge delas, e decisões arquiteturais reconstruíveis
  (Confirmado quando doc/comentário/commit afirma; senão Inferido; "motivo não documentado" é válido).
- **10 Segurança e Acesso**: autenticação ponta a ponta (como fluxo), sessão, autorização, perfis/roles/claims,
  guards, regras de segurança/RLS/policies, validação de entrada, sanitização de saída, variáveis
  expostas ao cliente, uploads, CORS, proteção de API. Só riscos demonstrados ou tecnicamente fundamentados.
- **11 Infra e Deploy**: hosting, ambientes, build, pipelines de CI/CD realmente configurados
  (branch → PR → CI → staging → produção, sem acrescentar passos que não estão na config; passos
  provavelmente manuais = ⚠️), processo de migrations, scripts npm (o que cada um roda de fato),
  tabela de env vars (| Nome | Onde é lida | Propósito | Ambiente | — só nomes), runbooks verificados
  em scripts/config (rodar localmente, rodar testes, adicionar tela/feature/entidade seguindo o padrão, deploy).
- **12 Qualidade**: ferramentas de teste, onde ficam, como rodar (sem rodar), contagem por área
  (com o comando), features cobertas e lacunas importantes, testes pulados (`.skip`, `xit`, `xdescribe`),
  lint/format; performance: estratégia de renderização, lazy loading, code splitting, cache, paginação,
  listas grandes, waterfalls, N+1 — separando comportamento atual, gargalo confirmado e oportunidade
  (sem medição, suspeita é oportunidade). SEO só se o app for público.
- **13 Pendências e Riscos**: TODO/FIXME, código suspeito, bugs aparentes, riscos de segurança, config
  commitada, inconsistências, dívida técnica, contradições docs × código, cruzamentos da Fase 3 —
  cada item com severidade (Crítica/Alta/Média/Baixa), evidência, impacto e, opcionalmente,
  direção sugerida marcada como opinião.
- **Glossário**: termos de domínio, nomes internos e siglas do código e da UI, cada um com significado
  em uma linha e link para a nota onde importa (no máximo `Inferido` sem definição explícita).
- **04 Componentes/Design System** (só se houver tokens/tema): tokens que existem de fato (cores
  com papéis semânticos, tipografia, espaçamento, raio, sombras, breakpoints, z-index, motion,
  temas claro/escuro), biblioteca de ícones, padrões de componente com variantes e estados, valores
  hardcoded que fogem dos tokens (estes vão também para 13 Pendências). Não invente um sistema arrumado
  que o projeto não tem.

Fatos e opiniões ficam separados: notas descrevem; riscos, inconsistências e sugestões vão para a
seção "Pontos de atenção" da nota e para 13 Pendências e Riscos.
