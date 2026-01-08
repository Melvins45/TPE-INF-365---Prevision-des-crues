# Étude Approfondie : Forêt Aléatoire (Random Forest)

Le modèle de **Forêt Aléatoire** est l'algorithme pilier de ce projet de prévision des crues. Il appartient à la famille des méthodes d'ensemble, spécifiquement le **Bagging**.

---

## 1. Concepts Found : Notions Clés

### 1.1 Qu'est-ce qu'un Arbre de Décision ?
Un arbre de décision est une structure de données qui fragmente le dataset en groupes de plus en plus petits basés sur des tests de variables. Chaque "nœud" pose une question binaire (ex: "La déforestation est-elle > 5 ?"). 
- **Problème** : Un seul arbre est instable et souffre de **Haute Variance** (il change radicalement si les données changent un peu).

### 1.2 Le Remède : Random Forest
La Forêt Aléatoire résout ce problème en créant des centaines d'arbres indépendants.
- **Bootstrap Sampling** : Chaque arbre n'est entraîné que sur une partie aléatoire des données (tirage avec remise).
- **Random Feature Selection** : À chaque nœud, l'arbre ne peut choisir la question qu'entre un nombre limité de variables choisies au hasard. Cela évite qu'un facteur dominant (comme la Mousson) ne masque les autres.

### 1.3 Agrégation (Averaging)
La prédiction finale du Random Forest est la moyenne arithmétique des prédictions de tous ses arbres. Cela permet d'annuler les erreurs individuelles de chaque arbre.

---

## 2. Analyse Technique du Projet

### 2.1 Hyperparamètres Utilisés
Dans notre code [app_prediction_gui.py](app_prediction_gui.py) :
- `n_estimators=50` : Le modèle construit 50 arbres de décision. C'est un équilibre entre précision et vitesse de calcul.
- `random_state=42` : Garantit que les résultats sont reproductibles à chaque lancement.
- `n_jobs=-1` : Utilise tous les cœurs du processeur pour accélérer l'entraînement parallélisé.

### 2.2 Analyse d'Importance (Feature Importance)
L'algorithme calcule l'importance de chaque variable en mesurant combien la pureté des nœuds augmente grâce à cette variable.
- **Signification** : Cela permet à notre application d'expliquer à l'utilisateur quels sont les 3 facteurs réels qui augmentent sa probabilité d'inondation.

---

## 3. Performance et Métriques

### 3.1 Précision Globale
- **R² Score** : ~0.85 (85%). Cela signifie que 85% de la variance de la probabilité d'inondation est expliquée par les 20 facteurs environnementaux saisis.
- **Robustesse** : Ce modèle supporte très bien les données bruitées et les relations non-linéaires entre les paramètres.

---

## 4. Conclusion
Le Random Forest est idéal pour les inondations car les catastrophes naturelles ne sont jamais le fruit d'un seul facteur, mais d'une combinaison complexe de conditions. La structure en "forêt" capture parfaitement ces interactions complexes.
