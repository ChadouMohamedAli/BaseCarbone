import pandas as pd
from datetime import datetime

# Load the ADEME Base Carbone Excel file
file_path = "dataSource/Base_Carbone_V23.6-v2.xlsx"  # Adjust if needed
df = pd.read_excel(file_path)

# Display the first few rows and column names to identify useful columns
print(df.head())
print(df.columns.tolist())

# Colonnes qu'on garde (ajuste selon tes besoins réels)
cols_to_keep = [
    "Identifiant de l'élément", "Nom base français", "Nom attribut français",
    "Code de la catégorie", "Tags français", "Unité français",
    "Localisation géographique", "Période de validité",
    "Type poste", "Nom poste français",
    "Total poste non décomposé", "CO2f", "CH4f", "CH4b", "N2O", "CO2b"
]

# Nettoyage du DataFrame
df_clean = df[cols_to_keep].copy()

# Renommage des colonnes (facultatif mais conseillé pour la DB)
df_clean.columns = [
    "id_element", "nom_base", "nom_attribut",
    "code_categorie", "tags", "unite",
    "localisation", "periode_validite",
    "type_poste", "nom_poste",
    "total_poste", "co2f", "ch4f", "ch4b", "n2o", "co2b"
]

# Supprimer les lignes où l'identifiant ou le total_poste est manquant
df_clean = df_clean[df_clean["id_element"].notna() & df_clean["total_poste"].notna()]

# Export CSV avec timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_filename = f"Db/base_carbone_cleaned_{timestamp}.csv"
df_clean.to_csv(output_filename, index=False)#, encoding='utf-8-sig')

print(f"Fichier nettoyé exporté sous : {output_filename}")