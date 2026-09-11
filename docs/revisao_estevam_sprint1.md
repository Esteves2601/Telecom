# Sprint 1 — Controle do Estevam (T-04 + revisões)

## T-04 — Montar repositório e ambiente [DONO: Estevam]
- [x] Repo `Telecom` criado no GitHub
- [ ] Rodrigo convidado como colaborador (fazer em Settings > Collaborators)
- [x] Estrutura DESIGN §6: `dados/ src/ notebooks/ painel/ docs/`
- [x] Python 3.11.9 + `venv`
- [x] `pandas 3.0.5` + `matplotlib` + `jupyter` instalados
- [x] `requirements.txt` gerado via `pip freeze`
- [x] `README.md` inicial + `.gitignore` (ignora `venv/`)
- [x] Teste: `import pandas` OK + `python src/dados.py` OK
- [x] Branch `estevam/modulo-dados` + push + PR aberto para Rodrigo revisar

**DoD T-04:** os dois clonam, instalam e rodam `import pandas` sem erro.
```bash
git clone https://github.com/Esteves2601/Telecom.git
cd Telecom
py -3.11 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -c "import pandas; print('ok!')"
```

## Prova de leitura do CSV de mentira (destrava Sprint 2)
- [x] `dados/vistorias_mentira.csv`: 20 linhas, 12 colunas exatas do DESIGN §2
- [x] `src/dados.py::carregar()` valida as 12 colunas + converte tipos + checa Invariante 5
- Resultado em 11/09/2026: 20 linhas, taxa 50.0%, por região Norte 25% / Leste 40% / Oeste 50% / Sul 66.67% / Centro 100%

## Revisões do Estevam (papel de REVISOR)
### T-01 — Requisitos e 6 perguntas (Rodrigo)
- [ ] As 6 perguntas estão escritas e numeradas?
- [ ] Persona-alvo escolhida (ex.: supervisor)?
- [ ] Seção `## Problema e Perguntas` existe?

### T-02 — Modelo de dados / schema (Rodrigo) — CONTRATO CRÍTICO
- [x] 12 colunas com nomes EXATOS (decisão vigente T-02, merge PR #1): `vistoria_id,data,tecnico,regiao,tipo,conforme,causa,multa_valor,checklist_score,tempo_minutos,reincidencia,equipamento`
- [x] Tipos e categorias batem com `docs/DESIGN.md §2` + `docs/dicionario_de_dados.md`? (`tipo`: instalacao/reparo/auditoria; `equipamento`: ONU/ROTEADOR/CABO)
- [x] **Assinatura Estevam:** programo contra essas 12 colunas, sem inventar coluna (GAIA_PROTOCOLO). `dados.py` alinhado.

### T-03 — Gerador do dataset (Rodrigo)
- [ ] `python src/gerar_dataset.py` cria `dados/vistorias.csv` com 600-1500 linhas?
- [ ] Respeita Invariante 5 (conforme => causa vazia, multa 0)?
- [ ] Vieses plantados mas NÃO contados ao Estevam? (`docs/gabarito_vieses.md` privado)

### T-05 — Dicionário de dados (Rodrigo)
- [ ] `docs/dicionario_de_dados.md` explica as 12 colunas (nome, tipo, descrição, valores, exemplo)?
- [ ] Uma pessoa de fora entende cada coluna só lendo?

## Próximo (Sprint 2 — T-09/T-10, já destravado)
- [ ] T-09: `carregar()` trocar caminho para `dados/vistorias_limpo.csv` quando Rodrigo entregar T-07
- [ ] T-10: conferir `taxa_conformidade()` à mão (Invariante 2)
