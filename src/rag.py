import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from summary import appeler_llm

# Modèle d'embeddings qui comprend le français (téléchargé au premier lancement)
NOM_MODELE = "paraphrase-multilingual-MiniLM-L12-v2"
modele_embedding = SentenceTransformer(NOM_MODELE)

CONSIGNE_QA = (
    "Tu réponds à des questions sur une réunion, en français. "
    "Utilise UNIQUEMENT les extraits fournis. "
    "Si la réponse n'est pas dans les extraits, réponds exactement : "
    "'Je ne trouve pas cette information dans la réunion.' "
    "Réponds en une ou deux phrases, sans rien inventer."
)


def construire_index(phrases):
    """Transforme chaque phrase en vecteur et les range dans FAISS."""
    textes = []
    for p in phrases:
        textes.append(p["speaker"] + " : " + p["text"])

    vecteurs = modele_embedding.encode(textes, normalize_embeddings=True)
    vecteurs = np.array(vecteurs, dtype="float32")

    index = faiss.IndexFlatIP(vecteurs.shape[1])   # IP = produit scalaire = similarité
    index.add(vecteurs)
    return index


def chercher(question, index, phrases, k=4):
    """Retourne les k phrases les plus proches de la question."""
    vecteur = modele_embedding.encode([question], normalize_embeddings=True)
    vecteur = np.array(vecteur, dtype="float32")

    scores, positions = index.search(vecteur, k)

    trouvees = []
    for pos in positions[0]:
        if pos != -1:
            trouvees.append(phrases[pos])

    # On remet dans l'ordre de la réunion pour que le LLM lise dans le bon sens
    trouvees.sort(key=lambda p: p["id"])
    return trouvees


def repondre(question, index, phrases, k=4):
    """Retourne (réponse, extraits utilisés)."""
    extraits = chercher(question, index, phrases, k)

    lignes = []
    for e in extraits:
        lignes.append("[" + e["time"] + "] " + e["speaker"] + " : " + e["text"])
    contexte = "\n".join(lignes)

    texte = "Extraits de la réunion :\n" + contexte + "\n\nQuestion : " + question
    reponse = appeler_llm(CONSIGNE_QA, texte)

    if reponse is None:
        reponse = "Le LLM n'a pas répondu. Voici les extraits trouvés."
    return reponse, extraits