# Explication du Code : L'Interface de Prédiction (GUI)

Ce document explique pas à pas le fonctionnement du fichier `app_prediction_gui.py`, qui est le cœur interactif de notre système.

---

## 1. Importations et Initialisation

```python
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
```
**Explication :**
- `tkinter` : Utilisé pour créer les fenêtres, boutons et curseurs.
- `pandas` & `numpy` : Pour la manipulation des données.
- `sklearn` : Contient l'intelligence artificielle (Random Forest) et les outils de préparation (StandardScaler).
- `joblib` : Sert à sauvegarder et charger le modèle sur le disque.

---

## 2. Chargement et Entraînement Automatique

```python
def load_and_train_model(self):
    # Tentative de chargement du modèle existant
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
    else:
        # Si absent, on entraîne sur flood.csv
        df = pd.read_csv(data_path)
        X = df.drop("FloodProbability", axis=1)
        y = df["FloodProbability"]
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestRegressor(n_estimators=50, n_jobs=-1)
        self.model.fit(X_scaled, y)
        joblib.dump(self.model, model_path)
```
**Explication :**
Cette partie vérifie si une IA a déjà été entraînée. Si ce n'est pas le cas, elle lit le fichier CSV, sépare les facteurs (X) du résultat (y), normalise les données et entraîne une **Forêt Aléatoire**. Elle sauvegarde ensuite tout pour gagner du temps au prochain démarrage.

---

## 3. Mise en Page Dynamique (Tableau de Bord)

```python
def create_widgets(self):
    # Création du canvas scrollable
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    # Grille responsive pour les 20 curseurs
    for i, feature in enumerate(self.feature_names):
        frame = tk.LabelFrame(scrollable_frame, text=feature)
        scale = tk.Scale(frame, from_=0, to_=20, orient=tk.HORIZONTAL)
```
**Explication :**
Comme nous avons 20 paramètres à régler, nous utilisons un **Canvas avec Scrollbar** pour que tout rentre dans la fenêtre. La boucle `for` crée automatiquement un curseur (Scale) pour chaque paramètre environnemental, organisé dans une grille responsive.

---

## 4. Le Moteur de Prédiction

```python
def predict(self):
    inputs = [float(self.input_fields[f]["entry"].get()) for f in self.feature_names]
    X_input_scaled = self.scaler.transform([inputs])
    probability = self.model.predict(X_input_scaled)[0]
    
    # Calcul de l'impact des facteurs
    importances = self.model.feature_importances_
    impact_scores = [(feat, X_input_scaled[0][i] * importances[i]) for i, feat in enumerate(self.feature_names)]
    impact_scores.sort(key=lambda x: x[1], reverse=True)
```
**Explication :**
1. On récupère les 20 valeurs saisies par l'utilisateur.
2. On les transforme avec le `scaler` (pour que l'IA comprenne l'échelle).
3. L'IA prédit la probabilité.
4. **Analyse d'impact** : On multiplie la valeur entrée par l'importance de la variable pour savoir quels sont les 3 facteurs qui aggravent le plus le risque.

---

## 5. Affichage des Résultats et Recommandations

```python
def display_result(self, probability, top_factors):
    if probability < 0.3:
        risk_level = "FAIBLE"
        color = "#27ae60"
    elif probability < 0.6:
        risk_level = "MOYEN"
        color = "#f39c12"
    else:
        risk_level = "ELEVE"
        color = "#e74c3c"
```
**Explication :**
Le script traduit la probabilité mathématique en un niveau de risque compréhensible (Faible, Moyen, Élevé) avec une couleur associée. Il affiche également des conseils de sécurité (Vigilance ou Évacuation) basés sur ce niveau.
