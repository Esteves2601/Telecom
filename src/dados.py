"""Módulo de leitura e agregações dos dados de vistorias."""
import pandas as pd


COLUNAS_ESPERADAS = [
    "vistoria_id", "data", "tecnico", "regiao", "tipo",
    "conforme", "causa", "multa_valor", "checklist_score",
    "tempo_minutos", "reincidencia", "equipamento"
]


def carregar(caminho: str = "dados/vistorias_mentira.csv") -> pd.DataFrame:
    """
    Lê o CSV de vistorias e valida as 12 colunas do contrato.
    Troque o caminho para 'dados/vistorias_limpo.csv' quando o Rodrigo entregar.
    """
    df = pd.read_csv(caminho, parse_dates=["data"])

    faltando = [c for c in COLUNAS_ESPERADAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas faltando no CSV: {faltando}")

    # Tipos esperados
    df["conforme"] = df["conforme"].astype(bool)
    df["reincidencia"] = df["reincidencia"].astype(bool)
    df["multa_valor"] = pd.to_numeric(df["multa_valor"], errors="coerce").fillna(0)
    df["checklist_score"] = pd.to_numeric(df["checklist_score"], errors="coerce")
    df["tempo_minutos"] = pd.to_numeric(df["tempo_minutos"], errors="coerce")

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