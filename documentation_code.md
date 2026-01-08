# Documentation Technique Exhaustive : Système de Prévision des Crues (TPE INF 365)

Ce document fournit une explication détaillée et approfondie de chaque aspect technique, mathématique et algorithmique du projet. Il est conçu pour être une référence complète couvrant toutes les notions rencontrées dans le code source et le processus de modélisation.

---

## 1. Fondements de l'Apprentissage Automatique (Machine Learning)

### 1.1 Qu'est-ce que la Régression ?
Contrairement à la classification qui prédit des catégories discrètes (ex: "Inondation" ou "Pas d'inondation"), la **Régression** prédit une valeur numérique continue. Dans notre cas précis, nous cherchons à quantifier le risque, ce qui se traduit par une probabilité comprise entre **0.0 (0%)** et **1.0 (100%)**.
- **Objectif Fondamental** : Le but est de trouver une fonction mathématique $f(X)$ qui mappe les entrées environnementales à la probabilité de crue. Le modèle cherche à minimiser l'écart entre sa prédiction et la réalité historique du dataset.
- **Variables Indépendantes ($X$)** : Ce sont les 20 paramètres d'entrée, tels que l'intensité de la mousson, le niveau d'urbanisation ou la qualité des infrastructures.
- **Variable Dépendante ($y$)** : C'est la `FloodProbability`, la cible que nous tentons d'estimer.

### 1.2 Normalisation des Données (StandardScaler)
Les modèles mathématiques sont souvent biaisés par l'échelle des nombres. Par exemple, si une variable varie de 0 à 1 et une autre de 100 à 1000, l'algorithme pourrait accorder une importance disproportionnée à la seconde simplement à cause de sa magnitude.
- **Notion de Score Z (Z-Score)** : Nous utilisons le `StandardScaler` pour transformer chaque donnée afin qu'elle suive une loi normale centrée réduite (moyenne $\mu = 0$ et écart-type $\sigma = 1$).
- **Formule Mathématique** : $$z = \frac{x - \mu}{\sigma}$$
- **Utilité** : Cela garantit que chaque facteur environnemental "pèse" de manière équitable lors de la phase d'apprentissage, permettant au modèle de se concentrer sur les relations logiques plutôt que sur les échelles numériques.

### 1.3 Division des Données (Train/Test Split)
Pour évaluer l'efficacité réelle d'un modèle, il ne faut jamais le tester sur les données qu'il a déjà "vues" lors de son entraînement. C'est le principe de la **validation**.
- **Ensemble d'Entraînement (80%)** : Utilisé par l'algorithme pour ajuster ses paramètres internes et "apprendre" les schémas de crues.
- **Ensemble de Test (20%)** : Utilisé comme un examen final. Le modèle prédit les résultats pour ces données inconnues, et nous comparons ses prédictions aux valeurs réelles pour calculer son score de précision.

---

## 2. Étude du Modèle : Random Forest (Forêt Aléatoire)

### 2.1 L'Arbre de Décision (Building Block)
L'unité structurelle du Random Forest est l'arbre de décision. Il fonctionne par une cascade de tests logiques binaires. Chaque "nœud" de l'arbre pose une question sur une variable (ex: "La déforestation est-elle supérieure à 7/10 ?"). La réponse oriente vers une branche ou une autre jusqu'à atteindre une estimation finale (la "feuille").

### 2.2 Notion de Forêt et de "Bagging"
Un inconvénient majeur d'un arbre de décision unique est qu'il est sujet à l'**overfitting** (sur-apprentissage) : il apprend les bruits et les erreurs du dataset par cœur plutôt que de comprendre la logique globale. 
- **La Solution** : Au lieu d'un seul arbre, on en crée une multitude (une forêt).
- **Bagging (Bootstrap Aggregating)** : Chaque arbre est entraîné sur un sous-échantillon aléatoire des données. 
- **Sagesse de la Foule** : La prédiction finale est la **moyenne** des prédictions de tous les arbres individuels. Les erreurs commises par certains arbres sont compensées par les autres, rendant le modèle final extrêmement robuste et précis.

### 2.3 Importance des Caractéristiques (Feature Importance)
L'un des avantages du Random Forest est sa capacité à classer les variables selon leur pouvoir prédictif. Le modèle calcule combien chaque variable contribue à réduire l'incertitude globale. 
- Dans notre interface, cela permet d'extraire les "Facteurs Aggravants Majeurs". Si le modèle détecte que la Mousson et l'Urbanisation sont les causes principales du risque calculé, il les isole pour l'utilisateur.

---

## 3. Architecture Logique de l'Application GUI (Tkinter)

### 3.1 Conception Orientée Objet
L'application est encapsulée dans la classe `FloodProbabilityApp`. Cette approche permet de maintenir un "état" persistant :
- Le modèle chargé en mémoire reste disponible pour toutes les prédictions futures.
- Les dictionnaires de widgets (`self.input_fields`) permettent d'accéder aux valeurs saisies n'importe où dans le code.

### 3.2 Gestion de l'Interface Dynamique (Responsive Design)
Contrairement aux interfaces statiques, ce GUI s'adapte à l'utilisateur :
- **Calcul de Grille** : La méthode `create_responsive_grid` utilise la division entière de la largeur de la fenêtre (`width // 280`) pour décider dynamiquement si elle doit afficher 1, 2, 3 ou 4 colonnes.
- **Événements (Binding)** : L'application "écoute" le redimensionnement de la fenêtre via `root.bind("<Configure>")` et réorganise les widgets instantanément.

### 3.3 Synchronisation Bidirectionnelle
Pour offrir une expérience utilisateur fluide, nous avons implémenté une synchronisation entre les éléments :
- Si vous faites glisser le **curseur (Scale)**, la boîte de texte se remplit avec la valeur exacte.
- Si vous tapez un chiffre dans la **boîte de texte (Entry)**, le curseur se déplace automatiquement à la position correspondante.
- Cette logique garantit que l'utilisateur peut choisir entre la rapidité visuelle et la précision numérique.

---

## 4. Analyse et Interprétation du Risque

### 4.1 Seuils de Risque Critiques
Le résultat brut (ex: 0.54) est traduit visuellement pour être compréhensible immédiatement :
- **Niveau VERT (0% - 30%)** : Risque considéré comme normal ou négligeable. Vigilance de routine.
- **Niveau ORANGE (30% - 60%)** : Risque modéré. Des mesures préventives individuelles doivent être envisagées.
- **Niveau ROUGE (> 60%)** : Risque critique. Une action immédiate ou une évacuation des zones vulnérables est préconisée.

### 4.2 Analyse d'Impact Localisé
Lorsqu'un utilisateur simule un scénario, l'application effectue un calcul additionnel. Elle multiplie la valeur que vous avez saisie (une fois normalisée) par l'importance globale de cette variable dans le modèle. 
- Cela répond à la question : "Pourquoi mon risque est-il si élevé ?". 
- L'application identifie les 3 variables qui "poussent" le plus le score vers le haut dans votre configuration spécifique.

---

## 5. Gestion des Données et Persistance (Joblib)

### 5.1 Pourquoi sauvegarder les modèles ?
L'entraînement d'un modèle de Machine Learning consomme des ressources CPU et du temps. Pour rendre l'interface instantanée pour l'utilisateur final, nous pratiquons le **"Model Versioning"**.
- **Sérialisation** : Avec `joblib`, nous transformons les objets Python complexes (le cerveau du modèle) en fichiers binaires sur le disque.
- **Chargement à la demande** : Au démarrage, le script vérifie si le fichier `.joblib` existe dans le dossier `models/`. Si oui, il est chargé en quelques millisecondes sans ré-entraînement.

### 5.2 Le rôle crucial du Scaler
Il est impératif de sauvegarder le `StandardScaler` utilisé lors de l'entraînement. Pourquoi ? Car les futures données saisies par l'utilisateur doivent être transformées en utilisant la **moyenne** et **l'écart-type originaux** du dataset d'entraînement. Si on utilisait une autre échelle, les prédictions seraient totalement fausses.

---

## 6. Métriques de Performance et Validation

### 6.1 R-Squared ($R^2$) - Coefficient de Détermination
C'est la métrique principale pour la régression. Elle exprime la proportion de la variance de la variable cible qui est expliquée par le modèle. 
- Un score de 0.85 signifie que 85% des causes des inondations sont capturées par nos 20 paramètres.

### 6.2 Validation Croisée (K-Fold Cross-Validation)
Pour s'assurer que le modèle est stable, nous pratiquons parfois la validation "K-Fold". On divise le dataset en 5 parties. On entraîne 5 fois le modèle, en utilisant à chaque fois une partie différente pour le test et les 4 autres pour l'entraînement. Si les scores sont similaires, le modèle est jugé fiable et robuste.

---

## 7. Outils de Communication et Automatisation

En plus de l'analyse IA, le projet intègre des scripts d'automatisation pour la présentation des résultats.

### 7.1 Génération de Présentation (PowerPoint) : `generate_ppt.py`
Ce script utilise la bibliothèque **python-pptx** pour transformer les résultats techniques en un support de présentation professionnel pour le jury.
- **Principe** : Création dynamique de "Slides" (diapositives) incluant le titre, les membres du groupe, la méthodologie et les performances des modèles.
- **Objectif** : Assurer une communication claire des concepts complexes à un public académique.

### 7.2 Extraction de Données PDF : `extract_pdf_info.py`
Cet outil permet de parser des documents de recherche au format PDF pour enrichir notre base de connaissances ou extraire des statistiques.
- **Principe** : Utilisation de **Py2PDF** ou **pdfplumber** pour lire le texte brut et identifier les mots-clés liés aux inondations.

---

## Conclusion Générale
Ce projet TPE n'est pas seulement une application de prédiction. C'est un écosystème complet qui va de la **Collecte de Données** à la **Prédiction IA**, en passant par la **Validation Scientifique** et la **Restitution des Résultats**. Chaque étape a été pensée pour être à la fois techniquement rigoureuse et utile pour la gestion réelle des risques de crues.

---
*Cette documentation exhaustive a été conçue pour offrir une transparence totale sur le fonctionnement interne du système de prévision de probabilité d'inondation.*
