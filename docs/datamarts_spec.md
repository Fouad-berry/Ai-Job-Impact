# 🧱 Spécification des datamarts

Un datamart est une table agrégée, orientée cas d'usage métier, pré-calculée et prête à brancher sur un outil BI (ici Looker Studio). Chaque datamart répond à **une question** précise, évite les jointures côté BI et garantit des KPIs cohérents entre les consommateurs.

---

## 1. `dm_global_kpis.csv`

**Grain** : 1 seule ligne
**Usage Looker** : scorecards en haut de la page d'accueil du dashboard

| Colonne | Description |
|---------|-------------|
| `total_employees` | Taille de l'échantillon |
| `pct_replaced` | % d'employés dont l'emploi a été remplacé |
| `pct_modified` | % dont le rôle a été modifié |
| `pct_unchanged` | % inchangés |
| `avg_salary_before` | Salaire moyen avant IA (USD) |
| `avg_salary_after` | Salaire moyen après IA (USD) |
| `avg_salary_change_pct` | Variation moyenne du salaire (%) |
| `avg_productivity_change` | Variation moyenne de productivité (%) |
| `avg_satisfaction` | Satisfaction moyenne (1–10) |
| `pct_upskilling_required` | % nécessitant de l'upskilling |
| `pct_remote` | % en télétravail |

---

## 2. `dm_industry_impact.csv`

**Grain** : 1 ligne par industrie (7 lignes)
**Question** : "Quelles industries sont les plus touchées ?"
**Usage Looker** : bar charts, tables détaillées sur la page "Industries"

Colonnes : `Industry`, `headcount`, `avg_salary_before`, `avg_salary_after`, `avg_salary_change_pct`, `avg_productivity_change`, `avg_job_satisfaction`, `pct_replaced`, `pct_impacted`, `pct_high_automation_risk`, `pct_upskilling_required`.

---

## 3. `dm_role_impact.csv`

**Grain** : 1 ligne par métier (21 lignes)
**Question** : "Quels métiers sont les plus à risque ?"
**Usage Looker** : top 10 bar chart, filtres interactifs

Colonnes : `Job_Role`, `headcount`, `avg_salary_before`, `avg_salary_after`, `avg_salary_change_pct`, `avg_productivity_change`, `pct_replaced`, `pct_high_risk`.

Tri : par `pct_replaced` décroissant.

---

## 4. `dm_demographics.csv`

**Grain** : âge × genre × niveau d'éducation
**Question** : "Qui est le plus impacté démographiquement ?"
**Usage Looker** : heatmaps, tables croisées, slicers

Colonnes : `Age_Group`, `Gender`, `Education_Level`, `headcount`, `avg_salary_change_pct`, `pct_replaced`, `avg_satisfaction`.

---

## 5. `dm_adoption_risk_matrix.csv`

**Grain** : adoption IA × risque d'automatisation (9 cellules)
**Question** : "L'adoption IA compense-t-elle le risque d'automatisation ?"
**Usage Looker** : heatmap central du dashboard

Colonnes : `AI_Adoption_Level`, `Automation_Risk`, `headcount`, `avg_productivity_change`, `avg_salary_change_pct`, `pct_replaced`, `avg_satisfaction`.

---

## 6. `dm_upskilling_outcomes.csv`

**Grain** : upskilling × job status (6 cellules)
**Question** : "L'upskilling améliore-t-il vraiment les résultats ?"
**Usage Looker** : bar charts comparatifs, page "ROI formation"

Colonnes : `Upskilling_Required`, `Job_Status`, `headcount`, `avg_salary_change_pct`, `avg_productivity_change`, `avg_satisfaction`.

---

## Règles de construction communes

- Toutes les moyennes sont arrondies à **2 décimales**
- Les pourcentages sont en **base 100** (pas 0.XX) pour affichage direct dans Looker
- Pour chaque agrégation, `headcount` est inclus afin de pondérer les analyses
- Les flags `Was_Replaced` / `Was_Impacted` sont transformés en pourcentages lors de l'agrégation
- Source : `data/processed/ai_job_impact_clean.csv`
- Destination : `data/datamarts/dm_*.csv` (préfixe `dm_` systématique)