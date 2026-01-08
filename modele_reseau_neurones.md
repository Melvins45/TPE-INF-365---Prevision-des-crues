# Deep Learning : Réseau de Neurones Artificiels (ANN)

Le modèle **Sequential** est l'approche la plus complexe testée pour cette prévision des crues. Il s'agit d'un neurone artificiel basé sur la bibliothèque **Keras/TensorFlow**.

---

## 1. Notions Fondamentales : Concepts Found

### 1.1 L'Architecture Séquentielle
Le terme "Sequential" signifie que les données circulent dans un seul sens, d'une couche à l'autre.
- **Couche d'Entrée (Input Layer)** : Reçoit les 20 variables préparées (Standardisées).
- **Couches Cachées (Hidden Layers)** : Les couches "Denses" où chaque neurone est connecté à tous les neurones de la couche précédente. C'est ici que l'intelligence se forme.
- **Couche de Sortie (Output Layer)** : Produit la valeur numérique finale du risque.

### 1.2 La Fonction d'Activation (ReLU)
Nous utilisons **ReLU** (Rectified Linear Unit) dans les couches cachées.
- **Formule** : $f(x) = \max(0, x)$
- **Rôle** : Elle permet au réseau d'apprendre des relations "non-linéaires". Sans elle, le réseau se comporterait comme une simple régression linéaire, peu importe le nombre de couches.

---

## 2. Processus d'Entraînement : Les Étapes

### 2.1 La Propagation Avant (Forward Propagation)
Les données entrent, sont multipliées par des **poids** ($w$) et additionnées à un **biais** ($b$). Le résultat passe par ReLU et continue son chemin jusqu'à la sortie.

### 2.2 La Fonction de Perte (Loss Function : MSE)
Le modèle mesure son erreur à l'aide de la **Mean Squared Error** (MSE). Plus le modèle se trompe, plus ce score est élevé.
- **Formule** : $MSE = \frac{1}{n} \sum (y_{reel} - y_{pred})^2$

### 2.3 L'Optimiseur (Adam)
C'est le "cerveau" de l'apprentissage. Il utilise la **Descente de Gradient** pour ajuster les poids à chaque erreur détectée. L'optimiseur "Adam" est choisi pour sa vitesse et sa capacité à ne pas rester bloqué dans des erreurs locales.

---

## 3. Paramètres de l'Étude
- **Batch Size** : Le nombre d'exemples traités avant de mettre à jour les poids.
- **Epochs** : Le nombre de fois que le modèle parcourt l'intégralité du dataset. Un nombre trop élevé mène à l'**Overfitting** (le modèle apprend par cœur au lieu de comprendre).

---

## 4. Conclusion
Le Réseau de Neurones est capable de détecter des interactions extrêmement subtiles entre les variables (ex: l'effet combiné d'une déforestation massive et d'une urbanisation rapide). C'est le modèle de pointe de ce projet TPE.
