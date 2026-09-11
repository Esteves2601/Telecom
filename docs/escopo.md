# Escopo — Problema e Perguntas de Análise

> **Task:** T-01 · **Responsável:** Rodrigo · **Revisor:** Estevam
> Baseado no `requirements/REQUIREMENTS.md` (§1, §2, §7).

---

## Problema

Uma operadora de internet/fibra registra centenas de vistorias de campo, mas os dados ficam parados: ninguém consegue enxergar onde a operação falha, por quê, e quanto isso custa. O objetivo do projeto é transformar esses registros em descobertas visuais — qual região não cumpre a norma, quais causas mais reprovam os serviços, quanto se perde em multa — para que a decisão saia de um painel com números, e não do achismo.

---

## As 6 perguntas de análise

| # | Pergunta | O que ela vai descobrir |
|---|----------|-------------------------|
| 1 | Qual região tem a pior taxa de conformidade? | Qual região sai com mais serviço reprovado pela norma |
| 2 | Quais causas mais reprovam as vistorias? (Pareto) | Se poucos motivos (ex.: cabo mal ancorado) explicam a maioria das falhas |
| 3 | Qual o custo total das multas, por tipo de serviço? | Qual tipo de serviço (instalação/reparo) mais gera multa em R$ |
| 4 | Qual a taxa de reincidência (retrabalho)? | Com que frequência o problema volta e o técnico precisa refazer |
| 5 | Técnico que faz mais vistorias é técnico que erra menos? | Se técnico produtivo é também o mais conforme |
| 6 | A conformidade piora em algum período? | Se existe um mês/semana em que a qualidade despencou |

---

## Persona-alvo do painel

<!-- Escolha uma persona (sugestão: supervisor). Ver REQUIREMENTS §3. -->

- [ ] Técnico de campo
- [x] Supervisor
- [ ] Gestor

---

## Check (DoD da T-01)

- [x] As 6 perguntas estão escritas e numeradas
- [ ] O Estevam leu e concorda que são respondíveis por um CSV
- [x] Problema escrito com palavras próprias