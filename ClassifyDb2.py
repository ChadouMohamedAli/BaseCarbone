import pandas as pd
import unicodedata
from datetime import datetime
import math

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


def normalize(text):
    if pd.isnull(text):
        return ''
    text = str(text).lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
# Combine all relevant columns for scanning
def combined_text(row):
    return ' '.join(normalize(row[col]) for col in cols_to_check if pd.notnull(row[col]))

def cleanArchive(dfs):
    print(dfs.shape)
    dfc = dfs[~dfs.apply(lambda row: row.astype(str).str.lower().str.contains("archiv").any(), axis=1)]
    print(dfc.shape)
    return dfc



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
    elif any(x in combined for x in ["electronique", "serveur", "data", "email", "cloud", "site web", "mail", "service"]): #service, mail
        return "service"
    else:
        return "autre"

# Define mapping rules
mapping_rules = [
    # Scope 1
    (["fixe", "combust", "charbon"], "1.1 Émissions directes des sources fixes de combustion", "1. ÉMISSIONS DIRECTES DE GES",
     "Scope 1"),
    (["mobile", "combust"], "1.2 Émissions directes des sources mobiles de combustion", "1. ÉMISSIONS DIRECTES DE GES",
     "Scope 1"),
    (["hors", "energie"], "1.3 Émissions directes des procedes hors energie", "1. ÉMISSIONS DIRECTES DE GES",
     "Scope 1"),
    (["fugitive", "emissions"], "1.4 Émissions directes fugitives", "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),
    (["sol", "foret", "utcf"], "1.5 Émissions issues de la biomasse (sols et forêts)",
     "1. ÉMISSIONS DIRECTES DE GES", "Scope 1"),

    # Scope 2
    (["electricite"], "2.1 Émissions indirectes liées à la consommation d’électricité",
     "2. ÉMISSIONS INDIRECTES ASSOCIÉES À L’ÉNERGIE", "Scope 2"),
    (["chaleur", "vapeur"], "2.2 Émissions indirectes liées à la consommation d’énergie autre que l’électricité",
     "2. ÉMISSIONS INDIRECTES ASSOCIÉES À L’ÉNERGIE", "Scope 2"),

    # Scope 3 - transport
    (["transport", "camion", "amont", "marchandise"], "3.1 Transport de marchandise amont",
     "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    (["transport", "aval", "livraison", "marchandise"], "3.2 Transport de marchandise aval",
     "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    (["transport", "deplacement", "domicile", "personnes"], "3.3 Deplacements domicile-travail",
     "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    (["transport", "deplacement", "visiteur", "client", "personnes"], "3.4 Deplacements des visiteurs et de clients",
     "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),
    (["transport", "voyage", "personnes", "avion", "deplacement"], "3.5 Déplacements professionnels",
     "3. ÉMISSIONS INDIRECTES ASSOCIÉES AU TRANSPORT", "Scope 3"),

    # Scope 3 - produits achetés
    (["achat", "biens"], "4.1 Achats de biens", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"), #produit
    (["immobilisation", "biens"], "4.2 Immobilisations de biens", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    (["dechet", "recyclage", "traitement"], "4.3 Gestion des déchets", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    (["produit", "Actifs", "leasing", "amont"], "4.4 Actifs en leasing amont", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),
    (["achat", "service"], "4.5 Achats de services", "4. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS ACHETÉS", "Scope 3"),

    # Scope 3 - produits vendus
    (["utilisation"], "5.1 Utilisation des produits vendus", "5. ÉMISSIONS INDIRECTES ASSOCIÉES AUX PRODUITS VENDUS", "Scope 3"),

    # Fallback
    ([], "Inconnu", "Inconnu", "Inconnu")
]

df = cleanArchive(df)

""" Version V1.01
def map_poste_and_scope(row):
    text = combined_text(row)
    for keywords, poste, categorie, scope in mapping_rules:
        if all(k in text for k in keywords):
            return pd.Series([poste, categorie, scope])
    return pd.Series(["Inconnu", "Inconnu", "Inconnu"])
"""

def map_poste_and_scope(row):
    text = combined_text(row)
    best_match = ("Inconnu", "Inconnu", "Inconnu")
    best_score = 0

    for keywords, poste, categorie, scope in mapping_rules:
        if not keywords:
            continue
        match_count = sum(1 for k in keywords if k in text)
        required_matches = math.ceil(0.6 * len(keywords))  # round up

        if match_count >= required_matches and match_count > best_score:
            best_match = (poste, categorie, scope)
            best_score = match_count

    return pd.Series(best_match)

# Apply process classification
df['type_processus'] = df.apply(lambda row: classify_processus(row), axis=1)

# Apply poste/categorie/scope classification
df[['poste', 'categorie', 'scope']] = df.apply(map_poste_and_scope, axis=1)

# Define the desired column order
desired_order = [
    "type_processus", "categorie", "poste", "scope",
    "Code de la catégorie", "Type poste", "Localisation géographique",
    "Code de la catégorie 1", "Code de la catégorie 2", "Code de la catégorie 3",
    "Code de la catégorie 4", "Code de la catégorie 5", "Code de la catégorie 6",
    "Identifiant de l'élément", "Type Ligne", "Structure", "Type de l'élément",
    "Statut de l'élément", "Nom base français", "Nom attribut français", "Nom frontière français",
    "Tags français", "Unité français", "Contributeur", "Autres Contributeurs", "Localisation géographique.1",
    "Sous-localisation géographique français", "Période de validité", "Incertitude", "Transparence",
    "Qualité", "Qualité TeR", "Qualité GR", "Qualité TiR", "Qualité C", "Qualité P", "Qualité M",
    "Commentaire français", "Commentaire espagnol", "Nom poste français", "Total poste non décomposé",
    "CO2f", "CH4f", "CH4b", "N2O",
    "Code gaz supplémentaire 1", "Valeur gaz supplémentaire 1",
    "Code gaz supplémentaire 2", "Valeur gaz supplémentaire 2",
    "Code gaz supplémentaire 3", "Valeur gaz supplémentaire 3",
    "Code gaz supplémentaire 4", "Valeur gaz supplémentaire 4",
    "Code gaz supplémentaire 5", "Valeur gaz supplémentaire 5",
    "Autres GES", "CO2b"
]

# Filter to existing columns (in case some are missing)
existing_order = [col for col in desired_order if col in df.columns]

# Add any remaining columns that are not in the desired list
remaining_cols = [col for col in df.columns if col not in desired_order]

# Reorder the DataFrame
df = df[existing_order + remaining_cols]
# Save result
filename = f"Db/Base_Carbone_classified_V{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
df.to_excel(filename, index=False)
df.to_csv(f"Db/Base_Carbone_classified_V{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index=False)
print("df saved to : ", filename," .")
