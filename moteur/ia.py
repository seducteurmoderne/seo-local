"""Appels à l'IA du moteur de brief.

Cascade : 1) Claude Code en mode non interactif (`claude -p`, l'abonnement du propriétaire) ;
2) sinon, la question est posée à l'agent qui exécute le moteur : elle est écrite dans
   briefs/<slug>/<étape>.prompt.md, l'agent écrit sa réponse JSON dans <étape>.json et relance.
Une réponse déjà obtenue n'est jamais redemandée (reprise après interruption).
"""
import os, re, json, subprocess


class IAIndisponible(Exception):
    pass


def extraire_json(texte):
    """Le premier objet JSON complet d'une réponse (avec ou sans bloc ```json)."""
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", texte, re.S)
    brut = m.group(1) if m else texte[texte.find("{"):texte.rfind("}") + 1]
    return json.loads(brut)


def demander(prompt, etape, dossier, timeout=600):
    reponse = os.path.join(dossier, f"{etape}.json")
    if os.path.exists(reponse):
        return json.load(open(reponse, encoding="utf-8"))
    erreur = ""
    try:
        r = subprocess.run(["claude", "-p", "--output-format", "json", "--max-turns", "1"], input=prompt,
                           capture_output=True, text=True, timeout=timeout, cwd=dossier)
        d = json.loads(r.stdout or "{}")
        if d.get("is_error") or not d.get("result"):
            erreur = d.get("result") or r.stderr[:200] or "réponse vide"
        else:
            data = extraire_json(d["result"])
            json.dump(data, open(reponse, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            return data
    except FileNotFoundError:
        erreur = "commande `claude` introuvable"
    except Exception as e:
        erreur = str(e)[:200]
    chemin = os.path.join(dossier, f"{etape}.prompt.md")
    open(chemin, "w", encoding="utf-8").write(prompt)
    raise IAIndisponible(f"IA non joignable ({erreur}). Réponds toi-même à {os.path.relpath(chemin)} "
                         f"en JSON dans {os.path.relpath(reponse)}, puis relance la même commande.")
