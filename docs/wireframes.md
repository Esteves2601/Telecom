# Wireframes Textuais — Vistoria de Campo

> Desenho das duas telas em ASCII. A **Tela 1** é a fonte do dado (só serve para entender de onde vem o dataset — não precisa ser construída de verdade). A **Tela 2** é a ENTREGA: o painel que o Estevam constrói.

---

## TELA 1 — Formulário de Coleta (celular do técnico)

> Papel: mostrar de onde nasce cada linha do CSV. Cada envio = 1 linha de dado.
> **No projeto, pode ser apenas SIMULADO pelo `gerar_dataset.py`** — não é obrigatório programar esta tela.

```
┌─────────────────────────────────────┐
│ ●●●        OS de Vistoria #4821      │
├─────────────────────────────────────┤
│                                     │
│  TIPO DE VISTORIA                   │
│  [ Instalação ]( Reparo )( Auditoria)│
│                                     │
│  REGIÃO                             │
│  ┌─────────────────────────────────┐│
│  │ Sul                            ▾ ││
│  └─────────────────────────────────┘│
│                                     │
│  CHECKLIST DE ENQUADRAMENTO         │
│   [x] Ancoragem do cabo drop        │
│   [x] Vedação da CTO                │
│   [!] Identificação da porta ◄ falha│
│   [x] Sobra técnica de fibra        │
│   → checklist_score = 3/4 = 0.75    │
│                                     │
│  FOTOS (evidência)                  │
│   ┌────┐ ┌────┐ ┌────┐              │
│   │ +  │ │ +  │ │ +  │              │
│   └────┘ └────┘ └────┘              │
│                                     │
│  RESULTADO                          │
│  ( Conforme )   [ NÃO-CONFORME ]    │
│                                     │
│  CAUSA (se não-conforme)            │
│  ┌─────────────────────────────────┐│
│  │ identificacao_porta            ▾ ││
│  └─────────────────────────────────┘│
│                                     │
│  MULTA?  ( Não )  [ SIM · R$ 450 ]  │
│                                     │
│  ┌─────────────────────────────────┐│
│  │        ENVIAR VISTORIA  →        ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
        │
▼ grava 1 linha no CSV:
    4821, 2026-03-14, tec_07, Sul, reparo,
    True, , 0.0, 0.75, 95, False, ONU
```

**Mapeamento campo → coluna** (importante para o Rodrigo ao gerar o dado):

| Campo da tela | Coluna no CSV |
|---------------|---------------|
| Tipo de vistoria | `tipo` |
| Região | `regiao` |
| Checklist (itens OK / total) | `checklist_score` |
| Resultado | `conforme` |
| Causa | `causa` |
| Multa | `multa_valor` |

---

## TELA 2 — Painel de Análise (desktop do supervisor) ← A ENTREGA

> Papel: responder as 6 perguntas visualmente. **Isto o Estevam constrói de verdade.**
> Nenhum número aqui é digitado — TODOS vêm de agregação do CSV.

```
┌──────────────────────────────────────────────────────────────────────┐
│ ●●●            Painel de Conformidade — Vistorias          [ mês ▾ ]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│  │ CONFORME   │ │ NÃO-CONF.  │ │ MULTAS R$  │ │ REINCIDÊNC.│         │
│  │            │ │            │ │            │ │            │         │
│  │   82%      │ │   143      │ │  28,6 mil  │ │   11%      │         │
│  │ ↑ 4pp mês  │ │ de 812     │ │ 61 casos   │ │ retrabalho │         │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘         │
│    KPI 1          KPI 2           KPI 3           KPI 4               │
│                                                                      │
│  ┌─────────────────────────────┐  ┌───────────────────────────────┐  │
│  │ CONFORMIDADE POR REGIÃO      │  │ CAUSAS DE NÃO-CONFORMIDADE     │  │
│  │ (gráfico de barras)          │  │ (Pareto — barras horizontais) │  │
│  │                             │  │                               │  │
│  │  100┤                       │  │ Identificação ███████████ 38% │  │
│  │   75┤ ██    ██        ██    │  │ Vedação CTO   ████████    27% │  │
│  │   50┤ ██ ██ ██ ▓▓ ██  ██    │  │ Ancoragem     █████       18% │  │
│  │   25┤ ██ ██ ██ ▓▓ ██  ██    │  │ Sobra fibra   ███         11% │  │
│  │    0┼──────────────────────  │  │ Outros        ██           6% │  │
│  │      Sul Nor Les Oes Cen    │  │                               │  │
│  │           ▲ Leste = 54% pior│  │ ▲ 2 causas = 65% das falhas   │  │
│  └─────────────────────────────┘  └───────────────────────────────┘  │
│      responde PERGUNTA 1              responde PERGUNTA 2             │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ TENDÊNCIA DE CONFORMIDADE (linha, por semana)                 │   │
│  │  90%┤        ╭─╮      ╭──╮                                    │   │
│  │  80%┤ ╭──╮ ╭─╯ ╰─╮ ╭──╯  ╰╮   ◀ queda na semana 4            │   │
│  │  70%┤╭╯  ╰─╯     ╰─╯       ╰──                                │   │
│  │     └S1──S2──S3──S4──S5──S6──S7                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│      responde PERGUNTA 6                                             │
└──────────────────────────────────────────────────────────────────────┘
```

**Cada elemento do painel → qual pergunta responde → qual função do back-end usa:**

| Elemento | Pergunta | Função em `dados.py` |
|----------|----------|----------------------|
| KPI Conforme | geral | `taxa_conformidade()` |
| KPI Não-conformes | RF-04 | `contagem_nao_conforme()` |
| KPI Multas | Pergunta 3 | `total_multas()` |
| KPI Reincidência | Pergunta 4 | `taxa_reincidencia()` |
| Barras por região | Pergunta 1 | `conformidade_por_regiao()` |
| Pareto de causas | Pergunta 2 | `causas_pareto()` |
| Linha tendência | Pergunta 6 | `conformidade_por_periodo()` |

> As perguntas 3 e 5 podem entrar como um 4º gráfico ou como tabela no relatório — decisão da dupla.

---

## Ciclo de estados de uma vistoria (base da análise de reincidência)

```
  ( aberta ) ──▶ [ em vistoria ] ──▶ < avaliada > ──── conforme ──▶ ( fim ✓ )
                                          │
                                          └── não-conforme ──▶ [ multa ] ──▶ [ reabre ]
                                                                                  │
                                          ┌───────────────────────────────────────┘
                                          ▼
                                   ( volta ao fluxo )
```

Quando uma vistoria passa por "reabre", a próxima vistoria daquele ponto ganha `reincidencia = True`. É isso que a **Pergunta 4** mede.

---

## Nota para o Estevam sobre os gráficos

- **Barras** → comparar categorias (região, técnico). Ordena do pior pro melhor.
- **Pareto (barras horizontais ordenadas)** → mostrar que poucas causas dominam.
- **Linha** → mostrar evolução no tempo.
- **Regra de título:** o título afirma o insight, não descreve o eixo.
  - ❌ "Conformidade por região"
  - ✅ "Leste concentra a pior conformidade (54%)"
