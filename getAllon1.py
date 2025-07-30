import os
import pandas as pd

# Folder path containing your Excel files
folder_path = "fwdfichierinnoetpointcarr"

# List to hold DataFrames
all_dataframes = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx") and not filename.startswith("~$"):  # skip temp files
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path)
        all_dataframes.append(df)

# Combine all DataFrames
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Save to a new Excel file
combined_df.to_excel("Retour2025-INNO.xlsx", index=False)
