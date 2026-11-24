import json


def construire_compte_rendu(titre, participants, mots_cles, resumes, decisions, actions):
    """Assemble toutes les informations dans un seul dictionnaire."""
    compte_rendu = {
        "titre": titre,
        "participants": participants,
        "sujets": [],
        "decisions": [],
        "actions": [],
    }

    for i in range(len(resumes)):
        resume = resumes[i]
        if resume is None:
            resume = "Résumé indisponible."
        compte_rendu["sujets"].append({
            "numero": i + 1,
            "mots_cles": mots_cles[i],
            "resume": resume,
        })

    for d in decisions:
        compte_rendu["decisions"].append({
            "texte": d["text"],
            "echeance": d["deadline"],
            "confiance": d["confidence"],
        })

    for a in actions:
        compte_rendu["actions"].append({
            "texte": a["text"],
            "responsable": a["responsible"],
            "echeance": a["deadline"],
            "confiance": a["confidence"],
        })

    return compte_rendu


def sauvegarder_json(compte_rendu, chemin):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(compte_rendu, f, ensure_ascii=False, indent=2)


def generer_markdown(cr):
    """Transforme le dictionnaire en texte Markdown."""
    lignes = []
    lignes.append("# " + cr["titre"])
    lignes.append("")
    lignes.append("**Participants :** " + ", ".join(cr["participants"]))
    lignes.append("")
    lignes.append("**Bilan :** " + str(len(cr["decisions"])) + " décisions, "
                  + str(len(cr["actions"])) + " actions")

    lignes.append("")
    lignes.append("## Résumé par sujet")
    for s in cr["sujets"]:
        lignes.append("")
        lignes.append("### Sujet " + str(s["numero"]) + " (" + ", ".join(s["mots_cles"]) + ")")
        lignes.append(s["resume"])

    lignes.append("")
    lignes.append("## Décisions")
    lignes.append("")
    if len(cr["decisions"]) == 0:
        lignes.append("Aucune décision détectée.")
    for d in cr["decisions"]:
        lignes.append("- " + d["texte"] + " *(confiance : " + str(d["confiance"]) + ")*")

    lignes.append("")
    lignes.append("## Actions")
    lignes.append("")
    lignes.append("| Action | Responsable | Échéance | Confiance |")
    lignes.append("|---|---|---|---|")
    for a in cr["actions"]:
        echeance = a["echeance"] if a["echeance"] else "-"
        lignes.append("| " + a["texte"] + " | " + a["responsable"] + " | "
                      + echeance + " | " + str(a["confiance"]) + " |")

    return "\n".join(lignes)


def sauvegarder_markdown(cr, chemin):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(generer_markdown(cr))