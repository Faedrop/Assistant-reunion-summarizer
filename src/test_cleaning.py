from cleaning import nettoyer_transcript

with open("data/reunion1.txt", encoding="utf-8") as f:
    texte_brut = f.read()


prises = nettoyer_transcript(texte_brut)
# affihcer results
for p in prises:
    print(p["time"], "|", p["speaker"], "|", p["text"])