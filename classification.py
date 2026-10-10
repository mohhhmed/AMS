from config import ARTICLES, PREP, NLIEU, TITRES
from normalisation import norm

def classer_candidat(nom, mots, debut, pos, verbes):
    k, N = len(nom), len(mots)
    milieu = pers = lieu = art = 0
    for i in pos.get(nom[0], []):
        if tuple(mots[i:i+k]) != nom or debut[i]: continue
        milieu += 1
        pv = norm(mots[i-1]) if i > 0 else ""
        p2 = norm(mots[i-2]) if i > 1 and not debut[i-1] else ""
        nx = norm(mots[i+k]) if i+k < N and not debut[i+k] else ""
        if pv in ARTICLES: art += 1
        if pv in PREP or p2 in NLIEU: lieu += 1
        elif pv in TITRES or pv in verbes or nx in verbes: pers += 1
    return milieu, pers, lieu, art
