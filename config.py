import re

MOT    = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
FIN    = re.compile(r'[.!?…:«—–"\"]')
ROMAIN = re.compile(r"^[IVXLCDM]+$")

TITRES   = set("m mme mlle dr docteur professeur maire sire empereur seigneur monsieur madame mademoiselle commandant capitaine colonel general roi reine prince princesse lord lady sir commodore marchand ambassadeur conseiller consul pere maitre maitres".split())
ARTICLES = set("le la l les un une du des au aux ce cette ces".split())
PREP     = set("sur vers dans depuis".split())
NLIEU    = set("planete monde systeme royaume ville capitale province secteur".split())

FICHIERS = [
    r"C:\Users\zix\Desktop\m1 ia\AMS\entite1.txt",
    r"C:\Users\zix\Desktop\m1 ia\AMS\ngramme\n2_gramme.txt",
    r"C:\Users\zix\Desktop\m1 ia\AMS\ngramme\n3_gramme.txt",
    r"C:\Users\zix\Desktop\m1 ia\AMS\ngramme\n4_gramme.txt",
]
