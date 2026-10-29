---
name: obsidian-project-docs
description: Produz um RAIO-X COMPLETO de um projeto de software e o registra num vault Obsidian como documentação de referência definitiva — lê o projeto inteiro, monta um inventário mecânico (rotas, telas, modais, componentes, formulários, chamadas a banco/HTTP, coleções, functions, serviços, integrações, env vars, testes, TODOs), documenta cada item com evidência e nível de confiança, gera visão transversal (navegação, ER, permissões, estados, cascatas) e audita a cobertura por script. Use sempre que o usuário invocar /obsidian-project-docs, pedir para documentar, mapear, "fazer o raio-x" ou entender um repositório no Obsidian, criar ou atualizar a base de conhecimento/wiki de um projeto, onboarding de pessoas ou agentes, ou atualizar a documentação após mudanças no código — mesmo que diga só "documenta esse projeto" ou "document this project in Obsidian".
---

# Obsidian Project Docs — Raio-X completo

Toda execução desta skill produz um **RAIO-X COMPLETO** do projeto e o registra no VAULT.
Não é resumo: é a documentação de referência definitiva. Quem nunca viu o código deve
conseguir entender, manter e evoluir o sistema lendo só o vault.

- **Sempre o projeto inteiro.** Não existe modo "rápido", "survey" ou "só uma área". Toda
  invocação percorre as Fases 0 → 1 → 2 → 3 → 4 sobre todo o escopo. Em vault já documentado,
  roda o Modo Atualização, que também refaz o inventário inteiro e a Fase 4 completa.
- **Profundidade > velocidade.** Proibido "o resto é parecido", "etc.", "entre outros".
- Entregar **PARCIAL e honesto** é aceitável. Entregar **COMPLETO e raso NÃO é**.
- Você atua como arquiteto, staff engineer e redator técnico. Não implementa, não corrige, não refatora.

## Parâmetros

- **VAULT**: pasta do vault onde escrever (contém `Home.md`). Vem do argumento da invocação
  (`/obsidian-project-docs <caminho do VAULT>`) ou da mensagem do usuário. Se não foi informado,
  não existe ou não tem `Home.md`, **PARE e pergunte**. Nunca adivinhe.
- **PROJETO**: diretório atual de trabalho (raiz do repositório), salvo indicação do usuário.

## Referências (leia cada uma no passo que aponta para ela)

| Arquivo | Quando ler |
|---|---|
| `references/fase-0-1-inventario.md` | Fase 0 e Fase 1 (escopo, buscas, inventário, portão) |
| `references/fase-2-documentacao.md` | Fase 2 (lotes, subagentes, rastreio até o destino final, cobertura por área) |
| `references/templates.md` | Toda vez que for escrever um tipo de nota novo |
| `references/formato-obsidian.md` | Antes de escrever a primeira nota (frontmatter, nomes, Mermaid, citações, marcadores) |
| `references/fase-3-transversal.md` | Fase 3 |
| `references/fase-4-auditoria.md` | Fase 4 e antes da resposta final |
| `references/ferramentas-externas.md` | Só se quiser contexto sobre ferramentas de terceiros (nunca instale nem rode durante a execução) |

Scripts (somente leitura, sem rede, só biblioteca padrão do Python):
`scripts/validate_vault.py` (Fase 4.2) e `scripts/cobertura_fontes.py` (Fase 4.1).
Para cumprir a regra 1.2 ao pé da letra, copie-os para `/tmp` (ou o diretório temporário da sessão) e rode de lá.

## 1. Regras inegociáveis

### 1.1 Onde escrever
- Escreva SOMENTE dentro de VAULT. Nunca crie vault/docs dentro do repositório. Nunca edite `.obsidian/`.
- Use o MCP do Obsidian só se confirmar que ele aponta para este mesmo VAULT (leia `Home.md`
  pelos dois meios e compare). Caso contrário, escreva os `.md` direto no sistema de arquivos.
- O `Home.md` existente É a nota "00 Home": mescle nele, não crie outra Home.

### 1.2 Somente leitura e sem efeitos externos
- Comandos permitidos: `ls`, `find`, `rg`/`grep`, `wc`, leitura de arquivos, `git status/log/diff/rev-parse`,
  + `node`/`python3` EXCLUSIVAMENTE para rodar scripts em `/tmp` que só LEEM o repositório/VAULT,
  escrevem só em `/tmp` ou no VAULT e não usam rede.
- Não use `git log -p` / `git show` em arquivos de segredo (o histórico pode conter valores).
- PROIBIDO: instalar dependências, buildar, rodar app/servidor/emulador/testes, qualquer CLI de nuvem
  (firebase, gcloud, supabase, aws, vercel), qualquer chamada de rede, acesso a banco real, alterar
  arquivos do projeto, commits/branches/PRs no projeto.
- Comportamento de runtime é deduzido do código e marcado como "Inferido".

### 1.3 Segredos e dados pessoais
- Não abra `.env*` (exceto `.env.example`/`.env.sample`), `*serviceAccount*.json`, `*.pem`, `*.key`, `credentials*`.
  Descubra variáveis com: `rg -o "process\.env\.\w+|import\.meta\.env\.\w+|environment\.\w+"`
- Vale para qualquer arquivo, inclusive README e docs: tokens, URLs assinadas, IDs de documentos
  reais e e-mails não são reproduzidos; registre só que existem e onde.
- Documente NOMES de chaves, nunca VALORES. Config commitada no código (ex.: `firebaseConfig` em
  `environment.ts`): registre só os nomes das chaves e anote em 13 Pendências
  "config commitada em arquivo → símbolo", sem reproduzir o valor.
- Exemplos JSON são SINTÉTICOS, montados a partir dos tipos (`"email": "usuario@exemplo.com"`) e
  rotulados "exemplo ilustrativo". Nunca copie dados de seeds, fixtures, mocks ou testes.

### 1.4 Evidência, com nível de confiança
- Toda afirmação técnica tem um nível (citação sem rótulo = Confirmado; escreva o rótulo só para
  Inferido e Não confirmado):
  `Confirmado` (cita o código) | `Inferido` (cita o código + explica o raciocínio) |
  `⚠️ Não confirmado #nao-confirmado` (diz exatamente o que buscou e onde).
- Objetivo do produto, público, regras de negócio e glossário sem texto explícito no código/README
  são no máximo `Inferido`.
- Citação: `` `caminho/arquivo.ts` → `Classe.metodo()` (L42) ``. O símbolo é a âncora; a linha vem
  de ferramenta (`rg -n`, `grep -n`, `cat -n`), NUNCA contada de cabeça.
- Célula de tabela sem evidência = "—" + motivo. Nunca preencha para completar a tabela.
- Seção "Não se aplica" só com a busca que comprova (ex.: "Não se aplica — `rg '\.open\('` sem resultados").

### 1.5 Preservação e reexecução
- Conteúdo gerado fica entre `<!-- gerado:inicio -->` e `<!-- gerado:fim -->`. Tudo fora desses
  marcadores é humano e NUNCA é alterado. Exceção: no frontmatter você gerencia só as chaves
  `tipo, commit, fontes, status, aliases, tags` (preserve qualquer outra). Na `Home.md`, acrescente
  um bloco gerado sem alterar o texto existente.
- Todo frontmatter inclui `commit: "<git rev-parse --short HEAD>"` e `fontes: [arquivos usados]`.
  Se `git status --porcelain` mostrar mudanças não commitadas, registre no Inventário
  "documentado sobre árvore com alterações locais: <arquivos>".

### 1.6 Formato Obsidian
Resumo (detalhes e exemplos em `references/formato-obsidian.md`):
- Nomes de arquivo únicos no vault inteiro, sem `/ \ : * ? " < > | # ^ [ ]`. Convenção:
  `Tela - <Módulo> - <Nome>`, `Modal - <Módulo> - <Nome>`, `Componente - <Nome>`,
  `Coleção - <caminho com / → " › " e {id} → "(id)">`, `API - <Nome>`, `Fluxo - <Nome>`,
  `Serviço - <Nome>`, `Integração - <Nome>`. Caminho técnico real no frontmatter e em `aliases`.
- YAML válido: todo valor string entre aspas duplas; `tags: [tela, kanban]` SEM `#`; `tipo` só de:
  `tela | modal | componente | colecao | api | fluxo | integracao | servico | meta`.
  Nota com qualquer item ⚠️ recebe `status: "parcial"`.
- Mermaid: só `flowchart`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`; no máximo ~40 nós
  (divida por módulo); IDs ASCII sem espaço; rótulos entre aspas; no `erDiagram`, atributos só `[A-Za-z0-9_]`.
- Idioma: português. Nomes técnicos exatamente como no código. Arquivos de `_meta` sem acento.

## Fluxo de trabalho

Comece SEMPRE pela Fase 0. Mantenha uma lista de tarefas com as fases e os lotes.

1. **Fase 0 — Reconhecimento e escopo** → `references/fase-0-1-inventario.md` §Fase 0.
   Valide VAULT (regra 1.1), leia o vault inteiro, detecte Modo Atualização
   (`_meta/Inventario.md` existe), levante apps/pacotes, stack, versões, ambientes, como rodar/buildar/deployar.
2. **Fase 1 — Inventário mecânico** → mesma referência §Fase 1. Crie `_meta/Inventario.md` ANTES de
   documentar: cada item é uma linha de checklist com id, `arquivo → símbolo` e o NOME EXATO da nota de destino.
   **Portão**: mais de ~150 itens, mais de um app/pacote ou escopo duvidoso → PARE e mostre
   apps/pacotes, exclusões, totais e número de lotes previsto; siga só com o OK do usuário.
   O portão confirma escopo e lotes; nunca reduz profundidade.
3. **Fase 2 — Documentação** → `references/fase-2-documentacao.md` + `references/templates.md`.
   Lotes por módulo (~10–15 itens), subagentes quando possível, rastreio de cada ação até a
   leitura/escrita/navegação final. Atualize o Inventário AO FINAL DE CADA LOTE.
4. **Fase 3 — Visão transversal** → `references/fase-3-transversal.md` (pasta `14 Visão Transversal/`,
   cruzamentos obrigatórios, `_meta/Mapa Codigo-Notas`).
5. **Fase 4 — Auditoria (obrigatória)** → `references/fase-4-auditoria.md`: refazer buscas e cruzar com
   `fontes` por script, validar o vault por script, verificação independente, `_meta/Relatorio de Cobertura.md`.

**Concluído** = zero itens `[ ]` no Inventário, `validate_vault.py` sem erros e `Home.md` linkando todas as seções.
Diferenças que não puderem ser resolvidas são listadas e justificadas, não escondidas.

Se contexto/tempo apertar: é PROIBIDO reduzir profundidade. Pare no limite de um lote, atualize o
Inventário e reporte onde parou (`PARCIAL`). A próxima execução retoma a partir do Inventário.

## Estrutura do vault

```text
VAULT/
  Home.md                       00 Home (já existe; mesclar em bloco gerado)
  01 Visão Geral.md
  02 Arquitetura.md
  03 Telas/                     Tela - … / Modal - …
  04 Componentes/               Componente - … + Catalogo UI.md (+ Design System.md se houver tokens)
  05 Fluxos/                    Fluxo - …
  06 Dados/                     Coleção - …
  07 APIs/                      API - …
  08 Serviços e Estado/         Serviço - …
  09 Integrações/               Integração - … + Links externos.md
  10 Segurança e Acesso.md
  11 Infra e Deploy.md
  12 Qualidade.md
  13 Pendências e Riscos.md
  14 Visão Transversal/
  Glossário.md
  _meta/                        Inventario.md, Mapa Codigo-Notas.md, Relatorio de Cobertura.md
  _arquivo/                     notas de itens removidos do código (Modo Atualização)
```

Crie pasta só quando houver nota para ela. Seções inteiras que não se aplicam viram uma linha
"Não se aplica — <busca que comprova>" na nota-pai ou na Home, nunca nota vazia.

## 7. Modo Atualização (vault já documentado)

Quando `_meta/Inventario.md` existe:
1. Leia o `commit` registrado e rode `git diff --name-only <commit>..HEAD`.
2. Refaça o inventário mecânico INTEIRO (Fase 1) e compare com o anterior: novos, removidos, alterados.
3. Reprocesse as notas cujas `fontes` mudaram e crie as dos itens novos, respeitando os marcadores
   de conteúdo humano (regra 1.5).
4. Itens removidos do código: mova a nota para `_arquivo/` com o motivo; não apague.
5. Rode a Fase 3 nas partes afetadas e a Fase 4 completa no final.

Se o commit registrado não existir mais no histórico, trate como primeira execução sobre o vault
existente (preservando conteúdo humano) e registre isso no Relatório de Cobertura.

## 8. Resposta final

Primeira linha: `COMPLETO` ou `PARCIAL — parei em <lote/item>, faltam N itens`, + commit documentado.
Depois, só:
- totais por categoria (inventariados × documentados);
- pendências e riscos (bugs aparentes, segurança, inconsistências, dívida técnica);
- os pontos ⚠️ que precisam de confirmação do usuário.

Sem resumo genérico.
