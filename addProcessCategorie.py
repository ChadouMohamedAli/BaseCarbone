#Add  Proces
import pandas as pd
import unicodedata
from datetime import datetime

df = pd.read_excel('dataSource/Base_Carbone_V23.6-v3.xlsx', sheet_name='F1')

cols_to_check = [
    'Type poste',
    'Code de la catégorie 1',
    'Code de la catégorie 2',
    'Code de la catégorie 3',
    'Code de la catégorie 4',
    'Code de la catégorie 5',
    'Code de la catégorie 6'
]

# Normalize and strip accents
def normalize(text):
    if pd.isnull(text):
        return ''
    text = str(text).lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

# Your classification function
def classify_row(row):
    combined_text = ' '.join(normalize(row[col]) for col in cols_to_check if pd.notnull(row[col]))

    if any(x in combined_text for x in ["gaz", "electricite", "chaleur", "fuel", "gazole", "biodiesel", "butane", "propane", "carburants", "essence", "diesel", "gpl", "charbon"]):
        return "energie"
    elif any(x in combined_text for x in ["transport", "camion", "vehicule", "voiture", "avion", "maritime", "train"]):
        return "transport"
    elif any(x in combined_text for x in ["coton", "tissu", "polyester", "matiere", "plastique", "textile", "metal"]):
        return "matiere"
    elif any(x in combined_text for x in ["dechet", "incineration", "recyclage"]):
        return "dechet"
    elif any(x in combined_text for x in ["beton", "roche", "tuiles"]):
        return "construction"
    elif "eau" in combined_text:
        return "eau"
    elif any(x in combined_text for x in ["electronique", "serveur", "data", "email", "cloud", "site web"]):
        return "service"
    else:
        return "autre"

# Apply it
df['type_processus'] = df.apply(classify_row, axis=1)


# Generate filename with current date and time
filename = f"Db/Base_Carbone_V{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
df.to_excel(filename, index=False)
df.to_csv(f"Db/Base_Carbone_V{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index=False)
print("df saved to : ", filename," .")