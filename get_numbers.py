import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/hariv/Downloads/files/hospital_project/diabetic_data_cleaned.csv')

print("=== KEY ACTUAL NUMBERS ===")
print("Total encounters:", f"{len(df):,}")
print("Unique patients:", f"{df['patient_nbr'].nunique():,}")
print("30-day readmissions:", f"{df['readmitted_binary'].sum():,}")
print("Readmission rate:", f"{df['readmitted_binary'].mean()*100:.2f}%")
print("Avg LOS:", f"{df['time_in_hospital'].mean():.2f}")
print("Avg medications:", f"{df['num_medications'].mean():.2f}")
print("Avg lab procedures:", f"{df['num_lab_procedures'].mean():.2f}")
print("Avg diagnoses:", f"{df['number_diagnoses'].mean():.2f}")
print("Avg emergency visits:", f"{df['number_emergency'].mean():.4f}")
print("Avg outpatient visits:", f"{df['number_outpatient'].mean():.4f}")
print("Avg inpatient visits:", f"{df['number_inpatient'].mean():.4f}")

print()
print("=== READMIT BY AGE (sorted by age group) ===")
AGE_ORDER = ['[0-10)','[10-20)','[20-30)','[30-40)','[40-50)','[50-60)','[60-70)','[70-80)','[80-90)','[90-100)']
age_data = df.groupby('age')['readmitted_binary'].agg(['mean','count']).reset_index()
age_data.columns = ['age','readmit_rate','count']
age_data['readmit_pct'] = (age_data['readmit_rate']*100).round(2)
age_data['age'] = pd.Categorical(age_data['age'], categories=AGE_ORDER, ordered=True)
age_data = age_data.sort_values('age')
print(age_data[['age','count','readmit_pct']].to_string(index=False))

print()
print("=== READMIT BY GENDER ===")
gender_data = df[df['gender'].notna()].groupby('gender')['readmitted_binary'].agg(['mean','count']).reset_index()
gender_data.columns = ['gender','readmit_rate','count']
gender_data['readmit_pct'] = (gender_data['readmit_rate']*100).round(2)
print(gender_data.to_string(index=False))

print()
print("=== READMIT BY RACE ===")
race_data = df[df['race'].notna()].groupby('race')['readmitted_binary'].agg(['mean','count']).reset_index()
race_data.columns = ['race','readmit_rate','count']
race_data['readmit_pct'] = (race_data['readmit_rate']*100).round(2)
race_data = race_data.sort_values('readmit_pct', ascending=False)
print(race_data.to_string(index=False))

print()
print("=== READMIT BY DIABETES MED ===")
dm = df.groupby('diabetesMed')['readmitted_binary'].agg(['mean','count']).reset_index()
dm.columns = ['diabetesMed','readmit_rate','count']
dm['readmit_pct'] = (dm['readmit_rate']*100).round(2)
print(dm.to_string(index=False))

print()
print("=== READMIT BY CHANGE ===")
ch = df.groupby('change')['readmitted_binary'].agg(['mean','count']).reset_index()
ch.columns = ['change','readmit_rate','count']
ch['readmit_pct'] = (ch['readmit_rate']*100).round(2)
print(ch.to_string(index=False))

print()
print("=== STAY CATEGORY distribution ===")
sc = df.groupby('stay_category').agg(
    count=('encounter_id','count'),
    readmit_mean=('readmitted_binary','mean')
).reset_index()
sc['readmit_pct'] = (sc['readmit_mean']*100).round(2)
sc['pct_of_total'] = (sc['count']/len(df)*100).round(2)
print(sc[['stay_category','count','pct_of_total','readmit_pct']].to_string(index=False))

print()
print("=== UTILIZATION CATEGORY ===")
uc = df.groupby('utilization_category').agg(
    count=('encounter_id','count'),
    readmit_mean=('readmitted_binary','mean')
).reset_index()
uc['readmit_pct'] = (uc['readmit_mean']*100).round(2)
print(uc.to_string(index=False))

print()
print("=== MEDICATION GROUP vs LOS ===")
MED_ORDER = ['Low (1-5)','Moderate (6-15)','High (16-25)','Very High (26+)']
mg = df.groupby('medication_group').agg(
    avg_los=('time_in_hospital','mean'),
    count=('encounter_id','count'),
    readmit_pct=('readmitted_binary','mean')
).reset_index()
mg['avg_los'] = mg['avg_los'].round(2)
mg['readmit_pct'] = (mg['readmit_pct']*100).round(2)
mg['medication_group'] = pd.Categorical(mg['medication_group'], categories=MED_ORDER, ordered=True)
mg = mg.sort_values('medication_group')
print(mg.to_string(index=False))

print()
print("=== DIAGNOSIS BURDEN ===")
DIAG_ORDER = ['Low (1-3)','Moderate (4-6)','High (7-9)','Very High (10+)']
db = df.groupby('diagnosis_burden').agg(
    avg_los=('time_in_hospital','mean'),
    count=('encounter_id','count'),
    readmit_pct=('readmitted_binary','mean')
).reset_index()
db['avg_los'] = db['avg_los'].round(2)
db['readmit_pct'] = (db['readmit_pct']*100).round(2)
db['diagnosis_burden'] = pd.Categorical(db['diagnosis_burden'], categories=DIAG_ORDER, ordered=True)
db = db.sort_values('diagnosis_burden')
print(db.to_string(index=False))

print()
print("=== EMERGENCY BINS ===")
df['emerg_bin'] = df['number_emergency'].apply(
    lambda x: '0' if x==0 else ('1' if x==1 else ('2' if x==2 else ('3' if x==3 else '4+')))
)
eb = df.groupby('emerg_bin')['readmitted_binary'].agg(['mean','count']).reset_index()
eb.columns = ['emergency_visits','readmit_rate','count']
eb['readmit_pct'] = (eb['readmit_rate']*100).round(2)
EMERG_ORDER = ['0','1','2','3','4+']
eb['emergency_visits'] = pd.Categorical(eb['emergency_visits'], categories=EMERG_ORDER, ordered=True)
eb = eb.sort_values('emergency_visits')
print(eb.to_string(index=False))
