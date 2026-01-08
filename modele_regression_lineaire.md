# Étude Approfondie : Régression Linéaire Multi-variée

La **Régression Linéaire** est le modèle mathématique fondamental utilisé comme "Baseline" (référence de base) dans ce projet. Bien que moins puissante que le Random Forest, elle offre une transparence totale.

---

## 1. Concepts Found : Notions Clés

### 1.1 L'Équation Linéaire
Le modèle part du postulat que la probabilité d'inondation ($y$) est une somme pondérée des variables d'entrée ($x$).
- **Équation** : $$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_{20} x_{20} + \epsilon$$
  - $\beta_0$ : L'ordonnée à l'origine (biais).
  - $\beta_i$ : Les coefficients (poids) de chaque variable.
  - $\epsilon$ : L'erreur résiduelle.

### 1.2 La Méthode des Moindres Carrés (OLS)
Pour trouver les meilleurs coefficients, l'algorithme utilise la méthode **Ordinary Least Squares (OLS)**. 
- **Objectif** : Minimiser la somme des carrés des erreurs. Plus la différence entre la prédiction et la réalité est petite, meilleur est le modèle.

---

## 2. Analyse du Comportement

### 2.1 Signification des Coefficients
Chaque coefficient $\beta_i$ nous indique comment la probabilité change si une variable augmente d'une unité.
- **Coefficient Positif** : Le facteur augmente le risque (ex: Intensité Mousson).
- **Coefficient Négatif** : Le facteur réduit le risque (ex: Excellent drainage).

### 2.2 Limites Stratégiques
- **Assomption de Linéarité** : Le modèle suppose que si vous doublez la déforestation, le risque double. En réalité, les inondations sont souvent le résultat d'un effet de "bascule" (non-linéaire).
- **Sensibilité aux Valeurs Extrêmes** : Les données aberrantes peuvent fortement "tirer" la ligne de régression et fausser les prédictions globalement.

---

## 3. Application au Projet

Dans notre étude comparée :
- **R² Score** : Inférieur au Random Forest (~0.80 contre 0.85).
- **Utilité** : Elle nous a permis de valider rapidement que nos 20 variables étaient bien corrélées au risque final avant d'utiliser des modèles plus complexes.

---

## 4. Conclusion
La Régression Linéaire est l'outil parfait pour comprendre la tendance globale. Elle confirme que chaque paramètre environnemental choisi pour ce TPE a un impact direct et quantifiable sur la sécurité des populations.
