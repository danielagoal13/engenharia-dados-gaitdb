# Relatório de Qualidade dos Dados

## Dataset

**Gait in Aging and Disease Database — PhysioNet**

A avaliação de qualidade foi realizada sobre a camada Gold do projeto, composta pela tabela fato `fato_passada` e pelas dimensões `dim_participante` e `dim_protocolo`.

Foram implementados testes executáveis em DuckDB para verificar unicidade, valores nulos, domínio, integridade referencial e completude.

## Resultados

| Verificação | Tipo | Violações | Resultado |
|---|---|---:|---|
| `participante_key` única | Unicidade | 0 | Passou |
| `intervalo_passada_(s)` não nulo | Nulo | 0 | Passou |
| Grupo dentro dos valores esperados | Domínio | 0 | Passou |
| Intervalo de passada maior que zero | Domínio | 0 | Passou |
| Participante da fato existente na dimensão | Chave estrangeira | 0 | Passou |
| Protocolo da fato existente na dimensão | Chave estrangeira | 0 | Passou |
| Idade coerente com a documentação | Completude | 0 | Passou |

## Problemas, correções e decisões

### 1. Idade ausente no grupo Parkinson

**Problema:**  
Os arquivos dos participantes com Parkinson não fornecem a idade individual associada a cada participante.

**Correção:**  
A idade foi representada como valor nulo verdadeiro (`NULL`/`NA`).


### 2. Tipagem dos dados

**Problema:**  
Os arquivos originais são arquivos de texto e não possuem um schema analítico explícito.

**Correção:**  
Na camada Silver, as variáveis foram convertidas para tipos definidos: identificadores e grupos como texto, idade como inteiro anulável e variáveis temporais como valores numéricos.

**Decisão:**  
Os dados brutos foram mantidos separadamente na camada Bronze para permitir auditoria e reprocessamento.

### 3. Integridade do esquema estrela

**Problema:**  
Chaves duplicadas em dimensões ou chaves estrangeiras sem correspondência poderiam alterar o número de registros após operações de JOIN.

**Correção:**  
Foram implementados testes de unicidade e integridade referencial entre `fato_passada`, `dim_participante` e `dim_protocolo`.

**Decisão:**  
A camada Gold somente utiliza dimensões com chaves únicas e relacionamentos verificáveis.

### 4. Valores do intervalo de passada

**Problema:**  
Valores ausentes ou menores ou iguais a zero comprometeriam estatísticas e futuras entradas de modelos.

**Correção:**  
Foram executados testes para verificar ausência e domínio da variável de intervalo de passada.
