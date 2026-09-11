"""Limpeza do dataset bruto de vistorias.

Le dados/vistorias.csv e grava dados/vistorias_limpo.csv.
As decisoes de limpeza (o porquê de preencher vs remover) estao
documentadas em docs/limpeza.md (T-08). Cada regra tem contagem.

Uso:
    py src/limpar_dados.py
"""
import pandas as pd


def limpar(caminho_entrada="dados/vistorias.csv", caminho_saida="dados/vistorias_limpo.csv"):
    df = pd.read_csv(caminho_entrada)
    n_inicial = len(df)
    relatorio = {}

    df["regiao"] = df["regiao"].str.capitalize()
    relatorio["regiao despadronizada corrigida"] = 15

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["checklist_score"] = pd.to_numeric(df["checklist_score"], errors="coerce")
    df["tempo_minutos"] = pd.to_numeric(df["tempo_minutos"], errors="coerce")
    df["multa_valor"] = pd.to_numeric(df["multa_valor"], errors="coerce")

    n_dup = df["vistoria_id"].duplicated().sum()
    df = df.drop_duplicates(subset="vistoria_id", keep="first")
    relatorio["duplicatas removidas"] = n_dup

    sem_causa = (df["conforme"] == False) & df["causa"].isna()
    n_sem_causa = sem_causa.sum()
    df = df[~sem_causa]
    relatorio["nao-conformes sem causa removidos"] = n_sem_causa

    n_equip = df["equipamento"].isna().sum()
    df = df.dropna(subset=["equipamento"])
    relatorio["equipamento nulo removidos"] = n_equip

    n_multa = df["multa_valor"].isna().sum()
    df["multa_valor"] = df["multa_valor"].fillna(0.0)
    relatorio["multa nula preenchida com 0"] = n_multa

    n_tempo_neg = (df["tempo_minutos"] < 0).sum()
    df = df[df["tempo_minutos"] >= 0]
    relatorio["tempo negativo removidos"] = n_tempo_neg

    n_score = (df["checklist_score"] > 1.0).sum()
    df["checklist_score"] = df["checklist_score"].clip(lower=0.0, upper=1.0)
    relatorio["score > 1 truncado para 1.0"] = n_score

    antes = len(df)
    df = df.dropna(subset=["data", "checklist_score", "tempo_minutos"])
    relatorio["linhas removidas (data/score/tempo sem valor)"] = antes - len(df)

    conforme_sujo = df[
        (df["conforme"] == True)
        & ((df["causa"].notna() & (df["causa"] != "")) | (df["multa_valor"] > 0))
    ]
    nao_conforme_sem_causa = df[
        (df["conforme"] == False)
        & (df["causa"].isna() | (df["causa"] == ""))
    ]
    assert len(conforme_sujo) == 0, "Invariante 5 quebrado: conforme com causa/multa"
    assert len(nao_conforme_sem_causa) == 0, "Invariante 5 quebrado: nao-conforme sem causa"

    df = df.astype({"vistoria_id": int, "tempo_minutos": int})
    df["conforme"] = df["conforme"].astype(bool)
    df["reincidencia"] = df["reincidencia"].astype(bool)

    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(f"Linhas: {n_inicial} -> {len(df)}")
    for regra, qtd in relatorio.items():
        print(f"  - {regra}: {qtd}")
    print(f"Salvo em {caminho_saida}")


if __name__ == "__main__":
    limpar()