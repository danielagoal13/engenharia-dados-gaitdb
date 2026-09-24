from pathlib import Path

import pandas as pd

# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE = Path(__file__).resolve().parents[1]

PASTA_RAW = BASE / "data" / "raw" / "gaitdb"
PASTA_PROCESSADA = BASE / "data" / "processed"

ARQUIVO_SAIDA = PASTA_PROCESSADA / "gaitdb.csv"

# ============================================================
# IDENTIFICAR PARTICIPANTE (PRATA)
# ============================================================

def obter_dados_participante(nome_arquivo):                   #Descobre o participante, grupo e idade usando o nome do arquivo.

    nome = nome_arquivo.replace("-si.txt", "")

    # Participantes com Parkinson
    if nome.startswith("pd"):
        participante = nome
        grupo = "parkinson"
        idade = pd.NA

    # Idosos saudáveis
    elif nome.startswith("o"):
        participante, idade = nome.split("-")
        grupo = "idoso"
        idade = int(idade)

    # Jovens saudáveis
    elif nome.startswith("y"):
        participante, idade = nome.split("-")
        grupo = "jovem"
        idade = int(idade)

    else:
        raise ValueError(
            f"Nome de arquivo não reconhecido: {nome_arquivo}"
        )

    return participante, grupo, idade


# ============================================================
# LER UM ARQUIVO
# ============================================================

def ler_arquivo(caminho):

    participante, grupo, idade = obter_dados_participante(caminho.name)

    dados = pd.read_csv(
        caminho,
        sep=r"\s+",
        names=["tempo_(s)", "intervalo_passada_(s)"]
    )

    dados.insert(0, "idade", idade)
    dados.insert(0, "grupo", grupo)
    dados.insert(0, "participante_id", participante)

    return dados


# ============================================================
# JUNTAR TODOS OS PARTICIPANTES
# ============================================================

def preparar_dataset():

    arquivos = sorted(PASTA_RAW.rglob("*-si.txt"))

    print(f"Arquivos encontrados: {len(arquivos)}")

    tabelas = []

    for arquivo in arquivos:

        print(f"Lendo: {arquivo.name}")

        dados_participante = ler_arquivo(arquivo)

        tabelas.append(dados_participante)

    dados = pd.concat(
        tabelas,
        ignore_index=True
    )

    return dados


# ============================================================
# SALVAR TABELA EM CSV
# ============================================================

def salvar_dataset(dados):

    PASTA_PROCESSADA.mkdir(
        parents=True,
        exist_ok=True
    )

    dados.to_csv(
        ARQUIVO_SAIDA,
        index=False
    )

    print()
    print(f"Arquivo salvo em:")
    print(ARQUIVO_SAIDA)

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    dados = preparar_dataset()

    salvar_dataset(dados)

    print()
    print("Dataset preparado com sucesso.")

    print()
    print("Dimensão da tabela:")
    print(dados.shape)

    print()
    print("Primeiras linhas:")
    print(dados.head())

    print()
    print("Participantes por grupo:")
    print(
        dados.groupby("grupo")["participante_id"]
        .nunique()
    )