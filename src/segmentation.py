import spacy

# On charge le modèle français une seule fois
nlp = spacy.load("fr_core_news_md")


def split_sentences(utterances):
    """Découpe chaque prise de parole en phrases (avec locuteur et heure)."""
    phrases = []

    for u in utterances:
        doc = nlp(u["text"])          # spaCy analyse le texte
        for sent in doc.sents:        # doc.sents = les phrases détectées
            texte = sent.text.strip()
            if len(texte.split()) >= 3:   # on ignore les phrases trop courtes
                phrases.append({
                    "id": len(phrases),
                    "time": u["time"],
                    "speaker": u["speaker"],
                    "text": texte,
                })
    return phrases