from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from topics import decouper_en_sujets, trouver_mots_cles

with open("data/reunion2.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)

# Les prénoms des participants, à ignorer dans les mots-clés
prenoms = []
for prise in prises:
    nom = prise["speaker"].lower()
    if nom not in prenoms:
        prenoms.append(nom)

sujets = decouper_en_sujets(phrases)
mots_cles = trouver_mots_cles(sujets, prenoms)

print(len(sujets), "sujets trouvés\n")

for i in range(len(sujets)):
    debut = sujets[i][0]["time"]
    fin = sujets[i][-1]["time"]
    print("Sujet", i + 1, "(", debut, "->", fin, ") :", len(sujets[i]), "phrases")
    print("   mots-clés :", ", ".join(mots_cles[i]))