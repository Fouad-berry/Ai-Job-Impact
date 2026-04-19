-- ============================================
-- create_tables.sql
-- Schéma BigQuery pour brancher Looker Studio
-- en mode entrepôt (au lieu de l'upload CSV direct).
-- ============================================

CREATE SCHEMA IF NOT EXISTS `ai_job_impact`;

-- ============================================
-- Table principale : une ligne par employé
-- ============================================
CREATE OR REPLACE TABLE `ai_job_impact.employees` (
    Employee_ID             STRING   NOT NULL,
    Age                     INT64    NOT NULL,
    Gender                  STRING   NOT NULL,
    Education_Level         STRING   NOT NULL,
    Industry                STRING   NOT NULL,
    Job_Role                STRING   NOT NULL,
    Years_Experience        INT64    NOT NULL,
    AI_Adoption_Level       STRING   NOT NULL,
    Automation_Risk         STRING   NOT NULL,
    Upskilling_Required     STRING   NOT NULL,
    Salary_Before_AI        INT64    NOT NULL,
    Salary_After_AI         INT64    NOT NULL,
    Job_Status              STRING   NOT NULL,
    Work_Hours_Per_Week     INT64    NOT NULL,
    Remote_Work             STRING   NOT NULL,
    Job_Satisfaction        INT64    NOT NULL,
    Productivity_Change_Pct FLOAT64  NOT NULL,

    -- Features dérivées
    Salary_Change           INT64,
    Salary_Change_Pct       FLOAT64,
    Age_Group               STRING,
    Experience_Bucket       STRING,
    Was_Impacted            INT64,
    Was_Replaced            INT64
);

-- ============================================
-- Datamarts (alimentés depuis les CSV générés)
-- ============================================

CREATE OR REPLACE TABLE `ai_job_impact.dm_global_kpis` (
    total_employees           INT64,
    pct_replaced              FLOAT64,
    pct_modified              FLOAT64,
    pct_unchanged             FLOAT64,
    avg_salary_before         FLOAT64,
    avg_salary_after          FLOAT64,
    avg_salary_change_pct     FLOAT64,
    avg_productivity_change   FLOAT64,
    avg_satisfaction          FLOAT64,
    pct_upskilling_required   FLOAT64,
    pct_remote                FLOAT64
);

CREATE OR REPLACE TABLE `ai_job_impact.dm_industry_impact` (
    Industry                    STRING,
    headcount                   INT64,
    avg_salary_before           FLOAT64,
    avg_salary_after            FLOAT64,
    avg_salary_change_pct       FLOAT64,
    avg_productivity_change     FLOAT64,
    avg_job_satisfaction        FLOAT64,
    pct_replaced                FLOAT64,
    pct_impacted                FLOAT64,
    pct_high_automation_risk    FLOAT64,
    pct_upskilling_required     FLOAT64
);

CREATE OR REPLACE TABLE `ai_job_impact.dm_role_impact` (
    Job_Role                STRING,
    headcount               INT64,
    avg_salary_before       FLOAT64,
    avg_salary_after        FLOAT64,
    avg_salary_change_pct   FLOAT64,
    avg_productivity_change FLOAT64,
    pct_replaced            FLOAT64,
    pct_high_risk           FLOAT64
);

CREATE OR REPLACE TABLE `ai_job_impact.dm_adoption_risk_matrix` (
    AI_Adoption_Level       STRING,
    Automation_Risk         STRING,
    headcount               INT64,
    avg_productivity_change FLOAT64,
    avg_salary_change_pct   FLOAT64,
    pct_replaced            FLOAT64,
    avg_satisfaction        FLOAT64
);