"""
datamarts.py
------------
Construction des 6 datamarts analytiques.

Un datamart = une table agrégée orientée cas d'usage.
Chaque fonction retourne un DataFrame prêt à être branché à Looker Studio
sans jointure supplémentaire.
"""

import pandas as pd


def build_global_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """KPIs globaux — 1 seule ligne — pour les scorecards."""
    return pd.DataFrame([{
        "total_employees": len(df),
        "pct_replaced": round(100 * df["Was_Replaced"].mean(), 2),
        "pct_modified": round(100 * (df["Job_Status"] == "Modified").mean(), 2),
        "pct_unchanged": round(100 * (df["Job_Status"] == "Unchanged").mean(), 2),
        "avg_salary_before": round(df["Salary_Before_AI"].mean(), 0),
        "avg_salary_after": round(df["Salary_After_AI"].mean(), 0),
        "avg_salary_change_pct": round(df["Salary_Change_Pct"].mean(), 2),
        "avg_productivity_change": round(df["Productivity_Change_%"].mean(), 2),
        "avg_satisfaction": round(df["Job_Satisfaction"].mean(), 2),
        "pct_upskilling_required": round(100 * (df["Upskilling_Required"] == "Yes").mean(), 2),
        "pct_remote": round(100 * (df["Remote_Work"] == "Yes").mean(), 2),
    }])


def build_industry_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par industrie — page dashboard 'Industries'."""
    out = df.groupby("Industry", observed=True).agg(
        headcount=("Employee_ID", "count"),
        avg_salary_before=("Salary_Before_AI", "mean"),
        avg_salary_after=("Salary_After_AI", "mean"),
        avg_salary_change_pct=("Salary_Change_Pct", "mean"),
        avg_productivity_change=("Productivity_Change_%", "mean"),
        avg_job_satisfaction=("Job_Satisfaction", "mean"),
        pct_replaced=("Was_Replaced", "mean"),
        pct_impacted=("Was_Impacted", "mean"),
        pct_high_automation_risk=("Automation_Risk", lambda s: (s == "High").mean()),
        pct_upskilling_required=("Upskilling_Required", lambda s: (s == "Yes").mean()),
    ).round(3).reset_index()
    for c in ["pct_replaced", "pct_impacted", "pct_high_automation_risk", "pct_upskilling_required"]:
        out[c] = (out[c] * 100).round(2)
    return out


def build_role_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par métier — trié par taux de remplacement décroissant."""
    out = df.groupby("Job_Role", observed=True).agg(
        headcount=("Employee_ID", "count"),
        avg_salary_before=("Salary_Before_AI", "mean"),
        avg_salary_after=("Salary_After_AI", "mean"),
        avg_salary_change_pct=("Salary_Change_Pct", "mean"),
        avg_productivity_change=("Productivity_Change_%", "mean"),
        pct_replaced=("Was_Replaced", lambda s: 100 * s.mean()),
        pct_high_risk=("Automation_Risk", lambda s: 100 * (s == "High").mean()),
    ).round(2).reset_index()
    return out.sort_values("pct_replaced", ascending=False)


def build_demographics(df: pd.DataFrame) -> pd.DataFrame:
    """Grain fin : âge × genre × éducation."""
    return df.groupby(
        ["Age_Group", "Gender", "Education_Level"], observed=True
    ).agg(
        headcount=("Employee_ID", "count"),
        avg_salary_change_pct=("Salary_Change_Pct", "mean"),
        pct_replaced=("Was_Replaced", lambda s: 100 * s.mean()),
        avg_satisfaction=("Job_Satisfaction", "mean"),
    ).round(2).reset_index()


def build_adoption_risk_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Matrice 3×3 : adoption IA × risque d'automatisation."""
    return df.groupby(
        ["AI_Adoption_Level", "Automation_Risk"], observed=True
    ).agg(
        headcount=("Employee_ID", "count"),
        avg_productivity_change=("Productivity_Change_%", "mean"),
        avg_salary_change_pct=("Salary_Change_Pct", "mean"),
        pct_replaced=("Was_Replaced", lambda s: 100 * s.mean()),
        avg_satisfaction=("Job_Satisfaction", "mean"),
    ).round(2).reset_index()


def build_upskilling_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """Upskilling × Job Status : ROI de la formation."""
    return df.groupby(
        ["Upskilling_Required", "Job_Status"], observed=True
    ).agg(
        headcount=("Employee_ID", "count"),
        avg_salary_change_pct=("Salary_Change_Pct", "mean"),
        avg_productivity_change=("Productivity_Change_%", "mean"),
        avg_satisfaction=("Job_Satisfaction", "mean"),
    ).round(2).reset_index()


def build_all(df: pd.DataFrame) -> dict:
    """Construit les 6 datamarts d'un coup."""
    return {
        "global_kpis": build_global_kpis(df),
        "industry_impact": build_industry_impact(df),
        "role_impact": build_role_impact(df),
        "demographics": build_demographics(df),
        "adoption_risk_matrix": build_adoption_risk_matrix(df),
        "upskilling_outcomes": build_upskilling_outcomes(df),
    }