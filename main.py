import json
from ressources import charger_interdits, charger_verbes
from corpus import indexer_corpus
from candidats import extraire_candidats
from classification import classer_candidat
from alias import regrouper_alias
from normalisation import norm

def main():
    interdits = charger_interdits()
    verbes    = charger_verbes()
    mots, debut, pos, propres = indexer_corpus()

    personnages, lieux = [], []
    for nom in extraire_candidats(interdits, propres):
        mil, pe, li, ar = classer_candidat(nom, mots, debut, pos, verbes)
        seuil = 1 if len(nom) >= 2 else 2
        if mil < seuil or ar / max(mil, 1) >= 0.30: continue
        if li >= 1 and li * 2 >= pe:               lieux.append(nom)
        elif pe >= seuil and pe > li:               personnages.append(nom)
        elif len(nom) == 1 and li == 0 and norm(nom[0]) in propres: personnages.append(nom)

    noms, al, canon = regrouper_alias(personnages)
    j = " ".join
    open("LP.txt", "w", encoding="utf-8").write("\n".join(sorted(j(n) for n in noms if canon[n] == n)))
    open("LL.txt", "w", encoding="utf-8").write("\n".join(sorted(j(n) for n in lieux)))
    json.dump(al, open("aliases.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(sum(1 for n in noms if canon[n] == n), "personnes,", len(al), "avec alias,", len(lieux), "lieux")

if __name__ == "__main__":
    main()