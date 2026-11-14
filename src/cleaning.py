# Liste des mots d'hésitation à supprimer (tu peux en ajouter)
FILLERS = ["euh", "heu", "hmm", "hum", "ben", "bah"]


def parse_line(line):
    """Transforme '[00:45] Karim: texte' en dictionnaire."""
    line = line.strip()
    if not line.startswith("["):
        return None  # ligne qui n'a pas le bon format

    fin_heure = line.find("]")              # position du ']'
    heure = line[1:fin_heure]               # "00:45"
    reste = line[fin_heure + 1:].strip()    # "Karim: texte"

    locuteur, texte = reste.split(":", 1)   # coupe au premier ':'
    return {"time": heure, "speaker": locuteur.strip(), "text": texte.strip()}


def clean_text(text):
    """Enlève les 'euh' et les mots répétés."""
    mots_gardes = []
    mot_precedent = ""

    for mot in text.split():
        # on enlève la ponctuation pour comparer: "euh," -> "euh"
        mot_simple = mot.lower().strip(",.!?;:")

        if mot_simple in FILLERS:
            continue  # on saute ce mot
        if mot_simple == mot_precedent:
            continue  # mot répété ("je je"), on saute
        mots_gardes.append(mot)
        mot_precedent = mot_simple

    texte = " ".join(mots_gardes)
    if texte:
        texte = texte[0].upper() + texte[1:]  # majuscule au début
    return texte


def clean_transcript(raw_text):
    """Lit tout le transcript et retourne une liste de prises de parole propres."""
    resultat = []
    for line in raw_text.splitlines():
        u = parse_line(line)
        if u is None:
            continue
        u["text"] = clean_text(u["text"])
        if u["text"]:
            resultat.append(u)
    return resultat