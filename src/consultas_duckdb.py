from pathlib import Path

import duckdb

# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE = Path(__file__).resolve().parents[1]

ARQUIVO_PARQUET = (
    BASE / "data" / "processed" / "gaitdb.parquet"
)

# Converte o caminho para um formato adequado ao SQL
caminho_parquet = ARQUIVO_PARQUET.as_posix()


# ============================================================
# CONEXÃO COM DUCKDB
# ============================================================

conexao = duckdb.connect()


# ============================================================
# CONSULTA 1 - QUANTIDADE TOTAL DE REGISTROS
# ============================================================

consulta_1 = f"""
SELECT
    COUNT(*) AS total_registros
FROM read_parquet('{caminho_parquet}');
"""

resultado_1 = conexao.execute(consulta_1).df()

print("CONSULTA 1 - TOTAL DE REGISTROS")
print(resultado_1)


# ============================================================
# CONSULTA 2 - PARTICIPANTES POR GRUPO
# ============================================================

consulta_2 = f"""
SELECT
    grupo,
    COUNT(DISTINCT participante_id) AS participantes
FROM read_parquet('{caminho_parquet}')
GROUP BY grupo
ORDER BY grupo;
"""

resultado_2 = conexao.execute(consulta_2).df()

print()
print("CONSULTA 2 - PARTICIPANTES POR GRUPO")
print(resultado_2)


# ============================================================
# CONSULTA 3 - ESTATÍSTICAS POR GRUPO
# ============================================================

consulta_3 = f"""
SELECT
    grupo,
    COUNT(*) AS registros,
    ROUND(AVG("intervalo_passada_(s)"), 4) AS media_intervalo_(s),
    ROUND(STDDEV_SAMP("intervalo_passada_(s)"), 4) AS desvio_padrao_(s)
FROM read_parquet('{caminho_parquet}')
GROUP BY grupo
ORDER BY grupo;
"""

resultado_3 = conexao.execute(consulta_3).df()

print()
print("CONSULTA 3 - ESTATÍSTICAS POR GRUPO")
print(resultado_3)


# ============================================================
# ENCERRAR CONEXÃO
# ============================================================

conexao.close()