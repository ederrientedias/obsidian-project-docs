# Fase 4 — Auditoria (obrigatória)

Copie os scripts da skill para `/tmp` (ou o diretório temporário da sessão) antes de rodar. Ambos só
leem o PROJETO/VAULT, não usam rede e usam só a biblioteca padrão do Python.

```bash
cp "<skill>/scripts/validate_vault.py" "<skill>/scripts/cobertura_fontes.py" /tmp/
```

## 1. Cobertura de arquivos por busca independente
Refaça as buscas da 3.2 de forma independente. Para cada ARQUIVO com ocorrência real, confirme por
script que ele aparece em `fontes` de alguma nota ou no `_meta/Mapa Codigo-Notas`.

```bash
python3 -I /tmp/cobertura_fontes.py "<PROJETO>" "<VAULT>"            # relatório legível
python3 -I /tmp/cobertura_fontes.py "<PROJETO>" "<VAULT>" --json     # para o relatório
```
O script aplica os padrões da 3.2 (com exclusões da Fase 0) e lista, por categoria, arquivos com
ocorrência que nenhuma nota cita. É um detector de CANDIDATOS: triagem manual de cada um (real →
documentar; falso positivo → registrar o motivo no Relatório). Use `--extra-pattern` para padrões
da stack que o script não cobre. Cubra os arquivos não cobertos e mostre comandos e contagens no relatório.

## 2. Validação mecânica do vault
```bash
python3 -I /tmp/validate_vault.py "<VAULT>"
```
Valida: links quebrados, notas órfãs, YAML inválido (aspas, `tags` com `#`, `tipo` fora da lista,
⚠️ sem `status: "parcial"`), nomes duplicados e caracteres proibidos, `[x]` sem link no Inventário,
notas sem `commit`/`fontes`, marcadores `gerado` desbalanceados, Mermaid fora dos tipos permitidos ou
com nós demais, strings com cara de segredo. Precisa terminar sem erros. Se o VAULT for subpasta de
um vault maior, passe `--vault-root <raiz do vault>` para checar unicidade de nomes no vault inteiro.

## 3. Verificação independente
Escolha as 3 telas com mais código, o maior formulário e a function/serviço com mais efeitos
colaterais. Se puder usar subagente: um subagente com contexto limpo recebe só a nota e os arquivos
citados e lista divergências (afirmação sem evidência, linha errada, interação faltando, efeito final
errado, campo faltando). Sem subagentes, faça você mesmo relendo os arquivos do zero. Corrija tudo e
registre as divergências.

Faça também o teste prático: escolha 2–3 tarefas realistas (adicionar um campo a uma coleção e
mostrá-lo numa tela; achar onde uma regra de negócio é aplicada; rodar o projeto localmente) e
confira que o vault sozinho leva aos arquivos e passos certos.

## 4. Relatório de Cobertura
Gere `_meta/Relatorio de Cobertura.md`: totais inventariados × documentados (com comandos), itens
`[~]` e `[!]`, saída resumida dos scripts 1 e 2, divergências corrigidas, lacunas que exigem
informação humana.

## Critério de conclusão
Concluído = zero itens `[ ]`, `validate_vault.py` sem erros e `Home.md` linkando todas as seções.
Diferenças que não puderem ser resolvidas são listadas e justificadas, não escondidas.
