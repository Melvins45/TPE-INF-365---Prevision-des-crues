# Explication du Code : Générateur de Présentation

Le fichier `generate_ppt.py` automatise la création du support de soutenance.

---

## 1. Initialisation de la Présentation

```python
from pptx import Presentation
prs = Presentation()
```
**Explication :**
On importe la bibliothèque `python-pptx` qui permet de créer des fichiers `.pptx` programmables. On initialise un objet `prs` qui représente notre futur diaporama.

---

## 2. Diapositives de Titre et de Groupe

```python
slide_layout = prs.slide_layouts[0] # Mise en page Titre
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
title.text = "Prévision des Crues"
subtitle.text = "Projet TPE INF 365 - Groupe 24..."
```
**Explication :**
Cette partie crée la première page. Elle utilise les informations du groupe 24, incluant les noms des 5 membres et le nom de l'examinateur (Dr Justin MOSKOLAI).

---

## 3. Synthèse de la Méthodologie

```python
content.text = (
    "1. Préparation des données :\n"
    "   - Nettoyage : Traitement des valeurs manquantes.\n"
    "   - Normalisation : StandardScaler.\n"
    "2. Modélisation : Regression, RF, NN."
)
```
**Explication :**
Le script remplit automatiquement les diapositives avec les étapes clés que nous avons suivies. Cela évite les erreurs de saisie manuelle et garantit que la méthodologie présentée correspond exactement au code.

---

## 4. Résultats et Conclusion

```python
prs.save('presentation_projet.pptx')
```
**Explication :**
Après avoir créé une dizaine de diapositives détaillant chaque modèle (Régression, Forêt Aléatoire, Deep Learning), le script enregistre le fichier final. Ce diaporama est prêt à être projeté devant le jury.
