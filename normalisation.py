import unicodedata

def norm(texte):
    """Minuscules et sans accents (ex: 'État' -> 'etat')."""
    s = unicodedata.normalize("NFD", texte.lower().replace("’", "'"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")
