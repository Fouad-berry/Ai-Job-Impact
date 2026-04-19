"""
preprocessing.py
----------------
Nettoyage et feature engineering.
"""

import pandas as pd
import numpy as np


def add_salary_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les features liées au changement de salaire."""
    df = df.copy()
    df["Salary_Change"] = df["Salary_After_AI"] - df["Salary_Before_AI"]
    df["Salary_Change_Pct"] = 100 * df["Salary_Change"] / df["Salary_Before_AI"]
    return df


def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Age_Group"] = pd.cut(
        df["Age"], bins=[20, 29, 39, 49, 60],
        labels=["20-29", "30-39", "40-49", "50-59"]
    )
    return df


def add_experience_bucket(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Experience_Bucket"] = pd.cut(
        df["Years_Experience"], bins=[-1, 5, 15, 25, 40],
        labels=["0-5", "6-15", "16-25", "26+"]
    )
    return df


def add_impact_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flags binaires pour faciliter les agrégations."""
    df = df.copy()
    df["Was_Impacted"] = (df["Job_Status"] != "Unchanged").astype(int)
    df["Was_Replaced"] = (df["Job_Status"] == "Replaced").astype(int)
    return df


def order_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Donne un ordre logique aux variables ordinales pour les graphiques."""
    df = df.copy()
    df["AI_Adoption_Level"] = pd.Categorical(
        df["AI_Adoption_Level"], ["Low", "Medium", "High"], ordered=True
    )
    df["Automation_Risk"] = pd.Categorical(
        df["Automation_Risk"], ["Low", "Medium", "High"], ordered=True
    )
    df["Job_Status"] = pd.Categorical(
        df["Job_Status"], ["Unchanged", "Modified", "Replaced"], ordered=True
    )
    return df


def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline complet : dédoublonnage + toutes les features."""
    df = df.drop_duplicates().reset_index(drop=True)
    df = add_salary_features(df)
    df = add_age_group(df)
    df = add_experience_bucket(df)
    df = add_impact_flags(df)
    df = order_categoricals(df)
    return df