from segmentation import nlp   # on réutilise le modèle spaCy déjà chargé


def ajouter_entites(phrases):
    """Ajoute à chaque phrase la liste des noms propres trouvés par spaCy."""
    for p in phrases:
        doc = nlp(p["text"])
        p["entities"] = []
        for entite in doc.ents:
            p["entities"].append((entite.text, entite.label_))
    return phrases