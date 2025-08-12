import streamlit as st
from keybert import KeyBERT
import spacy
import re


# Load models once
nlp_fr = spacy.load("fr_core_news_md")
nlp_en = spacy.load("en_core_web_md")

# Keep only certain POS tags
KEEP_POS = {"NOUN", "PROPN", "ADJ"}

def clean_and_tokenize(text, lang="fr"):
    """Clean text by keeping only selected POS and removing stopwords/numbers."""
    doc = nlp_fr(text) if lang == "fr" else nlp_en(text)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in KEEP_POS
        and not token.is_stop
        and token.is_alpha
    ]
    return " ".join(tokens)

def clean_text(text):
    #if pd.isnull(text):
        #return ""
    # Keep only letters (including accented ones), remove digits and special chars
    return re.sub(r"[^a-zA-ZÀ-ÖØ-öø-ÿ\s]", "", str(text)).strip().lower()


# Load multilingual model
kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')

st.set_page_config(page_title="Keyword Extractor", page_icon="🌱")

st.title("🌱 Keyword Extraction")
st.write("Enter your French or English text and get keywords instantly.")


# User input
doc = st.text_area(
    "✏️ Paste your text here:",
    "L’agriculture est responsable d’une part importante des émissions de méthane et de protoxyde d’azote. "
    "Les méthodes de culture, l’élevage et l’usage d’engrais jouent un rôle clé dans les émissions agricoles."
)

# Parameters
# Language selection
lang = st.radio("Select language:", ["French", "English"])
lang_code = "fr" if lang == "French" else "en"
st.sidebar.header("⚙️ Settings")
ngram_min = st.sidebar.slider("Min N-gram", 1, 3, 1)
ngram_max = st.sidebar.slider("Max N-gram", 1, 3, 2)
top_n = st.sidebar.slider("Number of keywords", 1, 20, 5)
diversity = st.sidebar.slider("MMR Diversity", 0.0, 1.0, 0.7)

if st.button("🚀 Extract Keywords"):
    cdoc = clean_and_tokenize(doc, lang_code)
    #c2doc = clean_text(cdoc)
    with st.spinner("Extracting..."):
        keywords = kw_model.extract_keywords(
            cdoc,
            keyphrase_ngram_range=(ngram_min, ngram_max),
            use_mmr=True,
            diversity=diversity,
            top_n=top_n
        )

    st.subheader("🔑 Extracted Keywords")
    for kw, score in keywords:
        st.write(f"- **{kw}** (score: {score:.4f})")
