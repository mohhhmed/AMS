import re

MOT    = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
FIN    = re.compile(r'[.!?…:«—–"\"]')
ROMAIN = re.compile(r"^[IVXLCDM]+$")

PRON_SUFFIX = re.compile(r"-(moi|toi|lui|nous|vous|le|la|les|leur|y|en|il|elle|ils|elles|on|ce|je|tu|t-il|t-elle|t-on)$", re.I)
DEMONYM     = re.compile(r"(ien|ienne|iens|iennes)$", re.I)
STOP        = {"royaumes", "royaume"}

TITRES     = set("m mme mlle dr docteur professeur maire sire empereur seigneur monsieur dame madame mademoiselle commandant capitaine colonel general roi reine prince princesse lord lady sir commodore marchand ambassadeur conseiller consul pere maitre maitres".split())
ARTICLES   = set("le la l les un une du des au aux ce cette ces".split())
PLACE_PREP = set("sur vers dans depuis".split())
PLACE_NOUN = set("planete monde systeme royaume ville capitale province secteur".split())

FICHIER_CORPUS = r"C:\Users\zix\Desktop\m1 ia\AMS\entite.txt"
FICHIERS_NGRAMMES = [
    r"C:\Users\zix\Desktop\m1 ia\AMS\entite.txt",
    r"C:\Users\zix\Desktop\m1 ia\AMS\ngramme\n2_gramme_.txt",
    r"C:\Users\zix\Desktop\m1 ia\AMS\ngramme\n3_gramme_.txt",
    r"C:\Users\zix\Desktop\m1 ia\AMS\ngramme\n4_gramme_.txt",
]
