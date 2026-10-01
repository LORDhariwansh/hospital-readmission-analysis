"""
==============================================================
HOSPITAL READMISSION ANALYSIS
Phase 1 - Data Understanding & Phase 2 - Data Cleaning
Dataset: UCI Diabetes 130-US Hospitals (1999-2008)
Project: DACS08 - Hospital Administration Analysis
==============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# Output directory for plots
PLOT_DIR = "C:/Users/hariv/Downloads/files/hospital_project/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

DATA_PATH = "C:/Users/hariv/Downloads/files/hospital_project/diabetic_data.csv"

# ==============================================================
# PHASE 1 – DATA UNDERSTANDING
# ==============================================================

print("=" * 60)
print("PHASE 1 – DATA UNDERSTANDING")
print("=" * 60)

# 1. Load dataset
df_raw = pd.read_csv(DATA_PATH)

# 2. Shape
print(f"\n1. Dataset Shape")
print(f"   Rows    : {df_raw.shape[0]:,}")
print(f"   Columns : {df_raw.shape[1]}")

# 3. Column names
print(f"\n2. All Column Names:")
for i, col in enumerate(df_raw.columns, 1):
    print(f"   {i:02d}. {col}")

# 4. Numerical vs Categorical
num_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df_raw.select_dtypes(include=['object']).columns.tolist()
print(f"\n3. Numerical Columns ({len(num_cols)}):")
print(f"   {num_cols}")
print(f"\n4. Categorical Columns ({len(cat_cols)}):")
print(f"   {cat_cols}")

# 5. Missing values + "?" check
print(f"\n5. Data Quality Summary:")
print(f"   {'Column':<35} {'DType':<10} {'Nulls':>8} {'?-marks':>8} {'Total Missing':>14} {'Missing%':>10} {'Unique':>8} Action")
print(f"   {'-'*110}")

quality_rows = []
for col in df_raw.columns:
    dtype = str(df_raw[col].dtype)
    null_cnt = int(df_raw[col].isna().sum())
    q_cnt = int((df_raw[col] == '?').sum()) if df_raw[col].dtype == object else 0
    total_miss = null_cnt + q_cnt
    miss_pct = round(total_miss / len(df_raw) * 100, 2)
    unique = df_raw[col].nunique()

    if col == 'weight':
        action = "Convert ? to NaN; 96.8% missing – retain but flag"
    elif col == 'race' and q_cnt > 0:
        action = "Convert ? to NaN; treat as Unknown"
    elif col == 'medical_specialty' and q_cnt > 0:
        action = "Convert ? to NaN; treat as Unknown"
    elif col == 'payer_code' and q_cnt > 0:
        action = "Convert ? to NaN; not used in core analysis"
    elif col == 'diag_1' and q_cnt > 0:
        action = "Convert ? to NaN; ICD-9 code"
    elif col == 'diag_2' and q_cnt > 0:
        action = "Convert ? to NaN; ICD-9 code"
    elif col == 'diag_3' and q_cnt > 0:
        action = "Convert ? to NaN; ICD-9 code"
    elif col == 'max_glu_serum':
        action = "94.75% missing – retain but note limitation"
    elif col == 'A1Cresult':
        action = "83.28% missing – retain but note limitation"
    elif total_miss == 0:
        action = "No action needed"
    else:
        action = "Review"

    quality_rows.append({
        'Column': col, 'DType': dtype,
        'Missing_Values': total_miss, 'Missing_Pct': miss_pct,
        'Unique_Values': unique, 'Action': action
    })
    print(f"   {col:<35} {dtype:<10} {null_cnt:>8} {q_cnt:>8} {total_miss:>14} {miss_pct:>9}% {unique:>8}  {action}")

quality_df = pd.DataFrame(quality_rows)
quality_df.to_csv(f"{PLOT_DIR}/data_quality_summary.csv", index=False)

# 6. Duplicates
print(f"\n6. Duplicate Records:")
print(f"   Duplicate encounter_id (should be 0): {df_raw['encounter_id'].duplicated().sum()}")
print(f"   Duplicate patient_nbr (multiple visits): {df_raw['patient_nbr'].duplicated().sum()}")
print(f"   NOTE: Same patient can have multiple encounters – this is expected in hospital data.")

# 7. Unique values in key categoricals
print(f"\n7. Unique Values in Key Categorical Columns:")
for col in ['race', 'gender', 'age', 'change', 'diabetesMed', 'readmitted']:
    print(f"\n   {col}:")
    print(f"   {df_raw[col].value_counts().to_dict()}")

# 8. Invalid values ("?")
print(f"\n8. Invalid Values ('?'):")
for col in df_raw.columns:
    if df_raw[col].dtype == object:
        q_cnt = (df_raw[col] == '?').sum()
        if q_cnt > 0:
            print(f"   {col}: {q_cnt:,} records ({round(q_cnt/len(df_raw)*100,2)}%)")

# 9. Target variable distribution
print(f"\n9. Target Variable Distribution (readmitted):")
vc = df_raw['readmitted'].value_counts()
print(vc)
print(f"\n   Readmitted within 30 days (<30)     : {vc.get('<30', 0):,} ({round(vc.get('<30',0)/len(df_raw)*100,2)}%)")
print(f"   Readmitted after 30 days (>30)      : {vc.get('>30', 0):,} ({round(vc.get('>30',0)/len(df_raw)*100,2)}%)")
print(f"   Not Readmitted (NO)                 : {vc.get('NO',  0):,} ({round(vc.get('NO', 0)/len(df_raw)*100,2)}%)")

# 10. Data quality problems summary
print(f"\n10. Summary of Data Quality Issues:")
print("""
   a. 'weight'           : 96.87% missing (coded as '?') – very high missingness
   b. 'race'             : 2,273 records coded as '?' (~2.23%)
   c. 'medical_specialty': 49,949 records coded as '?' (~49.08%)
   d. 'payer_code'       : coded as '?' for many records
   e. 'diag_1/2/3'       : some coded as '?' (ICD-9 codes)
   f. 'max_glu_serum'    : 94.75% NaN
   g. 'A1Cresult'        : 83.28% NaN
   h. 'gender'           : 3 records as 'Unknown/Invalid'
   i. 'patient_nbr'      : 30,248 duplicate – same patient, multiple encounters (valid)
   j. 'readmitted'       : Multi-class (NO, <30, >30) – must be binarized for ML
""")


# ==============================================================
# PHASE 2 – DATA CLEANING
# ==============================================================

print("=" * 60)
print("PHASE 2 – DATA CLEANING")
print("=" * 60)

df = df_raw.copy()

# Step 1: Convert "?" to NaN
print("\nStep 1: Converting '?' to NaN in object columns...")
for col in df.columns:
    if df[col].dtype == object:
        before = (df[col] == '?').sum()
        df[col] = df[col].replace('?', np.nan)
        if before > 0:
            print(f"   {col}: {before:,} '?' values replaced with NaN")

# Step 2: Convert 'Unknown/Invalid' gender to NaN
print("\nStep 2: Converting 'Unknown/Invalid' in gender to NaN...")
before = (df['gender'] == 'Unknown/Invalid').sum()
df['gender'] = df['gender'].replace('Unknown/Invalid', np.nan)
print(f"   gender: {before} 'Unknown/Invalid' replaced with NaN")

# Step 3: Create binary readmission target
print("\nStep 3: Creating binary readmission target...")
df['readmitted_binary'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)
print(f"   readmitted_binary (1=within 30 days, 0=otherwise):")
print(f"   {df['readmitted_binary'].value_counts().to_dict()}")

# Step 4: Create Age Group (using existing dataset categories as-is)
print("\nStep 4: Age Group (keeping original dataset categories)...")
# Age categories are already in the dataset as strings
df['age_group'] = df['age']  # Already categorical: [0-10), [10-20), etc.

# Step 5: Hospital Stay Category
print("\nStep 5: Creating Hospital Stay Category...")
def hospital_stay_category(days):
    if days <= 2:
        return '1-2 Days (Short)'
    elif days <= 5:
        return '3-5 Days (Moderate)'
    elif days <= 8:
        return '6-8 Days (Long)'
    else:
        return '9+ Days (Extended)'

df['stay_category'] = df['time_in_hospital'].apply(hospital_stay_category)
print(f"   {df['stay_category'].value_counts().to_dict()}")

# Step 6: Medication Group
print("\nStep 6: Creating Medication Group...")
def medication_group(n):
    if n <= 5:
        return 'Low (1-5)'
    elif n <= 15:
        return 'Moderate (6-15)'
    elif n <= 25:
        return 'High (16-25)'
    else:
        return 'Very High (26+)'

df['medication_group'] = df['num_medications'].apply(medication_group)
print(f"   {df['medication_group'].value_counts().to_dict()}")

# Step 7: Utilization Category
print("\nStep 7: Creating Utilization Category...")
def utilization_category(row):
    total = row['number_inpatient'] + row['number_outpatient'] + row['number_emergency']
    if total == 0:
        return 'No Prior Utilization'
    elif total <= 2:
        return 'Low Utilization (1-2)'
    elif total <= 5:
        return 'Moderate Utilization (3-5)'
    else:
        return 'High Utilization (6+)'

df['utilization_category'] = df.apply(utilization_category, axis=1)
print(f"   {df['utilization_category'].value_counts().to_dict()}")

# Step 8: Diagnosis Burden
print("\nStep 8: Creating Diagnosis Burden...")
def diagnosis_burden(n):
    if n <= 3:
        return 'Low (1-3)'
    elif n <= 6:
        return 'Moderate (4-6)'
    elif n <= 9:
        return 'High (7-9)'
    else:
        return 'Very High (10+)'

df['diagnosis_burden'] = df['number_diagnoses'].apply(diagnosis_burden)
print(f"   {df['diagnosis_burden'].value_counts().to_dict()}")

# Step 9: Weight Category (only for non-null weight)
print("\nStep 9: Weight - reporting missingness...")
weight_missing = df['weight'].isna().sum()
weight_pct = round(weight_missing / len(df) * 100, 2)
print(f"   Missing weight records: {weight_missing:,} ({weight_pct}%)")
print(f"   Available weight records: {df['weight'].notna().sum():,}")

# Step 10: Keep original, save cleaned
print("\nStep 10: Saving cleaned dataset...")
df.to_csv("C:/Users/hariv/Downloads/files/hospital_project/diabetic_data_cleaned.csv", index=False)
print(f"   Cleaned dataset saved: {len(df):,} rows, {len(df.columns)} columns")

print("\nCleaning Summary:")
print(f"   Original rows          : {len(df_raw):,}")
print(f"   Cleaned rows           : {len(df):,}")
print(f"   No rows deleted        : Preserved all records")
print(f"   New derived columns    : readmitted_binary, age_group, stay_category,")
print(f"                           medication_group, utilization_category, diagnosis_burden")
print(f"\nPhase 1 & 2 Complete!")
