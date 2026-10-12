import json
from config import MOT
from normalisation import norm

AUX = set("est etait fut sera sont etaient a avait eut ont avaient etre avoir ete et ne y en".split())

def charger_interdits():
    """Charge tous les mots de l'antidictionnaire."""
    interdits = set()
    for ligne in open(r"C:\Users\zix\Desktop\m1 ia\AMS\antidictio.txt", encoding="utf-8"):
        for t in MOT.findall(ligne):
            interdits.add(norm(t))
    return interdits

def _aplatir(x):
    """Parcourt la structure JSON pour extraire chaque forme verbale."""
    if isinstance(x, str):
        w = MOT.findall(x.lower())
        if w:
            yield norm(w[-1])
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from _aplatir(k)
            yield from _aplatir(v)
    elif isinstance(x, list):
        for v in x:
            yield from _aplatir(v)

def charger_verbes():
    """Charge directement votre fichier verbs.json."""
    donnees = json.load(open(r"C:\Users\zix\Desktop\m1 ia\AMS\verbs.json", encoding="utf-8"))
    return {v for v in _aplatir(donnees) if len(v) > 2} - AUX
