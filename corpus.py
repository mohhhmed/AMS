from collections import Counter, defaultdict
from config import MOT, FIN, TITRES, FICHIER_CORPUS
from normalisation import norm

def indexer_corpus():
    texte = open(FICHIER_CORPUS, encoding="utf-8").read()
    mots, debut, fin = [], [], 0

    for m in MOT.finditer(texte):
        gap = texte[fin:m.start()]
        est_debut = (len(mots) == 0) or bool(FIN.search(gap))
        # "M. Hardin" : le point après un titre n'est pas une fin de phrase
        if mots and norm(mots[-1]) in TITRES and gap.strip() == ".":
            est_debut = False
        mots.append(m.group())
        debut.append(est_debut)
        fin = m.end()

    pos = defaultdict(list)
    for i, w in enumerate(mots):
        pos[w].append(i)

    # Noms propres statistiques : majuscule en milieu de phrase, quasi jamais en minuscule
    minus = Counter(norm(w) for w in mots if w[0].islower())
    maj   = Counter(norm(w) for w, d in zip(mots, debut) if w[0].isupper() and not d)
    propres = {n for n in maj if maj[n] >= 2 and minus[n] <= 0.1 * maj[n]}

    return mots, debut, pos, propres
