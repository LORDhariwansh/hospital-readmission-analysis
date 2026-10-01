# Hospital Readmission Analysis – Complete Project Summary
## DACS08 | Portfolio Project | Data Analyst

---

## A. Complete Project Summary

### What Was Built
A full end-to-end data analytics project across 12 phases using 101,766 real hospital encounter records from the UCI Diabetes 130-US Hospitals dataset (1999–2008).

### What Was Found (Actual Numbers from Dataset)

| Metric | Actual Value |
|---|---|
| Total encounters | 101,766 |
| Unique patients | 71,518 |
| 30-day readmissions | 11,357 |
| **30-day readmission rate** | **11.16%** |
| Avg length of stay | 4.40 days |
| Avg medications | 16.02 |
| Avg lab procedures | 43.10 |
| Avg diagnoses | 7.42 |
| Patients on diabetes medication | 77.0% |
| Weight data missing | **96.87%** |
| Medical specialty missing | **49.08%** |
| Best ML model ROC-AUC | **0.669 (Random Forest)** |
| High-risk segment readmit rate | **24.4%** |

### Phases Completed
1. ✅ Data Understanding (50 cols, data quality table)
2. ✅ Data Cleaning (no rows deleted; 6 derived columns added)
3. ✅ EDA – 10 Basic Questions (actual calculations + charts)
4. ✅ Medium-Level Analysis (7 analyses; 2 marked unavailable)
5. ✅ Advanced Analytics (3 ML models + K-Means K=4)
6. ✅ SQL Analysis (19 MySQL queries)
7. ✅ Power BI Dashboard Design (4 pages)
8. ✅ DAX Measures (34 measures + calculated columns)
9. ✅ Visualization (20 professional charts)
10. ✅ Business Insights (Top 10)
11. ✅ Recommendations (10 data-driven)
12. ✅ Project Documentation (20-section report)

---

## B. Power BI Dashboard Layout

### Page 1 – Executive Overview

```
┌─────────────────────────────────────────────────────────────┐
│  HOSPITAL READMISSION ANALYSIS | Executive Overview          │
├───────────┬──────────────┬──────────────┬────────────────────┤
│ Slicers:  │ Age Group    │ Gender       │ Race               │
│           │ Medical Spec │ Diabetes Med │ Readmission Status │
├───────────┴──────────────┴──────────────┴────────────────────┤
│  KPI CARDS (Row 1):                                          │
│  [Total Encounters]  [Unique Patients]  [30-Day Readmissions]│
│     101,766              71,518              11,357           │
│                                                              │
│  KPI CARDS (Row 2):                                          │
│  [Readmission Rate%] [Avg LOS Days]    [Avg Medications]    │
│      11.16%              4.40               16.02            │
├──────────────────────────────┬──────────────────────────────┤
│ Bar: Readmit Rate by Age (L) │ Bar: Readmit by Gender (R)   │
├──────────────────────────────┼──────────────────────────────┤
│ Bar: Readmit by Race (L)     │ Bar: Readmit by DiabMed (R)  │
├──────────────────────────────┴──────────────────────────────┤
│      Bar: Readmission Rate by Hospital Stay Category         │
└─────────────────────────────────────────────────────────────┘
```

### Page 2 – Patient & Readmission Analysis

```
┌─────────────────────────────────────────────────────────────┐
│  PATIENT & READMISSION ANALYSIS                              │
├──────────────────────────────┬──────────────────────────────┤
│ Dual-Axis: Emergency Visits  │ Dual-Axis: Outpatient Visits │
│ (Bar=Count + Line=Readmit%)  │ (Bar=Count + Line=Readmit%)  │
├──────────────────────────────┼──────────────────────────────┤
│ Dual-Axis: Inpatient Visits  │ Bar: Diagnoses vs Readmit%   │
├──────────────────────────────┴──────────────────────────────┤
│ Matrix Heatmap: Race x Gender – Readmission Rate %          │
│      (Conditional formatting: Red=High, Green=Low)          │
├─────────────────────────────────────────────────────────────┤
│ Table: Top 20 Specialty Readmission Rates (filtered to 100+)│
└─────────────────────────────────────────────────────────────┘
```

### Page 3 – Hospital Operations

```
┌─────────────────────────────────────────────────────────────┐
│  HOSPITAL OPERATIONS                                         │
├──────────────────────────────┬──────────────────────────────┤
│ Horizontal Bar:              │ Bar:                         │
│ Avg LOS by Specialty (Top15) │ Patient Volume by Specialty  │
├──────────────────────────────┼──────────────────────────────┤
│ Bar: Avg Lab Procedures      │ Bar: Avg Medications         │
│ by Specialty                 │ by Specialty                 │
├──────────────────────────────┴──────────────────────────────┤
│ Donut: Hospital Stay Category Distribution                   │
│  Short 30.9% | Moderate 40.9% | Long 17.5% | Extended 10.7%│
├─────────────────────────────────────────────────────────────┤
│ Bar: Medication Count Group Distribution                     │
└─────────────────────────────────────────────────────────────┘
```

### Page 4 – Advanced Insights

```
┌─────────────────────────────────────────────────────────────┐
│  ADVANCED INSIGHTS                                           │
├──────────────────────────────┬──────────────────────────────┤
│ Bar: Readmission by Segment  │ Table: Segment Profiles      │
│  Seg0:8.1% Seg1:12.2%       │  (LOS, Meds, Emerg, Readmit) │
│  Seg2:24.4% Seg3:10.7%      │                              │
├──────────────────────────────┼──────────────────────────────┤
│ Table: ML Model Performance  │ Bar: Top 10 Features (RF)    │
│  LR: AUC=0.646 Recall=0.516  │  discharge_disposition_id    │
│  DT: AUC=0.662 Recall=0.598  │  number_inpatient            │
│  RF: AUC=0.669 Recall=0.580  │  number_emergency            │
│  (Highlight: RECALL most     │  time_in_hospital            │
│   important in healthcare)   │  ...                         │
├──────────────────────────────┴──────────────────────────────┤
│ Smart Narrative / Text Card: Key Risk Factors                │
│ • Emergency visit history • Prior hospitalizations          │
│ • Medication burden • Diagnosis complexity                   │
├─────────────────────────────────────────────────────────────┤
│ Text Card: Recommended Actions (5 bullet points)            │
└─────────────────────────────────────────────────────────────┘
```

---

## C. SQL Queries Summary

19 MySQL queries in `phase6_sql_queries.sql`:

| Query | Business Question |
|---|---|
| Q1 | Total patients and encounters |
| Q2 | Overall 30-day readmission rate |
| Q3 | Readmission rate by age group |
| Q4 | Readmission rate by gender |
| Q5 | Readmission rate by race |
| Q6 | Readmission rate by diabetes medication + change |
| Q7 | Average LOS overall |
| Q8 | Average LOS by specialty (100+ patients) |
| Q9 | Emergency visits vs readmission |
| Q10 | Outpatient visits vs readmission |
| Q11 | Medication count vs hospital stay |
| Q12 | Diagnosis count vs readmission |
| Q13 | Top specialties by patient volume |
| Q14 | High-utilization patient list (6+ prior visits) |
| Q15 | Readmission rate by utilization category |
| B16 | Discharge disposition vs readmission |
| B17 | Insulin use and readmission |
| B18 | Specialty x Age group heatmap data |
| B19 | Single-row KPI summary for dashboard |

---

## D. DAX Measures Summary

34 measures in `phase8_dax_measures.dax`:

**Core KPIs:**
```dax
Total Encounters = COUNTROWS(hospital_data)
Unique Patients = DISTINCTCOUNT(hospital_data[patient_nbr])
Total Readmissions = CALCULATE(COUNTROWS(hospital_data), hospital_data[readmitted_binary] = 1)
Readmission Rate % = DIVIDE([Total Readmissions], [Total Encounters], 0) * 100
Avg Length of Stay = AVERAGE(hospital_data[time_in_hospital])
Avg Medications = AVERAGE(hospital_data[num_medications])
```

**Segmentation:**
```dax
Readmission Rate - High Utilization % = 
CALCULATE([Readmission Rate %], 
    hospital_data[number_inpatient] + hospital_data[number_outpatient] 
    + hospital_data[number_emergency] >= 6)
```

**Calculated Columns:**
```dax
Stay Category = SWITCH(TRUE(),
    hospital_data[time_in_hospital] <= 2, "1-2 Days (Short)",
    hospital_data[time_in_hospital] <= 5, "3-5 Days (Moderate)",
    hospital_data[time_in_hospital] <= 8, "6-8 Days (Long)",
    "9+ Days (Extended)")
```

All `DIVIDE()` calls use 0 as the alternate result to prevent division-by-zero errors.

---

## E. Python EDA Code Summary

**Files:** `phase1_2_eda.py`, `phase3_4_eda.py`, `phase5_advanced.py`

**Libraries:** pandas, numpy, matplotlib, seaborn, scikit-learn

**Key code patterns:**

```python
# Binary target creation
df['readmitted_binary'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)

# Readmission rate by group
df.groupby('age')['readmitted_binary'].agg(['mean','count']).mul(100).round(2)

# ICD-9 classification
def classify_diag(code):
    n = float(code)
    if 390 <= n <= 459: return 'Circulatory'
    elif 250 <= n <= 250.99: return 'Diabetes'
    # ... etc
```

---

## F. Machine Learning Code Summary

**File:** `phase5_advanced.py`

**Pipeline:**
1. Feature selection (11 numeric + 13 categorical = 24 features)
2. LabelEncoder for categoricals; median imputation for numerics
3. StandardScaler for Logistic Regression
4. Train/test split: 80/20, stratified
5. class_weight='balanced' for class imbalance
6. Metrics: Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix

**Key Results:**
```
Model               | ROC-AUC | Accuracy | Recall  | F1
Logistic Regression | 0.6458  | 0.6688   | 0.5161  | 0.258
Decision Tree       | 0.6618  | 0.6390   | 0.5980  | 0.270
Random Forest       | 0.6692  | 0.6552   | 0.5795  | 0.273
```

**Clustering:**
```python
km = KMeans(n_clusters=4, random_state=42, n_init=10)
df['patient_segment'] = km.fit_predict(X_scaled)
```

---

## G. Key Insights (Top 10)

1. **Emergency history = top readmission predictor** → 22%+ readmit rate for 4+ visits
2. **High-risk segment (Seg 2)** has 24.4% readmit rate → 6.7K patients need care management
3. **49% specialty data missing** → critical documentation gap
4. **97% weight missing** → BMI analysis not possible
5. **Medications predict LOS** → 26+ meds = 7.2 day avg stay
6. **Baseline readmission rate = 11.16%** → benchmark set
7. **Diabetes medication alone ≠ readmission** → co-morbidities matter more
8. **3-5 day stays = 40.9% of all patients** → biggest operational group
9. **Random Forest: 58% recall** → can flag majority of true readmissions
10. **Prior inpatient visits = 2nd strongest model feature** → flag repeat hospitalizations

---

## H. Resume Project Description

**Hospital Readmission Analysis – Data Analytics Portfolio Project**

Analyzed 101,766 diabetic patient encounters from the UCI 130-US Hospitals dataset to identify 30-day readmission risk factors and build predictive models for a hypothetical hospital administration client.

**Key Contributions:**
- Designed and executed end-to-end data pipeline: data profiling, cleaning, EDA, ML, and dashboard design
- Identified that **11.16% of encounters resulted in 30-day readmission**, with high-utilization patients reaching **24.4%**
- Built and evaluated Logistic Regression, Decision Tree, and Random Forest models; best model achieved **ROC-AUC 0.669** and **Recall 0.58**
- Performed K-Means clustering to identify 4 patient segments, enabling targeted care management strategies
- Delivered 19 MySQL business queries and a 4-page Power BI dashboard with 34 custom DAX measures
- Documented 10 data-driven business recommendations for hospital administration, discharge planning, and care management teams

**Tools:** Python (pandas, scikit-learn, seaborn), MySQL, Power BI, DAX  
**Domain:** Healthcare Analytics | Hospital Operations | Patient Safety

---

## I. GitHub README

See [`README.md`](file:///C:/Users/hariv/Downloads/files/hospital_project/README.md) — the complete GitHub-ready README is already written.

**GitHub repository structure contains:**
- All Python scripts with inline comments
- 19 SQL queries (MySQL compatible)
- 34 DAX measures with explanations
- 20 professional visualization PNGs
- Full 20-section project documentation
- This README with badges, tables, and setup instructions

---

## J. 5-Minute Interview Explanation

---

**"Can you walk me through your hospital readmission analysis project?"**

---

**[1 minute – Problem and Context]**

"Sure. I built this project to simulate the role of a Data Analyst at a hospital that was concerned about increasing 30-day patient readmissions. I used the UCI Diabetes 130-US Hospitals dataset — a real clinical dataset with over 101,000 encounters from diabetic patients admitted to 130 US hospitals between 1999 and 2008.

The business problem was: how do we identify which patients are most likely to be readmitted within 30 days, and what can hospital administration do about it?"

---

**[1 minute – Data Understanding and Cleaning]**

"The first thing I did was a thorough data quality audit. This dataset had some significant issues — 97% of the weight column was missing, 49% of medical specialties were blank, and the target variable had three categories: NO, less than 30 days, and more than 30 days. I binarized it to create a clean 30-day readmission flag.

I made a key decision not to delete any rows — the dataset represents real patient encounters, and removing rows would introduce bias. Instead, I flagged missing data transparently and only analyzed fields where data was available."

---

**[1 minute – Key Findings from EDA]**

"The overall 30-day readmission rate was 11.16%. When I broke it down, the clearest pattern was in prior emergency visit history — patients with 3 or more prior emergency visits had nearly double the average readmission rate at around 18-22%. Prior inpatient visits also strongly predicted readmission.

I also found that patients on more medications had significantly longer hospital stays — those on 26+ medications averaged 7.2 days versus 2.8 days for those on fewer than 6. This tells us that medication complexity is a good proxy for clinical complexity."

---

**[1 minute – Advanced Analytics]**

"I then built three machine learning models — Logistic Regression, Decision Tree, and Random Forest — to predict 30-day readmission. Because the dataset was class-imbalanced with only 11% positive cases, I used class-weight balancing and focused on Recall as the primary metric. In healthcare, missing a high-risk patient is more costly than a false alarm.

The best model was Random Forest with ROC-AUC of 0.67 and Recall of 0.58 — meaning it can flag about 58% of actual readmissions. The most important features were discharge disposition ID, prior inpatient visits, prior emergency visits, and time in hospital.

I also ran K-Means clustering and found 4 patient segments. The high-risk segment — about 6,700 patients with high emergency and inpatient utilization history — had a 24.4% readmission rate, more than double the average."

---

**[1 minute – Deliverables and Recommendations]**

"I packaged the analysis into 19 SQL queries for operational reporting, a 4-page Power BI dashboard with 34 DAX measures, and a full 20-section project report.

My top recommendations were: implement a care management program for the high-risk patient segment, add post-discharge follow-up calls for patients with 2 or more prior emergency visits, and use the Random Forest model to proactively flag high-risk patients at discharge.

I was also honest about limitations — this model has moderate predictive power because it lacks real clinical variables like vital signs and lab trends. I clearly marked analyses that couldn't be done due to missing data, like cost analysis and time-series trends. For me, data integrity means never fabricating results to fill gaps."

---

**[Follow-up questions you may be asked:]**

- *"Why did you choose Recall over Accuracy?"* → Because in healthcare, false negatives (missed readmissions) are worse than false positives (unnecessary follow-up). Accuracy is misleading with imbalanced classes.
- *"What would improve the model?"* → Adding discharge notes (NLP), vital signs trends, lab values, SDOH data, and insurance type.
- *"How would you deploy this?"* → Build a risk score pipeline that runs nightly; flag patients with predicted probability > threshold in the EHR or discharge planning tool; A/B test the intervention.
- *"What's the biggest limitation?"* → The 97% weight missingness and 49% specialty missingness are serious. Real-world deployment would need better EHR data completeness.
- *"How did you handle class imbalance?"* → Used class_weight='balanced' in scikit-learn. Could also try SMOTE or adjusting the probability threshold from 0.5 to improve recall.
