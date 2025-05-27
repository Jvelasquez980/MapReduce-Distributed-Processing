import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None)
results = client.get("kgyi-qc7j", limit=20000)

df = pd.DataFrame.from_records(results)

# Drop rows with NaNs
df_cleaned = df.dropna()

# Save for MRJob
df_cleaned.to_csv("data/data/gdp_data.csv", index=False)
