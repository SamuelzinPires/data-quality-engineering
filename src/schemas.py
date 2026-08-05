import pandera.pandas as pa
import duckdb 

con = duckdb.connect("data/quality.duckdb")
df = con.execute("SELECT * FROM online_retail").df()

#Analisando a qualidade dos dados com Pandera
schema = pa.DataFrameSchema({
    "CustomerID": pa.Column(pa.Float64, nullable=False), 
    "Quantity": pa.Column(pa.Int64, nullable=False, checks=pa.Check.greater_than_or_equal_to(0)), 
    "UnitPrice": pa.Column(pa.Float64, nullable=False, checks=pa.Check.greater_than(0)), 
    "InvoiceNo": pa.Column(pa.String, nullable=False, checks=pa.Check.str_matches(r'^[0-9]+$')),
    "StockCode": pa.Column(pa.String, nullable=False, checks=pa.Check.str_matches(r'^[0-9]{5}[A-Z]?$'))
}, 
    unique=["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]  #Verifica duplicidade considerando todas as colunas
)
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as erro:   
    print(erro.failure_cases)