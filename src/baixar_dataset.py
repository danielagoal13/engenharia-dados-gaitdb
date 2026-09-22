from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE = Path(__file__).resolve().parents[1]                     #Onde está a raiz do projeto

PASTA_RAW = BASE / "data" / "raw"

ARQUIVO_ZIP = PASTA_RAW / "gaitdb_1.0.0.zip"

PASTA_DATASET = PASTA_RAW / "gaitdb"


# ============================================================
# ENDEREÇO DO DATASET
# ============================================================

URL_DATASET = "https://physionet.org/content/gaitdb/get-zip/1.0.0/"


# ============================================================
# DOWNLOAD
# ============================================================

def baixar_dataset():

    PASTA_RAW.mkdir(parents=True, exist_ok=True)

    if ARQUIVO_ZIP.exists():
        print("O arquivo ZIP já foi baixado.")
        return

    print("Baixando o dataset...")

    urlretrieve(URL_DATASET, ARQUIVO_ZIP)

    print("Download concluído.")


# ============================================================
# EXTRAÇÃO
# ============================================================

def extrair_dataset():

    arquivos_existentes = list(PASTA_DATASET.rglob("*-si.txt"))  #Procura arquivos semelhantes terminados em -si.txt

    if arquivos_existentes:
        print("O dataset já foi extraído.")
        return

    PASTA_DATASET.mkdir(parents=True, exist_ok=True)

    print("Extraindo arquivos...")

    with ZipFile(ARQUIVO_ZIP, "r") as arquivo:
        arquivo.extractall(PASTA_DATASET)

    print("Extração concluída.")


# ============================================================
# VERIFICAÇÃO
# ============================================================

def verificar_dataset():

    arquivos = list(PASTA_DATASET.rglob("*-si.txt"))

    print(f"Arquivos de participantes encontrados: {len(arquivos)}")

    if len(arquivos) != 15:
        raise RuntimeError(
            "Era esperado encontrar 15 arquivos de participantes."
        )

    print("Dataset verificado com sucesso.")


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    baixar_dataset()
    extrair_dataset()
    verificar_dataset()