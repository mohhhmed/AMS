from collections import defaultdict
from normalisation import norm

def regrouper_alias(personnages):
    """
    Associe les variantes courtes à leur forme complète :
    - 'Mulet' -> 'Le Mulet'
    - 'Callia' -> 'Dame Callia'
    - 'Seldon' -> 'Hari Seldon'
    Fusionne aussi les doublons en majuscules (ex: 'LE MULET' -> 'Le Mulet').
    """
    noms = sorted(personnages, key=len, reverse=True)
    alias = defaultdict(list)
    canon = {}

    for n in noms:
        n_norm = [norm(t) for t in n]
        parent = None

        # 1. Chercher un nom plus long qui contient tous les mots (ex: 'Mulet' dans 'Le Mulet')
        for f in canon.values():
            f_norm = [norm(t) for t in f]
            if len(f) > len(n) and all(t in f_norm for t in n_norm):
                parent = f
                break

        if parent:
            alias[" ".join(parent)].append(" ".join(n))
            canon[n] = parent
        else:
            # 2. Chercher si la même forme existe déjà avec une autre casse (ex: 'LE MULET' vs 'Le Mulet')
            meme = next((f for f in canon.values() if [norm(t) for t in f] == n_norm), None)
            if meme:
                alias[" ".join(meme)].append(" ".join(n))
                canon[n] = meme
            else:
                canon[n] = n

    return noms, alias, canon
