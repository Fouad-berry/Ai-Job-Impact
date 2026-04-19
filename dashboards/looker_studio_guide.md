# 📊 Guide Looker Studio

## 🔗 Lien du dashboard

> **[👉 Ouvrir le dashboard](https://lookerstudio.google.com/)** *(à remplacer par ton lien publié)*

---

## 🚀 Connexion des données

### Option A — Upload CSV direct (rapide, recommandé pour commencer)

1. [lookerstudio.google.com](https://lookerstudio.google.com/) → **Créer** → **Source de données**
2. Choisir le connecteur **File Upload**
3. Uploader les fichiers suivants depuis `data/exports/` :
   - `main_dataset.csv` (source principale, 2000 lignes)
   - `by_industry.csv` (source pour la page Industries)
   - `by_role.csv` (source pour la page Jobs)
   - `adoption_risk_matrix.csv` (source pour la heatmap)
   - `global_kpis.csv` (source pour les scorecards)
4. Pour chaque source : **Créer un rapport**

### Option B — Google Sheets (pour mise à jour facile)

1. Importer chaque CSV dans un Google Sheet distinct
2. Dans Looker Studio : **Ajouter une source** → **Google Sheets** → sélectionner le sheet
3. Les données se mettent à jour automatiquement si le sheet est modifié

### Option C — BigQuery (option avancée)

1. Exécuter `sql/create_tables.sql` dans BigQuery pour créer le schéma
2. Charger les CSV via l'UI BigQuery ou `bq load`
3. Dans Looker Studio : **Ajouter une source** → **BigQuery** → choisir la table
4. Utiliser les requêtes de `sql/queries.sql` comme sources de champs calculés

---

## 🎨 Structure recommandée en 5 pages

### 📄 Page 1 — Executive Overview

Source : `global_kpis.csv`

- **5 scorecards** sur une ligne : `total_employees`, `pct_replaced`, `pct_modified`, `avg_salary_change_pct`, `avg_productivity_change`
- **Donut chart** : répartition Unchanged / Modified / Replaced (source : `main_dataset`)
- **Bar chart horizontal** : taux de remplacement par industrie

### 📄 Page 2 — Industries

Source : `by_industry.csv` + `main_dataset.csv`

- **Table** : toutes les industries triées par `pct_replaced` décroissant
- **Bar chart groupé** : salaire avant vs après IA par industrie
- **Scatter chart** : `pct_high_automation_risk` (X) vs `pct_replaced` (Y), taille = headcount
- **Heatmap** : industrie × AI_Adoption_Level

### 📄 Page 3 — Jobs at Risk

Source : `by_role.csv`

- **Bar chart horizontal** : top 10 des métiers par `pct_replaced`
- **Bar chart horizontal** : top 10 des métiers par gain salarial
- **Table détaillée** : tous les métiers avec tri interactif
- **Filtre** : industrie (pour restreindre les métiers affichés)

### 📄 Page 4 — Demographics

Source : `main_dataset.csv`

- **Bar chart** : `pct_replaced` par `Age_Group`
- **Bar chart** : `pct_replaced` par `Education_Level`
- **Heatmap** : `Age_Group` × `Education_Level` = `avg_salary_change_pct`
- **Pie chart** : répartition par genre

### 📄 Page 5 — AI Adoption ROI

Source : `adoption_risk_matrix.csv`

- **Heatmap** : `AI_Adoption_Level` × `Automation_Risk` = productivité
- **Bar chart** : productivité moyenne par niveau d'adoption
- **Bar chart** : satisfaction par `Upskilling_Required` × `Job_Status`
- **Scorecard** : gain moyen de productivité des High adopters

---

## 🎛️ Filtres interactifs (haut de page)

Place ces contrôles en haut de chaque page pour une exploration libre :

- `Industry` (dropdown multiple)
- `Gender` (dropdown)
- `Education_Level` (dropdown multiple)
- `AI_Adoption_Level` (boutons Low/Medium/High)
- `Age_Group` (slider ou boutons)

---

## 📸 Captures d'écran

Place tes captures dans `images/` et référence-les ici :

```markdown
![Executive Overview](../images/dashboard_01_overview.png)
![Industries](../images/dashboard_02_industries.png)
![Jobs at Risk](../images/dashboard_03_jobs.png)
![Demographics](../images/dashboard_04_demographics.png)
![AI Adoption ROI](../images/dashboard_05_roi.png)
```

---

## 💡 Astuces de design

- **Palette cohérente** : vert `#2ecc71` pour positif, orange `#f39c12` pour neutre/attention, rouge `#e74c3c` pour risque/négatif
- **Typographie** : utiliser la même taille pour les titres de scorecards
- **Navigation** : ajouter des boutons en haut pour passer d'une page à l'autre
- **Date de dernière mise à jour** : ajouter un champ texte en pied de page
- **Logo / branding** : uploader un logo dans le header