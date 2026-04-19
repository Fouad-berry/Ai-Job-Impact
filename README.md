# 🤖 AI Job Impact Analysis

> Analyse de l'impact de l'intelligence artificielle sur **2 000 emplois** à travers 7 industries : qui est remplacé, qui voit son salaire évoluer, et quels profils s'adaptent le mieux.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![Looker Studio](https://img.shields.io/badge/Looker%20Studio-Dashboard-4285F4.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Objectif du projet

Comprendre comment l'IA transforme le marché du travail en analysant 2 000 employés sur **17 dimensions** (démographie, rôle, salaire avant/après IA, risque d'automatisation, satisfaction, productivité, etc.).

**Questions métier :**
- Quelles industries et quels métiers sont les plus touchés par l'IA ?
- L'IA augmente-t-elle ou réduit-elle les salaires en moyenne ?
- Quel profil démographique résiste le mieux au remplacement par l'IA ?
- L'upskilling fait-il vraiment une différence ?
- Y a-t-il une corrélation entre adoption de l'IA et productivité ?

Le livrable final est un **dashboard interactif Looker Studio** alimenté par des datamarts Python.

---

## 📊 Aperçu des résultats

### Répartition de l'impact sur l'emploi

![Job Status Distribution](images/figures/01_job_status_distribution.png)

> Sur les 2 000 employés, **5,3 %** ont été remplacés, **40 %** ont vu leur rôle modifié, et **54,6 %** sont inchangés.

### Top 10 des métiers les plus à risque

![Top 10 Roles at Risk](images/figures/03_top10_roles_at_risk.png)

### Productivité : adoption IA × risque d'automatisation

![Productivity Heatmap](images/figures/05_productivity_heatmap.png)

> Les employés à **forte adoption IA** gagnent en productivité quelle que soit leur exposition au risque.

### Évolution salariale par industrie

![Salary Before/After](images/figures/04_salary_before_after_by_industry.png)

📁 **10 figures générées** dans [`images/figures/`](images/figures/).

---

## 📁 Structure du projet

```
ai-job-impact/
│
├── data/
│   ├── raw/                              # Dataset brut (2000 × 17)
│   │   └── ai_job_impact.csv
│   ├── processed/                        # Données nettoyées + features dérivées
│   │   └── ai_job_impact_clean.csv
│   ├── datamarts/                        # 🧱 Tables agrégées orientées analyse
│   │   ├── dm_global_kpis.csv            # KPIs globaux (pour scorecards)
│   │   ├── dm_industry_impact.csv        # Impact par industrie
│   │   ├── dm_role_impact.csv            # Impact par métier
│   │   ├── dm_demographics.csv           # Âge × genre × éducation
│   │   ├── dm_adoption_risk_matrix.csv   # Matrice adoption IA × risque
│   │   └── dm_upskilling_outcomes.csv    # ROI de l'upskilling
│   └── exports/                          # Exports prêts pour Looker Studio
│
├── notebooks/
│   ├── 01_exploration.ipynb              # EDA
│   ├── 02_cleaning.ipynb                 # Nettoyage + feature engineering
│   ├── 03_datamarts.ipynb                # Construction des datamarts
│   └── 04_visualizations.ipynb           # Génération des figures
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py                    # Chargement des données
│   ├── preprocessing.py                  # Features dérivées
│   ├── datamarts.py                      # Construction des datamarts
│   ├── visualizations.py                 # Fonctions de plot
│   └── utils.py
│
├── sql/
│   ├── create_tables.sql                 # Schéma BigQuery
│   └── queries.sql                       # Requêtes analytiques
│
├── dashboards/
│   └── looker_studio_guide.md            # Guide de connexion + structure
│
├── docs/
│   ├── data_dictionary.md
│   ├── datamarts_spec.md                 # Spécification des datamarts
│   └── methodology.md
│
├── images/figures/                       # 10 visualisations PNG pré-générées
│
├── build_project.py                      # ⭐ Script maître : regénère tout
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

---

## 🧱 Les 6 datamarts

Un **datamart** est une table agrégée orientée cas d'usage : elle répond à une question métier précise et peut être branchée directement à Looker Studio sans jointure supplémentaire.

| Datamart | Grain | Usage Looker |
|----------|-------|--------------|
| `dm_global_kpis` | 1 ligne | Scorecards de vue d'ensemble |
| `dm_industry_impact` | 1 ligne par industrie | Page "Vue par industrie" |
| `dm_role_impact` | 1 ligne par métier | Bar chart des métiers à risque |
| `dm_demographics` | âge × genre × éducation | Analyses démographiques croisées |
| `dm_adoption_risk_matrix` | adoption IA × risque | Heatmap de productivité |
| `dm_upskilling_outcomes` | upskilling × statut | Démonstration du ROI |

📄 Spécification complète : [`docs/datamarts_spec.md`](docs/datamarts_spec.md).

---

## 🚀 Installation & utilisation

### 1. Cloner le repo

```bash
git clone https://github.com/<ton-username>/ai-job-impact.git
cd ai-job-impact
```

### 2. Environnement virtuel + dépendances

```bash
python -m venv venv
source venv/bin/activate       # Linux / Mac
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Générer tous les livrables en une commande

```bash
python build_project.py
```

Ce script :
1. Charge `data/raw/ai_job_impact.csv`
2. Nettoie et ajoute les features dérivées (`Salary_Change_Pct`, `Age_Group`, `Experience_Bucket`, `Was_Replaced`, `Was_Impacted`)
3. Construit les **6 datamarts** dans `data/datamarts/`
4. Copie les exports Looker dans `data/exports/`
5. Régénère les **10 figures PNG** dans `images/figures/`

### 4. Explorer avec les notebooks

```bash
jupyter notebook notebooks/
```

---

## 🔎 Workflow

```
Raw Data (CSV)
     │
     ▼
[1] Exploration & nettoyage
     │  • Vérification intégrité, dédoublonnage
     │  • Features : Salary_Change_Pct, Age_Group, Was_Replaced…
     ▼
[2] Construction des datamarts (src/datamarts.py)
     │  • 6 tables agrégées, une par question métier
     ▼
[3] Visualisations Python (10 figures PNG)
     │  • Utilisées dans ce README et le dashboard
     ▼
[4] Export vers Looker Studio
     │  • main_dataset.csv (grain individu)
     │  • 5 datamarts (grain agrégé)
     ▼
[5] Dashboard Looker Studio interactif
```

---

## 📈 Dashboard Looker Studio

Le dashboard est organisé en **5 pages** :

1. **Executive Overview** — KPIs globaux + répartition impact
2. **Industries** — Comparaison des 7 secteurs
3. **Jobs at Risk** — Top métiers remplacés
4. **Demographics** — Âge × genre × éducation
5. **AI Adoption ROI** — Productivité et upskilling

📄 Guide complet de connexion : [`dashboards/looker_studio_guide.md`](dashboards/looker_studio_guide.md).

---

## 📌 Principaux insights

- **Marketing** et **Education** sont les industries où le remplacement par l'IA est le plus élevé (~6-7 %)
- **Healthcare** et **Manufacturing** sont les plus résilients (~3,7-4,1 % de remplacement)
- Les employés en **haute adoption IA** gagnent **+11 %** de productivité en moyenne, contre +8 % pour ceux en faible adoption
- Le salaire moyen augmente de **+6,05 %** après l'introduction de l'IA (effet net positif à l'échelle globale)
- Les métiers les plus à risque sont : **Administrator**, **Investment Analyst**, **SEO Specialist**, **Digital Marketer**
- L'**upskilling est demandé à 51 %** de la population — une indication forte du besoin de formation continue

---

## 🛠️ Stack technique

- **Python 3.10+** · Pandas · NumPy · SciPy
- **Matplotlib** · Seaborn pour les visualisations Python
- **Jupyter** pour l'exploration
- **Looker Studio** pour le dashboard final
- **Git / GitHub** pour le versioning

---

## 📝 Licence

MIT — voir [`LICENSE`](LICENSE).

---

## 👤 Auteur

**Fouad MOUTAIROU**
- Portfolio : https://portfolio-fouad.netlify.app

---

## ⚠️ Disclaimer

Dataset synthétique à usage éducatif. Les conclusions ne doivent pas être extrapolées à la population réelle sans validation supplémentaire.