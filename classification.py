from config import ARTICLES, PLACE_PREP, PLACE_NOUN, TITRES
from normalisation import norm

def classer_candidat(nom, mots, debut, pos, verbes):
    k, N = len(nom), len(mots)
    milieu = lieu = art = 0
    # Si le nom commence par un titre (Dame, Docteur, Maire, etc.), c'est d'office une personne
    pers = 2 if norm(nom[0]) in TITRES else 0

    indices = list(pos.get(nom[0], []))
    # Si le nom commence par un article (ex: "Le Mulet"), en milieu de phrase "le" est en minuscule
    if norm(nom[0]) in {"le", "la"}:
        indices += pos.get(nom[0].lower(), [])

    c_norm = tuple(norm(w) for w in nom)
    for i in indices:
        if i + k > N:
            continue
        if tuple(norm(mots[i+j]) for j in range(k)) != c_norm or debut[i]:
            continue

        milieu += 1

        pv  = norm(mots[i-1]) if i > 0 else ""
        p2  = norm(mots[i-2]) if i > 1 and not debut[i-1] else ""
        nx  = norm(mots[i+k]) if i+k < N and not debut[i+k] else ""

        if pv in ARTICLES and norm(nom[0]) not in ARTICLES:
            art += 1

        place_ctx = (pv in PLACE_PREP or
                     p2 in PLACE_NOUN or
                     (pv in ARTICLES | {"de", "d"} and p2 in PLACE_NOUN))

        if place_ctx:
            lieu += 1
        elif pv in TITRES or pv in verbes or nx in verbes:
            pers += 1

    return milieu, pers, lieu, art
