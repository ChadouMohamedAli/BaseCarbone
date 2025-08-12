from keybert import KeyBERT

doc = """
         L’agriculture est responsable d’une part importante des émissions de méthane et de protoxyde d’azote. 
         Les méthodes de culture, l’élevage et l’usage d’engrais jouent un rôle clé dans les émissions agricoles.
      """
kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')
#keywords = kw_model.extract_keywords(doc)
keywords = kw_model.extract_keywords(
    doc,
    keyphrase_ngram_range=(1, 2),
    #stop_words='french',
    use_mmr=True,
    diversity=0.7,
    top_n=3
)
print(keywords)