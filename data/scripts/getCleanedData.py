import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None)
results = client.get("kgyi-qc7j", limit=20000)

df = pd.DataFrame.from_records(results)

# Show column names to confirm
print(df.columns)

# Keep only relevant columns
df_cleaned = df[['a_o', 'departamento', 'valor_miles_de_millones_de']].copy()


# Rename for clarity
df_cleaned.columns = ['year', 'department', 'value']

# Convert types
df_cleaned['year'] = pd.to_numeric(df_cleaned['year'], errors='coerce')
df_cleaned['value'] = pd.to_numeric(df_cleaned['value'], errors='coerce')

# Drop rows with NaNs
df_cleaned = df_cleaned.dropna()

# Save for MRJob
df_cleaned.to_csv("data\data\cleaned_gdp_data.csv", index=False)
