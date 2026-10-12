from config import MOT, FIN, ROMAIN, PRON_SUFFIX, DEMONYM, STOP, TITRES, FICHIERS_NGRAMMES
from normalisation import norm

def bad_token(t, interdits, propres):
    """Vérifie si un token est invalide (mot interdit, pronom, adjectif...)."""
    if not t[0].isupper() or len(t) < 2 or ROMAIN.match(t) or PRON_SUFFIX.search(t):
        return True
    n = norm(t)
    if n in STOP or (DEMONYM.search(n) and len(t) > 6):
        return True
    if n in propres:
        return False
    parts = t.split("-")
    return n in interdits or (len(parts) > 1 and any(norm(p) in interdits for p in parts))

def extraire_candidats(interdits, propres):
    cands = set()

    for fic in FICHIERS_NGRAMMES:
        try:
            for ligne in open(fic, encoding="utf-8"):
                suite = []
                prev_end = 0

                for m in MOT.finditer(ligne):
                    gap = ligne[prev_end:m.start()]
                    # Si une ponctuation sépare deux mots, on coupe la suite
                    if suite and FIN.search(gap):
                        _ajouter(suite, cands, interdits, propres)
                        suite = []

                    t = m.group()
                    n = norm(t)
                    # Accepte le token s'il est capitalisé et valide (ou titre/article initial)
                    if t[0].isupper() and (n in TITRES or (len(suite) == 0 and n in {"le", "la"}) or not bad_token(t, interdits, propres)):
                        suite.append(t)
                    else:
                        if suite:
                            _ajouter(suite, cands, interdits, propres)
                            suite = []
                    prev_end = m.end()

                if suite:
                    _ajouter(suite, cands, interdits, propres)
        except FileNotFoundError:
            pass

    return cands

def _ajouter(suite, cands, interdits, propres):
    # Ajouter la forme complète (ex: ("Le", "Mulet"), ("Dame", "Callia"))
    cands.add(tuple(suite))
    # Ajouter aussi la forme sans titre/article initial (ex: ("Mulet",), ("Callia",))
    sans = list(suite)
    while sans and (norm(sans[0]) in TITRES or norm(sans[0]) in {"le", "la"}):
        sans = sans[1:]
    if sans and not any(bad_token(t, interdits, propres) for t in sans):
        cands.add(tuple(sans))
