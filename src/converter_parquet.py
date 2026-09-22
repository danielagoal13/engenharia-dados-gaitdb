from pathlib import Path

import pandas as pd

# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE = Path(__file__).resolve().parents[1]

PASTA_PROCESSADA = BASE / "data" / "processed"

ARQUIVO_CSV = PASTA_PROCESSADA / "gaitdb.csv"
ARQUIVO_PARQUET = PASTA_PROCESSADA / "gaitdb.parquet"


# ============================================================
# CARREGAR OS DADOS
# ============================================================

def carregar_dados():                                          #Lê o arquivo CSV produzido anteriormente

    dados = pd.read_csv(ARQUIVO_CSV)

    return dados


# ============================================================
# DEFINIR OS TIPOS
# ============================================================

def definir_tipos(dados):

    dados["participante_id"] = dados["participante_id"].astype("string")

    dados["grupo"] = dados["grupo"].astype("string")

    dados["idade"] = dados["idade"].astype("Int16")

    dados["tempo_(s)"] = dados["tempo_(s)"].astype("Float64")

    dados["intervalo_passada_(s)"] = (dados["intervalo_passada_(s)"].astype("Float64")
    )

    return dados


# ============================================================
# SALVAR EM PARQUET
# ============================================================

def salvar_parquet(dados):

    dados.to_parquet(
        ARQUIVO_PARQUET,
        index=False,
        engine="pyarrow",
        compression="zstd"
    )

    print("Arquivo Parquet criado com sucesso.")
    print(f"Local: {ARQUIVO_PARQUET}")


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    dados = carregar_dados()

    dados = definir_tipos(dados)

    salvar_parquet(dados)
