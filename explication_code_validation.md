# Explication du Code : Validation Croisée

Le fichier `validation_croisee.py` sert à prouver scientifiquement quel modèle est le plus performant pour notre étude.

---

## 1. Préparation et Nettoyage des Données

```python
for col in num_cols:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df_clean[col] = df_clean[col].clip(lower, upper)
```
**Explication :**
Avant de tester, ce code nettoie les "Outliers" (valeurs aberrantes). Il utilise la méthode statistique de l'**Intervalle Interquartile (IQR)**. Tout ce qui est trop éloigné de la normale est "clippé" (ramené à la valeur limite) pour éviter de tromper l'IA.

---

## 2. Configuration du Test K-Fold

```python
kf = KFold(n_splits=5, shuffle=True, random_state=42)

for fold, (train_index, test_index) in enumerate(kf.split(X_scaled)):
    X_train, X_test = X_scaled[train_index], X_scaled[test_index]
    y_train, y_test = y[train_index], y[test_index]
```
**Explication :**
Le **KFold** divise le dataset en 5 morceaux. Le script va tourner 5 fois. À chaque tour, il utilise un morceau différent pour tester et les 4 autres pour apprendre. Cela garantit une évaluation impartiale.

---

## 3. Comparaison Triple (Modèles)

```python
# Modèle 1: Régression Linéaire
lr = LinearRegression()
lr.fit(X_train, y_train)

# Modèle 2: Forêt Aléatoire
rf = RandomForestRegressor(n_estimators=50, n_jobs=-1)
rf.fit(X_train, y_train)

# Modèle 3: Réseau de Neurones
model = Sequential([Dense(64, activation='relu'), Dense(1)])
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=10)
```
**Explication :**
Dans chaque boucle du K-Fold, nous entraînons simultanément les trois types d'IA. Cela permet de comparer leurs erreurs (MSE) et leur précision (R²) exactement sur les mêmes données.

---

## 4. Agrégation et Export JSON

```python
final_results[model_name] = {
    "mean_mse": float(np.mean(metrics["mse"])),
    "mean_r2": float(np.mean(metrics["r2"]))
}

with open('cv_results.json', 'w') as f:
    json.dump(final_results, f)
```
**Explication :**
À la fin, le script calcule la moyenne des performances pour chaque IA. Les résultats sont sauvegardés dans `cv_results.json`. Ce fichier est crucial car il justifie pourquoi nous avons choisi d'utiliser le Random Forest dans l'application finale.
