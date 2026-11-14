JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]
EXPRESSIONS = ["la semaine prochaine", "fin de la semaine", "fin du mois",
               "fin de journée", "ce soir", "demain", "aujourd'hui"]

# Si la phrase contient un de ces mots, c'est celui qui parle qui s'en occupe
MOTS_JE = ["je", "j'", "moi"]


def enlever_ponctuation(texte):
    """Met en minuscules et remplace la ponctuation par des espaces."""
    texte = texte.lower()
    for signe in [",", ".", "?", "!", ";", ":"]:
        texte = texte.replace(signe, " ")
    return texte


def trouver_responsable(phrase, participants):
    """Retourne le nom de la personne qui fait l'action."""
    texte = enlever_ponctuation(phrase["text"]).replace("'", "' ")
    mots = texte.split()

    # 1) "je" ou "moi" : c'est la personne qui parle
    for m in MOTS_JE:
        if m in mots:
            return phrase["speaker"]

    # 2) un participant est cité dans la phrase
    for nom in participants:
        if nom.lower() in mots:
            return nom

    return "Non précisé"


def trouver_echeance(phrase):
    """Retourne l'échéance trouvée dans la phrase, ou None."""
    texte = enlever_ponctuation(phrase["text"])
    mots = texte.split()

    # 1) une date avec un mois : "24 novembre" ou "lundi 24 novembre"
    for i in range(len(mots)):
        if mots[i] in MOIS and i > 0 and mots[i - 1].isdigit():
            date = mots[i - 1] + " " + mots[i]
            if i > 1 and mots[i - 2] in JOURS:
                date = mots[i - 2] + " " + date
            return date

    # 2) une expression comme "ce soir" ou "demain"
    for expression in EXPRESSIONS:
        if expression in texte:
            return expression

    # 3) un jour de la semaine, éventuellement suivi de "prochain"
    for i in range(len(mots)):
        if mots[i] in JOURS:
            if i + 1 < len(mots) and mots[i + 1] == "prochain":
                return mots[i] + " prochain"
            return mots[i]

    return None


def remplir_infos(elements, participants):
    """Ajoute 'responsible' et 'deadline' à chaque décision/action."""
    for e in elements:
        e["responsible"] = trouver_responsable(e, participants)
        e["deadline"] = trouver_echeance(e)
    return elements