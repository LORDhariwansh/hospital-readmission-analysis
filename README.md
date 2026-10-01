# Hospital Readmission Analysis
## Improving Patient Care Through Data Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow.svg)](https://powerbi.microsoft.com)
[![MySQL](https://img.shields.io/badge/MySQL-Compatible-orange.svg)](https://mysql.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green.svg)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## Project Overview

A **portfolio-level Data Analytics project** analyzing 101,766 hospital encounters from the UCI Diabetes 130-US Hospitals dataset to identify patterns and risk factors associated with 30-day patient readmissions.

**Project Title:** DACS08 – Hospital Administration Analysis  
**Dataset:** [UCI Diabetes 130-US Hospitals (1999–2008)](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)  
**Tools:** Python · SQL · Power BI · scikit-learn  

---

## Business Problem

A hospital is experiencing increased 30-day patient readmissions. The goal is to:
- Identify patient groups at high risk of readmission
- Understand operational patterns (LOS, medications, procedures)
- Build predictive models to support proactive care management
- Provide dashboard-ready insights for hospital leadership

---

## Key Results

| Metric | Value |
|---|---|
| Total Encounters Analyzed | 101,766 |
| Unique Patients | 71,518 |
| 30-Day Readmission Rate | **11.16%** |
| Average Length of Stay | 4.40 days |
| Best Model ROC-AUC | **0.669 (Random Forest)** |
| Best Model Recall | **0.58** |
| High-Risk Segment Readmit Rate | **24.4%** |

---

## Project Structure

```
hospital_project/
│
├── diabetic_data.csv               # Raw dataset (UCI)
├── diabetic_data_cleaned.csv       # Cleaned dataset (Phase 2 output)
│
├── phase1_2_eda.py                 # Phase 1: Data Understanding
│                                   # Phase 2: Data Cleaning
│
├── phase3_4_eda.py                 # Phase 3: Exploratory Data Analysis (10 questions)
│                                   # Phase 4: Medium-Level Analysis
│
├── phase5_advanced.py              # Phase 5: Machine Learning + Clustering
│
├── phase6_sql_queries.sql          # Phase 6: 19 MySQL-compatible SQL queries
│
├── phase8_dax_measures.dax         # Phase 8: 34 Power BI DAX measures
│
├── PROJECT_DOCUMENTATION.md        # Full 20-section project report
├── README.md                       # This file
│
└── plots/                          # All visualizations (PNG)
    ├── q1_readmit_by_age.png
    ├── q2_los_by_specialty.png
    ├── q3_emergency_vs_readmit.png
    ├── q4_diabetes_med_readmit.png
    ├── q5_med_change_readmit.png
    ├── q6_lab_proc_readmit.png
    ├── q7_race_gender_readmit.png
    ├── q8_weight_readmit.png
    ├── q9_medications_vs_los.png
    ├── q10_outpatient_readmit.png
    ├── m2_diagnosis_burden.png
    ├── m5_visits_by_diagnosis.png
    ├── m6_medication_readmit_comparison.png
    ├── ml_model_comparison.png
    ├── ml_roc_curves.png
    ├── ml_confusion_matrix_rf.png
    ├── ml_feature_importance.png
    ├── kmeans_elbow.png
    ├── kmeans_segments_pca.png
    ├── kmeans_segment_readmit.png
    ├── model_metrics.csv
    ├── patient_segments.csv
    └── data_quality_summary.csv
```

---

## Dataset Description

**Source:** UCI Machine Learning Repository – Diabetes 130-US Hospitals for Years 1999-2008  
**Size:** 101,766 rows × 50 columns  
**Type:** Diabetic patient encounters at 130 US hospitals

**Key Columns Used:**

| Column | Type | Description |
|---|---|---|
| `encounter_id` | Integer | Unique encounter ID |
| `patient_nbr` | Integer | Patient ID |
| `race` / `gender` / `age` | Categorical | Demographics |
| `time_in_hospital` | Integer | Days in hospital (1-14) |
| `num_lab_procedures` | Integer | Lab tests performed |
| `num_medications` | Integer | Medications prescribed |
| `number_emergency` | Integer | Prior emergency visits |
| `number_inpatient` | Integer | Prior inpatient stays |
| `number_diagnoses` | Integer | Diagnoses count |
| `readmitted` | Categorical | NO / <30 / >30 |
| `readmitted_binary` | Integer | 1 = readmitted within 30d |

**Important Data Quality Notes:**
- Weight: 96.87% missing
- Medical specialty: 49.08% missing
- No date fields → no time-series analysis possible
- No cost/billing data → no financial analysis possible

---

## Project Phases

### Phase 1 – Data Understanding
- 50 columns, 101,766 rows
- Data quality summary table generated
- Invalid `?` values identified in race, weight, medical_specialty, diag fields

### Phase 2 – Data Cleaning
- `?` converted to NaN (no rows deleted)
- Binary target `readmitted_binary` created
- 5 derived columns: stay_category, medication_group, utilization_category, diagnosis_burden, diag1_category

### Phase 3 – EDA (10 Basic Questions)
Readmission analyzed by: age group, medical specialty, emergency visits, diabetes medication, medication change, lab procedures, race, gender, weight, outpatient visits

### Phase 4 – Medium-Level Analysis
- Time-series: NOT AVAILABLE (no date field)
- Diagnosis burden vs LOS and readmission
- Medication prescribing patterns (23 diabetes medications)
- Demographics vs lab/medication averages
- Patient satisfaction: NOT AVAILABLE

### Phase 5 – Advanced Analytics
**Machine Learning (30-Day Readmission Prediction):**

| Model | ROC-AUC | Recall | F1 |
|---|---|---|---|
| Logistic Regression | 0.6458 | 0.516 | 0.258 |
| Decision Tree | 0.6618 | 0.598 | 0.270 |
| **Random Forest** | **0.6692** | **0.580** | **0.273** |

**Patient Segmentation (K-Means, K=4):**

| Segment | Size | Readmit Rate |
|---|---|---|
| Low-Acuity Stable | 29,204 | 8.1% |
| High Medication Burden | 21,745 | 12.2% |
| **High-Risk Emergency-Prone** | **6,705** | **24.4%** |
| Moderate Stable | 44,112 | 10.7% |

**Financial Analysis:** Not available (no cost data)  
**Social Determinants:** Partial (demographics only; no SDOH data)

### Phase 6 – SQL Analysis
19 MySQL-compatible queries including:
- Dashboard KPI summary
- Readmission rate by all dimensions
- High-utilization patient identification
- Specialty operational metrics

### Phase 7 – Power BI Dashboard
4-page professional dashboard:
1. **Executive Overview** – KPIs + Readmission by Demographics
2. **Patient & Readmission Analysis** – Detailed readmission breakdown
3. **Hospital Operations** – LOS, Lab Procedures, Medications by Specialty
4. **Advanced Insights** – ML results, Segments, Risk Factors

### Phase 8 – DAX Measures
34 DAX measures and calculated columns including all KPIs, percentage measures, segmentation measures, and safe DIVIDE() handling.

---

## Top 10 Insights

1. **Emergency visit history** is the strongest readmission predictor (22%+ for 4+ visits)
2. **High-risk segment** (24.4% readmit) represents 6.6% of patients
3. **49.08% specialty data missing** — major documentation gap
4. **96.87% weight data missing** — critical clinical variable absent
5. **Medication burden** strongly predicts length of stay
6. **11.16%** overall 30-day readmission rate as a baseline
7. Diabetes medication alone is a weak predictor — co-morbidities matter more
8. **Moderate-stay patients (3-5 days)** are the largest group — highest operational impact
9. Random Forest model can flag **~58%** of future readmissions
10. **Prior inpatient visits** is the 2nd most important model feature

---

## Recommendations

1. Implement high-risk care management for Segment 2 (emergency-prone patients)
2. Post-discharge follow-up calls within 48-72 hours for 2+ emergency history patients
3. Pharmacy-led medication reconciliation for 20+ medication patients
4. Improve documentation: specialty and weight fields at every admission
5. Flag medication-changed patients for enhanced monitoring
6. Deploy predictive model in staging for pilot clinical use
7. Implement structured discharge planning starting day 2
8. Monthly readmission rate tracking by utilization category as board KPI

---

## How to Run

### Requirements
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Run All Phases
```bash
# Windows - Set UTF-8 encoding
$env:PYTHONUTF8=1

# Phase 1 & 2 - Data Understanding and Cleaning
python phase1_2_eda.py

# Phase 3 & 4 - EDA
python phase3_4_eda.py

# Phase 5 - Machine Learning and Clustering
python phase5_advanced.py
```

### SQL
Import `diabetic_data_cleaned.csv` into MySQL as `hospital_data` and run `phase6_sql_queries.sql`.

### Power BI
1. Load `diabetic_data_cleaned.csv` into Power BI Desktop
2. Add calculated columns from `phase8_dax_measures.dax`
3. Create measures from the same file
4. Build visuals per the 4-page dashboard layout in [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## Limitations

- No date fields → no time-series analysis
- 96.87% weight data missing
- 49.08% specialty data missing
- No cost or billing data → no financial analysis
- ROC-AUC of 0.67 → moderate predictive power (lacks clinical features like vitals, lab values)
- Historical data (1999–2008) — medical practices have evolved
- Diabetic patients only — findings not generalizable to all hospital populations

---

## Ethical Considerations

- No personal identifiers used
- Race/gender differences should never be used to deprioritize care
- Predictive model must be monitored for disparate impact before clinical deployment
- All clinical decisions remain with licensed healthcare providers
- HIPAA compliance required for real-world deployment

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Python 3.11+ | Data cleaning, EDA, visualization, ML |
| pandas | Data manipulation |
| matplotlib / seaborn | Visualization |
| scikit-learn | Machine learning, clustering |
| MySQL | SQL analysis |
| Power BI Desktop | Dashboard and DAX |

---

## Author

**[Your Name]**  
Data Analyst | Healthcare Analytics Enthusiast  
LinkedIn: [your-linkedin]  
GitHub: [your-github]  

---

## License

This project is licensed under the MIT License.  
Dataset: UCI Machine Learning Repository (Public Domain)

---

*Dataset Source: Beata Strack, Jonathan P. DeShazo, Chris Gennings, et al. "Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records." BioMed Research International. 2014.*
