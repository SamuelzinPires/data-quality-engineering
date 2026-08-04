import pandas as pd 
import duckdb

con = duckdb.connect("data/quality.duckdb")
df = pd.read_excel("data/Online Retail.xlsx") 
con.execute("CREATE OR REPLACE TABLE online_retail AS SELECT * FROM df")

print(df.shape)  # confirmando volume antes de seguir — se vier 0 linhas, o caminho do arquivo está errado
print(df.head()) 

resultado = con.execute("SELECT COUNT(*) AS total_linhas FROM online_retail").fetchall()
print(resultado)

duplicatas = con.sql("""
    SELECT COUNT(*) AS total_linhas,
        COUNT(*) - COUNT(DISTINCT (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)) AS total_duplicatas
    FROM online_retail
""")
duplicatas.show()

stockcode_suspeitos = con.sql("""
    SELECT StockCode, COUNT(*) AS ocorrencias
    FROM online_retail
    WHERE NOT regexp_matches(StockCode, '^[0-9]+$')  -- Filtra StockCodes que não são apenas números
    GROUP BY StockCode
    ORDER BY ocorrencias DESC
""")