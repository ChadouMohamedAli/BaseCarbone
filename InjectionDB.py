import pandas as pd
import mysql.connector
from datetime import datetime
import numpy as np

# === SETTINGS ===
EXCEL_FILE = 'Db/Base_Carbone_classified_V2025-07-30_11-20-00.xlsx'  # <-- Replace with your actual file
CHUNK_SIZE = 500
TABLE_NAME = 'emission_data'

# === STEP 1: LOAD DATA ===
df = pd.read_excel(EXCEL_FILE)
df = df.fillna('')
df = df.loc[:, ~df.columns.isna()]                      # Drop NaN headers
df = df.loc[:, df.columns.str.strip() != ""]
df = df.loc[:, df.columns.astype(str).str.lower() != "nan"]       # remove literal "nan"
df.columns = [col.strip().replace(" ", "_").replace(".", "_").replace("-", "_") for col in df.columns]
#print(df.columns)
df = df.where(pd.notnull(df), None) # Replace NaN with None
df = df.applymap(lambda x: None if str(x).strip().lower() == "nan" else x)
#print(df.columns)

# Clean 'Incertitude' column
def clean_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

float_cols = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
print(float_cols)
for col in float_cols:
    df[col] = df[col].apply(clean_float)

# === STEP 2: CONNECT TO MYSQL ===
db = mysql.connector.connect(
    host="192.168.2.3",
    user="divatex",
    password="Divatex@NafNaf2023!!",
    database="gg"
)
cursor = db.cursor()

# === STEP 3: CREATE TABLE IF NOT EXISTS ===
columns_sql = []
for col in df.columns:
    dtype = "TEXT"
    if pd.api.types.is_numeric_dtype(df[col]):
        dtype = "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        dtype = "DATETIME"
    columns_sql.append(f"`{col}` {dtype}")

create_query = f"""
CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {', '.join(columns_sql)}
);
"""
#print(create_query)
cursor.execute(create_query)

# === STEP 4: PREPARE INSERT QUERY ===
placeholders = ', '.join(['%s'] * len(df.columns))
insert_query = f"""
INSERT INTO `{TABLE_NAME}` ({', '.join([f'`{col}`' for col in df.columns])})
VALUES ({placeholders});
"""
#print(insert_query)
# === STEP 5: CHUNKED INSERTION ===
print(f"⏳ Inserting {len(df)} rows in chunks of {CHUNK_SIZE}...")

for i in range(0, len(df), CHUNK_SIZE):
    chunk = df.iloc[i:i+CHUNK_SIZE]
    cursor.executemany(insert_query, [tuple(row) for row in chunk.itertuples(index=False)])
    db.commit()
    print(f"✅ Inserted rows {i} to {i+len(chunk)-1}")

# === CLEAN UP ===
cursor.close()
db.close()
print(f"\n✅ All done. {len(df)} rows inserted into `{TABLE_NAME}`.")
