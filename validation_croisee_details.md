# La Rigueur Scientifique : Validation Croisée (K-Fold)

La validation croisée est la méthode ultime pour vérifier si l'IA sera capable de prédire des inondations sur des données qu'elle n'a **jamais** vues auparavant. Sans elle, nous pourrions avoir un modèle qui semble parfait sur le papier mais qui échoue totalement dans le monde réel.

---

## 1. Notions de Base : Pourquoi Faire Cela ?

### 1.1 Le Biais de l'Échantillonnage
Si nous utilisons toujours les mêmes données pour tester, le modèle finit par s'habituer à ces données spécifiques. C'est le problème de la **Généralisation**. La validation croisée "mélange les cartes" pour forcer le modèle à rester vigilant.

### 1.2 Overfitting (Sur-apprentissage)
C'est le risque qu'un modèle apprenne le "bruit" ou les erreurs du dataset au lieu d'apprendre la logique réelle de l'hydrologie.

---

## 2. Processus des Étapes (Le 5-Fold)

Dans ce projet, nous avons utilisé un **K-Fold avec K=5**. Voici le détail des étapes :

1. **Découpage** : On divise les 1,1 million de lignes de données en 5 blocs égaux (environ 220 000 lignes par bloc).
2. **Rotation Itérative** :
   - *Tour 1* : On entraîne sur les blocs 2, 3, 4, 5. On teste sur le bloc 1.
   - *Tour 2* : On entraîne sur les blocs 1, 3, 4, 5. On teste sur le bloc 2.
   - ... et ainsi de suite jusqu'au tour 5.
3. **Récolte des Scores** : Chaque tour donne un score R² différent.
4. **Agrégation** : On calcule la **Moyenne** et l'**Écart-type** des scores.

---

## 3. Interprétation des Résultats Found

Le fichier `cv_results.json` stocke ces données. 
- **Moyenne Élevée** : Indique une précision globale solide.
- **Faible Écart-type** : Indique que le modèle est **Stable**. Si les scores varient trop d'un bloc à l'autre, le modèle est jugé instable et non fiable pour une mise en service réelle.

---

## 4. Conclusion Stratégique
Grâce à cette étape systématique, nous avons pu confirmer que le **Random Forest** était le modèle le plus équilibré pour notre GUI. Il a montré la plus grande stabilité à travers tous les blocs de données, garantissant aux utilisateurs du logiciel des prévisions fiables, peu importe la région géographique simulée.
