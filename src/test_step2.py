from cleaning import clean_transcript
from segmentation import split_sentences

with open("data/reunion1.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises_de_parole = clean_transcript(texte_brut)
phrases = split_sentences(prises_de_parole)

print(len(prises_de_parole), "prises de parole ->", len(phrases), "phrases")
for p in phrases:
    print(p["id"], p["time"], p["speaker"], "|", p["text"])