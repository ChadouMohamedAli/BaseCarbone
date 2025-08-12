import pandas as pd
import sqlite3

# === SETTINGS ===
EXCEL_FILE = 'your_file.xlsx'
SHEET_NAME = None  # set to sheet name or None for first
DB_FILE = 'output.db'
MAX_UNIQUE_FOR_DIM = 100

# === LOAD DATA ===
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# === INIT DB ===
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# === CLASSIFY COLUMNS ===
dimension_cols = []
main_cols = []

for col in df.columns:
    unique_vals = df[col].dropna().unique()
    if len(unique_vals) <= MAX_UNIQUE_FOR_DIM and df[col].dtype != 'float64':
        dimension_cols.append(col)
    else:
        main_cols.append(col)

print(f"Dimension columns: {dimension_cols}")
print(f"Main table columns: {main_cols}")

# === CREATE & INSERT DIMENSION TABLES ===
for col in dimension_cols:
    dim_table = f"dim_{col}"
    unique_vals = df[col].dropna().unique()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {dim_table} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value TEXT UNIQUE
    )""")

    for val in unique_vals:
        cursor.execute(f"INSERT OR IGNORE INTO {dim_table} (value) VALUES (?)", (str(val),))

# === CREATE MAIN TABLE ===
main_table = "main_data"
main_schema = ",\n  ".join([f"{col} TEXT" for col in main_cols])
cursor.execute(
    f"CREATE TABLE IF NOT EXISTS {main_table} (\n  id INTEGER PRIMARY KEY AUTOINCREMENT,\n  {main_schema}\n)")

# === INSERT MAIN DATA ===
main_df = df[main_cols].fillna("")

for _, row in main_df.iterrows():
    values = tuple(str(val) for val in row)
    placeholders = ', '.join('?' for _ in values)
    cursor.execute(f"INSERT INTO {main_table} ({', '.join(main_cols)}) VALUES ({placeholders})", values)

# === DONE ===
conn.commit()
conn.close()
print(f"\n✅ Done. DB saved to: {DB_FILE}")
