# Fase 0 e Fase 1 — Reconhecimento, escopo e inventário mecânico

## Fase 0 — Reconhecimento e escopo

1. **Validar VAULT** (regra 1.1). Sem VAULT, VAULT inexistente ou sem `Home.md` → PARE e pergunte.
   Se o MCP do Obsidian estiver disponível, leia `Home.md` por ele e pelo sistema de arquivos e
   compare; só use o MCP se forem o mesmo arquivo.
2. **Ler o vault inteiro** (todas as notas `.md`, exceto `.obsidian/`). Registre nomes já usados:
   nomes de nota precisam ser únicos no vault todo.
3. **Modo**: se `_meta/Inventario.md` existe → Modo Atualização (SKILL.md §7).
4. **Estado do git**:
   ```bash
   git rev-parse --short HEAD
   git status --porcelain
   git log --oneline -n 30
   ```
   Árvore suja → registrar no Inventário "documentado sobre árvore com alterações locais: <arquivos>".
5. **Escopo**: liste TODOS os `package.json`, `project.json` (Nx), `angular.json > projects`,
   `functions/`, `supabase/`, `server/`, `apps/`, `libs/` (e equivalentes em outras stacks:
   `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `pubspec.yaml`,
   `Gemfile`, `composer.json`). Cada um é um app/pacote do inventário.
   ```bash
   find . -name package.json -not -path "*/node_modules/*" -not -path "*/dist/*"
   ```
6. **NUNCA leia**: `node_modules`, `dist`, `build`, `.angular`, `.firebase`, `.next`, `.nx`, `coverage`,
   `tmp`, `*.min.js`, assets binários (e equivalentes: `vendor/`, `target/`, `.venv/`, `__pycache__/`, `Pods/`).
7. **NÃO inventarie como itens** (mas PODE ler como fonte de tipos/schema): `*.generated.*`,
   `database.types.ts`, clientes de API gerados por codegen. Registre as exclusões no Inventário.
8. **NÃO leia lockfiles inteiros**; para versão exata use grep pontual
   (`grep -n '"@angular/core"' package-lock.json | head -3`).
9. **Leia**: README, `package.json`, configs (`angular.json`, `tsconfig*`, `firebase.json`, `.firebaserc`,
   `*.rules`, `*indexes.json`, vite/next config, `Dockerfile`, compose, CI em `.github/workflows` etc.,
   `.env.example`, `ngsw-config.json`), docs existentes (`docs/`, ADRs, `CLAUDE.md`, `AGENTS.md`) —
   docs são evidência a confirmar no código, e contradição docs × código vai para 13 Pendências.
   Migrations: liste todas; leia só as que definem ou alteram tabelas usadas pelo código (ou o schema
   consolidado, se existir).
10. **Identifique**: stack e versões, estrutura de pastas (propósito de cada pasta de topo), ambientes,
    como rodar/buildar/deployar (a partir de scripts e configs — sem executar nada), tamanho por área:
    ```bash
    find src -type f \( -name "*.ts" -o -name "*.html" \) | wc -l
    ```

### Adaptação à stack

As buscas e templates usam vocabulário de web app (Angular/React/Firebase/Supabase), o caso comum.
Traduza para a stack encontrada e registre "Não se aplica" com a busca que comprova.

| Tipo de projeto | Ênfase | Geralmente não se aplica |
|---|---|---|
| SPA/SSR web | Rotas, telas, modais, componentes, formulários, estado, fluxos | — |
| Angular | Rotas + guards/resolvers, standalone/NgModules, serviços e DI, interceptors, signals/RxJS, pipes, diretivas | "hooks" (usar serviços/signals/pipes) |
| React/Next | Roteamento por arquivo (`app/`, `pages/`), hooks, contexts, stores, server actions, route handlers | — |
| Backend/API | Endpoints, domínio, persistência, jobs, eventos, auth, contratos de erro | Telas, Catalogo UI |
| Mobile | Telas, pilha de navegação, módulos nativos, offline/sync, permissões | — |
| CLI/biblioteca | Comandos ou API pública, opções, pontos de extensão, empacotamento | Telas, rotas |
| Pipeline de dados/ML | Fontes, transformações, agendamentos, linhagem, checagens de qualidade | Telas, componentes |
| Infra (IaC) | Recursos, ambientes, módulos, ordem de deploy, raio de impacto | Telas, componentes |
| Monorepo | Mapa de apps/pacotes e dependências; inventário por app | Decidir por pacote |

## Fase 1 — Inventário mecânico (antes de documentar)

Crie `_meta/Inventario.md`. Cada item é uma linha de checklist com id, `arquivo → símbolo` e destino.

### 3.1 Definições
- **TELA** = rota, modal/dialog, bottom sheet ou drawer com ações próprias. Modal NÃO é rota, mas é
  tela: tem nota própria (`tipo: "modal"`).
- **Modos** (ex.: login/cadastro/reset no mesmo componente), **abas** e **passos de stepper** são SEÇÕES
  da nota da tela, cada um com suas próprias tabelas. Viram nota própria só se tiverem rota própria ou
  forem abertos de mais de um lugar.
- Componente **PÁGINA** = referenciado em rota ou aberto como modal. **COMPARTILHADO** = usado por 2+
  módulos ou com lógica/serviço injetado. **UI** = apresentacional, sem serviço de dados.
  Precedência: PÁGINA > COMPARTILHADO > UI (cada componente cai em uma só categoria).

### 3.2 Buscas mínimas
Adapte à stack e resolva constantes/template strings até o nome real. Sempre com exclusões
(`-g '!node_modules' -g '!dist'` …) e `-n` para ter linha.

- **Rotas**: arquivos de rotas + `loadChildren`, `loadComponent`, `children`, `canActivate`, `canMatch`,
  `canDeactivate`, `resolve`, `redirectTo`, `"**"`, `data`, `title`. Roteamento por arquivo: árvore de
  `app/` ou `pages/`.
- **Componentes**: `rg "@Component\(|export default function|export function [A-Z]"` (inclui templates inline).
- **Modais**: `rg "\.open\(|bottomSheet|modalCtrl\.create|Dialog"`
- **Formulários**: `FormGroup`, `FormBuilder`, `formControlName`, `ngModel`, `form(`, `useForm`, `<form`
- **Dados**: `collection(`, `collectionGroup(`, `.doc(`, `batch(`, `runTransaction(`, `FieldValue.`,
  `arrayUnion`, `arrayRemove`, `onSnapshot`, `valueChanges`, `snapshotChanges`, `.from(`, `.rpc(`,
  `storage`, `ref(`, `uploadBytes`, `getDownloadURL`, `http.(get|post|put|patch|delete)`, `fetch(`,
  `axios`, `httpResource`, `resource(`
- **Backend**: `onCall`, `onRequest`, `onDocument*`, `onSchedule`, `functions.`, rotas de servidor
  (express/nest/hono/fastify/koa; decorators `@Get(` `@Post(` …)
- **Auth**: `signIn*`, `createUser*`, `signOut`, `sendPasswordReset*`, providers, claims, roles
- **Também**: integrações externas (SDKs importados, URLs base), variáveis de ambiente (comando da
  regra 1.3), regras de segurança, índices, testes, scripts npm, CI/CD, `TODO`/`FIXME`/`HACK`/`XXX`,
  código comentado, i18n, analytics, feature flags, service worker, links externos estáticos (`href="http`).

**Resultados de busca são CANDIDATOS, não itens** (ex.: "storage" casa `localStorage`, `.open(` casa
`window.open`). Faça triagem: registre no Inventário só itens reais e, para cada padrão,
"N ocorrências, M descartadas (motivo)".

### 3.3 Destino de cada categoria (o checklist só fecha quando o destino existe)

| Categoria | Destino |
|---|---|
| Tela / modal / modo | 1 nota em `03 Telas` |
| Componente compartilhado | 1 nota em `04 Componentes` |
| Componente de UI | 1 linha em `04 Componentes/Catalogo UI` |
| Formulário | seção da nota da Tela/Modal onde aparece |
| Chamada ao banco | linha em "Chamadas" da Tela ou Serviço E em "Quem lê/escreve" da Coleção |
| Chamada HTTP | linha em "Chamadas" da Tela ou Serviço E na nota da API/Integração chamada |
| Coleção/tabela | 1 nota em `06 Dados` |
| Function/endpoint | 1 nota em `07 APIs` |
| Serviço/store | 1 nota em `08 Serviços e Estado` |
| Integração externa (SDK/API/serviço) | 1 nota em `09 Integrações` |
| Link externo estático (href) | 1 linha em `09 Integrações/Links externos` |
| Env var | linha na tabela de `11 Infra e Deploy` |
| TODO/FIXME/código suspeito | linha em `13 Pendências e Riscos` |
| Teste | contagem por área em `12 Qualidade` |

### 3.4 Estados do checklist
`[ ]` pendente | `[x]` documentado (com `[[link]]` para nota existente) | `[~]` parcial (motivo) |
`[!]` não confirmado (o que buscou). PROIBIDO `[x]` sem link.

Cada item já nasce com o NOME EXATO da nota de destino (seguindo a regra 1.6); todos os links usam
esse nome. No topo do Inventário: commit documentado, apps/pacotes, exclusões e TOTAIS por categoria
COM o comando que gerou cada contagem. Modelo em `templates.md` §Inventário.

### 3.5 Portão
Se o inventário tiver mais de ~150 itens, mais de um app/pacote, ou se o escopo for duvidoso:
PARE e mostre ao usuário apps/pacotes, exclusões, totais e número de lotes previsto. Siga só com o OK.
Fora desses casos, siga direto para a Fase 2.
