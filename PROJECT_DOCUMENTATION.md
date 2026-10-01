# Hospital Readmission Analysis
## Improving Patient Care Through Data Analytics
### DACS08 – Hospital Administration Analysis | Portfolio Project

---

## 1. Project Title
**Hospital Readmission Analysis – Improving Patient Care Through Data Analytics**

---

## 2. Executive Summary

This project analyzes **101,766 hospital encounters** from the UCI Diabetes 130-US Hospitals dataset (1999–2008) to understand patterns of 30-day hospital readmissions. The analysis applies end-to-end data analytics including data cleaning, exploratory analysis, machine learning prediction, patient segmentation, SQL analysis, and Power BI dashboard design.

**Key Findings:**
- The overall **30-day readmission rate is 11.16%** (11,357 of 101,766 encounters)
- **High-utilization patients** (6+ prior visits) have a readmission rate of **~24%** — more than double the average
- **Emergency visit history** is the strongest signal for readmission risk
- Patients with **changed diabetes medication** show higher readmission rates
- **77.02%** of patients are on diabetes medication
- The **Random Forest model** achieves ROC-AUC = **0.669** with recall of **0.58** for 30-day readmissions

> [!IMPORTANT]
> No causation is claimed from any finding. All correlations require clinical validation before being used in patient care decisions.

---

## 3. Business Problem

The hospital administration has observed an increase in 30-day patient readmissions. Each readmission represents:
- **Patient harm** — returning to hospital indicates incomplete recovery or care gaps
- **Operational burden** — readmissions consume bed capacity and clinical resources
- **Financial exposure** — under value-based care models, excessive readmissions may incur penalties (e.g., CMS Hospital Readmissions Reduction Program)

The hospital needs a data-driven approach to identify high-risk patients, understand contributing factors, and support evidence-based interventions.

---

## 4. Business Objective

1. Quantify the 30-day readmission rate and identify at-risk patient groups
2. Understand operational patterns in hospital stay, medications, and procedures
3. Build a predictive model to flag high-risk patients
4. Identify patient segments for targeted care management
5. Deliver actionable, dashboard-ready insights to hospital leadership

---

## 5. Stakeholders

| Stakeholder | Interest |
|---|---|
| Hospital Board | Strategic performance, readmission benchmarks |
| CEO / CMO | Overall readmission rate, patient safety metrics |
| CFO | Financial impact of readmissions (penalty risk) |
| COO | Operational efficiency, bed management |
| Department Heads | Specialty-level LOS and readmission data |
| Physicians | Patient-level risk signals |
| Nursing Teams | Discharge readiness, follow-up protocols |
| Administrative Staff | Encounter documentation quality |
| Insurance / Payers | Utilization patterns, claims risk |
| Patients | Continuity of care after discharge |

---

## 6. Dataset Description

| Property | Value |
|---|---|
| **Source** | UCI ML Repository – Diabetes 130-US Hospitals (1999–2008) |
| **Kaggle Dataset** | shivavashishtha/hospital-administration-data |
| **Rows** | 101,766 encounters |
| **Columns** | 50 (original) → 56 (after derived columns) |
| **Time Period** | 1999–2008 (no specific date column available) |
| **Patient Type** | Diabetic patients admitted to 130 US hospitals |
| **Target Variable** | `readmitted` → binarized to `readmitted_binary` |

---

## 7. Data Dictionary

| Column | Type | Description |
|---|---|---|
| `encounter_id` | Integer | Unique encounter identifier |
| `patient_nbr` | Integer | Patient identifier (may repeat across encounters) |
| `race` | Categorical | Patient race (Caucasian, AfricanAmerican, Hispanic, Asian, Other; 2.23% missing) |
| `gender` | Categorical | Male / Female (3 Unknown/Invalid records) |
| `age` | Categorical | Age group in 10-year bands: [0-10) to [90-100) |
| `weight` | Categorical | Weight category in lbs – **96.87% missing** |
| `admission_type_id` | Integer | Coded type of admission (e.g., Emergency, Elective) |
| `discharge_disposition_id` | Integer | Coded discharge destination |
| `admission_source_id` | Integer | Coded source of admission |
| `time_in_hospital` | Integer | Days in hospital (1–14) |
| `payer_code` | Categorical | Insurance payer code – high missingness |
| `medical_specialty` | Categorical | Admitting specialty – **49.08% missing** |
| `num_lab_procedures` | Integer | Number of lab tests during encounter |
| `num_procedures` | Integer | Number of clinical procedures |
| `num_medications` | Integer | Number of distinct medications |
| `number_outpatient` | Integer | Prior outpatient visits (past year) |
| `number_emergency` | Integer | Prior emergency visits (past year) |
| `number_inpatient` | Integer | Prior inpatient visits (past year) |
| `diag_1`, `diag_2`, `diag_3` | String | ICD-9 primary, secondary, tertiary diagnosis codes |
| `number_diagnoses` | Integer | Total diagnoses recorded |
| `max_glu_serum` | Categorical | Glucose serum test result – **94.75% missing** |
| `A1Cresult` | Categorical | HbA1c test result – **83.28% missing** |
| `metformin` … `metformin-pioglitazone` | Categorical | 23 diabetes medication indicators: No / Steady / Up / Down |
| `change` | Categorical | Whether diabetes medication was changed (Ch / No) |
| `diabetesMed` | Categorical | Whether patient is on diabetes medication (Yes / No) |
| `readmitted` | Categorical | NO / <30 / >30 (original target) |

**Derived Columns Created:**

| Derived Column | Description |
|---|---|
| `readmitted_binary` | 1 = readmitted within 30 days; 0 = otherwise |
| `stay_category` | Short (1-2d) / Moderate (3-5d) / Long (6-8d) / Extended (9+d) |
| `medication_group` | Low (1-5) / Moderate (6-15) / High (16-25) / Very High (26+) |
| `utilization_category` | Based on sum of prior inpatient + outpatient + emergency visits |
| `diagnosis_burden` | Low / Moderate / High / Very High based on `number_diagnoses` |
| `diag1_category` | ICD-9 classified into 13 broad clinical categories |

---

## 8. Data Cleaning

### Issues Found and Actions Taken

| Issue | Count | Action |
|---|---|---|
| `weight` coded as `?` | 98,569 (96.87%) | Converted to NaN; analysis limited to 3.13% available |
| `race` coded as `?` | 2,273 (2.23%) | Converted to NaN; treated as Unknown |
| `medical_specialty` coded as `?` | 49,949 (49.08%) | Converted to NaN; filtered in specialty-level analyses |
| `gender` = `Unknown/Invalid` | 3 records | Converted to NaN |
| `max_glu_serum` all NaN | 94.75% | Retained with limitation note |
| `A1Cresult` all NaN | 83.28% | Retained with limitation note |
| Duplicate `patient_nbr` | 30,248 | Retained — same patient, multiple encounters is valid |
| Duplicate `encounter_id` | 0 | No duplicates in PK |
| Multi-class target | readmitted: NO/<30/>30 | Binarized: `readmitted_binary` = 1 if <30, else 0 |
| Rows deleted | **0** | No rows removed — dataset integrity preserved |

---

## 9. Phase 3 – EDA: Basic Questions & Results

### Q1: Readmission Rate by Age Group

| Age Group | Patients | Readmission Rate |
|---|---|---|
| [0-10) | 161 | ~7.5% |
| [20-30) | 1,657 | ~10.5% |
| [30-40) | 3,775 | ~11.2% |
| [40-50) | 9,685 | ~11.8% |
| [50-60) | 17,256 | ~12.1% |
| [60-70) | 22,483 | ~11.4% |
| [70-80) | 26,068 | ~10.8% |
| [80-90) | 17,197 | ~10.2% |
| [90-100) | 2,793 | ~9.8% |

**Insight:** Working-age adult groups (40-60) show slightly elevated readmission rates. This may reflect complexity of managing chronic diabetes alongside other conditions during peak working years.

---

### Q2: Hospital Stay by Medical Specialty

- **Longest stays:** Surgery-type specialties and complex medical specialties (Cardiology, Nephrology) exceed 5+ days average
- **Shortest stays:** Outpatient/same-day care specialties
- **Note:** 49.08% of encounters have no specialty recorded — results apply to recorded specialties only

---

### Q3: Emergency Visits vs Readmission

| Prior Emergency Visits | Readmission Rate |
|---|---|
| 0 | ~10.7% |
| 1 | ~13.5% |
| 2 | ~16.8% |
| 3 | ~18.2% |
| 4+ | ~22%+ |

**Insight:** A clear positive association exists between prior emergency visits and 30-day readmission. Patients with 3+ emergency visits are nearly twice as likely to be readmitted. This is one of the **strongest signals** in the dataset.

---

### Q4: Diabetic Medication Patients – Readmission

| Diabetes Medication | Patients | Readmission Rate |
|---|---|---|
| Yes | 78,363 (77.0%) | ~11.5% |
| No | 23,403 (23.0%) | ~9.9% |

**Insight:** Patients on diabetes medication have slightly higher readmission rates. This likely reflects greater disease complexity rather than medication effects — they are managing active diabetes, which increases overall health vulnerability.

---

### Q5: Medication Change vs Readmission

| Medication Change | Patients | Readmission Rate |
|---|---|---|
| Changed | 47,011 | ~11.8% |
| No Change | 54,755 | ~10.6% |

**Insight:** Patients with changed medications show a modestly higher readmission rate, which may indicate clinical instability at the time of discharge.

---

### Q6: Lab Procedures vs Readmission

| Lab Procedures | Readmission Rate |
|---|---|
| 1-20 | ~11.4% |
| 21-40 | ~10.8% |
| 41-60 | ~11.0% |
| 61-80 | ~11.6% |
| 80+ | ~12.1% |

**Insight:** Readmission rate is relatively consistent across lab procedure counts, with a slight uptick at very high counts. High lab test volumes may reflect monitoring of complex cases.

---

### Q7: Readmission by Race and Gender

**Race:**

| Race | Readmission Rate |
|---|---|
| AfricanAmerican | ~11.4% |
| Caucasian | ~11.1% |
| Hispanic | ~10.6% |
| Asian | ~10.1% |
| Other | ~11.0% |

**Gender:**

| Gender | Readmission Rate |
|---|---|
| Male | ~11.1% |
| Female | ~11.2% |

> [!WARNING]
> Differences by race and gender are small and should NOT be interpreted as causal. Social determinants of health (income, access to care, housing) are not available in this dataset and likely explain most observed variation.

---

### Q8: Weight Categories vs Readmission

> [!CAUTION]
> **96.87% of weight data is missing.** Results below apply to only 3.13% of patients and must be interpreted with extreme caution.

| Weight (lbs) | Patients | Readmission Rate |
|---|---|---|
| [0-25) | 48 | 16.7% |
| [25-50) | 97 | 8.3% |
| [50-75) | 897 | 11.7% |
| [75-100) | 1,336 | 11.5% |
| [100-125) | 625 | 10.7% |

No reliable conclusions can be drawn due to the high missingness.

---

### Q9: Medications vs Length of Stay

| Medication Group | Avg LOS (Days) |
|---|---|
| Low (1-5 meds) | ~2.8 |
| Moderate (6-15 meds) | ~3.8 |
| High (16-25 meds) | ~5.4 |
| Very High (26+) | ~7.2 |

**Insight:** Strong positive relationship between medication count and hospital stay length. More medications indicate greater clinical complexity, which requires longer hospital treatment.

---

### Q10: Outpatient Visits vs Readmission

| Prior Outpatient Visits | Readmission Rate |
|---|---|
| 0 | ~11.0% |
| 1 | ~11.9% |
| 2 | ~12.3% |
| 3 | ~12.8% |
| 4+ | ~13.5% |

**Insight:** Patients with more prior outpatient visits show modestly higher readmission rates, possibly reflecting ongoing disease management needs.

---

## 10. Phase 4 – Medium-Level Analysis

### M1: Time-Series Analysis
**NOT AVAILABLE** – The dataset does not contain admission dates. No trend-over-time analysis is possible.

### M2: Comorbidities vs LOS and Readmission

| Diagnosis Burden | Avg LOS | Readmission Rate |
|---|---|---|
| Low (1-3) | ~2.8 days | ~8.5% |
| Moderate (4-6) | ~3.9 days | ~9.8% |
| High (7-9) | ~4.7 days | ~11.4% |
| Very High (10+) | ~5.6 days | ~13.2% |

### M3: Discharge Disposition
`discharge_disposition_id` **IS available** in the dataset. Readmission rate varies significantly by discharge destination. Patients discharged to home generally have different outcomes than those transferred to skilled nursing facilities.

### M4: Demographics vs Lab/Medications
Minor variations in lab procedure and medication counts exist across racial groups. Most variation is likely explained by clinical factors (comorbidities, severity) rather than demographics.

### M5: Visits by Primary Diagnosis Category

| Diagnosis Category | Avg Inpatient | Avg Emergency |
|---|---|---|
| Supplementary | 1.19 | 0.08 |
| Mental Disorders | 0.75 | 0.37 |
| Diabetes | 0.89 | 0.35 |
| Circulatory | 0.56 | 0.14 |

### M6: Medication Indicators (23 medications)
Insulin has the highest usage rate (~53% of patients). Metformin, glipizide, and glyburide are also frequently prescribed. Insulin users show slightly higher readmission rates compared to non-users.

### M9: Patient Satisfaction
**NOT AVAILABLE** – No satisfaction column exists in this dataset.

---

## 11. Phase 5 – Advanced Analytics

### 11.1 Machine Learning – 30-Day Readmission Prediction

**Class Distribution:** 11.16% positive class (readmitted within 30 days) — imbalanced dataset.
**Handling:** `class_weight='balanced'` applied to all models.

**Model Results:**

| Model | ROC-AUC | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|---|
| Logistic Regression | 0.6458 | 0.6688 | 0.172 | 0.516 | 0.258 |
| Decision Tree | 0.6618 | 0.6390 | 0.174 | 0.598 | 0.270 |
| **Random Forest** | **0.6692** | 0.6552 | **0.178** | **0.580** | **0.273** |

**Best Model:** Random Forest (highest ROC-AUC and Recall)

**Top Feature Importances (Random Forest):**
1. `discharge_disposition_id` — highest impact
2. `number_inpatient` — prior inpatient visits
3. `number_emergency` — prior emergency visits
4. `time_in_hospital` — length of current stay
5. `num_lab_procedures` — clinical complexity proxy
6. `num_medications` — medication burden
7. `number_diagnoses` — comorbidity count
8. `admission_type_id` — urgency of admission

**Healthcare Recall vs Precision Trade-off:**
> In hospital readmission prediction, **Recall (0.58)** is the primary metric. A **False Negative** (missed readmission = patient not flagged for follow-up) is more harmful than a **False Positive** (unnecessary follow-up call). Clinical teams should set probability threshold based on resource availability for follow-up interventions.

**Limitation:** ROC-AUC of ~0.67 is moderate. This dataset lacks important predictors like discharge notes, vital signs, lab values, and social determinants that would improve predictive power in a real clinical setting.

---

### 11.2 Patient Segmentation (K-Means, K=4)

| Segment | Size | Avg LOS | Avg Meds | Emergency | Inpatient | Readmit Rate |
|---|---|---|---|---|---|---|
| Seg 0: Low-Acuity / Stable | 29,204 | 3.0d | 11.8 | 0.08 | 0.30 | **8.1%** |
| Seg 1: High Medication Burden | 21,745 | 8.0d | 25.2 | 0.11 | 0.51 | **12.2%** |
| Seg 2: High-Risk / Emergency-Prone | 6,705 | 4.5d | 17.3 | 1.53 | 3.69 | **24.4%** |
| Seg 3: Low-Acuity / Stable | 44,112 | 3.5d | 14.1 | 0.12 | 0.45 | **10.7%** |

**Segment Business Descriptions:**

- **Seg 0 – Low-Acuity Stable** (29K patients, 8.1% readmit): Short stays, few medications, low prior utilization. Standard discharge protocols may suffice.
- **Seg 1 – High Medication Burden** (22K patients, 12.2% readmit): Long stays, many medications, complex management. Enhanced medication reconciliation recommended.
- **Seg 2 – High-Risk Emergency-Prone** (6.7K patients, **24.4% readmit**): High prior emergency and inpatient visits. **Top priority for care management programs.**
- **Seg 3 – Moderate Stable** (44K patients, 10.7% readmit): Largest group, moderate complexity. Standard follow-up with targeted outreach for highest-risk individuals.

### 11.3 Financial Impact
**NOT AVAILABLE** — No cost, billing, or reimbursement data exists in this dataset. Financial analysis would require integration with hospital billing systems.

### 11.4 Social Determinants
**PARTIAL** — Only race, gender, and age are available. True social determinants (income, housing, food security) are absent. Differences by demographic group should not be causally attributed to those demographics without SDOH data.

---

## 12. Phase 6 – SQL Analysis

See [`phase6_sql_queries.sql`](file:///C:/Users/hariv/Downloads/files/hospital_project/phase6_sql_queries.sql) for 19 complete MySQL-compatible queries covering:
- KPI summary (Q19: single-row dashboard metrics)
- Readmission rates by all demographic and clinical dimensions
- High-utilization patient identification
- Specialty-level operational metrics
- Discharge disposition analysis
- Medication prescribing patterns

**Sample Result – KPI Summary Query:**
- Total Encounters: 101,766
- Unique Patients: 71,518
- 30-Day Readmissions: 11,357
- Readmission Rate: 11.16%
- Average LOS: 4.40 days
- Average Medications: 16.02

---

## 13. Phase 7 – Power BI Dashboard

### Page 1 – Executive Overview
**KPI Cards:** Total Encounters · Unique Patients · 30-Day Readmissions · Readmission Rate · Avg LOS · Avg Medications

**Charts:**
- Bar: Readmission Rate by Age Group
- Bar: Readmission Rate by Gender
- Bar: Readmission Rate by Race
- Bar: Readmission Rate by Diabetes Medication
- Bar: Readmission Rate by Hospital Stay Category

**Slicers:** Age Group · Gender · Race · Medical Specialty · Diabetes Medication · Readmission Status

---

### Page 2 – Patient & Readmission Analysis
- Readmission Rate by Age (bar)
- Emergency Visits vs Readmission (dual-axis: bar + line)
- Outpatient Visits vs Readmission (dual-axis)
- Inpatient Visits vs Readmission (dual-axis)
- Diagnoses vs Readmission (bar)
- Race x Gender Readmission Heatmap (matrix)

---

### Page 3 – Hospital Operations
- Avg LOS by Specialty (horizontal bar, top 15)
- Avg Lab Procedures by Specialty (bar)
- Avg Medications by Specialty (bar)
- Patient Volume by Specialty (bar)
- Stay Category Distribution (donut)
- Medication Group Distribution (bar)

---

### Page 4 – Advanced Insights
- Patient Segment Breakdown (bar: readmission by segment)
- Segment Profile Table (matrix: avg LOS, meds, emergency, readmit%)
- ML Model Performance Table (accuracy, recall, ROC-AUC)
- Feature Importance Chart (horizontal bar – top 10 features)
- Key Risk Factors Summary (text card / smart narrative)
- Recommended Actions (text card)

---

## 14. Phase 8 – DAX Measures

See [`phase8_dax_measures.dax`](file:///C:/Users/hariv/Downloads/files/hospital_project/phase8_dax_measures.dax) for 34 complete DAX measures and calculated columns including:

| Measure | Formula Logic |
|---|---|
| Total Encounters | `COUNTROWS(hospital_data)` |
| Unique Patients | `DISTINCTCOUNT(hospital_data[patient_nbr])` |
| Readmission Rate % | `DIVIDE([Total Readmissions], [Total Encounters], 0) * 100` |
| Avg Length of Stay | `AVERAGE(hospital_data[time_in_hospital])` |
| Readmission Rate Delta | Current filtered rate minus ALL() overall rate |

All `DIVIDE()` calls use 0 as the safe alternate value to prevent division-by-zero errors.

---

## 15. Key KPIs

| KPI | Value |
|---|---|
| Total Encounters | 101,766 |
| Unique Patients | 71,518 |
| 30-Day Readmissions | 11,357 |
| **30-Day Readmission Rate** | **11.16%** |
| Avg Length of Stay | 4.40 days |
| Avg Medications | 16.02 |
| Avg Lab Procedures | 43.10 |
| Avg Diagnoses | 7.42 |
| Patients on Diabetes Medication | 77.0% |
| High-Utilization Patients (6+ visits) | ~4.3% |

---

## 16. Top 10 Key Insights

### Insight 1 – Emergency Visit History is the Strongest Readmission Signal
**What the data shows:** Patients with 3+ prior emergency visits have ~18-22% readmission rate vs 10.7% for those with none.
**Why it matters:** These patients have demonstrated a pattern of acute illness that often leads to repeated hospital visits.
**Stakeholders:** CMO, Emergency Department Head, Case Managers
**Action:** Implement post-discharge care management calls for patients with 2+ prior emergency visits.

---

### Insight 2 – High-Risk Patient Segment (Seg 2) has 24.4% Readmission Rate
**What the data shows:** 6,705 patients (6.6% of total) with high prior utilization have a 24.4% readmission rate — more than double the average.
**Why it matters:** A small patient subset drives disproportionate readmissions.
**Stakeholders:** COO, Case Management Department, Hospital Board
**Action:** Prioritize this segment for a dedicated high-risk patient care management program.

---

### Insight 3 – 49.08% of Specialties are Unknown
**What the data shows:** Nearly half of encounters have no medical specialty recorded.
**Why it matters:** This is a significant data quality gap that limits specialty-level analysis.
**Stakeholders:** CIO, Administrative Staff, Department Heads
**Action:** Improve admission documentation protocols to ensure specialty is always recorded.

---

### Insight 4 – 96.87% of Weight Data is Missing
**What the data shows:** Only ~3,197 records have weight information.
**Why it matters:** Weight is an important clinical variable for diabetes management. Its near-complete absence severely limits BMI-related analysis.
**Stakeholders:** CMO, IT/EHR Team
**Action:** Mandate weight recording at every admission; integrate with EHR systems.

---

### Insight 5 – Medication Burden Strongly Correlates with Length of Stay
**What the data shows:** Patients on 26+ medications have an average LOS of ~7.2 days vs ~2.8 days for those on 1-5 medications.
**Why it matters:** High medication burden indicates clinical complexity and guides resource planning.
**Stakeholders:** COO, Department Heads, Pharmacists
**Action:** Establish pharmacy-led medication reconciliation for patients with 20+ medications.

---

### Insight 6 – 11.16% 30-Day Readmission Rate is Clinically Significant
**What the data shows:** 11,357 of 101,766 encounters resulted in readmission within 30 days.
**Why it matters:** Under value-based care, this exposes the hospital to regulatory scrutiny and potential payment penalties.
**Stakeholders:** CEO, CFO, Hospital Board
**Action:** Set a formal readmission reduction target and track quarterly progress.

---

### Insight 7 – Diabetes Patients Have Only Slightly Higher Readmission Rates
**What the data shows:** Patients on diabetes medication have ~11.5% readmission vs ~9.9% for those not on it.
**Why it matters:** Diabetes alone is not the primary readmission driver — co-existing conditions and utilization patterns matter more.
**Stakeholders:** Physicians, Endocrinology Department
**Action:** Focus on patients with diabetes PLUS high prior emergency utilization as the highest-risk combination.

---

### Insight 8 – Largest Patient Group has 3-5 Day Hospital Stays
**What the data shows:** 41,646 patients (40.9%) stayed 3-5 days.
**Why it matters:** This is the operational "core" — optimizing care transitions for moderate-stay patients has the largest system-wide impact.
**Stakeholders:** COO, Nursing Directors
**Action:** Implement structured discharge planning protocols starting at day 2 of admission.

---

### Insight 9 – The Random Forest Model Can Flag At-Risk Patients
**What the data shows:** ROC-AUC = 0.669, Recall = 0.58 — the model correctly identifies ~58% of patients who will be readmitted.
**Why it matters:** Even an imperfect model can be used to triage high-risk patients for additional follow-up.
**Stakeholders:** CMO, Data/Analytics Team, Case Management
**Action:** Deploy model in staging environment; evaluate clinical utility with a pilot program before full rollout.

---

### Insight 10 – Prior Inpatient Visits are a Key Risk Indicator
**What the data shows:** Prior inpatient visit count is the 2nd most important feature in the predictive model (after discharge disposition).
**Why it matters:** Patients who have been hospitalized before are more likely to be hospitalized again.
**Stakeholders:** Discharge Planning Team, Case Managers
**Action:** Automatically flag any patient with 2+ prior inpatient visits for enhanced discharge planning.

---

## 17. Recommendations

| # | Recommendation | Data Evidence | Stakeholder |
|---|---|---|---|
| 1 | **Implement high-risk patient care management** for Segment 2 (24.4% readmit, high emergency history) | K-Means segmentation | COO, CMO |
| 2 | **Establish post-discharge follow-up calls** within 48-72 hours for patients with 2+ prior emergency visits | Emergency visits vs readmission analysis | Case Management |
| 3 | **Pharmacy-led medication reconciliation** at discharge for patients with 20+ medications | Medication count vs LOS correlation | Pharmacists, Physicians |
| 4 | **Improve documentation quality** for medical specialty (49% missing) and weight (97% missing) | Data quality audit | Administrative Staff, IT |
| 5 | **Flag changed-medication patients** for additional monitoring (11.8% readmit vs 10.6%) | Medication change analysis | Physicians, Nurses |
| 6 | **Deploy predictive model** (Random Forest, Recall=0.58) to proactively identify high-risk patients at admission or discharge | ML model results | Analytics Team, CMO |
| 7 | **Structured discharge planning** starting day 2 for all patients (largest group is 3-5 day stays) | LOS distribution analysis | Nursing Directors |
| 8 | **Specialty-level capacity review** for high-LOS specialties (surgery, nephrology, cardiology) | Specialty LOS analysis | Department Heads |
| 9 | **Track readmission rate by utilization category** as a monthly KPI | Utilization category analysis | Hospital Board, CEO |
| 10 | **Collect SDOH data** at admission to enable more complete risk stratification | Social determinants limitation | Strategy Team |

> [!NOTE]
> None of these recommendations claim to guarantee readmission reduction. They are data-informed priorities for investigation and clinical evaluation.

---

## 18. Limitations

1. **No date fields** — Time-series trends cannot be analyzed
2. **96.87% weight missing** — BMI-based analysis not feasible
3. **49.08% medical specialty missing** — Specialty analysis covers only ~half the dataset
4. **94.75% glucose serum missing** and **83.28% A1Cresult missing** — Lab value analysis not possible
5. **Class imbalance** (11.16% positive) — ML models are inherently challenged; clinical threshold setting is needed
6. **Moderate predictive power** (AUC ~0.67) — Model performs better than random but lacks clinical variables (vital signs, lab trends, nursing notes) needed for strong prediction
7. **No cost data** — Financial impact cannot be quantified
8. **No intervention data** — Cannot evaluate whether any treatment or program reduced readmissions
9. **Historical dataset** — Data from 1999-2008; clinical practices have evolved significantly
10. **Single disease focus** — Dataset is diabetic patients only; findings should not be generalized to all hospital patients

---

## 19. Ethical and Privacy Considerations

1. **Data anonymization** — The dataset uses encounter IDs and patient numbers; no actual names, dates of birth, or direct identifiers are present
2. **Racial disparities** — Small observed differences in readmission rates across racial groups should never be used to deny or deprioritize care
3. **Predictive model bias** — The ML model should be monitored for disparate impact across demographic groups before any clinical deployment
4. **No medical decisions** — This analysis is for operational planning only; clinical decisions must remain with licensed healthcare providers
5. **Patient privacy** — Any real-world application must comply with HIPAA and applicable data protection regulations
6. **SDOH framing** — Demographic differences in outcomes likely reflect structural inequities in healthcare access, not inherent group characteristics

---

## 20. Conclusion

This project demonstrates a complete data analytics pipeline applied to hospital readmission data:

- **101,766 encounters** analyzed across 50+ clinical and demographic variables
- **11.16%** 30-day readmission rate established as baseline benchmark
- **Emergency visit history** and **prior inpatient visits** identified as strongest readmission indicators
- A **high-risk patient segment** (6.6% of patients, 24.4% readmit rate) identified for priority intervention
- **Random Forest model** (AUC=0.669, Recall=0.58) built as a clinical decision support tool
- **19 SQL queries** written for operational reporting
- **34 DAX measures** designed for Power BI dashboard implementation
- **4-page Power BI dashboard** designed covering executive, patient, operational, and advanced analytics views

The project is structured for portfolio presentation, GitHub documentation, Power BI portfolio, and Data Analyst interview discussion.

---

*Project by: [Your Name] | Dataset: UCI Diabetes 130-US Hospitals | Tools: Python, SQL, Power BI, Scikit-learn*
