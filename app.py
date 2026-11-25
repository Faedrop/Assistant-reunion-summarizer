import sys
import os
import json
import time

sys.path.append("src")   # pour que Python trouve nos fichiers dans src/

import pandas as pd
import streamlit as st

from pipeline import analyser_reunion
from rag import construire_index, repondre
from report import generer_markdown
from export_pdf import sauvegarder_pdf

st.set_page_config(page_title="Assistant de comptes rendus", layout="wide")
st.title("Assistant intelligent de comptes rendus de réunion")

# --- 1) Charger et analyser ---------------------------------------------
fichier = st.file_uploader("Charge un transcript (.txt)", type=["txt"])

if fichier is not None and st.button("Analyser la réunion"):
    texte = fichier.read().decode("utf-8-sig")

    with st.spinner("Analyse en cours..."):
        debut = time.time()
        cr, phrases = analyser_reunion(texte)
        index = construire_index(phrases)
        duree = round(time.time() - debut, 1)

    # On range les résultats pour les garder quand la page se rafraîchit
    st.session_state["cr"] = cr
    st.session_state["phrases"] = phrases
    st.session_state["index"] = index
    st.session_state["duree"] = duree
    st.session_state["historique"] = []

    # On efface les anciens résumés modifiés
    for cle in list(st.session_state.keys()):
        if cle.startswith("resume_"):
            del st.session_state[cle]

# --- 2) Affichage des résultats -----------------------------------------
if "cr" in st.session_state:
    cr = st.session_state["cr"]

    st.success("Analyse terminée en " + str(st.session_state["duree"]) + " secondes.")
    st.write("**Participants :** " + ", ".join(cr["participants"]))

    # Résumés modifiables
    st.header("Résumé par sujet")
    for i in range(len(cr["sujets"])):
        s = cr["sujets"][i]
        titre = "Sujet " + str(s["numero"]) + " (" + ", ".join(s["mots_cles"]) + ")"
        nouveau_texte = st.text_area(titre, value=s["resume"],
                                     key="resume_" + str(i), height=130)
        s["resume"] = nouveau_texte   # on garde la version modifiée

    # Décisions
    st.header("Décisions")
    if len(cr["decisions"]) == 0:
        st.info("Aucune décision détectée.")
    else:
        tableau = pd.DataFrame(cr["decisions"])
        tableau.columns = ["Décision", "Échéance", "Confiance"]
        st.dataframe(tableau, use_container_width=True)

    # Actions
    st.header("Actions")
    if len(cr["actions"]) == 0:
        st.info("Aucune action détectée.")
    else:
        tableau = pd.DataFrame(cr["actions"])
        tableau.columns = ["Action", "Responsable", "Échéance", "Confiance"]
        st.dataframe(tableau, use_container_width=True)

    # Téléchargements
    st.header("Exporter")
    os.makedirs("output", exist_ok=True)
    sauvegarder_pdf(cr, "output/compte_rendu.pdf")
    with open("output/compte_rendu.pdf", "rb") as f:
        contenu_pdf = f.read()

    col1, col2, col3 = st.columns(3)
    col1.download_button("Télécharger Markdown", generer_markdown(cr),
                         file_name="compte_rendu.md")
    col2.download_button("Télécharger JSON",
                         json.dumps(cr, ensure_ascii=False, indent=2),
                         file_name="compte_rendu.json")
    col3.download_button("Télécharger PDF", contenu_pdf,
                         file_name="compte_rendu.pdf")

    # --- 3) Chat avec la réunion (RAG) ----------------------------------
    st.header("Pose une question sur la réunion")

    for message in st.session_state["historique"]:
        with st.chat_message(message["role"]):
            st.write(message["texte"])
            if message["role"] == "assistant":
                with st.expander("Sources"):
                    for e in message["sources"]:
                        st.write("[" + e["time"] + "] " + e["speaker"] + " : " + e["text"])

    question = st.chat_input("Ex : Qui doit contacter les fournisseurs ?")
    if question:
        st.session_state["historique"].append(
            {"role": "user", "texte": question, "sources": []})
        reponse, extraits = repondre(question, st.session_state["index"],
                                     st.session_state["phrases"])
        st.session_state["historique"].append(
            {"role": "assistant", "texte": reponse, "sources": extraits})
        st.rerun()