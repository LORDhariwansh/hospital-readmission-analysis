-- ==============================================================
-- HOSPITAL READMISSION ANALYSIS
-- Phase 6 – SQL Analysis (MySQL Compatible)
-- Dataset: Hospital Administration Data / UCI Diabetes 130-US Hospitals
-- ==============================================================

-- SETUP: Create and use the database
CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- NOTE: Import diabetic_data_cleaned.csv into a table named 'hospital_data'
-- Use MySQL Workbench Data Import or LOAD DATA INFILE

-- ==============================================================
-- TABLE STRUCTURE REFERENCE
-- ==============================================================
/*
Key Columns:
- encounter_id         : Unique encounter identifier (PK)
- patient_nbr          : Patient identifier (can repeat – multiple visits)
- race                 : Patient race
- gender               : Patient gender
- age                  : Age group (e.g., [50-60))
- weight               : Weight category (96.87% NULL)
- admission_type_id    : Type of admission (numeric code)
- discharge_disposition_id : Discharge destination (numeric code)
- time_in_hospital     : Number of days in hospital
- medical_specialty    : Treating specialty (49% NULL)
- num_lab_procedures   : Number of lab tests
- num_procedures       : Number of procedures
- num_medications      : Number of medications
- number_outpatient    : Prior outpatient visits
- number_emergency     : Prior emergency visits
- number_inpatient     : Prior inpatient visits
- number_diagnoses     : Number of diagnoses recorded
- diag_1, diag_2, diag_3 : ICD-9 diagnosis codes
- change               : Whether diabetes medication was changed
- diabetesMed          : Whether patient is on diabetes medication
- readmitted           : NO, <30, >30
- readmitted_binary    : 1 = readmitted within 30 days, 0 = otherwise
*/

-- ==============================================================
-- QUERY 1: Total Patients and Encounters
-- ==============================================================
-- Business Question: How many patients and encounters does this dataset contain?

SELECT
    COUNT(encounter_id)                   AS total_encounters,
    COUNT(DISTINCT patient_nbr)           AS unique_patients,
    ROUND(COUNT(encounter_id) /
          COUNT(DISTINCT patient_nbr), 2) AS avg_encounters_per_patient
FROM hospital_data;

-- ==============================================================
-- QUERY 2: Overall Readmission Rate
-- ==============================================================
-- Business Question: What is the overall 30-day readmission rate?

SELECT
    COUNT(encounter_id)                                AS total_encounters,
    SUM(readmitted_binary)                             AS total_readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)                AS readmission_rate_pct,
    SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmit_lt30,
    SUM(CASE WHEN readmitted = '>30' THEN 1 ELSE 0 END) AS readmit_gt30,
    SUM(CASE WHEN readmitted = 'NO'  THEN 1 ELSE 0 END) AS not_readmitted
FROM hospital_data;

-- ==============================================================
-- QUERY 3: Readmission Rate by Age Group
-- ==============================================================
-- Business Question: Which age groups have the highest readmission rates?

SELECT
    age                                              AS age_group,
    COUNT(encounter_id)                              AS total_patients,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
GROUP BY age
ORDER BY FIELD(age,
    '[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)',
    '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)');

-- ==============================================================
-- QUERY 4: Readmission Rate by Gender
-- ==============================================================
-- Business Question: Is there a difference in readmission rates by gender?

SELECT
    gender,
    COUNT(encounter_id)                              AS total_patients,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
WHERE gender IS NOT NULL AND gender != 'Unknown/Invalid'
GROUP BY gender
ORDER BY readmission_rate_pct DESC;

-- ==============================================================
-- QUERY 5: Readmission Rate by Race
-- ==============================================================
-- Business Question: How does readmission rate vary by race?

SELECT
    COALESCE(race, 'Unknown')                        AS race,
    COUNT(encounter_id)                              AS total_patients,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
WHERE race IS NOT NULL
GROUP BY race
ORDER BY readmission_rate_pct DESC;

-- ==============================================================
-- QUERY 6: Readmission Rate by Diabetes Medication Status
-- ==============================================================
-- Business Question: Do patients on diabetes medication have higher readmissions?

SELECT
    diabetesMed                                      AS on_diabetes_med,
    change                                           AS medication_changed,
    COUNT(encounter_id)                              AS total_patients,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
WHERE diabetesMed IS NOT NULL
GROUP BY diabetesMed, change
ORDER BY diabetesMed, change;

-- ==============================================================
-- QUERY 7: Average Hospital Stay (Overall)
-- ==============================================================
-- Business Question: What is the average length of hospital stay?

SELECT
    ROUND(AVG(time_in_hospital), 2)     AS avg_los_days,
    MIN(time_in_hospital)               AS min_los_days,
    MAX(time_in_hospital)               AS max_los_days,
    ROUND(STDDEV(time_in_hospital), 2)  AS stddev_los
FROM hospital_data;

-- ==============================================================
-- QUERY 8: Average Hospital Stay by Medical Specialty
-- ==============================================================
-- Business Question: Which specialties have the longest/shortest stays?
-- Filter: Only specialties with >= 100 patients

SELECT
    COALESCE(medical_specialty, 'Unknown')   AS medical_specialty,
    COUNT(encounter_id)                      AS patient_count,
    ROUND(AVG(time_in_hospital), 2)          AS avg_los_days,
    ROUND(AVG(num_lab_procedures), 2)        AS avg_lab_procedures,
    ROUND(AVG(num_medications), 2)           AS avg_medications
FROM hospital_data
WHERE medical_specialty IS NOT NULL
GROUP BY medical_specialty
HAVING COUNT(encounter_id) >= 100
ORDER BY avg_los_days DESC;

-- ==============================================================
-- QUERY 9: Emergency Visits vs Readmission Rate
-- ==============================================================
-- Business Question: Do patients with more emergency visits get readmitted more?

SELECT
    CASE
        WHEN number_emergency = 0 THEN '0 Emergency Visits'
        WHEN number_emergency = 1 THEN '1 Emergency Visit'
        WHEN number_emergency = 2 THEN '2 Emergency Visits'
        WHEN number_emergency = 3 THEN '3 Emergency Visits'
        ELSE '4+ Emergency Visits'
    END                                              AS emergency_category,
    COUNT(encounter_id)                              AS patient_count,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct,
    ROUND(AVG(time_in_hospital), 2)                  AS avg_los
FROM hospital_data
GROUP BY emergency_category
ORDER BY FIELD(emergency_category,
    '0 Emergency Visits','1 Emergency Visit','2 Emergency Visits',
    '3 Emergency Visits','4+ Emergency Visits');

-- ==============================================================
-- QUERY 10: Outpatient Visits vs Readmission Rate
-- ==============================================================
-- Business Question: Does prior outpatient engagement affect readmissions?

SELECT
    CASE
        WHEN number_outpatient = 0 THEN '0 Outpatient Visits'
        WHEN number_outpatient = 1 THEN '1 Outpatient Visit'
        WHEN number_outpatient = 2 THEN '2 Outpatient Visits'
        WHEN number_outpatient = 3 THEN '3 Outpatient Visits'
        ELSE '4+ Outpatient Visits'
    END                                              AS outpatient_category,
    COUNT(encounter_id)                              AS patient_count,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
GROUP BY outpatient_category
ORDER BY FIELD(outpatient_category,
    '0 Outpatient Visits','1 Outpatient Visit','2 Outpatient Visits',
    '3 Outpatient Visits','4+ Outpatient Visits');

-- ==============================================================
-- QUERY 11: Medication Count vs Hospital Stay
-- ==============================================================
-- Business Question: Do patients with more medications stay longer?

SELECT
    CASE
        WHEN num_medications <= 5  THEN 'Low (1-5 meds)'
        WHEN num_medications <= 15 THEN 'Moderate (6-15 meds)'
        WHEN num_medications <= 25 THEN 'High (16-25 meds)'
        ELSE 'Very High (26+ meds)'
    END                                              AS medication_group,
    COUNT(encounter_id)                              AS patient_count,
    ROUND(AVG(time_in_hospital), 2)                  AS avg_los_days,
    ROUND(AVG(num_medications), 2)                   AS avg_medications,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
GROUP BY medication_group
ORDER BY FIELD(medication_group,
    'Low (1-5 meds)','Moderate (6-15 meds)',
    'High (16-25 meds)','Very High (26+ meds)');

-- ==============================================================
-- QUERY 12: Diagnosis Count vs Readmission Rate
-- ==============================================================
-- Business Question: Do patients with more diagnoses get readmitted more?

SELECT
    CASE
        WHEN number_diagnoses <= 3  THEN 'Low (1-3 diagnoses)'
        WHEN number_diagnoses <= 6  THEN 'Moderate (4-6 diagnoses)'
        WHEN number_diagnoses <= 9  THEN 'High (7-9 diagnoses)'
        ELSE 'Very High (10+ diagnoses)'
    END                                              AS diagnosis_burden,
    COUNT(encounter_id)                              AS patient_count,
    ROUND(AVG(time_in_hospital), 2)                  AS avg_los,
    ROUND(AVG(num_diagnoses), 2)                     AS avg_diagnoses,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
GROUP BY diagnosis_burden
ORDER BY FIELD(diagnosis_burden,
    'Low (1-3 diagnoses)','Moderate (4-6 diagnoses)',
    'High (7-9 diagnoses)','Very High (10+ diagnoses)');

-- ==============================================================
-- QUERY 13: Top Medical Specialties by Patient Volume
-- ==============================================================
-- Business Question: Which specialties handle the most patients?

SELECT
    COALESCE(medical_specialty, 'Unknown/Not Recorded')  AS medical_specialty,
    COUNT(encounter_id)                                   AS patient_volume,
    ROUND(COUNT(encounter_id) * 100.0 /
          (SELECT COUNT(*) FROM hospital_data), 2)        AS volume_pct,
    ROUND(AVG(time_in_hospital), 2)                       AS avg_los,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)                   AS readmission_rate_pct
FROM hospital_data
GROUP BY medical_specialty
ORDER BY patient_volume DESC
LIMIT 20;

-- ==============================================================
-- QUERY 14: High-Utilization Patients
-- ==============================================================
-- Business Question: Who are the highest-utilization patients?
-- Definition: Inpatient + Outpatient + Emergency visits >= 6

SELECT
    encounter_id,
    patient_nbr,
    age,
    gender,
    COALESCE(race, 'Unknown')             AS race,
    number_inpatient,
    number_outpatient,
    number_emergency,
    (number_inpatient + number_outpatient + number_emergency) AS total_prior_visits,
    time_in_hospital,
    num_medications,
    number_diagnoses,
    readmitted
FROM hospital_data
WHERE (number_inpatient + number_outpatient + number_emergency) >= 6
ORDER BY total_prior_visits DESC, num_medications DESC
LIMIT 50;

-- Count of high-utilization patients
SELECT
    COUNT(*) AS high_utilization_patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hospital_data), 2) AS pct_of_total,
    ROUND(SUM(readmitted_binary) / COUNT(*) * 100, 2) AS readmission_rate_pct,
    ROUND(AVG(time_in_hospital), 2) AS avg_los
FROM hospital_data
WHERE (number_inpatient + number_outpatient + number_emergency) >= 6;

-- ==============================================================
-- QUERY 15: Readmission Rate by Utilization Category
-- ==============================================================
-- Business Question: How does prior utilization relate to readmission risk?

SELECT
    CASE
        WHEN (number_inpatient + number_outpatient + number_emergency) = 0
            THEN 'No Prior Utilization'
        WHEN (number_inpatient + number_outpatient + number_emergency) <= 2
            THEN 'Low (1-2 total visits)'
        WHEN (number_inpatient + number_outpatient + number_emergency) <= 5
            THEN 'Moderate (3-5 total visits)'
        ELSE 'High (6+ total visits)'
    END                                              AS utilization_category,
    COUNT(encounter_id)                              AS patient_count,
    ROUND(AVG(time_in_hospital), 2)                  AS avg_los,
    ROUND(AVG(num_medications), 2)                   AS avg_medications,
    SUM(readmitted_binary)                           AS readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
GROUP BY utilization_category
ORDER BY FIELD(utilization_category,
    'No Prior Utilization', 'Low (1-2 total visits)',
    'Moderate (3-5 total visits)', 'High (6+ total visits)');

-- ==============================================================
-- BONUS QUERY 16: Discharge Disposition vs Readmission
-- ==============================================================
-- Business Question: Does discharge destination affect readmission risk?

SELECT
    discharge_disposition_id,
    COUNT(encounter_id)                              AS patient_count,
    ROUND(AVG(time_in_hospital), 2)                  AS avg_los,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
GROUP BY discharge_disposition_id
HAVING COUNT(encounter_id) >= 50
ORDER BY readmission_rate_pct DESC;

-- ==============================================================
-- BONUS QUERY 17: Insulin Use and Readmission
-- ==============================================================
-- Business Question: How does insulin prescription affect readmission?

SELECT
    insulin,
    COUNT(encounter_id)                              AS patient_count,
    ROUND(AVG(time_in_hospital), 2)                  AS avg_los,
    ROUND(AVG(num_medications), 2)                   AS avg_medications,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)              AS readmission_rate_pct
FROM hospital_data
WHERE insulin IS NOT NULL
GROUP BY insulin
ORDER BY readmission_rate_pct DESC;

-- ==============================================================
-- BONUS QUERY 18: Specialty + Age Group Heatmap Data
-- ==============================================================
-- Business Question: Which specialty x age combinations have highest readmissions?

SELECT
    COALESCE(medical_specialty, 'Unknown') AS medical_specialty,
    age,
    COUNT(encounter_id)                    AS patient_count,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)    AS readmission_rate_pct
FROM hospital_data
WHERE medical_specialty IS NOT NULL
GROUP BY medical_specialty, age
HAVING COUNT(encounter_id) >= 50
ORDER BY readmission_rate_pct DESC
LIMIT 30;

-- ==============================================================
-- BONUS QUERY 19: Summary Dashboard KPIs
-- ==============================================================
-- Business Question: Single-row KPI summary for dashboard cards

SELECT
    COUNT(encounter_id)                                      AS total_encounters,
    COUNT(DISTINCT patient_nbr)                              AS unique_patients,
    SUM(readmitted_binary)                                   AS total_readmissions,
    ROUND(SUM(readmitted_binary) /
          COUNT(encounter_id) * 100, 2)                      AS readmission_rate_pct,
    ROUND(AVG(time_in_hospital), 2)                          AS avg_los_days,
    ROUND(AVG(num_medications), 2)                           AS avg_medications,
    ROUND(AVG(num_lab_procedures), 2)                        AS avg_lab_procedures,
    ROUND(AVG(num_procedures), 2)                            AS avg_procedures,
    ROUND(AVG(number_diagnoses), 2)                          AS avg_diagnoses,
    ROUND(AVG(number_emergency), 4)                          AS avg_emergency_visits,
    ROUND(AVG(number_outpatient), 4)                         AS avg_outpatient_visits,
    ROUND(AVG(number_inpatient), 4)                          AS avg_inpatient_visits
FROM hospital_data;
