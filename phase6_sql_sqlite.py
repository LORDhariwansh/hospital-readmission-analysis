"""
==============================================================
HOSPITAL READMISSION ANALYSIS
Phase 6 – SQL Analysis using SQLite (no MySQL install needed)
SQLite is built into Python – zero installation required!
==============================================================
"""

import sqlite3
import pandas as pd
import os

# ── Setup ──────────────────────────────────────────────────────
CSV_PATH = "C:/Users/hariv/Downloads/files/hospital_project/diabetic_data_cleaned.csv"
DB_PATH  = "C:/Users/hariv/Downloads/files/hospital_project/hospital_data.db"
OUT_DIR  = "C:/Users/hariv/Downloads/files/hospital_project/plots"
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print(" PHASE 6 – SQL ANALYSIS (SQLite)")
print("=" * 60)

# ── Load CSV into SQLite ───────────────────────────────────────
print("\nLoading data into SQLite database...")
df = pd.read_csv(CSV_PATH)
conn = sqlite3.connect(DB_PATH)
df.to_sql("hospital_data", conn, if_exists="replace", index=False)
print(f"  Loaded {len(df):,} rows into SQLite table: hospital_data")
print(f"  Database saved to: {DB_PATH}")


def run_query(title, sql, top_n=None):
    """Helper to run and print a query result."""
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")
    result = pd.read_sql_query(sql, conn)
    if top_n:
        result = result.head(top_n)
    print(result.to_string(index=False))
    return result


# ──────────────────────────────────────────────────────────────
# Q1: Total Patients and Encounters
# ──────────────────────────────────────────────────────────────
run_query("Q1: Total Encounters and Unique Patients", """
    SELECT
        COUNT(encounter_id)          AS total_encounters,
        COUNT(DISTINCT patient_nbr)  AS unique_patients
    FROM hospital_data;
""")

# ──────────────────────────────────────────────────────────────
# Q2: Overall 30-Day Readmission Rate
# ──────────────────────────────────────────────────────────────
run_query("Q2: Overall 30-Day Readmission Rate", """
    SELECT
        SUM(readmitted_binary)                                       AS total_readmissions,
        COUNT(*)                                                     AS total_encounters,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)         AS readmission_rate_pct
    FROM hospital_data;
""")

# ──────────────────────────────────────────────────────────────
# Q3: Readmission Rate by Age Group
# ──────────────────────────────────────────────────────────────
run_query("Q3: Readmission Rate by Age Group", """
    SELECT
        age                                                           AS age_group,
        COUNT(*)                                                      AS patient_count,
        SUM(readmitted_binary)                                        AS readmissions,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY age
    ORDER BY age;
""")

# ──────────────────────────────────────────────────────────────
# Q4: Readmission Rate by Gender
# ──────────────────────────────────────────────────────────────
run_query("Q4: Readmission Rate by Gender", """
    SELECT
        gender,
        COUNT(*)                                                      AS patient_count,
        SUM(readmitted_binary)                                        AS readmissions,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    WHERE gender IS NOT NULL AND gender != ''
    GROUP BY gender
    ORDER BY readmission_rate_pct DESC;
""")

# ──────────────────────────────────────────────────────────────
# Q5: Readmission Rate by Race
# ──────────────────────────────────────────────────────────────
run_query("Q5: Readmission Rate by Race", """
    SELECT
        race,
        COUNT(*)                                                      AS patient_count,
        SUM(readmitted_binary)                                        AS readmissions,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    WHERE race IS NOT NULL AND race != ''
    GROUP BY race
    ORDER BY readmission_rate_pct DESC;
""")

# ──────────────────────────────────────────────────────────────
# Q6: Readmission Rate by Diabetes Medication + Change
# ──────────────────────────────────────────────────────────────
run_query("Q6: Readmission by Diabetes Medication and Change Status", """
    SELECT
        diabetesMed                                                   AS diabetes_medication,
        change                                                        AS med_change,
        COUNT(*)                                                      AS patient_count,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY diabetesMed, change
    ORDER BY readmission_rate_pct DESC;
""")

# ──────────────────────────────────────────────────────────────
# Q7: Average Length of Stay Overall
# ──────────────────────────────────────────────────────────────
run_query("Q7: Average Length of Stay", """
    SELECT
        ROUND(AVG(time_in_hospital), 2)                              AS avg_los_days,
        MIN(time_in_hospital)                                        AS min_los_days,
        MAX(time_in_hospital)                                        AS max_los_days,
        ROUND(AVG(num_medications), 2)                               AS avg_medications,
        ROUND(AVG(num_lab_procedures), 2)                            AS avg_lab_procedures,
        ROUND(AVG(number_diagnoses), 2)                              AS avg_diagnoses
    FROM hospital_data;
""")

# ──────────────────────────────────────────────────────────────
# Q8: Average LOS by Medical Specialty (min 100 patients)
# ──────────────────────────────────────────────────────────────
run_query("Q8: Average LOS by Medical Specialty (Top 15, min 100 patients)", """
    SELECT
        medical_specialty,
        COUNT(*)                                                      AS patient_count,
        ROUND(AVG(time_in_hospital), 2)                              AS avg_los_days,
        ROUND(AVG(num_lab_procedures), 2)                            AS avg_lab_procedures,
        ROUND(AVG(num_medications), 2)                               AS avg_medications
    FROM hospital_data
    WHERE medical_specialty IS NOT NULL AND medical_specialty != ''
    GROUP BY medical_specialty
    HAVING COUNT(*) >= 100
    ORDER BY avg_los_days DESC
    LIMIT 15;
""")

# ──────────────────────────────────────────────────────────────
# Q9: Emergency Visits vs Readmission
# ──────────────────────────────────────────────────────────────
run_query("Q9: Emergency Visits vs Readmission Rate", """
    SELECT
        CASE
            WHEN number_emergency = 0 THEN '0 Visits'
            WHEN number_emergency = 1 THEN '1 Visit'
            WHEN number_emergency = 2 THEN '2 Visits'
            WHEN number_emergency = 3 THEN '3 Visits'
            ELSE '4+ Visits'
        END                                                           AS emergency_visits,
        COUNT(*)                                                      AS patient_count,
        SUM(readmitted_binary)                                        AS readmissions,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY emergency_visits
    ORDER BY readmission_rate_pct;
""")

# ──────────────────────────────────────────────────────────────
# Q10: Outpatient Visits vs Readmission
# ──────────────────────────────────────────────────────────────
run_query("Q10: Outpatient Visits vs Readmission Rate", """
    SELECT
        CASE
            WHEN number_outpatient = 0 THEN '0 Visits'
            WHEN number_outpatient BETWEEN 1 AND 2 THEN '1-2 Visits'
            WHEN number_outpatient BETWEEN 3 AND 5 THEN '3-5 Visits'
            ELSE '6+ Visits'
        END                                                           AS outpatient_visits,
        COUNT(*)                                                      AS patient_count,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY outpatient_visits
    ORDER BY readmission_rate_pct;
""")

# ──────────────────────────────────────────────────────────────
# Q11: Medication Count vs Hospital Stay
# ──────────────────────────────────────────────────────────────
run_query("Q11: Medication Group vs Avg Length of Stay", """
    SELECT
        medication_group,
        COUNT(*)                                                      AS patient_count,
        ROUND(AVG(time_in_hospital), 2)                              AS avg_los_days,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY medication_group
    ORDER BY avg_los_days;
""")

# ──────────────────────────────────────────────────────────────
# Q12: Diagnosis Count vs Readmission
# ──────────────────────────────────────────────────────────────
run_query("Q12: Diagnosis Burden vs Readmission + LOS", """
    SELECT
        diagnosis_burden,
        COUNT(*)                                                      AS patient_count,
        ROUND(AVG(time_in_hospital), 2)                              AS avg_los_days,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY diagnosis_burden
    ORDER BY avg_los_days;
""")

# ──────────────────────────────────────────────────────────────
# Q13: Top Specialties by Patient Volume
# ──────────────────────────────────────────────────────────────
run_query("Q13: Top 15 Specialties by Patient Volume", """
    SELECT
        medical_specialty,
        COUNT(*)                                                      AS patient_count,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct,
        ROUND(AVG(time_in_hospital), 2)                              AS avg_los_days
    FROM hospital_data
    WHERE medical_specialty IS NOT NULL AND medical_specialty != ''
    GROUP BY medical_specialty
    ORDER BY patient_count DESC
    LIMIT 15;
""")

# ──────────────────────────────────────────────────────────────
# Q14: High Utilization Patients (6+ prior visits)
# ──────────────────────────────────────────────────────────────
run_query("Q14: High-Utilization Patients (6+ prior visits) – Sample 10", """
    SELECT
        encounter_id,
        patient_nbr,
        age,
        race,
        gender,
        number_inpatient,
        number_outpatient,
        number_emergency,
        (number_inpatient + number_outpatient + number_emergency) AS total_prior_visits,
        time_in_hospital,
        readmitted_binary
    FROM hospital_data
    WHERE (number_inpatient + number_outpatient + number_emergency) >= 6
    ORDER BY total_prior_visits DESC
    LIMIT 10;
""")

# ──────────────────────────────────────────────────────────────
# Q15: Readmission Rate by Utilization Category
# ──────────────────────────────────────────────────────────────
run_query("Q15: Readmission Rate by Utilization Category", """
    SELECT
        utilization_category,
        COUNT(*)                                                      AS patient_count,
        SUM(readmitted_binary)                                        AS readmissions,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY utilization_category
    ORDER BY readmission_rate_pct DESC;
""")

# ──────────────────────────────────────────────────────────────
# Q16: Discharge Disposition vs Readmission (Top 10 highest)
# ──────────────────────────────────────────────────────────────
run_query("Q16: Discharge Disposition vs Readmission (Top 10)", """
    SELECT
        discharge_disposition_id,
        COUNT(*)                                                      AS patient_count,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY discharge_disposition_id
    HAVING COUNT(*) >= 50
    ORDER BY readmission_rate_pct DESC
    LIMIT 10;
""")

# ──────────────────────────────────────────────────────────────
# Q17: Insulin Use and Readmission
# ──────────────────────────────────────────────────────────────
run_query("Q17: Insulin Use vs Readmission Rate", """
    SELECT
        CASE WHEN insulin = 'No' THEN 'Not Using Insulin'
             ELSE 'Using Insulin' END                                 AS insulin_status,
        COUNT(*)                                                      AS patient_count,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    WHERE insulin IS NOT NULL
    GROUP BY insulin_status
    ORDER BY readmission_rate_pct DESC;
""")

# ──────────────────────────────────────────────────────────────
# Q18: Stay Category vs Readmission
# ──────────────────────────────────────────────────────────────
run_query("Q18: Hospital Stay Category vs Readmission", """
    SELECT
        stay_category,
        COUNT(*)                                                      AS patient_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hospital_data), 2) AS pct_of_total,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct
    FROM hospital_data
    GROUP BY stay_category
    ORDER BY readmission_rate_pct;
""")

# ──────────────────────────────────────────────────────────────
# Q19: Complete KPI Dashboard Summary (one row)
# ──────────────────────────────────────────────────────────────
run_query("Q19: DASHBOARD KPI SUMMARY (Single Row)", """
    SELECT
        COUNT(encounter_id)                                                AS total_encounters,
        COUNT(DISTINCT patient_nbr)                                        AS unique_patients,
        SUM(readmitted_binary)                                             AS total_readmissions,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)               AS readmission_rate_pct,
        ROUND(AVG(time_in_hospital), 2)                                    AS avg_los_days,
        ROUND(AVG(num_medications), 2)                                     AS avg_medications,
        ROUND(AVG(num_lab_procedures), 2)                                  AS avg_lab_procedures,
        ROUND(AVG(number_diagnoses), 2)                                    AS avg_diagnoses,
        ROUND(AVG(number_emergency), 4)                                    AS avg_emergency_visits,
        ROUND(AVG(number_outpatient), 4)                                   AS avg_outpatient_visits,
        ROUND(AVG(number_inpatient), 4)                                    AS avg_inpatient_visits
    FROM hospital_data;
""")

# ── Save all results to a CSV ──────────────────────────────────
print("\n" + "=" * 60)
print(" Saving SQL results summary to CSV...")
summary_sql = """
    SELECT
        age                                                           AS dimension,
        COUNT(*)                                                      AS patient_count,
        ROUND(SUM(readmitted_binary) * 100.0 / COUNT(*), 2)          AS readmission_rate_pct,
        ROUND(AVG(time_in_hospital), 2)                              AS avg_los,
        ROUND(AVG(num_medications), 2)                               AS avg_medications
    FROM hospital_data
    GROUP BY age
    ORDER BY age;
"""
summary_df = pd.read_sql_query(summary_sql, conn)
summary_df.to_csv(f"{OUT_DIR}/sql_results_by_age.csv", index=False)
print(f"  Saved: sql_results_by_age.csv")

conn.close()
print("\n" + "=" * 60)
print(" PHASE 6 SQL ANALYSIS COMPLETE!")
print(f" Database file: {DB_PATH}")
print(" All 19 queries executed successfully.")
print("=" * 60)
