# T-10 — Conferência à mão (Invariante 2) — 11/09/2026

Método independente: contagem via `csv` puro (sem pandas, sem `dados.py`),
linha a linha no `dados/vistorias_mentira.csv` (20 linhas).

## Contagem manual por região
| Região | Total | Conformes | Conta | Função `conformidade_por_regiao()` | Bate? |
|--------|-------|-----------|-------|------------------------------------|-------|
| Sul | 6 (4821 T, 4823 T, 4824 F, 4829 T, 4834 F, 4839 T) | 4 | 4/6 = 66.67% | 66.67% | ✅ |
| Norte | 4 (4822 F, 4826 F, 4831 T, 4836 F) | 1 | 1/4 = 25.0% | 25.0% | ✅ |
| Oeste | 4 (4825 T, 4830 F, 4835 T, 4840 F) | 2 | 2/4 = 50.0% | 50.0% | ✅ |
| Leste | 5 (4827 T, 4828 F, 4832 F, 4833 T, 4838 F) | 2 | 2/5 = 40.0% | 40.0% | ✅ |
| Centro | 1 (4837 T) | 1 | 1/1 = 100.0% | 100.0% | ✅ |
| **Geral** | **20** | **10** | **10/20 = 50.0%** | `taxa_conformidade()` = **50.0%** | ✅ |

## Invariante 5 (coerência)
0 linhas "conforme com causa/multa" — CSV íntegro.

## Conclusão DoD T-10
Números da função batem com a conta manual. Bug futuro estará no dado ou no gráfico, não na função.
Quando `dados/vistorias_limpo.csv` (T-07, Rodrigo) existir, `carregar()` usa ele
automaticamente; repetir esta conferência no limpo antes da Sprint 3.
