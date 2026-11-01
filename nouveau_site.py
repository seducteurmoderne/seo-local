#!/usr/bin/env python3
"""Crée le dossier d'un nouveau site à partir de modele-site/.

  python3 nouveau_site.py "NOM DU DOSSIER" domaine.be

Le dossier est créé dans sites/, branché sur le moteur commun.
Rien n'est envoyé à WordPress : la suite est dans <dossier>/setup/DEMARRAGE.md.
"""
import os, re, sys, shutil

ICI = os.path.dirname(os.path.abspath(__file__))
MODELE = os.path.join(ICI, "modele-site")
TEXTES = (".md", ".json", ".txt", ".csv", ".exemple", ".php")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    nom, domaine = sys.argv[1].strip(), sys.argv[2].strip().lower()
    domaine = re.sub(r"^https?://", "", domaine).strip("/")
    if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", domaine):
        sys.exit(f"Domaine invalide : {domaine}")
    dest = os.path.join(ICI, "sites", nom)
    if os.path.exists(dest):
        sys.exit(f"Le dossier existe déjà : {dest}")
    shutil.copytree(MODELE, dest)
    valeurs = {
        "{{DOMAINE}}": domaine,
        "{{DOSSIER_SITE}}": dest,
        "{{SLUG_SITE}}": re.sub(r"[^a-z0-9]+", "-", domaine.rsplit(".", 1)[0]).strip("-"),
        "{{CHEMIN_MOTEUR}}": os.path.relpath(os.path.join(ICI, "moteur"), dest),
    }
    for racine, _, fichiers in os.walk(dest):
        for f in fichiers:
            p = os.path.join(racine, f)
            if not f.endswith(TEXTES):
                continue
            t = open(p, encoding="utf-8").read()
            for k, v in valeurs.items():
                t = t.replace(k, v)
            open(p, "w", encoding="utf-8").write(t)
    print(f"✔ Site créé : {dest}")
    print(f"  Tâche planifiée à créer : pilote-{valeurs['{{SLUG_SITE}}']} (modèle : {os.path.join(ICI, 'tache-planifiee.md')})")
    print(f"  Étapes suivantes : {os.path.join(dest, 'setup', 'DEMARRAGE.md')}")


if __name__ == "__main__":
    main()
