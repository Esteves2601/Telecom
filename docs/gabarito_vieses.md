# Gabarito de Vieses — Sprint 1 (arquivo privado, só o professor)

> Este arquivo documenta os padrões plantados de propósito no `vistorias.csv`.
> Os alunos NON devem ler antes da análise (T-15). Serve para o professor conferir
> se a dupla descobriu os vieses pela análise, e não pelo gabarito.

## Vieses plantados em `src/gerar_dataset.py`

| # | Viés | Como foi plantado | Onde aparece |
|---|------|-------------------|--------------|
| 1 | Região com conformidade bem pior | `CONF_REGIAO["Leste"] = 0.54` | Leste ≈ 54% de conformidade |
| 2 | Causa dominando não-conformidades | Peso 0.45 para `identificacao_porta` | ≈ 48% das não-conformidades |
| 3 | Técnicos com retrabalho concentrado | `RETRABALHO_TEC["tec_05"]=0.26`, `["tec_09"]=0.24` | tec_05 ≈ 25%, tec_09 ≈ 22% de reincidência |
| 4 | Queda de conformidade num período | `MES_QUEDA=(2026,3)`, `FATOR_QUEDA=0.70` | Março/2026: ~64% vs ~75% nos demais |

## Sujeira plantada (para a Sprint 2)

- `PROB_REGIAO_MINUSCULA = 0.02` → ~2% das regiões em minúsculo (`sul` em vez de `Sul`), para treinar padronização na limpeza.
- `PROB_CAUSA_NULA = 0.015` → ~1,5% dos não-conformes sem `causa` (nulo a ser decidido na limpeza).
- `PROB_MULTA_NULA = 0.02` → ~2% das multas não-conformes sem valor (`multa_valor` nulo).
- `PROB_EQUIPAMENTO_NULO = 0.02` → ~2% sem `equipamento`.
- `QTD_ABSURDOS = 4` → 2 linhas com `tempo_minutos` negativo e 2 com `checklist_score` > 1.
- `QTD_DUPLICATAS = 5` → 5 linhas duplicadas por `vistoria_id`.

## Obervação de reprodutibilidade

- Rodar sem `--seed` gera uma execução aleatória válida (DoD).
- Rodar com `--seed 42` reproduz exatamente o arquivo de referência.