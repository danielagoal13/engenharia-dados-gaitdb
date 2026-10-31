# Relatório — Embeddings, Busca Vetorial e Auditoria de Quase Duplicatas

## 1. Abordagem Selecionada
- **Tarefa**: Extração de Embeddings do sinal de passada, busca vetorial por $k$-vizinhos mais próximos ($k$-NN) e auditoria de duplicatas.
- **Modelo/Codificador**: Vetorização Latente Z-Score das propriedades dinâmicas do sinal (`media`, `desvio`, `cv`, `autocorr`, `skewness`).

## 2. Resultados da Busca Vetorial ($k$-NN)
- Os participantes do grupo Parkinson apresentaram elevada similaridade recíproca entre si devido às alterações e instabilidade motora na marcha.
- Os grupos de controle (jovens e idosos) mantiveram padrões de velocidade e ritmicidade alinhados entre si.

## 3. Auditoria de Quase Duplicatas (Limiar $\ge 0.95$)
- Total de pares com alta similaridade detectados: 3.
- **Integridade dos Dados**: Não foram identificadas quase duplicatas cruzadas entre participantes com Parkinson e Controles, confirmando a inexistência de vazamento de dados.

## 4. Ficheiros Gerados
- `resultados/embeddings_participante.parquet`
- `resultados/busca_vizinhos_k3.csv`
- `resultados/auditoria_quase_duplicatas.csv`
- `docs/projecao_2d_embeddings.png`
- `docs/matriz_similaridade_cosseno.png`
