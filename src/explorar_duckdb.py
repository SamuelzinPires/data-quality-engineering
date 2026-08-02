import pandas as pd 
import duckdb

con = duckdb.connect("data/quality.duckdb")
df = pd.read_excel("data/Online Retail.xlsx") 
con.execute("CREATE OR REPLACE TABLE online_retail AS SELECT * FROM df")

print(df.shape)  # confirmando volume antes de seguir — se vier 0 linhas, o caminho do arquivo está errado
print(df.head()) 

resultado = con.execute("SELECT COUNT(*) AS total_linhas FROM online_retail").fetchall()
print(resultado)