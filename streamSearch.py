import streamlit as st
import pandas as pd

# ------------------------
# Config
# ------------------------
DATA_PATH = "keywords_BertModel(full File).xlsx"  # Path to your file
KEYWORD_COLUMN = "extracted_keywords"  # Name of the column with extracted keywords

# ------------------------
# Load Data (cached for speed)
# ------------------------
@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)

# ------------------------
# App UI
# ------------------------
st.title("Intelligent Keyword Search")

df = load_data()
st.sidebar.header("⚙️ Settings")
lang        = st.sidebar.radio("Select language:", ["French", "English"])
lang_code   = "fr" if lang == "French" else "en"
st.write(f"Data loaded: **{len(df)} rows**, keyword column: **{KEYWORD_COLUMN}**")

search_query = st.text_input("Enter keywords to search (comma-separated)", "")

if search_query.strip():
    search_terms = [term.strip().lower() for term in search_query.split(",")]

    def match_keywords(keywords):
        if pd.isna(keywords):
            return False
        keywords_str = str(keywords).lower()
        return all(term in keywords_str for term in search_terms)

    filtered_df = df[df[KEYWORD_COLUMN].apply(match_keywords)]

    st.subheader(f"✅ {len(filtered_df)} matches found")
    st.dataframe(filtered_df)

    # Download filtered data
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download results", csv, "filtered_results.csv", "text/csv")
else:
    st.info("Enter one or more keywords to search in the data.")
