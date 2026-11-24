import os
import requests
from dotenv import load_dotenv

load_dotenv()   
API_KEY = os.getenv("OPENROUTER_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"   
CONSIGNE = (
    "Tu es un assistant qui rédige des comptes rendus de réunion en français. "
    "Résume le passage de réunion fourni en 2 à 3 phrases claires. "
    "Utilise uniquement des informations explicitement dites dans le texte. "
    "N'ajoute aucune interprétation : ne dis pas que 'tout le monde' est d'accord "
    "si seules certaines personnes l'ont dit, et ne précise pas d'heure ou de moment "
    "qui n'est pas mentionné. "
    "Écris un petit paragraphe, sans liste."
)

def appeler_llm(consigne, texte):
    """Envoie une consigne + un texte au LLM et retourne sa réponse."""
    if not API_KEY:
        print("Erreur : OPENROUTER_API_KEY introuvable dans le fichier .env")
        return None

    reponse = requests.post(
        URL,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "HTTP-Referer": "http://localhost",
            "X-Title": "Assistant reunion summarizer",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": consigne},
                {"role": "user", "content": texte},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )

    if reponse.status_code != 200:
        print("Erreur OpenRouter :", reponse.status_code, reponse.text)
        return None

    return reponse.json()["choices"][0]["message"]["content"]


def resumer_sujet(sujet):
    """Résume un sujet (une liste de phrases)."""
    lignes = []
    for p in sujet:
        lignes.append(p["speaker"] + " : " + p["text"])
    texte = "\n".join(lignes)
    return appeler_llm(CONSIGNE, texte)