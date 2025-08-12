import pandas as pd

# === CONFIG ===
EXCEL_FILE = 'Db/Base_Carbone_classified_V2025-07-30_11-20-00.xlsx'   # Replace with your actual file path
SHEET_NAME = None               # Or specify sheet name
MAX_UNIQUE = 150

# === LOAD DATA ===
df = pd.read_excel(EXCEL_FILE)
print(df.columns)
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# === ANALYZE COLUMNS ===
report = []

for col in df.columns:
    unique_vals = df[col].dropna().unique()
    num_unique = len(unique_vals)
    is_dim_candidate = num_unique <= MAX_UNIQUE
    report.append({
        'Column': col,
        'Unique Values': num_unique,
        'Data Type': df[col].dtype,
        'As Dimension Table?': '✅ YES' if is_dim_candidate else '❌ NO'
    })

# === DISPLAY REPORT ===
report_df = pd.DataFrame(report).sort_values(by='Unique Values')
print(report_df.to_string(index=False))
