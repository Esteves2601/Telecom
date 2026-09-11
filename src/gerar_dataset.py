"""Gera o dataset bruto de vistorias de campo (Telecom).

Uso:
    py src/gerar_dataset.py                # gera dados/vistorias.csv
    py src/gerar_dataset.py --seed 42      # mesma execucao sempre (reprodutivel)
    py src/gerar_dataset.py --linhas 800   # define o numero de linhas
"""
import argparse
import csv
import random
from datetime import date, timedelta

COLUNAS = [
    "vistoria_id", "data", "tecnico", "regiao", "tipo", "conforme",
    "causa", "multa_valor", "checklist_score", "tempo_minutos",
    "reincidencia", "equipamento",
]

REGIOES = ["Norte", "Sul", "Leste", "Oeste", "Centro"]
TIPOS = ["instalacao", "reparo", "auditoria"]
CAUSAS = [
    "identificacao_porta", "vedacao_cto", "ancoragem_cabo",
    "sobra_fibra", "documentacao", "outros",
]
TECNICOS = [f"tec_{i:02d}" for i in range(1, 13)]
EQUIPAMENTOS = ["ONU", "ROTEADOR", "CABO"]

CONF_REGIAO = {
    "Norte": 0.86, "Sul": 0.84, "Leste": 0.54,
    "Oeste": 0.83, "Centro": 0.85,
}

MES_QUEDA = (2026, 3)
FATOR_QUEDA = 0.70

RETRABALHO_TEC = {f"tec_{i:02d}": 0.08 for i in range(1, 13)}
RETRABALHO_TEC["tec_05"] = 0.26
RETRABALHO_TEC["tec_09"] = 0.24

PESOS_CAUSA = [0.45, 0.20, 0.13, 0.08, 0.07, 0.07]
MULTA_FAIXA = {
    "identificacao_porta": (400.0, 800.0),
    "vedacao_cto": (300.0, 700.0),
    "ancoragem_cabo": (200.0, 500.0),
    "sobra_fibra": (100.0, 350.0),
    "documentacao": (80.0, 250.0),
    "outros": (100.0, 400.0),
}
PROB_MULTA = 0.60
PROB_REGIAO_MINUSCULA = 0.02
PROB_CAUSA_NULA = 0.015
PROB_MULTA_NULA = 0.02
PROB_EQUIPAMENTO_NULO = 0.02
QTD_ABSURDOS = 4
QTD_DUPLICATAS = 5

DATA_INICIO = date(2025, 7, 1)
DATA_FIM = date(2026, 6, 30)


def data_aleatoria(rng):
    delta = (DATA_FIM - DATA_INICIO).days
    return DATA_INICIO + timedelta(days=rng.randint(0, delta))


def vez_queda(data):
    return (data.year, data.month) == MES_QUEDA


def gerar_linha(rng, vistoria_id):
    regiao = rng.choice(REGIOES)
    if rng.random() < PROB_REGIAO_MINUSCULA:
        regiao = regiao.lower()
    tipo = rng.choice(TIPOS)
    tecnico = rng.choice(TECNICOS)
    equipamento = rng.choices(EQUIPAMENTOS, weights=[0.45, 0.40, 0.15])[0]

    data = data_aleatoria(rng)
    score_bruto = rng.uniform(0.35, 1.0)
    prob = CONF_REGIAO[regiao.capitalize()] * (0.55 + 0.60 * score_bruto)
    prob = min(prob, 0.98)
    if vez_queda(data):
        prob *= FATOR_QUEDA
    conforme = rng.random() < prob

    checklist_score = (
        rng.uniform(0.72, 1.0) if conforme else rng.uniform(0.30, 0.85)
    )
    causa = ""
    multa_valor = 0.0
    if not conforme:
        causa = rng.choices(CAUSAS, weights=PESOS_CAUSA)[0]
        if rng.random() < PROB_MULTA:
            minimo, maximo = MULTA_FAIXA[causa]
            multa_valor = round(rng.uniform(minimo, maximo), 2)

    tempo_minutos = (
        rng.randint(35, 90) if conforme else rng.randint(90, 200)
    )

    prob_reinc = RETRABALHO_TEC[tecnico]
    if not conforme:
        prob_reinc = min(0.9, prob_reinc * 2.5)
    reincidencia = rng.random() < prob_reinc

    return {
        "vistoria_id": vistoria_id,
        "data": data.isoformat(),
        "tecnico": tecnico,
        "regiao": regiao,
        "tipo": tipo,
        "conforme": str(conforme),
        "causa": causa,
        "multa_valor": f"{multa_valor:.2f}",
        "checklist_score": f"{checklist_score:.2f}",
        "tempo_minutos": tempo_minutos,
        "reincidencia": str(reincidencia),
        "equipamento": equipamento,
    }


def plantar_sujeira(rng, rows):
    for r in rows:
        if r["conforme"] == "False" and rng.random() < PROB_CAUSA_NULA:
            r["causa"] = ""
        if (
            r["conforme"] == "False"
            and r["multa_valor"] != ""
            and float(r["multa_valor"]) > 0
            and rng.random() < PROB_MULTA_NULA
        ):
            r["multa_valor"] = ""
        if rng.random() < PROB_EQUIPAMENTO_NULO:
            r["equipamento"] = ""

    absurdos = rng.sample(range(len(rows)), QTD_ABSURDOS)
    for i, idx in enumerate(absurdos):
        r = rows[idx]
        if i < 2:
            r["tempo_minutos"] = rng.randint(-60, -5)
        else:
            r["checklist_score"] = f"{rng.uniform(1.05, 1.20):.2f}"

    for id_duplicar in rng.sample([r["vistoria_id"] for r in rows], QTD_DUPLICATAS):
        for r in rows:
            if r["vistoria_id"] == id_duplicar:
                rows.append(r.copy())
                break


def main():
    parser = argparse.ArgumentParser(description="Gerador do dataset de vistorias")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--linhas", type=int, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    n_linhas = args.linhas if args.linhas else rng.randint(800, 1100)

    rows = [gerar_linha(rng, 1000 + i) for i in range(1, n_linhas + 1)]
    plantar_sujeira(rng, rows)

    caminho = "dados/vistorias.csv"
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Salvo em {caminho}")
    print(f"Linhas: {len(rows)}")
    print(f"Colunas: {len(COLUNAS)}")


if __name__ == "__main__":
    main()