import pandas as pd

df1 = pd.read_excel('FoundKeys_BC2.xlsx')
print(df1.columns)
print(df1.shape)
df2 = pd.read_excel('Db/Base_Carbone_classified_V2025-07-10_13-10-53.xlsx')
print(df2.columns)
print(df2.shape)

merge = pd.merge(df2, df1[["Identifiant de l'élément", "found_keys",'Nom base anglais','Nom attribut anglais','Tags anglais', "Total poste non décomposé", "Type de l'élément"]], on=["Identifiant de l'élément", "Type de l'élément", "Total poste non décomposé"], how="left")
print(merge.shape)

merge = merge.drop_duplicates()
merge.to_excel("Db/Base_Carbone_classified_V2025-07-30_11-20-00.xlsx", index=False)
print('Done')