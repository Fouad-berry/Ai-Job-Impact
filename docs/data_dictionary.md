# 📖 Data Dictionary

## Dataset source : `ai_job_impact.csv`

**2 000 lignes × 17 colonnes** (dataset synthétique).

### Identifiant

| Variable | Type | Description |
|----------|------|-------------|
| `Employee_ID` | string | Identifiant unique de l'employé (ex: `E0001`) |

### Démographie

| Variable | Type | Domaine | Description |
|----------|------|---------|-------------|
| `Age` | int | 22–59 | Âge de l'employé |
| `Gender` | string | `Male`, `Female`, `Other` | Genre déclaré |
| `Education_Level` | string | `High School`, `Bachelor`, `Master`, `PhD` | Plus haut niveau d'études |

### Profil professionnel

| Variable | Type | Domaine | Description |
|----------|------|---------|-------------|
| `Industry` | string | 7 modalités | Education, Finance, Healthcare, IT, Manufacturing, Marketing, Retail |
| `Job_Role` | string | 21 modalités | Accountant, Data Analyst, Software Engineer, Teacher, … |
| `Years_Experience` | int | 0–37 | Années d'expérience professionnelle |
| `Work_Hours_Per_Week` | int | | Heures travaillées par semaine |
| `Remote_Work` | string | `Yes`, `No` | Télétravail ou non |

### Impact de l'IA

| Variable | Type | Domaine | Description |
|----------|------|---------|-------------|
| `AI_Adoption_Level` | string | `Low`, `Medium`, `High` | Niveau d'adoption de l'IA dans le poste |
| `Automation_Risk` | string | `Low`, `Medium`, `High` | Risque d'automatisation du métier |
| `Upskilling_Required` | string | `Yes`, `No` | Indique si formation complémentaire requise |
| `Job_Status` | string | `Unchanged`, `Modified`, `Replaced` | Statut de l'emploi après l'introduction de l'IA |

### Indicateurs financiers

| Variable | Type | Description |
|----------|------|-------------|
| `Salary_Before_AI` | int | Salaire annuel avant introduction de l'IA (USD) |
| `Salary_After_AI` | int | Salaire annuel après (USD) |

### Indicateurs de perception / performance

| Variable | Type | Domaine | Description |
|----------|------|---------|-------------|
| `Job_Satisfaction` | int | 3–9 | Satisfaction auto-déclarée |
| `Productivity_Change_%` | float | -20 à +40 | Variation de productivité déclarée après l'IA |

---

## Variables dérivées (générées par `src/preprocessing.py`)

| Variable | Calcul | Description |
|----------|--------|-------------|
| `Salary_Change` | `Salary_After_AI - Salary_Before_AI` | Différence absolue de salaire |
| `Salary_Change_Pct` | `100 * Salary_Change / Salary_Before_AI` | Variation de salaire en % |
| `Age_Group` | Bins `[20-29, 30-39, 40-49, 50-59]` | Tranche d'âge |
| `Experience_Bucket` | Bins `[0-5, 6-15, 16-25, 26+]` | Tranche d'expérience |
| `Was_Impacted` | `1 if Job_Status != 'Unchanged' else 0` | Flag binaire : emploi modifié ou remplacé |
| `Was_Replaced` | `1 if Job_Status == 'Replaced' else 0` | Flag binaire : emploi remplacé |

## Notes méthodologiques

- **Valeurs manquantes** : aucune dans le dataset
- **Doublons** : aucun `Employee_ID` n'est dupliqué
- **Classe cible** : `Was_Replaced` est déséquilibrée (~5,3 % de cas positifs)
- Les variables `AI_Adoption_Level`, `Automation_Risk` et `Job_Status` sont converties en catégoriel ordonné pour que les graphiques respectent l'ordre logique `Low < Medium < High` / `Unchanged < Modified < Replaced`.