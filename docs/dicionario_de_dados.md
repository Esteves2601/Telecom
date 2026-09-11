# Dicionário de Dados — `vistorias.csv`

> **Task:** T-05 · **Responsável:** Rodrigo · **Revisor:** Estevam
> Define cada coluna do `vistorias.csv` (e do `vistorias_limpo.csv`). O schema vigente está em `docs/DESIGN.md §2` — este dicionário é a fonte de consulta dos dois alunos (Invariante 1 e 6).
> **Granularidade:** 1 linha = 1 vistoria concluída.

## Dicionário das 12 colunas

| Coluna | Tipo | Descrição | Valores possíveis | Exemplo |
|--------|------|-----------|-------------------|---------|
| `vistoria_id` | inteiro | Identificador único da vistoria (chave) | inteiro positivo, sem repetição | 4821 |
| `data` | data | Data em que a vistoria foi realizada | `YYYY-MM-DD` | 2026-03-14 |
| `tecnico` | categoria | Código do técnico que executou o serviço | `tec_01` … `tec_12` | "tec_07" |
| `regiao` | categoria | Zona da cidade onde o serviço foi feito | `Norte`, `Sul`, `Leste`, `Oeste`, `Centro` | "Sul" |
| `tipo` | categoria | Tipo de serviço executado | `instalacao`, `reparo`, `auditoria` | "reparo" |
| `conforme` | booleano | Veredito da vistoria: passou na norma? | `True` / `False` | False |
| `causa` | categoria | Item que reprovou a vistoria (vazio se conforme) | `identificacao_porta`, `vedacao_cto`, `ancoragem_cabo`, `sobra_fibra`, `documentacao`, `outros` | "identificacao_porta" |
| `multa_valor` | decimal | Valor da multa aplicada (0 se não houve multa) | ≥ 0, em R$ | 450.00 |
| `checklist_score` | decimal | Itens OK ÷ total de itens do checklist | de 0.00 a 1.00 | 0.75 |
| `tempo_minutos` | inteiro | Duração da vistoria em minutos | inteiro > 0 | 95 |
| `reincidencia` | booleano | Esta vistoria voltou não-conforme (retrabalho de um problema anterior)? | `True` / `False` | False |
| `equipamento` | categoria | Tipo de equipamento envolvido no serviço | `ONU`, `ROTEADOR`, `CABO` | "ONU" |

## Regras de coerência (Invariante 5)

- Se `conforme = True` → `causa` fica vazia **e** `multa_valor = 0.00`.
- Se `conforme = False` → `causa` obrigatoriamente preenchida.
- `multa_valor` só pode ser maior que zero em vistorias não-conformes.
- `reincidencia = True` indica retrabalho de um problema já vistoriado antes.

## Observação (Invariante 1)

O painel usa apenas colunas que existem aqui. Se uma coluna for lida no código (`dados.py`) e não estiver neste dicionário, é violação do Invariante 1.