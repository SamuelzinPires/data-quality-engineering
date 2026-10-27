# Data Quality Engineering — Online Retail

Pipeline que ingere um dataset real de transações de e-commerce, aplica um conjunto explícito de regras de qualidade de dados e gera um relatório auditável de todos os problemas encontrados — nulos, tipos, formato e duplicatas.

O foco do projeto é **detectar e reportar** problemas de qualidade, não corrigir os dados automaticamente. A decisão de como tratar cada violação (imputar, remover, investigar) fica a critério de quem consome o relatório — o pipeline só garante que nada passe despercebido.

##  Stack

- **Python 3.14**
- **DuckDB** — banco analítico local, usado para profiling exploratório via SQL
- **Pandas** — carga e manipulação dos dados
- **Pandera** — definição declarativa de schema e regras de qualidade sobre o DataFrame inteiro

##  Dataset

[Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) (UCI Machine Learning Repository) — 541.909 transações de uma varejista online do Reino Unido, entre dezembro/2010 e dezembro/2011.

Escolhido deliberadamente por ter problemas de qualidade **orgânicos** (não simulados): ~25% de `CustomerID` nulo, `Quantity` e `UnitPrice` negativos, `InvoiceNo` com prefixo de cancelamento, `StockCode` fora do padrão de produto e milhares de linhas duplicadas.

> O arquivo bruto (`.xlsx`, ~23MB) não é versionado neste repositório (ver [Como rodar](#-como-rodar-localmente)) — baixe direto da fonte acima e salve em `data/Online Retail.xlsx`.

## Como o pipeline funciona

```
Online Retail.xlsx
        │  pandas.read_excel
        ▼
data/quality.duckdb  (banco local persistente)
        │  profiling exploratório (SUMMARIZE, duplicatas, formatos)
        ▼
schema Pandera (6 regras de qualidade)
        │  schema.validate(df, lazy=True)
        ▼
relatório de violações
   ├── data/relatorio_qualidade.csv        (detalhado, linha a linha)
   └── relatorios/resumo_qualidade.csv     (agregado, por coluna + regra)
```

##  Regras de qualidade implementadas

| Dimensão | Coluna | Regra | Violações encontradas |
|---|---|---|---:|
| Completude | `CustomerID` | não pode ser nulo | 135.080 |
| Range | `Quantity` | deve ser ≥ 0 | 10.624 |
| Range | `UnitPrice` | deve ser > 0 | 2.517 |
| Formato | `InvoiceNo` | apenas dígitos (sem prefixo de cancelamento) | 9.291 |
| Formato | `StockCode` | 5 dígitos + letra maiúscula opcional | 5.265 |
| Unicidade | linha inteira (8 colunas) | não pode haver linha duplicada | 5.268 cópias extras |

Sobre um total de 541.909 linhas × 8 colunas.

> **Sobre as duplicatas:** os dois números medem coisas diferentes. O profiling no DuckDB (`COUNT(*) - COUNT(DISTINCT ...)`) conta **5.268 cópias extras**, que são as linhas que sobrariam para remover. Já o Pandera marca **todas** as linhas de cada grupo repetido, inclusive a primeira ocorrência, e por isso o resumo mostra **10.147 linhas** na regra de unicidade.

##  Estrutura do projeto

```
data-quality-engineering/
├── data/                        # dataset bruto + banco DuckDB local (fora do Git)
├── relatorios/
│   └── resumo_qualidade.csv     # resumo das violações por regra
├── src/
│   ├── explorar_duckdb.py       # carga inicial + profiling exploratório (DuckDB)
│   └── schemas.py               # regras de qualidade (Pandera) + geração do relatório
├── requirements.txt
└── README.md
```

##  Como rodar localmente

```bash
git clone https://github.com/SamuelzinPires/data-quality-engineering.git
cd data-quality-engineering

python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows PowerShell

pip install -r requirements.txt
```

Baixe o dataset em [archive.ics.uci.edu/dataset/352/online+retail](https://archive.ics.uci.edu/dataset/352/online+retail) e salve como `data/Online Retail.xlsx`.

```bash
python src/explorar_duckdb.py    # cria o banco local e carrega os dados
python src/schemas.py            # roda a validação e gera os relatórios
```

## Próximos passos

- Validação de registro único com **Pydantic** (complementar ao Pandera, para o caso de validar uma transação chegando individualmente).
- Investigar a pequena divergência de contagem de duplicatas em `CustomerID` no resumo agregado.
