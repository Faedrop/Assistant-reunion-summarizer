from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from ner import ajouter_entites
from classifiers import charger_modele, classer_phrases, extraire_decisions_actions
from slots import remplir_infos
from topics import decouper_en_sujets, trouver_mots_cles
from summary import resumer_sujet
from report import construire_compte_rendu


def analyser_reunion(texte_brut, titre="Compte rendu de réunion"):
    """Fait toute la chaîne. Retourne (compte_rendu, phrases)."""

    # 1) nettoyage, phrases, entités
    prises = nettoyer_transcript(texte_brut)
    phrases = decouper_en_phrases(prises)
    phrases = ajouter_entites(phrases)

    # 2) décisions et actions
    modele = charger_modele()
    phrases = classer_phrases(phrases, modele)
    decisions, actions = extraire_decisions_actions(phrases)

    participants = []
    for prise in prises:
        if prise["speaker"] not in participants:
            participants.append(prise["speaker"])

    decisions = remplir_infos(decisions, participants)
    actions = remplir_infos(actions, participants)

    # 3) sujets, mots-clés, résumés
    prenoms = []
    for nom in participants:
        prenoms.append(nom.lower())

    sujets = decouper_en_sujets(phrases)
    mots_cles = trouver_mots_cles(sujets, prenoms)

    resumes = []
    for sujet in sujets:
        resumes.append(resumer_sujet(sujet))

    # 4) assemblage
    cr = construire_compte_rendu(titre, participants, mots_cles,
                                 resumes, decisions, actions)
    return cr, phrases