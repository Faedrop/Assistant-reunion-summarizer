MOTS_INUTILES = ["euh", "heu", "hmm", "hum", "ben", "bah"]


def lire_ligne(ligne):
    """Transforme '[00:45] Karim: bonjour' en dictionnaire."""
    ligne = ligne.strip()

    # Si la ligne ne commence pas par '[', on l'ignore
    if not ligne.startswith("["):
        return None

    position_crochet = ligne.find("]")
    heure = ligne[1:position_crochet]            # ex: "00:45"
    reste = ligne[position_crochet + 1:].strip() # ex: "Karim: bonjour"

  
    if ":" not in reste:
        return None

    nom, texte = reste.split(":", 1)             # coupe au premier ':'

    return {"time": heure, "speaker": nom.strip(), "text": texte.strip()}


def nettoyer_texte(texte):
    """Enlève les 'euh' et les mots répétés."""
    mots_gardes = []
    mot_avant = ""

    for mot in texte.split():
        
        mot_simple = mot.lower().strip(",.!?;:")

        if mot_simple in MOTS_INUTILES:
            continue            
        if mot_simple == mot_avant:
            continue            # mot répété ("je je"), on saute

        mots_gardes.append(mot)
        mot_avant = mot_simple

    texte_propre = " ".join(mots_gardes)

    # Majuscule au début de la phrase
    if texte_propre != "":
        texte_propre = texte_propre[0].upper() + texte_propre[1:]

    return texte_propre


def nettoyer_transcript(texte_brut):
    """Lit tout le transcript et retourne la liste des prises de parole propres."""
    resultat = []

    for ligne in texte_brut.splitlines():
        prise = lire_ligne(ligne)
        if prise is None:
            continue

        prise["text"] = nettoyer_texte(prise["text"])

        if prise["text"] != "":
            resultat.append(prise)

    return resultat