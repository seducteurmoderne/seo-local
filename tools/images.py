#!/usr/bin/env python3
"""Lanceur : exécute, sur ce site, l'outil du même nom dans le moteur commun.

Copie identique dans <site>/tools/autopilote.py et <site>/tools/images.py — ne pas modifier.
Le chemin du moteur est lu dans site.json → "moteur" (relatif au dossier du site).
"""
import os, sys, json, runpy

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["SITE_DIR"] = SITE
with open(os.path.join(SITE, "site.json"), encoding="utf-8") as f:
    MOTEUR = os.path.normpath(os.path.join(SITE, json.load(f)["moteur"]))
sys.path.insert(0, MOTEUR)
sys.argv[0] = os.path.join(MOTEUR, os.path.basename(__file__))
runpy.run_path(sys.argv[0], run_name="__main__")
