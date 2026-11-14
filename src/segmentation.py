import spacy

# On charge le modèle français de spaCy (une seule fois)
nlp = spacy.load("fr_core_news_md")


def decouper_en_phrases(prises):
    """Coupe chaque prise de parole en phrases.
    On garde l'heure et le nom de celui qui parle avec chaque phrase."""
    phrases = []

    for prise in prises:
        doc = nlp(prise["text"])       # spaCy analyse le texte

        for morceau in doc.sents:      # doc.sents = les phrases trouvées
            texte = morceau.text.strip()

            # On ignore les phrases de moins de 3 mots ("Oui.", "Parfait.")
            if len(texte.split()) < 3:
                continue

            phrases.append({
                "id": len(phrases),
                "time": prise["time"],
                "speaker": prise["speaker"],
                "text": texte,
            })

    return phrases