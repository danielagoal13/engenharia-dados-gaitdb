from pathlib import Path

import duckdb
import pandas as pd


# ============================================================
# CAMINHOS
# ============================================================

BASE = Path(__file__).resolve().parents[1]

PASTA_RAW = BASE / "data" / "raw"
PASTA_BRONZE = BASE / "data" / "bronze"
PASTA_SILVER = BASE / "data" / "silver"
PASTA_GOLD = BASE / "data" / "gold"

PASTA_BRONZE.mkdir(parents=True, exist_ok=True)
PASTA_SILVER.mkdir(parents=True, exist_ok=True)
PASTA_GOLD.mkdir(parents=True, exist_ok=True)


ARQUIVO_BRONZE = PASTA_BRONZE / "gaitdb_bronze.parquet"
ARQUIVO_SILVER = PASTA_SILVER / "gaitdb_silver.parquet"


# ============================================================
# BRONZE
# ============================================================

def criar_bronze():                                            #Junta os arquivos originais sem alterar o significado dos valores

    arquivos = sorted(
        PASTA_RAW.rglob("*-si.txt")
    )

    tabelas = []

    for arquivo in arquivos:

        dados = pd.read_csv(
            arquivo,
            sep=r"\s+",
            names=[
                "tempo_raw",
                "intervalo_passada_raw"
            ],
            dtype="string"
        )

        dados["arquivo_origem"] = arquivo.name

        tabelas.append(dados)

    bronze = pd.concat(
        tabelas,
        ignore_index=True
    )

    bronze.to_parquet(
        ARQUIVO_BRONZE,
        index=False,
        compression="zstd"
    )

    print("BRONZE criado.")
    print(f"Linhas: {len(bronze)}")

    return bronze


# ============================================================
# IDENTIFICAR PARTICIPANTE
# ============================================================

def extrair_metadados(nome_arquivo):

    nome = nome_arquivo.replace("-si.txt", "")

    if nome.startswith("pd"):

        participante_id = nome
        grupo = "parkinson"
        idade = pd.NA

    elif nome.startswith("o"):

        participante_id, idade = nome.split("-")
        grupo = "idoso"
        idade = int(idade)

    elif nome.startswith("y"):

        participante_id, idade = nome.split("-")
        grupo = "jovem"
        idade = int(idade)

    else:

        raise ValueError(
            f"Arquivo não reconhecido: {nome_arquivo}"
        )

    return participante_id, grupo, idade


# ============================================================
# SILVER (PRATA)
# ============================================================

def criar_silver(bronze):

    silver = bronze.copy()

    metadados = silver["arquivo_origem"].apply(
        extrair_metadados
    )

    silver["participante_id"] = metadados.apply(
        lambda x: x[0]
    )

    silver["grupo"] = metadados.apply(
        lambda x: x[1]
    )

    silver["idade"] = metadados.apply(
        lambda x: x[2]
    )

    # Tipagem explícita
    silver["participante_id"] = (
        silver["participante_id"]
        .astype("string")
    )

    silver["grupo"] = (
        silver["grupo"]
        .astype("string")
    )

    silver["idade"] = (
        silver["idade"]
        .astype("Int16")
    )

    silver["tempo_(s)"] = pd.to_numeric(
        silver["tempo_raw"],
        errors="coerce"
    ).astype("Float64")

    silver["intervalo_passada_(s)"] = pd.to_numeric(
        silver["intervalo_passada_raw"],
        errors="coerce"
    ).astype("Float64")

    # Mantemos somente as colunas analíticas
    silver = silver[
        [
            "participante_id",
            "grupo",
            "idade",
            "tempo_(s)",
            "intervalo_passada_(s)",
            "arquivo_origem"
        ]
    ]

    silver.to_parquet(
        ARQUIVO_SILVER,
        index=False,
        compression="zstd"
    )

    print()
    print("SILVER criado.")
    print(f"Linhas: {len(silver)}")

    return silver


# ============================================================
# DIMENSÃO PARTICIPANTE
# ============================================================

def criar_dim_participante(silver):

    dim_participante = (
        silver[
            [
                "participante_id",
                "grupo",
                "idade"
            ]
        ]
        .drop_duplicates()
        .sort_values("participante_id")
        .reset_index(drop=True)
    )

    dim_participante.insert(
        0,
        "participante_key",
        range(1, len(dim_participante) + 1)
    )

    return dim_participante


# ============================================================
# DIMENSÃO PROTOCOLO
# ============================================================

def criar_dim_protocolo():

    dim_protocolo = pd.DataFrame(
        {
            "protocolo_key": [1, 2],
            "protocolo": [
                "controle",
                "parkinson"
            ],
            "duracao_prevista_min": [
                15,
                6
            ],
            "tipo_percurso": [
                "trajetoria aproximadamente circular",
                "ida e volta em corredor"
            ]
        }
    )

    return dim_protocolo


# ============================================================
# TABELA FATO
# ============================================================

def criar_fato_passada(
    silver,
    dim_participante
):

    fato = silver.merge(
        dim_participante[
            [
                "participante_key",
                "participante_id"
            ]
        ],
        on="participante_id",
        how="left"
    )

    # Protocolo usado em cada grupo
    fato["protocolo_key"] = (
        fato["grupo"]
        .map(
            {
                "jovem": 1,
                "idoso": 1,
                "parkinson": 2
            }
        )
        .astype("Int8")
    )

    fato = fato[
        [
            "participante_key",
            "protocolo_key",
            "tempo_(s)",
            "intervalo_passada_(s)"
        ]
    ]

    fato.insert(
        0,
        "passada_key",
        range(1, len(fato) + 1)
    )

    return fato


# ============================================================
# SALVAR GOLD
# ============================================================

def salvar_gold(
    fato,
    dim_participante,
    dim_protocolo
):

    fato.to_parquet(
        PASTA_GOLD / "fato_passada.parquet",
        index=False,
        compression="zstd"
    )

    dim_participante.to_parquet(
        PASTA_GOLD / "dim_participante.parquet",
        index=False,
        compression="zstd"
    )

    dim_protocolo.to_parquet(
        PASTA_GOLD / "dim_protocolo.parquet",
        index=False,
        compression="zstd"
    )

    print()
    print("CAMADA GOLD criada.")

    print(
        f"Fato: {len(fato)} linhas"
    )

    print(
        f"Participantes: {len(dim_participante)}"
    )

    print(
        f"Protocolos: {len(dim_protocolo)}"
    )


# ============================================================
# EXIBIR TABELAS NO TERMINAL
# ============================================================

def exibir_tabela(nome, tabela, linhas=10):

    print()
    print("=" * 70)
    print(nome)
    print("=" * 70)

    print(f"Linhas: {tabela.shape[0]}")
    print(f"Colunas: {tabela.shape[1]}")

    print()

    if len(tabela) <= linhas:
        print(tabela.to_string(index=False))
    else:
        print(tabela.head(linhas).to_string(index=False))

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    # BRONZE
    bronze = criar_bronze()

    exibir_tabela(
        "CAMADA BRONZE",
        bronze
    )

    # SILVER
    silver = criar_silver(bronze)

    exibir_tabela(
        "CAMADA SILVER",
        silver
    )

    # GOLD
    dim_participante = criar_dim_participante(
        silver
    )

    dim_protocolo = criar_dim_protocolo()

    fato = criar_fato_passada(
        silver,
        dim_participante
    )


    exibir_tabela(
        "GOLD - DIMENSÃO PARTICIPANTE",
        dim_participante,
        linhas=20
    )

    exibir_tabela(
        "GOLD - DIMENSÃO PROTOCOLO",
        dim_protocolo,
        linhas=10
    )

    exibir_tabela(
        "GOLD - TABELA FATO PASSADA",
        fato
    )
