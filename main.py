import json
from ressources import charger_interdits, charger_verbes
from corpus import indexer_corpus
from candidats import extraire_candidats
from classification import classer_candidat
from alias import regrouper_alias
from normalisation import norm

def main():
    print("1. Chargement des ressources (antidictio.txt, verbs.json)...")
    interdits = charger_interdits()
    verbes    = charger_verbes()

    print("2. Indexation du corpus...")
    mots, debut, pos, propres = indexer_corpus()

    print("3. Extraction des candidats...")
    candidats = extraire_candidats(interdits, propres)

    personnages = []
    lieux       = []

    print("4. Classification...")
    for nom in candidats:
        mil, pe, li, ar = classer_candidat(nom, mots, debut, pos, verbes)

        seuil = 1 if len(nom) >= 2 else 2
        if mil < seuil:
            continue

        # Filtre d'articles : ne pas rejeter si le nom a des indices de personne et aucun de lieu (ex: Mulet)
        if ar / max(mil, 1) >= 0.30 and not (pe >= 1 and li == 0):
            continue

        # Décision Lieu vs Personne
        if li >= 1 and li * 2 >= pe:
            lieux.append(nom)
        elif pe >= seuil and pe > li:
            personnages.append(nom)
        elif len(nom) == 1 and li == 0 and norm(nom[0]) in propres:
            personnages.append(nom)

    print("5. Regroupement des alias...")
    noms, al, canon = regrouper_alias(personnages)

    # 6. Écriture des résultats
    j = " ".join
    pers_lignes = "\n".join(sorted(j(n) for n in noms if canon[n] == n))
    lieu_lignes = "\n".join(sorted(j(n) for n in lieux))

    # Écriture dans le dossier courant et à la racine
    for dossier in ["", r"C:\Users\zix\Desktop\m1 ia\AMS\\"]:
        try:
            with open(dossier + "LP.txt", "w", encoding="utf-8") as f:
                f.write(pers_lignes)
            with open(dossier + "LL.txt", "w", encoding="utf-8") as f:
                f.write(lieu_lignes)
            with open(dossier + "aliases.json", "w", encoding="utf-8") as f:
                json.dump(al, f, ensure_ascii=False, indent=1)
        except Exception:
            pass

    print(f"Terminé : {sum(1 for n in noms if canon[n] == n)} personnes, {len(al)} avec alias, {len(lieux)} lieux")

if __name__ == "__main__":
    main()