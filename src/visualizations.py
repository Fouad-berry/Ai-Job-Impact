"""
visualizations.py
-----------------
Fonctions de plotting réutilisables.
Toutes les figures sont utilisées dans build_project.py
et peuvent aussi être appelées depuis les notebooks.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


PALETTE_STATUS = {"Unchanged": "#2ecc71", "Modified": "#f39c12", "Replaced": "#e74c3c"}
PALETTE_RISK = {"Low": "#27ae60", "Medium": "#f39c12", "High": "#c0392b"}


def set_style():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 140,
        "savefig.bbox": "tight",
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
    })


def plot_job_status(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5.5))
    counts = df["Job_Status"].value_counts().reindex(["Unchanged", "Modified", "Replaced"])
    colors = [PALETTE_STATUS[s] for s in counts.index]
    bars = ax.bar(counts.index, counts.values, color=colors, edgecolor="black")
    for bar, val in zip(bars, counts.values):
        pct = 100 * val / len(df)
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f"{val}\n({pct:.1f}%)", ha="center", fontweight="bold")
    ax.set_title("Impact de l'IA sur l'emploi")
    ax.set_ylabel("Nombre d'employés")
    return ax


def plot_replacement_by_industry(dm_industry, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5.5))
    data = dm_industry.sort_values("pct_replaced", ascending=True)
    bars = ax.barh(data["Industry"], data["pct_replaced"],
                   color=sns.color_palette("Reds_r", len(data)), edgecolor="black")
    for bar, val in zip(bars, data["pct_replaced"]):
        ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}%", va="center", fontweight="bold")
    ax.set_title("Taux de remplacement par IA selon l'industrie")
    ax.set_xlabel("% d'employés remplacés")
    return ax


def plot_productivity_heatmap(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5.5))
    pivot = df.pivot_table(
        values="Productivity_Change_%",
        index="AI_Adoption_Level",
        columns="Automation_Risk",
        aggfunc="mean", observed=True,
    )
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn", center=0,
                cbar_kws={"label": "Variation productivité (%)"}, ax=ax, linewidths=0.5)
    ax.set_title("Productivité moyenne\nAdoption IA × Risque")
    return ax


def plot_salary_distribution(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5.5))
    for status in ["Unchanged", "Modified", "Replaced"]:
        data = df.loc[df["Job_Status"] == status, "Salary_Change_Pct"]
        ax.hist(data, bins=30, alpha=0.55, label=status,
                color=PALETTE_STATUS[status], edgecolor="black", linewidth=0.5)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_title("Distribution du changement salarial par statut")
    ax.set_xlabel("Variation salaire (%)")
    ax.legend(title="Job Status")
    return ax