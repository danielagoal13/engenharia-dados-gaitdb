# GaitDB Project

Projeto desenvolvido para a disciplina **Engenharia de Dados e IA Multimodal em Engenharia Biomédica — PPGEB/UFU**.

O objetivo desta etapa é construir um fluxo reproduzível para download, organização, preparação e análise exploratória do **Gait in Aging and Disease Database**, disponibilizado pelo PhysioNet.

## Dataset

- **Nome:** Gait in Aging and Disease Database
- **Versão:** 1.0.0
- **Fonte:** PhysioNet
- **DOI:** 10.13026/C2C889
- **URL:** https://physionet.org/content/gaitdb/1.0.0/
- **Licença:** Open Data Commons Attribution License v1.0

O conjunto contém séries temporais de intervalos de passada de **15 participantes**:

- 5 jovens saudáveis;
- 5 idosos saudáveis;
- 5 indivíduos com doença de Parkinson.

Neste projeto, os 15 arquivos individuais geraram uma tabela analítica com **9.144 registros** e **5 variáveis**.

---

## Pergunta de pesquisa

> Existem diferenças na duração e na variabilidade dos intervalos de passada entre indivíduos jovens saudáveis, idosos saudáveis e indivíduos com doença de Parkinson?

O projeto tem finalidade **educacional e exploratória**. O dataset é pequeno e não deve ser utilizado para afirmar desempenho diagnóstico ou generalização clínica.

---

## Estrutura do projeto

```text
gaitdb_project/
│
├── data/
│   ├── raw/
│   │   └── gaitdb/
│   └── processed/
│       └── gaitdb.csv
│
├── docs/
│   └── ficha_tecnica.md
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── resultados/
│
├── src/
│   ├── baixar_dataset.py
│   └── preparar_dados.py
│
├── requirements.txt
└── README.md
```

### Significado das principais pastas

- `data/raw/`: dados originais baixados do PhysioNet. Devem permanecer sem alterações.
- `data/processed/`: dados derivados e organizados para análise.
- `src/`: scripts responsáveis pela ingestão e preparação dos dados.
- `notebooks/`: análise exploratória.
- `docs/`: documentação técnica do dataset.
- `resultados/`: espaço reservado para resultados e arquivos derivados produzidos nas etapas seguintes.

---

## Requisitos

Este projeto foi desenvolvido localmente no **VS Code**, utilizando Python em um ambiente virtual `.venv`.

Ambiente utilizado durante o desenvolvimento:

```text
Python 3.14.0
```

As versões das bibliotecas instaladas estão fixadas no arquivo `requirements.txt`.

---

## Como reproduzir o projeto do zero

Os comandos abaixo consideram **Windows + VS Code**.

### 1. Abrir a pasta do projeto

No VS Code:

```text
File → Open Folder → gaitdb_project
```

Abra um terminal em:

```text
Terminal → New Terminal
```

### 2. Criar o ambiente virtual

```bash
py -m venv .venv
```

### 3. Ativar o ambiente virtual

```bash
.venv\Scripts\activate
```

O terminal deverá passar a mostrar algo parecido com:

```text
(.venv) C:\...\gaitdb_project>
```

### 4. Selecionar o interpretador no VS Code

Pressione `Ctrl + Shift + P`, selecione `Python: Select Interpreter` e escolha:

```text
.venv\Scripts\python.exe
```

### 5. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Baixar o dataset

```bash
python src\baixar_dataset.py
```

O script cria as pastas necessárias, baixa o dataset, extrai os arquivos e verifica se os 15 participantes esperados foram encontrados.

Saída esperada:

```text
Arquivos de participantes encontrados: 15
Dataset verificado com sucesso.
```

### 7. Preparar a tabela analítica

```bash
python src\preparar_dados.py
```

O script lê os arquivos individuais, identifica participante e grupo e cria uma única tabela.

Saída esperada:

```text
Dimensão da tabela:
(9144, 5)
```

Arquivo gerado:

```text
data/processed/gaitdb.csv
```

Colunas:

| Coluna | Significado |
|---|---|
| `participante_id` | Identificador do participante |
| `grupo` | Jovem, idoso ou Parkinson |
| `idade` | Idade individual quando disponível |
| `tempo_s` | Tempo em segundos |
| `intervalo_passada_s` | Intervalo de passada em segundos |

Para os participantes com Parkinson, a idade individual é mantida como valor ausente porque ela não pode ser determinada a partir dos arquivos publicados.

---

## Análise exploratória — EDA

O notebook está em:

```text
notebooks/01_eda.ipynb
```

Para executá-lo:

1. abra o arquivo no VS Code;
2. selecione o kernel correspondente ao `.venv`;
3. execute as células em ordem ou utilize `Run All`.

O notebook inclui inspeção do tamanho e tipos das variáveis, dados ausentes, participantes por grupo, número de passadas por participante, estatísticas descritivas e gráficos de distribuição e séries temporais.

---

## Resultado descritivo inicial

| Grupo | Registros | Média (s) | Desvio padrão (s) | Mediana (s) |
|---|---:|---:|---:|---:|
| Idoso | 4.110 | 1,021679 | 0,083542 | 1,0200 |
| Jovem | 3.813 | 1,101055 | 0,064379 | 1,1030 |
| Parkinson | 1.221 | 1,138236 | 0,162533 | 1,1133 |

Os resultados são apenas **descritivos e exploratórios**.

Os registros de passada não devem ser tratados como participantes independentes, pois cada pessoa contribui com várias medições.

---

## Reprodutibilidade

O projeto usa caminhos relativos à raiz do repositório, evitando caminhos absolutos específicos do computador do autor.

Outra pessoa deve conseguir reproduzir o fluxo ao:

1. obter esta pasta;
2. criar o `.venv`;
3. instalar `requirements.txt`;
4. executar `baixar_dataset.py`;
5. executar `preparar_dados.py`;
6. abrir e executar `01_eda.ipynb`.

Os arquivos originais são preservados separadamente dos dados derivados.

---

## Cuidados metodológicos

O conjunto possui apenas **15 participantes**.

Além disso, o protocolo de coleta não foi idêntico entre os grupos:

- participantes saudáveis caminharam aproximadamente 15 minutos;
- participantes com Parkinson caminharam aproximadamente 6 minutos.

Por isso, a quantidade de passadas é muito menor no grupo Parkinson.

---

## Esquema estrela

Para a camada analítica foi adotado um esquema estrela simples.

### Grão

Cada linha da tabela fato representa **um intervalo de passada registrado para um participante em determinado instante da caminhada**.

### Tabela fato

#### `fato_passada`

Contém as medidas obtidas ao longo da caminhada.

| Campo | Descrição |
|---|---|
| `participante_id` | Identificador do participante e ligação com a dimensão participante |
| `tempo_s` | Tempo decorrido do registro, em segundos |
| `intervalo_passada_s` | Intervalo entre passadas, em segundos |

A principal medida quantitativa é `intervalo_passada_s`, utilizada para calcular estatísticas como média, mediana e desvio padrão.

### Dimensão

#### `dim_participante`

Contém as características descritivas do participante.

| Campo | Descrição |
|---|---|
| `participante_id` | Identificador único do participante |
| `grupo` | Jovem, idoso ou Parkinson |
| `idade` | Idade quando disponível |

A idade dos participantes do grupo Parkinson permanece nula porque a idade individual não é informada nos arquivos utilizados.

### Representação

```text
                  dim_participante
              ┌─────────────────────┐
              │ participante_id     │
              │ grupo               │
              │ idade               │
              └──────────┬──────────┘
                         │
                         ▼
                  fato_passada
              ┌─────────────────────┐
              │ participante_id     │
              │ tempo_s             │
              │ intervalo_passada_s │
              └─────────────────────┘


# Arquitetura dos Dados

O projeto utiliza uma organização em camadas para manter a rastreabilidade das transformações realizadas sobre o dataset.

## Camada Bronze

A camada Bronze contém os dados provenientes dos arquivos originais do dataset, preservando os valores da fonte e registrando o arquivo de origem de cada observação.

Arquivo principal:

`data/bronze/gaitdb_bronze.parquet`

## Camada Silver

Na camada Silver são realizadas as transformações necessárias para utilização analítica dos dados, incluindo:

- identificação do participante;
- classificação do grupo;
- definição da idade quando disponível;
- conversão dos valores para tipos numéricos adequados;
- padronização da estrutura dos dados.

Arquivo principal:

`data/silver/gaitdb_silver.parquet`

## Camada Gold

A camada Gold contém o modelo analítico utilizado no projeto.

Foram criadas uma tabela fato e duas dimensões:

- `fato_passada.parquet`
- `dim_participante.parquet`
- `dim_protocolo.parquet`

A utilização das camadas permite separar os dados de origem dos dados tratados e das estruturas destinadas à análise.



# Modelo Analítico

Foi utilizado um modelo dimensional em esquema estrela.

## Tabela fato

### fato_passada

A tabela `fato_passada` contém as observações dos intervalos de passada.

**Granularidade:**

Cada linha da tabela `fato_passada` representa um intervalo de passada registrado para um participante em determinado instante da caminhada.

Principais atributos:

- `passada_key`
- `participante_key`
- `protocolo_key`
- `tempo_(s)`
- `intervalo_passada_(s)`

## Dimensão participante

### dim_participante

Contém as informações referentes aos participantes:

- `participante_key`
- `participante_id`
- `grupo`
- `idade`

## Dimensão protocolo

### dim_protocolo

Representa as características do protocolo de coleta:

- `protocolo_key`
- `protocolo`
- `duracao_prevista_min`
- `tipo_percurso`

As chaves das dimensões são utilizadas para relacionar as informações de contexto à tabela fato.



# Testes de Qualidade

Foram implementados testes automatizados utilizando DuckDB para verificar a qualidade e a integridade da camada Gold.

Os testes estão disponíveis em:

`src/testes_qualidade.ipynb`

Foram avaliadas as seguintes regras:

| Teste | Tipo |
|---|---|
| Unicidade de `participante_key` | Unicidade |
| Ausência de valores nulos em `intervalo_passada_(s)` | Nulo |
| Valores válidos da variável `grupo` | Domínio |
| Intervalos de passada maiores que zero | Domínio |
| Existência do participante na dimensão | Chave estrangeira |
| Existência do protocolo na dimensão | Chave estrangeira |
| Coerência da idade com a documentação | Completude |

Na execução atual, todos os testes apresentaram zero violações.

O resultado consolidado dos testes é armazenado em:

`resultados/testes_qualidade.csv`

O relatório contendo os problemas avaliados, correções e decisões adotadas está disponível em:

`docs/relatorio_qualidade.md`


# Preparação para Inteligência Artificial

Embora a base processada possua 9.144 registros de passadas, esses registros pertencem a apenas 15 participantes.

Por esse motivo, a unidade de análise considerada para uma futura aplicação de Machine Learning é o **participante**, e não cada intervalo de passada individual.

As estatísticas dos intervalos de passada foram previamente agregadas por participante durante a análise exploratória.

## Separação entre treino e teste

A separação entre treino e teste foi realizada no nível do participante.

Todas as observações provenientes de uma mesma pessoa devem permanecer na mesma partição, evitando que registros do mesmo participante estejam simultaneamente nos conjuntos de treino e teste.

Como demonstração metodológica:

- 12 participantes foram destinados ao treino;
- 3 participantes foram destinados ao teste;
- foi selecionado 1 participante de cada grupo para o conjunto de teste.

Foi realizada uma verificação explícita para confirmar que nenhum participante aparece simultaneamente nas duas partições.

A divisão utilizada está registrada em:

`resultados/particao_participantes.csv`

Devido ao pequeno número de participantes, essa separação possui finalidade metodológica e não deve ser interpretada como suficiente para avaliar o desempenho clínico de um modelo de Machine Learning.