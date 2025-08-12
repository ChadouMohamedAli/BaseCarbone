import streamlit as st
import spacy
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

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

# Load KeyBERT multilingual model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
kw_model = KeyBERT(model=model)

# ---- STREAMLIT UI ----
st.title("🌱 Keyword Extraction 🔑")
#st.write("Paste your text below, choose the language, and extract keywords.")
# User input
user_text = st.text_area(
    "✏️ Paste your text here:",
    "L’agriculture est responsable d’une part importante des émissions de méthane et de protoxyde d’azote. "
    "Les méthodes de culture, l’élevage et l’usage d’engrais jouent un rôle clé dans les émissions agricoles."
)
# Text input
#user_text = st.text_area("Enter your text:", height=200)

# Parameters
st.sidebar.header("⚙️ Settings")
# Language selection
lang        = st.sidebar.radio("Select language:", ["French", "English"])
lang_code   = "fr" if lang == "French" else "en"
top_n       = st.sidebar.slider("Number of keywords:", min_value=3, max_value=15, value=5)
ngram_min   = st.sidebar.slider("Min N-gram", 1, 3, 1)
ngram_max   = st.sidebar.slider("Max N-gram", 1, 3, 2)
#use_mmr     = st.sidebar.checkbox("Use MMR (diverse keywords)?", value=True)
diversity   = st.sidebar.slider("Diversity (if MMR is on):", 0.1, 1.0, 0.7)

if st.button("Extract Keywords"):
    if user_text.strip():
        # Clean text
        cleaned_text = clean_and_tokenize(user_text, lang_code)
        st.subheader("🧹 Cleaned Text:")
        st.write(cleaned_text)

        # Extract keywords
        keywords = kw_model.extract_keywords(
            cleaned_text,
            keyphrase_ngram_range=(ngram_min, ngram_max),
            #keyphrase_ngram_range=(1, 2),
            use_mmr     = True,
            diversity   = diversity,
            top_n       = top_n
        )

        st.subheader("🔑 Extracted Keywords:")
        for kw, score in keywords:
            st.write(f"{kw} — **{score:.4f}**")
    else:
        st.warning("Please enter some text.")
