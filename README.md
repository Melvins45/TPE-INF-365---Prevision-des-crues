# Système Intelligent de Prévision des Crues (TPE INF 365)
**Projet Académique - Groupe 24**

## 🌊 Vue d'ensemble du Projet
Ce système utilise le **Machine Learning** de pointe pour quantifier le risque d'inondation à partir de 20 paramètres critiques. Il a été conçu comme une solution d'aide à la décision pour les autorités de protection civile et les urbanistes, permettant une anticipation proactive des catastrophes climatiques.

### 🎯 Objectifs de ce Travail
1.  **Modélisation Prédictive** : Comparer et optimiser des algorithmes de régression (Linéaire, Forêt Aléatoire, Réseaux de Neurones).
2.  **Analyse d'Impact** : Identifier les facteurs sociétaux (déforestation, urbanisation) et météorologiques aggravant le risque.
3.  **Interface Intuitive** : Offrir un outil de simulation interactive pour le grand public et les experts.

---

## 📊 Données et Méthodologie

### Le Dataset
- **Localisation** : [datas/flood.csv](datas/flood.csv)
- **Volume** : Plus de 50 000 exemples d'inondations historiques.
- **Paramètres (20)** : Incluant l'intensité de la mousson, la qualité des infrastructures, la déforestation, et la stabilité politique.

### Les Modèles Implémentés
1.  **Forêt Aléatoire (Random Forest)** : Notre modèle le plus performant, capable de capturer des interactions non-linéaires complexes. (Voir [modeleForetAleatoire.ipynb](modeleForetAleatoire.ipynb)).
2.  **Régression Linéaire** : Modèle de référence pour sa simplicité et sa transparence. (Voir [modeleRegressionLineaire.ipynb](modeleRegressionLineaire.ipynb)).
3.  **Réseaux de Neurones (MLP)** : Utilisation de Keras/TensorFlow pour explorer les relations profondes. (Voir [modeleReseauNeuronesSequential.ipynb](modeleReseauNeuronesSequential.ipynb)).

---

## 🖥️ Logiciel de Prédiction (GUI)

L'application principale est [app_prediction_gui.py](app_prediction_gui.py). Elle permet une interaction directe avec le modèle Random Forest entraîné.

### Fonctionnalités Clés :
-   **Interface Responsive** : Le design s'adapte automatiquement à la taille de votre écran (grille dynamique).
-   **Synchronisation en Temps Réel** : Les curseurs (Scales) et les zones de texte sont liés pour une saisie rapide et précise.
-   **Analyse d'Importance** : Lors de chaque clic sur "Prédire", le logiciel isole les 3 facteurs qui ont le plus contribué au risque calculé.
-   **Résultats Scrollables** : Un rapport de risque détaillé avec recommandations de sécurité.

---

## 🚀 Installation et Démarrage

### 1. Installation des dépendances
Assurez-vous d'avoir Python 3.8+ installé, puis lancez :
```bash
pip install -r requirements.txt
```

### 2. Lancer l'Application
```bash
python app_prediction_gui.py
```

---

## 📂 Organisation du Workspace

-   **Logiciel Principal** : [app_prediction_gui.py](app_prediction_gui.py) (Version finale épurée de commentaires).
-   **Documentation Fondamentale** : [documentation_code.md](documentation_code.md) (Explications exhaustives de toutes les notions ML et techniques).
-   **Validation Scientifique** : [validation_croisee.py](validation_croisee.py) et [validation_croisee_details.md](validation_croisee_details.md).
-   **Modèles Sauvegardés** : Le dossier `models/` contient les fichiers `.joblib` pour un chargement instantané sans ré-entraînement.

---

## 📜 Licence & Crédits
Ce projet a été réalisé dans le cadre du cours **INF 365 - Intelligence Artificielle et Systèmes Complexes** par le **Groupe 24**.

- **Responsable IA** : [Votre Nom]
- **Ingénierie Logicielle** : [Votre Nom]
- **Dataset Analysis** : [Votre Nom]

---
*Fin du document README.*

```python
import pandas as pd
df = pd.read_csv("datas/flood.csv")
df.head()
df.info()
```

**Concepts clés** :
- **DataFrame** : Structure de données tabulaire (lignes et colonnes)
- **Exploration** : Comprendre la structure, les types de données, et les statistiques descriptives

### 2️⃣ Nettoyage des Données

**Objectif** : Assurer la qualité des données pour un apprentissage efficace.

#### ✅ Vérification des valeurs manquantes
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.show()
```
- Les valeurs manquantes peuvent biaiser le modèle.
- Dans notre cas, pas de valeurs manquantes détectées.

#### ✅ Détection des doublons
```python
print("Nombre de lignes dupliquées:", df.duplicated().sum())
```
- Les doublons réduisent la diversité de l'apprentissage.

#### ✅ Gestion des Outliers (Valeurs Aberrantes)

**Concept** : Un outlier est une valeur extrêmement différente des autres.

**Méthode IQR (Interquartile Range)** :
```python
for col in num_cols:
    Q1 = df[col].quantile(0.25)  # 1er quartile (25%)
    Q3 = df[col].quantile(0.75)  # 3e quartile (75%)
    IQR = Q3 - Q1                # Écart interquartile
    lower = Q1 - 1.5 * IQR       # Limite inférieure
    upper = Q3 + 1.5 * IQR       # Limite supérieure
    
    # Plafonner les valeurs hors limites
    df[col] = df[col].clip(lower, upper)
```

**Pourquoi** :
- Les outliers peuvent avoir un impact disproportionné sur les modèles.
- Exemple : Une intensité de mousson à 1000 (impossible) vs normale à 10.

#### ✅ Analyse de Corrélation
```python
import seaborn as sns
sns.heatmap(df.corr(), cmap="coolwarm", center=0)
plt.show()
```

**Concept** : La **corrélation** mesure la relation linéaire entre deux variables.
- **Corrélation positive** : Quand une augmente, l'autre augmente aussi.
- **Corrélation négative** : Quand une augmente, l'autre diminue.
- **Corrélation = 0** : Pas de relation linéaire.

---

### 3️⃣ Préparation des Données pour le Machine Learning

#### ✅ Séparation Train/Test
```python
from sklearn.model_selection import train_test_split

X = df.drop("FloodProbability", axis=1)  # Features (entrées)
y = df["FloodProbability"]               # Target (sortie)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

**Ratio 80/20** :
- **80%** des données pour **entraîner** le modèle.
- **20%** des données pour **tester** le modèle (données non vues pendant l'apprentissage).

**Pourquoi `random_state=42`** :
- Garantit la **reproductibilité** des résultats.

#### ✅ Normalisation (Scaling)
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Concept** : La normalisation met toutes les variables à la même échelle.

**Formule** : $X_{scaled} = \frac{X - \mu}{\sigma}$
- $\mu$ = moyenne
- $\sigma$ = écart-type

**Pourquoi** :
- Certaines variables (ex: Population) peuvent avoir des valeurs beaucoup plus grandes que d'autres (ex: Intensité).
- Cela peut biaiser les modèles, particulièrement ceux basés sur la distance (comme KNN) et les réseaux de neurones.

---

## 🤖 Les Trois Modèles

### Modèle 1 : Régression Linéaire

**Fichier** : `modeleRegressionLineaire.ipynb`

**Concept** : 
Suppose une relation **linéaire** entre les features et la cible.

**Formule** : $y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n$

**Avantages** :
✅ Simple et rapide à entraîner  
✅ Facile à interpréter  
✅ Bon baseline pour comparer d'autres modèles  

**Inconvénients** :
❌ Suppose une relation linéaire (souvent peu réaliste)  
❌ Sensible aux outliers  
❌ Performance faible sur les données complexes  

**Code clé** :
```python
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred = lr.predict(X_test_scaled)
```

**Résultats attendus** :
- Performance modérée sur ce dataset complexe.
- Dispersion importante des prédictions autour de la ligne parfaite.

---

### Modèle 2 : Forêt Aléatoire (Random Forest)

**Fichier** : `modeleForetAleatoire.ipynb`

**Concept** : 
Ensemble de **100 arbres de décision** qui votent ensemble pour la prédiction.

**Analogie** : 
Si vous demandez à 100 experts independants leur opinion et prenez la moyenne, vous aurez une meilleure prédiction qu'un seul expert.

**Fonctionnement** :
1. Chaque arbre apprend une partie différente des données.
2. Chaque arbre fait une prédiction.
3. La prédiction finale = **moyenne** de toutes les prédictions.

**Avantages** :
✅ Gère bien les **relations non-linéaires**  
✅ Robuste contre les **overfitting** (surapprentissage)  
✅ Pas besoin de normaliser les données  
✅ Capture les interactions complexes entre variables  

**Inconvénients** :
❌ Plus lent à entraîner que la régression linéaire  
❌ Moins interprétable (boîte noire)  
❌ Peut être gourmand en mémoire  

**Code clé** :
```python
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred = rf.predict(X_test_scaled)
```

**Résultats attendus** :
- Meilleure performance que la régression linéaire.
- Points plus serrés autour de la ligne parfaite.
- MSE significativement plus bas.

---

### Modèle 3 : Réseau de Neurones (Deep Learning)

**Fichier** : `modeleReseauNeuronesSequential.ipynb`

**Concept** : 
Un réseau de **neurones artificiels** organisés en couches, inspiré par le cerveau humain.

**Architecture du modèle** :
```
Input (20 features) → Dense(64, ReLU) → Dense(32, ReLU) → Dense(1, Linear) → Output
```

**Explication** :
- **Input** : 20 caractéristiques environnementales
- **Dense(64, ReLU)** : Première couche cachée avec 64 neurones, activation ReLU
  - **ReLU** (Rectified Linear Unit) : Active le neurone si entrée > 0, sinon 0
  - Permet au réseau d'apprendre des relations non-linéaires
- **Dense(32, ReLU)** : Deuxième couche cachée avec 32 neurones
- **Dense(1, Linear)** : Couche de sortie avec 1 neurone et activation linéaire
  - Génère une prédiction continue entre 0 et 1

**Entraînement** :
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(64, activation='relu', input_shape=(20,)),
    Dense(32, activation='relu'),
    Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train_scaled, y_train, epochs=10, validation_data=(X_test_scaled, y_test))
```

**Concepts clés** :
- **Optimizer (Adam)** : Algorithme pour ajuster les poids du réseau
- **Loss (MSE)** : Erreur quadratique moyenne - mesure l'écart entre prédictions et réalité
- **Epochs** : Nombre de fois où on passe les données dans le réseau

**Avantages** :
✅ Peut apprendre des **relations très complexes**  
✅ Excellent potentiel de performance  
✅ Flexible et adaptable  

**Inconvénients** :
❌ Nécessite **beaucoup de données** (nous avons 50k ✅)  
❌ Requiert du **tuning** (ajustement des hyperparamètres)  
❌ Temps d'entraînement plus long  
❌ Moins interprétable (boîte noire)  
❌ Risque d'overfitting  

**Résultats attendus** :
- Meilleures performances globales.
- Points très proches de la ligne parfaite.
- MSE très faible.

---

## 📈 Validation Croisée (Cross-Validation)

**Fichier** : `validation_croisee.py`

### Pourquoi la Validation Croisée ?

Imaginez que vous testez un modèle sur une seule partition de test. Vous pourriez avoir de la **malchance** :
- Cette partition contient des données faciles à prédire → Performance gonflée.
- Cette partition contient des données difficiles → Performance sous-estimée.

**Solution** : Faire plusieurs tests avec différentes partitions et faire la moyenne.

### Méthode K-Fold

```python
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    # Entraîner et tester le modèle
```

**Processus (5-Fold)** :

1. **Fold 1** : Test sur 20%, Entraînement sur les 80% restants
2. **Fold 2** : Test sur les 20% suivants, Entraînement sur les 80% restants
3. **Fold 3** : ...
4. **Fold 4** : ...
5. **Fold 5** : ...

**Résultat final** = **Moyenne** des 5 scores de performance

### Métriques d'Évaluation

#### 1️⃣ **Mean Squared Error (MSE)**
$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_{true,i} - y_{pred,i})^2$$

- Mesure l'écart moyen (au carré) entre les prédictions et la réalité.
- **Valeur basse = bon modèle**
- Les erreurs importantes sont pénalisées fortement (au carré)

#### 2️⃣ **R² Score (Coefficient de Détermination)**
$$R^2 = 1 - \frac{\sum (y_{true} - y_{pred})^2}{\sum (y_{true} - \bar{y})^2}$$

- Mesure le pourcentage de variance expliquée par le modèle.
- **Plage** : 0 à 1 (et peut être négatif pour très mauvais modèles)
- **R² = 1** : Prédictions parfaites
- **R² = 0** : Le modèle n'est pas meilleur qu'une prédiction moyenne
- **R² < 0** : Le modèle est pire qu'une simple moyenne

### Résultats Attendus de la Validation Croisée

```
Linear Regression:
  - MSE moyen : ~0.005
  - R² moyen : ~0.85

Random Forest:
  - MSE moyen : ~0.001
  - R² moyen : ~0.95

Neural Network:
  - MSE moyen : ~0.0005
  - R² moyen : ~0.98
```

---

## 🚀 Comment Exécuter le Projet

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Exécuter les modèles individuels (Notebooks Jupyter)
```bash
# Ouvrir les notebooks dans Jupyter
jupyter notebook modeleRegressionLineaire.ipynb
jupyter notebook modeleForetAleatoire.ipynb
jupyter notebook modeleReseauNeuronesSequential.ipynb
```

### 3. Exécuter la validation croisée
```bash
python validation_croisee.py
```
Génère un fichier `cv_results.json` avec les scores de chaque modèle.

### 4. Générer la présentation
```bash
python generate_ppt.py
```
Crée `presentation_projet.pptx` avec les explications et emplacements pour les graphiques.

---

## 📁 Structure du Projet

```
TPE INF 365 - Prevision des crues/
├── datas/
│   └── flood.csv                          # Dataset (50k exemples)
├── modeleRegressionLineaire.ipynb         # Régression linéaire
├── modeleForetAleatoire.ipynb             # Forêt aléatoire
├── modeleReseauNeuronesSequential.ipynb   # Réseau de neurones
├── validation_croisee.py                  # Script de validation croisée
├── generate_ppt.py                        # Générateur de présentation
├── create_theme.py                        # Créateur de thème
├── extract_pdf_info.py                    # Extracteur d'infos PDF
├── requirements.txt                       # Dépendances Python
├── README.md                              # Ce fichier
├── presentation_projet.pptx               # Présentation finale
└── cv_results.json                        # Résultats de validation croisée
```

---

## 📚 Concepts Clés à Retenir

| Concept | Définition |
|---------|-----------|
| **Feature** | Variable d'entrée (ex: intensité de mousson) |
| **Target** | Variable de sortie à prédire (FloodProbability) |
| **Outlier** | Valeur anormalement éloignée des autres |
| **Normalisation** | Mise à l'échelle des variables |
| **Overfitting** | Modèle qui mémorise au lieu d'apprendre |
| **Validation Croisée** | Technique de test robuste avec plusieurs partitions |
| **MSE** | Erreur quadratique moyenne |
| **R²** | Pourcentage de variance expliquée |

---

## 🎓 Apprentissages du Projet

1. **Importance de la préparation** : 80% du temps en data science va à la préparation des données
2. **Comparaison de modèles** : Pas d'algorithme unique meilleur pour tous les cas
3. **Validation robuste** : La validation croisée donne une estimation plus fiable de la performance
4. **Trade-offs** : Complexité vs Interprétabilité vs Temps d'entraînement
5. **Normalisation** : Cruciale pour les modèles basés sur la distance et réseaux de neurones

---

## 👥 Membres du Groupe 24

- **NITOPOP JEATSA GUILLAUME MELVIN** (CHEF) - 20S43003
- **DEMANOU KEMKENG DILAN** - 25S03516
- **NOSSI YIMGO LYNDSEY SULIVANE** - 23S87713
- **TCHIEUTCHOUA FOTEPING ASHLEY MEGANE** - 23S87863
- **WANGA POUYA KAVEN SAMIRA** - 23S88070

**Examinateur** : Dr Justin MOSKOLAI  
**Université** : Université de Douala - Faculté des Sciences

---

## 📞 Questions et Clarifications

Pour toute question sur le projet, consultez d'abord les notebooks individuels, puis les ressources en ligne sur scikit-learn, TensorFlow et pandas.

---

**Dernière modification** : January 2026
