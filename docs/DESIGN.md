# DESIGN — Vistoria de Campo (arquitetura viva)

> **Como o projeto é montado por dentro.** Enxuto de propósito — o projeto é simples e deve continuar simples. Este documento é o mapa técnico do Rodrigo, mas o Estevam também lê para saber o que consome.

---

## 1. As 4 camadas (do dado ao insight)

```
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 1 · FONTE                                            │
│  O formulário de vistoria (papel, planilha, ou script).     │
│  No projeto: um PROGRAMA que SIMULA vistorias reais.        │
│  → dono: Rodrigo                                            │
└───────────────────────────┬─────────────────────────────────┘
                            │ gera
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 2 · DADO                                            │
│  vistorias.csv (cru) ──limpeza──▶ vistorias_limpo.csv       │
│  Uma tabela plana. 1 linha = 1 vistoria.                    │
│  → dono: Rodrigo   |   FONTE DA VERDADE do projeto          │
└───────────────────────────┬─────────────────────────────────┘
                            │ é lido por
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 3 · ANÁLISE (back-end)                              │
│  dados.py: carrega o CSV e oferece funções de agregação     │
│  (taxa_conformidade, causas_pareto, multas_por_tipo, …)     │
│  → dono: Estevam                                           │
└───────────────────────────┬─────────────────────────────────┘
                            │ alimenta
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 4 · VISUALIZAÇÃO (front-end)                        │
│  painel: KPIs + gráficos (barras, Pareto, linha)            │
│  → dono: Estevam                                           │
└─────────────────────────────────────────────────────────────┘
```

**Princípio de ouro:** o dado flui numa direção só, de cima para baixo. A Camada 4 nunca inventa número — ela só mostra o que a Camada 3 calculou a partir da Camada 2.

---

## 2. Modelo de dados — `vistorias.csv`

**Uma tabela só, plana.** Sem banco relacional. Cada linha é uma vistoria concluída.

| Coluna | Tipo | Valores possíveis | Exemplo |
|--------|------|-------------------|---------|
| `vistoria_id` | inteiro | único (chave) | 4821 |
| `data` | data | — | 2026-03-14 |
| `tecnico` | categoria | `tec_01` … `tec_12` | "tec_07" |
| `regiao` | categoria | `Norte`, `Sul`, `Leste`, `Oeste`, `Centro` | "Sul" |
| `tipo` | categoria | `instalacao`, `reparo`, `auditoria` | "reparo" |
| `conforme` | booleano | `True` / `False` | True |
| `causa` | categoria | `identificacao_porta`, `vedacao_cto`, `ancoragem_cabo`, `sobra_fibra`, `documentacao`, `outros` (vazio se conforme) | "identificacao_porta" |
| `multa_valor` | decimal | ≥ 0 (0 se conforme) | 450.00 |
| `checklist_score` | decimal 0–1 | 0.0 – 1.0 | 0.75 |
| `tempo_minutos` | inteiro | > 0 | 95 |
| `reincidencia` | booleano | `True` / `False` | False |
| `equipamento` | categoria | `ONU`, `ROTEADOR`, `CABO` | "ONU" |

> **Nota de decisão:** a coluna `supervisor` do desenho original foi substituída por `equipamento`, e `tempo_exec_min` foi renomeada para `tempo_minutos`, para casar com o schema já implementado em `src/dados.py` pelo Estevam. Nome e tipo desta tabela são o **contrato** — qualquer mudança exige DEC + aviso (GAIA).

### Regras do modelo (invariantes)
- Se `conforme = True`, então `causa` é vazia e `multa_valor = 0`.
- `checklist_score` alto tende a `conforme = True`, mas **nem sempre** (deixe ruído realista).
- `reincidencia = True` só existe em vistorias que já foram não-conformes antes.

### Vieses plantados de propósito (para os alunos DESCOBRIREM)
> Isto é o que torna o projeto interessante. Rodrigo planta padrões escondidos; a análise revela.
- Uma região (ex.: "Leste") tem conformidade bem pior que as outras.
- Uma causa (ex.: "identificacao_porta") domina as não-conformidades.
- Um ou dois técnicos concentram o retrabalho.
- A conformidade cai num período específico (ex.: um mês de pico).

---

## 3. Categorias sugeridas (o "vocabulário" do dado)

- **tipo:** `instalacao`, `reparo`, `auditoria`
- **regiao:** `Norte`, `Sul`, `Leste`, `Oeste`, `Centro`
- **causa:** `identificacao_porta`, `vedacao_cto`, `ancoragem_cabo`, `sobra_fibra`, `documentacao`, `outros`
- **tecnico:** `tec_01` … `tec_12`
- **equipamento:** `ONU`, `ROTEADOR`, `CABO`

---

## 4. Ponto de costura Rodrigo ↔ Estevam (o contrato de interface)

Este é o único lugar onde as duas frentes se tocam. Tratem como um **contrato**.

```
        RODRIGO ENTREGA                    ESTEVAM CONSOME
   ┌──────────────────────────┐      ┌──────────────────────────┐
   │ vistorias_limpo.csv      │      │ pd.read_csv(...)         │
   │ com EXATAMENTE as 12     │─────▶│ espera as 12 colunas     │
   │ colunas do §2, nos tipos │      │ com os nomes e tipos     │
   │ combinados               │      │ combinados               │
   └──────────────────────────┘      └──────────────────────────┘
              │                                  │
              └──── dicionario_de_dados.md ──────┘
                    (a fonte que os dois consultam)
```

**Contrato de estabilidade:** o nome e o tipo de cada coluna **não mudam** depois de combinados no fim da Sprint 1. Se precisar mudar, é uma **decisão registrada** (`decisoes/DEC-001.md`) e o Estevam é avisado antes.

---

## 5. Escolhas técnicas (mantidas simples)

| Decisão | Escolha | Por quê |
|---------|---------|---------|
| Linguagem | Python 3 | padrão de análise de dados, gratuito |
| Biblioteca de dados | pandas | manipula tabelas com facilidade |
| Gráficos | matplotlib (e/ou seaborn) | simples, roda em qualquer lugar |
| Formato de análise | Jupyter Notebook (`.ipynb`) | mistura código, número e texto |
| Painel | notebook OU HTML estático simples | sem servidor, sem complexidade |
| Versionamento | Git + GitHub | os dois trabalham no mesmo repo |

> **Alternativa sem código:** se travar no Python, a Camada 2/3/4 pode ser feita no Google Sheets (tabela dinâmica + gráficos). Perde-se rigor, mas fecha o ciclo. Decisão do professor.

---

## 6. Estrutura de pastas do repositório (o que o Rodrigo monta na Sprint 1)

```
vistoria-campo/
├── README.md                 # como rodar (Rodrigo, Sprint 4)
├── dados/
│   ├── vistorias.csv         # cru
│   └── vistorias_limpo.csv   # limpo (fonte da verdade)
├── src/
│   ├── gerar_dataset.py      # Rodrigo, Sprint 1
│   ├── limpar_dados.py       # Rodrigo, Sprint 2
│   └── dados.py              # Estevam, Sprint 2 (leitura + agregações)
├── notebooks/
│   └── analise.ipynb         # ambos, Sprint 3
├── painel/                   # Estevam, Sprint 4
├── docs/
│   └── dicionario_de_dados.md
└── RELATORIO_FINAL.md        # Rodrigo, Sprint 4
```
