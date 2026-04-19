-- ============================================
-- queries.sql
-- Requêtes d'analyse pour Looker Studio / exploration
-- ============================================

-- 1. KPIs globaux
SELECT
    COUNT(*)                                              AS total_employees,
    ROUND(100 * AVG(Was_Replaced), 2)                     AS pct_replaced,
    ROUND(AVG(Salary_Before_AI), 0)                       AS avg_salary_before,
    ROUND(AVG(Salary_After_AI), 0)                        AS avg_salary_after,
    ROUND(AVG(Salary_Change_Pct), 2)                      AS avg_salary_change_pct,
    ROUND(AVG(Productivity_Change_Pct), 2)                AS avg_productivity_change,
    ROUND(AVG(Job_Satisfaction), 2)                       AS avg_satisfaction
FROM `ai_job_impact.employees`;


-- 2. Classement des industries par taux de remplacement
SELECT
    Industry,
    COUNT(*) AS headcount,
    ROUND(100 * AVG(Was_Replaced), 2) AS pct_replaced,
    ROUND(AVG(Salary_Change_Pct), 2)  AS avg_salary_change_pct,
    ROUND(AVG(Productivity_Change_Pct), 2) AS avg_productivity
FROM `ai_job_impact.employees`
GROUP BY Industry
ORDER BY pct_replaced DESC;


-- 3. Top 10 des métiers les plus à risque
SELECT
    Job_Role,
    COUNT(*) AS headcount,
    ROUND(100 * AVG(Was_Replaced), 2)               AS pct_replaced,
    ROUND(100 * AVG(IF(Automation_Risk = 'High', 1, 0)), 2) AS pct_high_risk,
    ROUND(AVG(Salary_Change_Pct), 2)                AS avg_salary_change_pct
FROM `ai_job_impact.employees`
GROUP BY Job_Role
ORDER BY pct_replaced DESC
LIMIT 10;


-- 4. Matrice adoption × risque
SELECT
    AI_Adoption_Level,
    Automation_Risk,
    COUNT(*) AS headcount,
    ROUND(AVG(Productivity_Change_Pct), 2) AS avg_productivity,
    ROUND(AVG(Salary_Change_Pct), 2)       AS avg_salary_change,
    ROUND(100 * AVG(Was_Replaced), 2)      AS pct_replaced,
    ROUND(AVG(Job_Satisfaction), 2)        AS avg_satisfaction
FROM `ai_job_impact.employees`
GROUP BY AI_Adoption_Level, Automation_Risk
ORDER BY AI_Adoption_Level, Automation_Risk;


-- 5. Comparaison démographique (âge × éducation)
SELECT
    Age_Group,
    Education_Level,
    COUNT(*) AS headcount,
    ROUND(100 * AVG(Was_Replaced), 2) AS pct_replaced,
    ROUND(AVG(Salary_Change_Pct), 2)  AS avg_salary_change_pct,
    ROUND(AVG(Job_Satisfaction), 2)   AS avg_satisfaction
FROM `ai_job_impact.employees`
GROUP BY Age_Group, Education_Level
ORDER BY Age_Group, Education_Level;


-- 6. ROI de l'upskilling
SELECT
    Upskilling_Required,
    Job_Status,
    COUNT(*) AS headcount,
    ROUND(AVG(Salary_Change_Pct), 2)       AS avg_salary_change_pct,
    ROUND(AVG(Productivity_Change_Pct), 2) AS avg_productivity_change,
    ROUND(AVG(Job_Satisfaction), 2)        AS avg_satisfaction
FROM `ai_job_impact.employees`
GROUP BY Upskilling_Required, Job_Status
ORDER BY Upskilling_Required, Job_Status;


-- 7. Profils les plus impactés (remplacés avec grosse perte salariale)
SELECT
    Employee_ID, Age, Gender, Education_Level, Industry, Job_Role,
    Salary_Before_AI, Salary_After_AI, Salary_Change_Pct,
    AI_Adoption_Level, Automation_Risk
FROM `ai_job_impact.employees`
WHERE Was_Replaced = 1
ORDER BY Salary_Change_Pct ASC
LIMIT 20;


-- 8. Profils gagnants (productivité et salaire en hausse)
SELECT
    Employee_ID, Industry, Job_Role, AI_Adoption_Level,
    Salary_Change_Pct, Productivity_Change_Pct, Job_Satisfaction
FROM `ai_job_impact.employees`
WHERE Salary_Change_Pct > 10
  AND Productivity_Change_Pct > 20
ORDER BY Salary_Change_Pct DESC
LIMIT 20;