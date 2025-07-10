import pandas as pd
import unicodedata

# Load the Base Carbone file
df = pd.read_excel('dataSource/Base_Carbone_V23.6-v3.xlsx', sheet_name='F1')

# Columns to look into for classification
cols_to_check = [
    'Type poste',
    'Code de la catégorie 1',
    'Code de la catégorie 2',
    'Code de la catégorie 3',
    'Code de la catégorie 4',
    'Code de la catégorie 5',
    'Code de la catégorie 6'
]

# Accent and case normalization
def normalize(text):
    if pd.isnull(text):
        return ''
    text = str(text).lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

# First classify type_processus (your current logic)
def classify_processus(row):
    combined = ' '.join(normalize(row[col]) for col in cols_to_check if pd.notnull(row[col]))
    if any(x in combined for x in ["gaz", "electricite", "chaleur", "fuel", "gazole", "biodiesel", "butane", "propane", "carburants", "essence", "diesel", "gpl", "charbon"]):
        return "energie"
    elif any(x in combined for x in ["transport", "camion", "vehicule", "voiture", "avion", "maritime", "train"]):
        return "transport"
    elif any(x in combined for x in ["coton", "tissu", "polyester", "matiere", "plastique", "textile", "metal"]):
        return "matiere"
    elif any(x in combined for x in ["dechet", "incineration", "recyclage"]):
        return "dechet"
    elif any(x in combined for x in ["beton", "roche", "tuiles"]):
        return "construction"
    elif "eau" in combined:
        return "eau"
    elif any(x in combined for x in ["electronique", "serveur", "data", "email", "cloud", "site web"]):
        return "service"
    else:
        return "autre"

df['type_processus'] = df.apply(classify_processus, axis=1)

# --- 📌 REFERENCE TABLE FROM THE IMAGE ---
reference = [
    # Scope 1
    ("1.1 Émissions directes des sources fixes de combustion", "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),
    ("1.2 Émissions directes des sources mobiles de combustion", "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),
    ("1.3 Émissions directes des procédés hors énergie", "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),
    ("1.4 Émissions directes fugitives", "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),
    ("1.5 Émissions issues de la biomasse (sols et forêts)", "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),

    # Scope 2
    ("2.1 Émissions indirectes liées à la consommation d’électricité", "2. ÉMISSIONS INDIRECTES ASSOCIÉES À L’ÉNERGIE", "Scope 2"),
    ("2.2 Émissions indirectes liées à la consommation d’énergie autre que l’électricité", "2. ÉMISSIONS INDIRECTES ASSOCIÉES À L’ÉNERGIE", "Scope 2"),

    # Scope 3 – Transport
    ("3.1 Transport de marchandise amont", "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    ("3.2 Transport de marchandise aval", "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    ("3.3 Déplacements domicile-travail", "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    ("3.4 Déplacements des visiteurs et des clients", "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    ("3.5 Déplacements professionnels", "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),

    # Scope 3 – Produits achetés
    ("4.1 Achats de biens", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    ("4.2 Immobilisations de biens", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    ("4.3 Gestion des déchets", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    ("4.4 Actifs en leasing amont", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    ("4.5 Achats de services", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),

    # Scope 3 – Produits vendus
    ("5.1 Utilisation des produits vendus", "5. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS VENDUS", "Scope 3"),
    ("5.2 Actifs en leasing aval", "5. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS VENDUS", "Scope 3"),
    ("5.3 Fin de vie des produits vendus", "5. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS VENDUS", "Scope 3"),
    ("5.4 Investissements", "5. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS VENDUS", "Scope 3"),

    # Scope 3 – Autres
    ("6.1 Autres émissions indirectes", "6. AUTRES ÉMISSIONS INDIRECTES", "Scope 3")
]

# Turn into DataFrame for joining
ref_df = pd.DataFrame(reference, columns=["poste", "categorie", "scope"])

# Normalize the 'poste' column in both DataFrames for merging
df['poste_clean'] = df['Poste'].fillna('').apply(normalize)
ref_df['poste_clean'] = ref_df['poste'].apply(normalize)

# Merge the info back into the main dataframe
df = df.merge(ref_df[['poste_clean', 'categorie', 'scope']], on='poste_clean', how='left')

# Drop helper column
df.drop(columns=['poste_clean'], inplace=True)

# Save result
df.to_excel("Db/Base_Carbone_classified.xlsx", index=False)
