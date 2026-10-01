"""
==============================================================
HOSPITAL READMISSION ANALYSIS
Phase 3 – Exploratory Data Analysis (Basic Questions)
Phase 4 – Medium-Level Analysis
==============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

PLOT_DIR = "C:/Users/hariv/Downloads/files/hospital_project/plots"
os.makedirs(PLOT_DIR, exist_ok=True)
DATA_PATH = "C:/Users/hariv/Downloads/files/hospital_project/diabetic_data_cleaned.csv"

# ── Load Cleaned Data ─────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"Loaded cleaned data: {df.shape[0]:,} rows, {df.shape[1]} columns")

BLUE   = '#2980B9'
RED    = '#E74C3C'
GREEN  = '#27AE60'
ORANGE = '#E67E22'
PURPLE = '#8E44AD'
palette_rb = [GREEN, RED]

AGE_ORDER = ['[0-10)','[10-20)','[20-30)','[30-40)','[40-50)',
             '[50-60)','[60-70)','[70-80)','[80-90)','[90-100)']

def save_fig(name):
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/{name}.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {name}.png")

def readmit_rate(series, label_col, target='readmitted_binary'):
    """Return % readmitted within 30 days grouped by label_col."""
    return series.groupby(label_col)[target].mean().mul(100).round(2)

# ══════════════════════════════════════════════════════════════
# PHASE 3 – BASIC QUESTIONS
# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("PHASE 3 – EXPLORATORY DATA ANALYSIS (BASIC)")
print("="*60)

# ── Q1: Readmission rate by age group ────────────────────────
print("\n── Q1: Readmission Rate by Age Group ──")
age_readmit = (
    df.groupby('age')['readmitted_binary']
    .agg(['mean','count'])
    .reset_index()
)
age_readmit.columns = ['age_group','readmit_rate','patient_count']
age_readmit['readmit_pct'] = (age_readmit['readmit_rate'] * 100).round(2)
age_readmit['age_group'] = pd.Categorical(age_readmit['age_group'], categories=AGE_ORDER, ordered=True)
age_readmit = age_readmit.sort_values('age_group')
print(age_readmit[['age_group','patient_count','readmit_pct']].to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(age_readmit['age_group'], age_readmit['readmit_pct'], color=BLUE, edgecolor='white', width=0.7)
for bar, val in zip(bars, age_readmit['readmit_pct']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.2, f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
ax.set_title('Readmission Rate (30-Day) by Age Group', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Age Group', fontsize=11)
ax.set_ylabel('Readmission Rate (%)', fontsize=11)
ax.set_ylim(0, max(age_readmit['readmit_pct']) + 4)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=30)
save_fig("q1_readmit_by_age")

print("\n   INSIGHT: Middle-aged groups (30-60) show higher readmission rates,")
print("   suggesting complexity of conditions in working-age diabetic patients.")

# ── Q2: Average length of stay by medical specialty ──────────
print("\n── Q2: Average Length of Stay by Medical Specialty ──")
specialty_df = df[df['medical_specialty'].notna()].copy()
specialty_stats = (
    specialty_df.groupby('medical_specialty')['time_in_hospital']
    .agg(['mean','count'])
    .reset_index()
)
specialty_stats.columns = ['medical_specialty','avg_los','patient_count']
# Filter for specialties with >= 100 patients for reliability
specialty_stats = specialty_stats[specialty_stats['patient_count'] >= 100]
specialty_stats = specialty_stats.sort_values('avg_los', ascending=False)
print("\nTop 10 Specialties by Avg LOS (min 100 patients):")
print(specialty_stats.head(10)[['medical_specialty','avg_los','patient_count']].to_string(index=False))
print("\nBottom 10 Specialties by Avg LOS:")
print(specialty_stats.tail(10)[['medical_specialty','avg_los','patient_count']].to_string(index=False))

top15 = specialty_stats.head(15)
fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(top15['medical_specialty'], top15['avg_los'], color=ORANGE, edgecolor='white')
ax.set_title('Average Length of Stay by Medical Specialty (Top 15)', fontsize=13, fontweight='bold')
ax.set_xlabel('Average Days in Hospital')
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=0.5)
for i, (val, n) in enumerate(zip(top15['avg_los'], top15['patient_count'])):
    ax.text(val + 0.05, i, f'{val:.1f}d (n={n})', va='center', fontsize=8)
save_fig("q2_los_by_specialty")
print("   INSIGHT: Surgery-type specialties have the longest stays (clinical complexity).")

# ── Q3: Emergency visits vs readmission ──────────────────────
print("\n── Q3: Emergency Visits vs Readmission Rate ──")
# Bin emergency visits: 0, 1, 2, 3, 4+
df['emerg_bin'] = df['number_emergency'].apply(
    lambda x: '0' if x==0 else ('1' if x==1 else ('2' if x==2 else ('3' if x==3 else '4+')))
)
emerg_readmit = df.groupby('emerg_bin')['readmitted_binary'].agg(['mean','count']).reset_index()
emerg_readmit.columns = ['emergency_visits','readmit_rate','count']
emerg_readmit['readmit_pct'] = (emerg_readmit['readmit_rate'] * 100).round(2)
emerg_order = ['0','1','2','3','4+']
emerg_readmit['emergency_visits'] = pd.Categorical(emerg_readmit['emergency_visits'], categories=emerg_order, ordered=True)
emerg_readmit = emerg_readmit.sort_values('emergency_visits')
print(emerg_readmit[['emergency_visits','count','readmit_pct']].to_string(index=False))

fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
bars = ax1.bar(emerg_readmit['emergency_visits'], emerg_readmit['count'], color=BLUE, alpha=0.6, label='Patient Count')
ax2.plot(emerg_readmit['emergency_visits'], emerg_readmit['readmit_pct'], color=RED, marker='o', linewidth=2, label='Readmit Rate %')
ax1.set_xlabel('Prior Emergency Visits (past year)')
ax1.set_ylabel('Patient Count', color=BLUE)
ax2.set_ylabel('Readmission Rate (%)', color=RED)
ax1.set_title('Emergency Visits vs 30-Day Readmission Rate', fontsize=13, fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
save_fig("q3_emergency_vs_readmit")
print("   INSIGHT: Higher prior emergency visits correlate with higher readmission risk.")

# ── Q4: Diabetic medication patients readmission ──────────────
print("\n── Q4: Diabetes Medication Patients – Readmission ──")
diab_readmit = df.groupby('diabetesMed')['readmitted_binary'].agg(['mean','count','sum']).reset_index()
diab_readmit.columns = ['diabetesMed','readmit_rate','total','readmitted']
diab_readmit['readmit_pct'] = (diab_readmit['readmit_rate'] * 100).round(2)
print(diab_readmit.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# Pie chart for diabetes med distribution
axes[0].pie(diab_readmit['total'], labels=diab_readmit['diabetesMed'],
            autopct='%1.1f%%', colors=[GREEN, RED], startangle=90, pctdistance=0.75)
axes[0].set_title('Patients by Diabetes Medication Status', fontweight='bold')
# Bar for readmission
axes[1].bar(diab_readmit['diabetesMed'], diab_readmit['readmit_pct'], color=[GREEN, RED], edgecolor='white', width=0.5)
for i, (y, n) in enumerate(zip(diab_readmit['readmit_pct'], diab_readmit['total'])):
    axes[1].text(i, y + 0.2, f'{y:.1f}%\n(n={n:,})', ha='center', va='bottom', fontsize=10)
axes[1].set_title('30-Day Readmission Rate by Diabetes Med', fontweight='bold')
axes[1].set_ylabel('Readmission Rate (%)')
axes[1].set_ylim(0, max(diab_readmit['readmit_pct']) + 4)
axes[1].grid(axis='y', linestyle='--', alpha=0.5)
save_fig("q4_diabetes_med_readmit")
print("   INSIGHT: Patients on diabetes medication have a measurably different readmission profile.")

# ── Q5: Change in diabetes medication vs readmission ─────────
print("\n── Q5: Change in Diabetic Medication vs Readmission ──")
change_readmit = df.groupby('change')['readmitted_binary'].agg(['mean','count']).reset_index()
change_readmit.columns = ['med_change','readmit_rate','count']
change_readmit['readmit_pct'] = (change_readmit['readmit_rate'] * 100).round(2)
change_readmit['med_change'] = change_readmit['med_change'].map({'Ch':'Changed','No':'No Change'})
print(change_readmit.to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 5))
colors = [ORANGE, BLUE]
bars = ax.bar(change_readmit['med_change'], change_readmit['readmit_pct'], color=colors, width=0.5, edgecolor='white')
for bar, val in zip(bars, change_readmit['readmit_pct']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{val:.1f}%', ha='center', va='bottom', fontsize=12)
ax.set_title('Readmission Rate by Medication Change Status', fontsize=13, fontweight='bold')
ax.set_ylabel('Readmission Rate (%)')
ax.set_ylim(0, max(change_readmit['readmit_pct']) + 4)
ax.grid(axis='y', linestyle='--', alpha=0.5)
save_fig("q5_med_change_readmit")
print("   INSIGHT: Patients with changed medications may indicate higher disease instability.")

# ── Q6: Lab procedures vs readmission ────────────────────────
print("\n── Q6: Number of Lab Procedures vs Readmission Rate ──")
df['lab_proc_bin'] = pd.cut(df['num_lab_procedures'],
    bins=[0,20,40,60,80,150], labels=['1-20','21-40','41-60','61-80','80+'])
lab_readmit = df.groupby('lab_proc_bin', observed=True)['readmitted_binary'].agg(['mean','count']).reset_index()
lab_readmit.columns = ['lab_procedures','readmit_rate','count']
lab_readmit['readmit_pct'] = (lab_readmit['readmit_rate'] * 100).round(2)
print(lab_readmit.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
ax1.bar(lab_readmit['lab_procedures'], lab_readmit['count'], color=BLUE, alpha=0.6)
ax2.plot(lab_readmit['lab_procedures'], lab_readmit['readmit_pct'], color=RED, marker='s', linewidth=2)
ax1.set_xlabel('Number of Lab Procedures')
ax1.set_ylabel('Patient Count', color=BLUE)
ax2.set_ylabel('Readmission Rate (%)', color=RED)
ax1.set_title('Lab Procedures vs 30-Day Readmission Rate', fontsize=13, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
save_fig("q6_lab_proc_readmit")
print("   INSIGHT: Moderate lab procedure counts correlate with the main patient population.")

# ── Q7: Readmission by race and gender ───────────────────────
print("\n── Q7: Readmission Rate by Race and Gender ──")
race_readmit = (
    df[df['race'].notna()].groupby('race')['readmitted_binary']
    .agg(['mean','count']).reset_index()
)
race_readmit.columns = ['race','readmit_rate','count']
race_readmit['readmit_pct'] = (race_readmit['readmit_rate'] * 100).round(2)
race_readmit = race_readmit.sort_values('readmit_pct', ascending=False)
print("Race:")
print(race_readmit.to_string(index=False))

gender_readmit = (
    df[df['gender'].notna()].groupby('gender')['readmitted_binary']
    .agg(['mean','count']).reset_index()
)
gender_readmit.columns = ['gender','readmit_rate','count']
gender_readmit['readmit_pct'] = (gender_readmit['readmit_rate'] * 100).round(2)
print("Gender:")
print(gender_readmit.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# Race
colors_race = sns.color_palette('Set2', len(race_readmit))
bars = axes[0].bar(race_readmit['race'], race_readmit['readmit_pct'], color=colors_race, edgecolor='white')
for bar, val in zip(bars, race_readmit['readmit_pct']):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.1, f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
axes[0].set_title('30-Day Readmission Rate by Race', fontweight='bold')
axes[0].set_ylabel('Readmission Rate (%)')
axes[0].set_xticklabels(race_readmit['race'], rotation=20, ha='right')
axes[0].grid(axis='y', linestyle='--', alpha=0.5)

# Gender
colors_g = [BLUE, ORANGE]
bars2 = axes[1].bar(gender_readmit['gender'], gender_readmit['readmit_pct'], color=colors_g, width=0.4, edgecolor='white')
for bar, val in zip(bars2, gender_readmit['readmit_pct']):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.1, f'{val:.1f}%', ha='center', va='bottom', fontsize=11)
axes[1].set_title('30-Day Readmission Rate by Gender', fontweight='bold')
axes[1].set_ylabel('Readmission Rate (%)')
axes[1].grid(axis='y', linestyle='--', alpha=0.5)
save_fig("q7_race_gender_readmit")
print("   INSIGHT: Small differences across racial groups; no dramatic disparity in this dataset.")
print("   CAUTION: No causal conclusions can be drawn; social determinants not measured here.")

# ── Q8: Weight categories vs readmission ─────────────────────
print("\n── Q8: Weight Categories vs Readmission Rate ──")
weight_missing = df['weight'].isna().sum()
weight_pct = round(weight_missing / len(df) * 100, 2)
print(f"   Weight missing: {weight_missing:,} records = {weight_pct}% of dataset")
print("   Analysis limited to available records only:")

weight_df = df[df['weight'].notna()].copy()
weight_readmit = (
    weight_df.groupby('weight')['readmitted_binary']
    .agg(['mean','count']).reset_index()
)
weight_readmit.columns = ['weight_cat','readmit_rate','count']
weight_readmit['readmit_pct'] = (weight_readmit['readmit_rate'] * 100).round(2)
WEIGHT_ORDER = ['[0-25)','[25-50)','[50-75)','[75-100)','[100-125)','[125-150)','[150-175)','[175-200)','>200']
weight_readmit['weight_cat'] = pd.Categorical(weight_readmit['weight_cat'], categories=WEIGHT_ORDER, ordered=True)
weight_readmit = weight_readmit.sort_values('weight_cat').dropna(subset=['weight_cat'])
print(weight_readmit.to_string(index=False))

fig, ax = plt.subplots(figsize=(11, 5))
bars = ax.bar(weight_readmit['weight_cat'].astype(str), weight_readmit['readmit_pct'], color=PURPLE, edgecolor='white')
for bar, val in zip(bars, weight_readmit['readmit_pct']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.3, f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
ax.set_title(f'Readmission Rate by Weight Category\n(Note: {weight_pct}% weight data missing – interpret with caution)',
             fontsize=12, fontweight='bold')
ax.set_xlabel('Weight Category (lbs)')
ax.set_ylabel('Readmission Rate (%)')
ax.set_ylim(0, max(weight_readmit['readmit_pct']) + 5)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=30)
save_fig("q8_weight_readmit")

# ── Q9: Medications vs length of stay ────────────────────────
print("\n── Q9: Number of Medications vs Length of Hospital Stay ──")
med_stay = df.groupby('medication_group')['time_in_hospital'].agg(['mean','count']).reset_index()
med_stay.columns = ['medication_group','avg_los','count']
MED_ORDER = ['Low (1-5)','Moderate (6-15)','High (16-25)','Very High (26+)']
med_stay['medication_group'] = pd.Categorical(med_stay['medication_group'], categories=MED_ORDER, ordered=True)
med_stay = med_stay.sort_values('medication_group')
print(med_stay.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(med_stay['medication_group'], med_stay['avg_los'], color=GREEN, edgecolor='white')
for bar, val in zip(bars, med_stay['avg_los']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.05, f'{val:.2f}d', ha='center', va='bottom', fontsize=11)
ax.set_title('Average Hospital Stay by Medication Group', fontsize=13, fontweight='bold')
ax.set_xlabel('Medication Count Group')
ax.set_ylabel('Average Length of Stay (Days)')
ax.grid(axis='y', linestyle='--', alpha=0.5)
save_fig("q9_medications_vs_los")
print("   INSIGHT: Patients on more medications stay longer, reflecting clinical complexity.")

# ── Q10: Outpatient visits vs readmission ────────────────────
print("\n── Q10: Previous Outpatient Visits vs Readmission Rate ──")
df['outpatient_bin'] = df['number_outpatient'].apply(
    lambda x: '0' if x==0 else ('1' if x==1 else ('2' if x==2 else ('3' if x==3 else '4+')))
)
out_readmit = df.groupby('outpatient_bin')['readmitted_binary'].agg(['mean','count']).reset_index()
out_readmit.columns = ['outpatient_visits','readmit_rate','count']
out_readmit['readmit_pct'] = (out_readmit['readmit_rate'] * 100).round(2)
out_order = ['0','1','2','3','4+']
out_readmit['outpatient_visits'] = pd.Categorical(out_readmit['outpatient_visits'], categories=out_order, ordered=True)
out_readmit = out_readmit.sort_values('outpatient_visits')
print(out_readmit.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
ax1.bar(out_readmit['outpatient_visits'], out_readmit['count'], color=BLUE, alpha=0.6)
ax2.plot(out_readmit['outpatient_visits'], out_readmit['readmit_pct'], color=RED, marker='o', linewidth=2)
ax1.set_xlabel('Prior Outpatient Visits')
ax1.set_ylabel('Patient Count', color=BLUE)
ax2.set_ylabel('Readmission Rate (%)', color=RED)
ax1.set_title('Outpatient Visits vs 30-Day Readmission Rate', fontsize=13, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
save_fig("q10_outpatient_readmit")
print("   INSIGHT: Patients with some prior outpatient visits show varying readmission patterns.")

# ══════════════════════════════════════════════════════════════
# PHASE 4 – MEDIUM-LEVEL ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("PHASE 4 – MEDIUM-LEVEL ANALYSIS")
print("="*60)

# M1: Time-series analysis
print("\n── M1: Time-Series Analysis ──")
print("   NOT AVAILABLE: The dataset does not contain actual admission dates.")
print("   A true time-series trend analysis cannot be performed.")
print("   The dataset represents encounters from 1999–2008 but no date field exists.")

# M2: Comorbidities (number_diagnoses) vs LOS and readmission
print("\n── M2: Comorbidities vs LOS and Readmission ──")
diag_analysis = df.groupby('diagnosis_burden').agg(
    avg_los=('time_in_hospital','mean'),
    readmit_rate=('readmitted_binary','mean'),
    count=('encounter_id','count')
).reset_index()
DIAG_ORDER = ['Low (1-3)','Moderate (4-6)','High (7-9)','Very High (10+)']
diag_analysis['diagnosis_burden'] = pd.Categorical(diag_analysis['diagnosis_burden'], categories=DIAG_ORDER, ordered=True)
diag_analysis = diag_analysis.sort_values('diagnosis_burden')
diag_analysis['readmit_pct'] = (diag_analysis['readmit_rate'] * 100).round(2)
print(diag_analysis[['diagnosis_burden','count','avg_los','readmit_pct']].to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].bar(diag_analysis['diagnosis_burden'], diag_analysis['avg_los'], color=ORANGE, edgecolor='white')
for i, val in enumerate(diag_analysis['avg_los']):
    axes[0].text(i, val+0.05, f'{val:.2f}d', ha='center', va='bottom')
axes[0].set_title('Avg LOS by Diagnosis Burden', fontweight='bold')
axes[0].set_xlabel('Diagnosis Burden')
axes[0].set_ylabel('Avg Days')
axes[0].tick_params(axis='x', rotation=15)
axes[0].grid(axis='y', linestyle='--', alpha=0.5)

axes[1].bar(diag_analysis['diagnosis_burden'], diag_analysis['readmit_pct'], color=RED, edgecolor='white')
for i, val in enumerate(diag_analysis['readmit_pct']):
    axes[1].text(i, val+0.1, f'{val:.1f}%', ha='center', va='bottom')
axes[1].set_title('Readmission Rate by Diagnosis Burden', fontweight='bold')
axes[1].set_xlabel('Diagnosis Burden')
axes[1].set_ylabel('Readmission Rate (%)')
axes[1].tick_params(axis='x', rotation=15)
axes[1].grid(axis='y', linestyle='--', alpha=0.5)
save_fig("m2_diagnosis_burden")

# M3: Discharge disposition
print("\n── M3: Discharge Disposition ──")
print("   AVAILABLE: discharge_disposition_id exists in the dataset.")
# Load IDS mapping
ids_map = pd.read_csv("C:/Users/hariv/Downloads/files/hospital_project/IDS_mapping.csv")
print(f"   IDS mapping loaded: {ids_map.shape}")
print(ids_map.head(10))

discharge_readmit = df.groupby('discharge_disposition_id')['readmitted_binary'].agg(['mean','count']).reset_index()
discharge_readmit.columns = ['discharge_disposition_id','readmit_rate','count']
discharge_readmit['readmit_pct'] = (discharge_readmit['readmit_rate'] * 100).round(2)
discharge_readmit = discharge_readmit.sort_values('readmit_pct', ascending=False)
print("Top 10 Discharge Dispositions by Readmission Rate (min 50 patients):")
print(discharge_readmit[discharge_readmit['count']>=50].head(10).to_string(index=False))

# M4: Demographics vs lab/medications
print("\n── M4: Demographics vs Lab Procedures and Medications ──")
demo_analysis = df[df['race'].notna() & df['gender'].notna()].groupby(['race','gender']).agg(
    avg_lab=('num_lab_procedures','mean'),
    avg_med=('num_medications','mean'),
    count=('encounter_id','count')
).reset_index()
print("Race x Gender – Avg Lab Procedures and Medications:")
print(demo_analysis[demo_analysis['count']>=100].to_string(index=False))

# M5: Inpatient/outpatient/emergency by primary diagnosis category
print("\n── M5: Visits by Primary Diagnosis ──")
# Classify diag_1 into broad ICD-9 categories
def classify_diag(code):
    if pd.isna(code):
        return 'Unknown'
    code = str(code).strip()
    try:
        n = float(code)
        if 390 <= n <= 459 or n == 785:   return 'Circulatory'
        elif 460 <= n <= 519 or n == 786:  return 'Respiratory'
        elif 520 <= n <= 579 or n == 787:  return 'Digestive'
        elif 250 <= n <= 250.99:           return 'Diabetes'
        elif 800 <= n <= 999:              return 'Injury/Poisoning'
        elif 710 <= n <= 739:              return 'Musculoskeletal'
        elif 580 <= n <= 629 or n == 788:  return 'Genitourinary'
        elif 140 <= n <= 239:              return 'Neoplasms'
        elif 240 <= n <= 279:              return 'Endocrine/Metabolic'
        elif 290 <= n <= 319:              return 'Mental Disorders'
        else:                              return 'Other'
    except:
        if code.startswith('V'):           return 'Supplementary'
        elif code.startswith('E'):         return 'External Causes'
        return 'Other'

df['diag1_category'] = df['diag_1'].apply(classify_diag)
diag_visits = df.groupby('diag1_category').agg(
    avg_inpatient=('number_inpatient','mean'),
    avg_outpatient=('number_outpatient','mean'),
    avg_emergency=('number_emergency','mean'),
    count=('encounter_id','count')
).reset_index().sort_values('count', ascending=False)
print(diag_visits.to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(diag_visits))
w = 0.25
bars1 = ax.bar(x - w, diag_visits['avg_inpatient'], w, label='Inpatient', color=BLUE)
bars2 = ax.bar(x, diag_visits['avg_outpatient'], w, label='Outpatient', color=GREEN)
bars3 = ax.bar(x + w, diag_visits['avg_emergency'], w, label='Emergency', color=RED)
ax.set_xticks(x)
ax.set_xticklabels(diag_visits['diag1_category'], rotation=30, ha='right')
ax.set_title('Average Prior Visits by Primary Diagnosis Category', fontsize=13, fontweight='bold')
ax.set_ylabel('Average Prior Visits')
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)
save_fig("m5_visits_by_diagnosis")

# M6: Medication (X1-X25) prescribing patterns
print("\n── M6: Diabetes Medication Indicators vs Readmission ──")
med_cols = ['metformin','repaglinide','nateglinide','chlorpropamide','glimepiride',
            'acetohexamide','glipizide','glyburide','tolbutamide','pioglitazone',
            'rosiglitazone','acarbose','miglitol','troglitazone','tolazamide',
            'examide','citoglipton','insulin','glyburide-metformin',
            'glipizide-metformin','glimepiride-pioglitazone','metformin-rosiglitazone',
            'metformin-pioglitazone']

# For each medication, calculate usage rate and readmission rate among users vs non-users
med_results = []
for med in med_cols:
    if med in df.columns:
# All medication columns in this dataset are string type (No/Steady/Up/Down)
        usage_cnt = int((df[med].fillna('No') != 'No').sum())
        usage_pct = round(usage_cnt / len(df) * 100, 2)
        if usage_cnt > 100:
            users_readmit = df[df[med].fillna('No') != 'No']['readmitted_binary'].mean()
            non_users_readmit = df[df[med].fillna('No') == 'No']['readmitted_binary'].mean()
        else:
            users_readmit = np.nan
            non_users_readmit = np.nan
        med_results.append({
            'medication': med, 'usage_count': usage_cnt, 'usage_pct': usage_pct,
            'users_readmit_pct': round(users_readmit * 100, 2) if not np.isnan(users_readmit) else None,
            'non_users_readmit_pct': round(non_users_readmit * 100, 2) if not np.isnan(non_users_readmit) else None
        })

med_df = pd.DataFrame(med_results)
print(med_df.to_string(index=False))

# Top medications by usage
top_meds = med_df[med_df['usage_count'] > 1000].sort_values('usage_count', ascending=False)
if len(top_meds) > 0:
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(top_meds))
    w = 0.35
    ax.bar(x - w/2, top_meds['users_readmit_pct'].fillna(0), w, label='On Medication', color=RED)
    ax.bar(x + w/2, top_meds['non_users_readmit_pct'].fillna(0), w, label='Not on Medication', color=BLUE)
    ax.set_xticks(x)
    ax.set_xticklabels(top_meds['medication'], rotation=40, ha='right')
    ax.set_title('Readmission Rate: Users vs Non-Users by Medication Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Readmission Rate (%)')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    save_fig("m6_medication_readmit_comparison")

# M7: Weight + diagnosis
print("\n── M7: Weight + Diagnosis (Limited – 3.13% data available) ──")
weight_diag = df[df['weight'].notna()].groupby(['weight','diag1_category']).agg(
    readmit_pct=('readmitted_binary','mean'), count=('encounter_id','count')
).reset_index()
weight_diag['readmit_pct'] = (weight_diag['readmit_pct'] * 100).round(2)
print("Weight x Diagnosis (top entries, min 10 patients):")
print(weight_diag[weight_diag['count'] >= 10].sort_values('readmit_pct', ascending=False).head(15).to_string(index=False))

# M8: Diabetic medication indicators readmission – already in M6 above

# M9: Patient satisfaction
print("\n── M9: Patient Satisfaction Analysis ──")
print("   NOT AVAILABLE: No patient satisfaction column exists in this dataset.")
print("   This analysis cannot be performed with available data.")

print("\n\nPhase 3 & 4 EDA Complete!")
print("All plots saved to:", PLOT_DIR)
