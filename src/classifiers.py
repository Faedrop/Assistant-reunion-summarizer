import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

CHEMIN_MODELE = "models/classifier.joblib"
SEUIL = 0.45   # en dessous de ce score, on ne garde pas la phrase


def creer_modele():
    """Crée le modèle : TF-IDF + régression logistique."""
    return make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)),   # mots seuls ET paires de mots
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )


def entrainer(chemin_csv="data/phrases.csv"):
    """Apprend à partir du CSV, affiche les scores, sauvegarde le modèle."""
    donnees = pd.read_csv(chemin_csv)

    X_train, X_test, y_train, y_test = train_test_split(
        donnees["phrase"], donnees["label"],
        test_size=0.2, random_state=42, stratify=donnees["label"],
    )

    modele = creer_modele()
    modele.fit(X_train, y_train)          

    print("=== Résultats sur les 20% de test ===")
    print(classification_report(y_test, modele.predict(X_test)))

   
    modele = creer_modele()
    modele.fit(donnees["phrase"], donnees["label"])

    os.makedirs("models", exist_ok=True)
    joblib.dump(modele, CHEMIN_MODELE)
    print("Modèle sauvegardé dans", CHEMIN_MODELE)


def charger_modele():
    return joblib.load(CHEMIN_MODELE)


def classer_phrases(phrases, modele):
    """Ajoute 'label' et 'confidence' à chaque phrase."""
    textes = [p["text"] for p in phrases]
    probabilites = modele.predict_proba(textes)   # une proba par classe
    classes = list(modele.classes_)               # ['action', 'autre', 'decision']

    for phrase, probas in zip(phrases, probabilites):
        meilleur = probas.argmax()                # position de la plus grande proba
        phrase["label"] = classes[meilleur]
        phrase["confidence"] = round(float(probas[meilleur]), 2)

    return phrases


def extraire_decisions_actions(phrases):
    """Garde seulement les décisions et actions assez sûres."""
    decisions = []
    actions = []

    for p in phrases:
        if p["confidence"] < SEUIL:
            continue                              # on saute
        if p["label"] == "decision":
            decisions.append(p)
        elif p["label"] == "action":
            actions.append(p)

    return decisions, actions


if __name__ == "__main__":
    entrainer()