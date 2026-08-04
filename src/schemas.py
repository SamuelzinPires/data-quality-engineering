import pandera.pandas as pa
import duckdb 

con = duckdb.connect("data/quality.duckdb")
df = con.execute("SELECT * FROM online_retail").df()

schema = pa.DataFrameSchema({
    "CustomerID": pa.Column(pa.Float64, nullable=False),
    "Quantity": pa.Column(pa.Int64, nullable=False, checks=pa.Check.greater_than_or_equal_to(0)),
})

try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as erro:   
    print(erro.failure_cases)