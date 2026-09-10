# Vistoria de Campo — Telecom

Análise de dados de vistorias de campo para identificar falhas, causas e custos.

## Estrutura
- `dados/` — CSVs (bruto e limpo)
- `src/` — código Python (`gerar_dataset.py`, `limpar_dados.py`, `dados.py`)
- `notebooks/` — EDA e análise (`limpeza.ipynb`, `analise.ipynb`)
- `painel/` — dashboard (`painel.ipynb`)
- `docs/` — dicionário, limpeza, relatório final

## Como rodar
```bash
pip install -r requirements.txt
python src/gerar_dataset.py          # gera dados/vistorias.csv
python src/limpar_dados.py           # gera dados/vistorias_limpo.csv
jupyter notebook notebooks/analise.ipynb
jupyter notebook painel/painel.ipynb
```