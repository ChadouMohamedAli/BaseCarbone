import pandas as pd

df1 = pd.read_excel('FoundKeys_BC2.xlsx')
print(df1.columns)
df2 = pd.read_excel('Db/Base_Carbone_classified_V2025-07-10_13-10-53.xlsx')
print(df2.columns)

merge = pd.merge(df2, df1[["Identifiant de l'élément", "found_keys",'Nom base anglais','Nom attribut anglais','Tags anglais']], on="Identifiant de l'élément", how="left")

merge.to_excel("Db/Base_Carbone_classified_V2025-07-24_11-30-00.xlsx", index=False)
print('Done')