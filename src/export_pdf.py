from fpdf import FPDF
def pour_pdf(texte):
    """Remplace les caractères que la police du PDF ne sait pas écrire."""
    if texte is None:
        return ""

    remplacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "…": "...",
    }
    for ancien, nouveau in remplacements.items():
        texte = texte.replace(ancien, nouveau)

    # Tous les espaces bizarres (insécables, fines...) deviennent un espace normal
    resultat = ""
    for caractere in texte:
        if caractere.isspace():
            resultat = resultat + " "
        else:
            resultat = resultat + caractere

    # Si un caractère reste incompatible, on le remplace par '?'
    return resultat.encode("latin-1", "replace").decode("latin-1")

def ecrire_titre(pdf, texte):
    pdf.set_font("Helvetica", "B", 13)
    pdf.ln(3)
    pdf.cell(0, 8, pour_pdf(texte), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)


def ecrire_paragraphe(pdf, texte):
    pdf.multi_cell(0, 6, pour_pdf(texte), new_x="LMARGIN", new_y="NEXT")


def sauvegarder_pdf(cr, chemin):
    """Crée un PDF à partir du dictionnaire du compte rendu."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Titre
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, pour_pdf(cr["titre"]), new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    ecrire_paragraphe(pdf, "Participants : " + ", ".join(cr["participants"]))
    ecrire_paragraphe(pdf, "Bilan : " + str(len(cr["decisions"])) + " décisions, "
                      + str(len(cr["actions"])) + " actions")

    # Résumés
    ecrire_titre(pdf, "Résumé par sujet")
    for s in cr["sujets"]:
        pdf.set_font("Helvetica", "B", 11)
        ecrire_paragraphe(pdf, "Sujet " + str(s["numero"]) + " (" + ", ".join(s["mots_cles"]) + ")")
        pdf.set_font("Helvetica", "", 11)
        ecrire_paragraphe(pdf, s["resume"])
        pdf.ln(2)

    # Décisions
    ecrire_titre(pdf, "Décisions")
    if len(cr["decisions"]) == 0:
        ecrire_paragraphe(pdf, "Aucune décision détectée.")
    for d in cr["decisions"]:
        ecrire_paragraphe(pdf, "- " + d["texte"] + " (confiance : " + str(d["confiance"]) + ")")

    # Actions
    ecrire_titre(pdf, "Actions")
    for a in cr["actions"]:
        echeance = a["echeance"] if a["echeance"] else "non précisée"
        ecrire_paragraphe(pdf, "- " + a["texte"])
        pdf.set_font("Helvetica", "I", 10)
        ecrire_paragraphe(pdf, "     Responsable : " + a["responsable"]
                          + " | Échéance : " + echeance
                          + " | Confiance : " + str(a["confiance"]))
        pdf.set_font("Helvetica", "", 11)

    pdf.output(chemin)