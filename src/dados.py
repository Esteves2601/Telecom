"""Módulo de leitura e agregações dos dados de vistorias."""
import pandas as pd


# Contrato de schema — DESIGN.md §2 (não mudar sem DEC + aviso, ver GAIA_PROTOCOLO)
COLUNAS_ESPERADAS = [
    "vistoria_id", "data", "tipo", "regiao", "tecnico", "supervisor",
    "checklist_score", "conforme", "causa", "multa_valor",
    "reincidencia", "tempo_exec_min",
]


def carregar(caminho: str = "dados/vistorias_mentira.csv") -> pd.DataFrame:
    """
    Lê o CSV de vistorias e valida as 12 colunas do contrato.
    Troque o caminho para 'dados/vistorias_limpo.csv' quando o Rodrigo entregar.
    """
    df = pd.read_csv(caminho, parse_dates=["data"])

    faltando = [c for c in COLUNAS_ESPERADAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas faltando no CSV: {faltando} (contrato DESIGN §2)")

    # Tipos esperados — aceita "True/False" como texto ou booleano
    for col in ("conforme", "reincidencia"):
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"true": True, "1": True, "false": False, "0": False})
        )
    df["multa_valor"] = pd.to_numeric(df["multa_valor"], errors="coerce").fillna(0)
    df["checklist_score"] = pd.to_numeric(df["checklist_score"], errors="coerce")
    df["tempo_exec_min"] = pd.to_numeric(df["tempo_exec_min"], errors="coerce")
    df["vistoria_id"] = pd.to_numeric(df["vistoria_id"], errors="coerce")

    # Invariante 5: conforme => sem causa e sem multa (só avisa, não quebra)
    incoerentes = df[(df["conforme"] == True) & ((df["causa"].fillna("").str.strip() != "") | (df["multa_valor"] != 0))]
    if len(incoerentes):
        print(f"Aviso Invariante 5: {len(incoerentes)} linha(s) 'conforme com causa/multa'.")

    return df


def taxa_conformidade(df: pd.DataFrame) -> float:
    """% de vistorias conformes (0 a 100)."""
    return round(df["conforme"].mean() * 100, 2)


def conformidade_por_regiao(df: pd.DataFrame) -> pd.Series:
    """Taxa de conformidade por região, ordenada do pior pro melhor."""
    return (
        df.groupby("regiao")["conforme"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values()
    )


if __name__ == "__main__":
    # Teste rápido
    df = carregar()
    print(f"Linhas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    print(f"Taxa conformidade geral: {taxa_conformidade(df)}%")
    print("\nPor região:")
    print(conformidade_por_regiao(df))