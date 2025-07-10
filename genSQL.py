import pandas as pd
import datetime

# === CONFIGURATION ===
input_file = "dataSource/Base_Carbone_V23.6-v3.xlsx"  # or .csv
output_sql_file = "insert_base_carbone.sql"
table_name = "Base_Carbone_V2025_07_09_12_12_22"  # Use _ instead of - and remove special chars

# === Load file ===
if input_file.endswith(".xlsx"):
    df = pd.read_excel(input_file)
else:
    df = pd.read_csv(input_file)

# === Clean column names for SQL (backtick-wrapped) ===
columns = [f"`{col.strip()}`" for col in df.columns]
columns_sql = ", ".join(columns)

# === Format values row-by-row ===
def format_value(val):
    if pd.isna(val):
        return "NULL"
    elif isinstance(val, (int, float)):
        return str(val)
    else:
        val = str(val).replace("'", "''")  # Escape single quotes for SQL
        return f"'{val}'"

# === Generate INSERT statements ===
with open(output_sql_file, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        values = ", ".join(format_value(v) for v in row)
        insert = f"INSERT INTO `{table_name}` ({columns_sql}) VALUES ({values});\n"
        f.write(insert)

print(f"✅ SQL insert file generated: {output_sql_file}")
