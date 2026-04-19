# 🔬 Méthodologie

## 1. Exploration (EDA)

- Inspection des types, dimensions, valeurs manquantes et doublons
- Statistiques descriptives sur les variables numériques et catégorielles
- Visualisation des distributions (histogrammes)
- Première mise en évidence : salaire avant/après IA

## 2. Nettoyage et feature engineering

Pipeline implémenté dans `src/preprocessing.py` :

1. Dédoublonnage par `Employee_ID`
2. Calcul de `Salary_Change` et `Salary_Change_Pct`
3. Création de `Age_Group` et `Experience_Bucket` (variables catégorielles ordonnées)
4. Création des flags binaires `Was_Impacted` et `Was_Replaced`
5. Conversion des variables ordinales en `pd.Categorical` pour des graphiques ordonnés

## 3. Construction des datamarts

Implémentée dans `src/datamarts.py`. Six datamarts, un par question métier (voir [`datamarts_spec.md`](datamarts_spec.md)).

## 4. Visualisation

- **Python** (Matplotlib / Seaborn) pour les figures incluses dans le README et générées automatiquement par `build_project.py`
- **Looker Studio** pour le dashboard interactif final destiné aux parties prenantes

Choix stylistiques :
- Palette sémantique : vert pour `Unchanged` / `Low risk`, orange pour `Modified` / `Medium`, rouge pour `Replaced` / `High`
- Annotations directes sur chaque barre pour éviter la lecture de l'axe
- Hauteurs fixes (DPI=140) pour une intégration propre dans le README

## 5. Export vers Looker Studio

Deux options possibles :

**Option légère (recommandée)** : upload direct des CSV de `data/exports/`

- `main_dataset.csv` (2000 lignes) → source principale
- `by_industry.csv`, `by_role.csv`, `adoption_risk_matrix.csv`, `global_kpis.csv` → sources agrégées pour les scorecards et graphiques spécifiques

**Option entrepôt (avancée)** : charger les tables dans BigQuery avec `sql/create_tables.sql`, puis brancher Looker Studio sur BigQuery. Avantages : mise à jour automatique, requêtes SQL directes via `sql/queries.sql`.

## 6. Limitations

- **Dataset synthétique** : les conclusions ne doivent pas être extrapolées à la population réelle
- **Classe cible déséquilibrée** : seulement 5,3 % de cas `Replaced`, à prendre en compte pour tout modèle prédictif
- **Données transversales** : pas de dimension temporelle, on ne peut pas mesurer la dynamique d'adoption de l'IA
- **Auto-déclaration** : `Job_Satisfaction` et `Productivity_Change_%` sont des perceptions, pas des mesures objectives