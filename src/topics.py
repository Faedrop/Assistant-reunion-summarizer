from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# Si une phrase contient un de ces morceaux, un nouveau sujet commence
MARQUEURS = ["passons", "parlons", "dernière chose", "point suivant",
             "prochain point", "autre sujet"]

# Mots français inutiles (le, la, de, et...) + quelques mots de réunion
MOTS_VIDES = set(stopwords.words("french"))
MOTS_VIDES.update(["donc", "alors", "bien", "très", "parfait", "super",
                   "pense", "trouve", "faire", "avons", "avait", "sera", "tout"])


def decouper_en_sujets(phrases):
    """Regroupe les phrases par sujet. Retourne une liste de blocs."""
    sujets = []
    bloc = []

    for p in phrases:
        texte = p["text"].lower()

        # Est-ce que cette phrase annonce un nouveau sujet ?
        nouveau_sujet = False
        for marqueur in MARQUEURS:
            if marqueur in texte:
                nouveau_sujet = True

        # Si oui, on termine le bloc en cours et on en commence un autre
        if nouveau_sujet and len(bloc) > 0:
            sujets.append(bloc)
            bloc = []

        bloc.append(p)

    if len(bloc) > 0:
        sujets.append(bloc)

    return sujets


def trouver_mots_cles(sujets, a_ignorer, nombre=3):
    """Pour chaque sujet, retourne ses mots les plus caractéristiques (TF-IDF)."""
    textes = []

    for sujet in sujets:
        mots_gardes = []
        for p in sujet:
            texte = p["text"].lower()
            for signe in [",", ".", "?", "!", ";", ":", "'", "-"]:
                texte = texte.replace(signe, " ")

            for mot in texte.split():
                if len(mot) < 4:
                    continue                 # mots trop courts
                if mot in MOTS_VIDES or mot in a_ignorer:
                    continue                 # mots inutiles ou prénoms
                if mot.isdigit():
                    continue                 # nombres
                mots_gardes.append(mot)

        textes.append(" ".join(mots_gardes))

    # TF-IDF : un mot est "important" pour un sujet s'il y apparaît
    # souvent, mais pas dans les autres sujets
    vectoriseur = TfidfVectorizer()
    matrice = vectoriseur.fit_transform(textes)
    tous_les_mots = vectoriseur.get_feature_names_out()

    resultat = []
    for i in range(len(textes)):
        scores = matrice[i].toarray()[0]
        meilleurs = scores.argsort()[::-1][:nombre]   # les plus grands scores
        mots = []
        for j in meilleurs:
            if scores[j] > 0:
                mots.append(tous_les_mots[j])
        resultat.append(mots)

    return resultat