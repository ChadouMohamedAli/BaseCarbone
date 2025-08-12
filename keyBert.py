import pandas as pd
from keybert import KeyBERT
from tqdm import tqdm
import re


def clean_text(text):
    if pd.isnull(text):
        return ""
    # Keep only letters (including accented ones), remove digits and special chars
    return re.sub(r"[^a-zA-ZÀ-ÖØ-öø-ÿ\s]", "", str(text)).strip().lower()
# Load Excel file
file_path = 'Db/Base_Carbone_classified_V2025-07-30_11-20-00.xlsx'  # Update with your filename
df = pd.read_excel(file_path)

# Detect string columns
string_cols = df.select_dtypes(include="object").columns.tolist()

# Combine text fields
df["text_blob"] = df[string_cols].fillna("").astype(str).agg(" ".join, axis=1)
df["text_blob"] = df["text_blob"].apply(clean_text)
# Init KeyBERT model
#kw_model = KeyBERT(model='all-MiniLM-L6-v2') #English simple
kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')

# Extract keywords per row
def extract_keywords(text, top_n=10):
    try:
        keywords = kw_model.extract_keywords(
            text, keyphrase_ngram_range=(1, 2),
            #stop_words='english',
            use_mmr=True,
            diversity=0.6,
            top_n=top_n)
        return [kw for kw, score in keywords]
    except:
        return []

# Apply to all rows with progress bar
tqdm.pandas()
df["extracted_keywords"] = df["text_blob"].progress_apply(extract_keywords)

# Save for inspection
df.to_excel("keywords_BertModel(full File).xlsx", index=False)

print("✅ Done: Keywords extracted and saved to keywords_output.xlsx")
