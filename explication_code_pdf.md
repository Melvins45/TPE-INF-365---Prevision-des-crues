# Explication du Code : Lecteur de Documents PDF

Le fichier `extract_pdf_info.py` est un outil utilitaire pour lire les rapports de projet.

---

## 1. Analyse des Fichiers PDF

```python
from pypdf import PdfReader

pdf_files = [
    "TPE INF 365... Cahier de charges.pdf",
    "TPE INF 365... Etat d'avancement.pdf"
]
```
**Explication :**
On définit une liste contenant les noms des documents officiels du projet (Cahier de charges et État d'avancement).

---

## 2. Extraction Automatisée du Texte

```python
reader = PdfReader(pdf_file)
for i in range(min(3, len(reader.pages))):
    page = reader.pages[i]
    text = page.extract_text()
    print(text)
```
**Explication :**
Pour chaque fichier, le script :
1. Ouvre le document avec `PdfReader`.
2. Parcourt les 3 premières pages (qui contiennent généralement les infos cruciales comme les membres du groupe ou les objectifs).
3. Extrait le texte brut et l'affiche dans la console. 

Cet outil permet de vérifier rapidement le contenu des livrables PDF sans avoir à les ouvrir manuellement.
