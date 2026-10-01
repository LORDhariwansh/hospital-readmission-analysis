"""
==============================================================
HOSPITAL READMISSION ANALYSIS
Phase 5 – Advanced Analytics
- Predictive Modeling (Logistic Regression, Decision Tree, Random Forest)
- Patient Segmentation (K-Means Clustering)
- Financial Impact: NOT AVAILABLE (no cost data)
- Social Determinants: PARTIAL (demographics only)
==============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    roc_curve, precision_recall_curve, ConfusionMatrixDisplay
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

PLOT_DIR = "C:/Users/hariv/Downloads/files/hospital_project/plots"
os.makedirs(PLOT_DIR, exist_ok=True)
DATA_PATH = "C:/Users/hariv/Downloads/files/hospital_project/diabetic_data_cleaned.csv"

def save_fig(name):
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/{name}.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {name}.png")

BLUE = '#2980B9'; RED = '#E74C3C'; GREEN = '#27AE60'; ORANGE = '#E67E22'; PURPLE = '#8E44AD'

# ── Load Data ─────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

# ==============================================================
# 5.1 – PREDICTIVE MODELING
# ==============================================================
print("\n" + "="*60)
print("5.1 – PREDICTIVE MODELING")
print("="*60)

# Feature selection – using available columns
NUM_FEATURES = [
    'time_in_hospital', 'num_lab_procedures', 'num_procedures',
    'num_medications', 'number_outpatient', 'number_emergency',
    'number_inpatient', 'number_diagnoses', 'admission_type_id',
    'discharge_disposition_id', 'admission_source_id'
]

CAT_FEATURES = [
    'race', 'gender', 'age', 'change', 'diabetesMed',
    'insulin', 'metformin', 'glipizide', 'glyburide', 'pioglitazone',
    'rosiglitazone', 'A1Cresult', 'max_glu_serum'
]

TARGET = 'readmitted_binary'

# Build feature matrix
df_ml = df[NUM_FEATURES + CAT_FEATURES + [TARGET]].copy()

# Encode categoricals
le = LabelEncoder()
for col in CAT_FEATURES:
    df_ml[col] = df_ml[col].fillna('Unknown')
    df_ml[col] = le.fit_transform(df_ml[col].astype(str))

# Fill any remaining NaN in numerics
for col in NUM_FEATURES:
    df_ml[col] = df_ml[col].fillna(df_ml[col].median())

X = df_ml[NUM_FEATURES + CAT_FEATURES]
y = df_ml[TARGET]

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target distribution:")
print(f"  Class 0 (not readmitted in 30d): {(y==0).sum():,} ({(y==0).mean()*100:.1f}%)")
print(f"  Class 1 (readmitted in 30d)    : {(y==1).sum():,} ({(y==1).mean()*100:.1f}%)")
print(f"\nNOTE: Class imbalance ~11% positive class. Using class_weight='balanced' for models.")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain set: {X_train.shape[0]:,} | Test set: {X_test.shape[0]:,}")

# Scale
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

results = {}

# ── Model 1: Logistic Regression ─────────────────────────────
print("\n── Model 1: Logistic Regression ──")
lr = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
lr.fit(X_train_sc, y_train)
y_pred_lr = lr.predict(X_test_sc)
y_prob_lr = lr.predict_proba(X_test_sc)[:, 1]
roc_lr = roc_auc_score(y_test, y_prob_lr)
report_lr = classification_report(y_test, y_pred_lr, output_dict=True)
results['Logistic Regression'] = {
    'model': lr, 'y_pred': y_pred_lr, 'y_prob': y_prob_lr,
    'roc_auc': roc_lr, 'report': report_lr
}
print(f"   ROC-AUC: {roc_lr:.4f}")
print(f"   Accuracy: {report_lr['accuracy']:.4f}")
print(f"   Precision (class 1): {report_lr['1']['precision']:.4f}")
print(f"   Recall    (class 1): {report_lr['1']['recall']:.4f}")
print(f"   F1-Score  (class 1): {report_lr['1']['f1-score']:.4f}")

# ── Model 2: Decision Tree ────────────────────────────────────
print("\n── Model 2: Decision Tree ──")
dt = DecisionTreeClassifier(class_weight='balanced', max_depth=8, random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
y_prob_dt = dt.predict_proba(X_test)[:, 1]
roc_dt = roc_auc_score(y_test, y_prob_dt)
report_dt = classification_report(y_test, y_pred_dt, output_dict=True)
results['Decision Tree'] = {
    'model': dt, 'y_pred': y_pred_dt, 'y_prob': y_prob_dt,
    'roc_auc': roc_dt, 'report': report_dt
}
print(f"   ROC-AUC: {roc_dt:.4f}")
print(f"   Accuracy: {report_dt['accuracy']:.4f}")
print(f"   Precision (class 1): {report_dt['1']['precision']:.4f}")
print(f"   Recall    (class 1): {report_dt['1']['recall']:.4f}")
print(f"   F1-Score  (class 1): {report_dt['1']['f1-score']:.4f}")

# ── Model 3: Random Forest ────────────────────────────────────
print("\n── Model 3: Random Forest ──")
rf = RandomForestClassifier(
    n_estimators=100, class_weight='balanced',
    max_depth=10, random_state=42, n_jobs=-1
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]
roc_rf = roc_auc_score(y_test, y_prob_rf)
report_rf = classification_report(y_test, y_pred_rf, output_dict=True)
results['Random Forest'] = {
    'model': rf, 'y_pred': y_pred_rf, 'y_prob': y_prob_rf,
    'roc_auc': roc_rf, 'report': report_rf
}
print(f"   ROC-AUC: {roc_rf:.4f}")
print(f"   Accuracy: {report_rf['accuracy']:.4f}")
print(f"   Precision (class 1): {report_rf['1']['precision']:.4f}")
print(f"   Recall    (class 1): {report_rf['1']['recall']:.4f}")
print(f"   F1-Score  (class 1): {report_rf['1']['f1-score']:.4f}")

# ── Model Comparison Chart ────────────────────────────────────
print("\n── Model Comparison ──")
model_names = list(results.keys())
metrics = {
    'ROC-AUC':  [results[m]['roc_auc'] for m in model_names],
    'Recall':   [results[m]['report']['1']['recall'] for m in model_names],
    'Precision':[results[m]['report']['1']['precision'] for m in model_names],
    'F1-Score': [results[m]['report']['1']['f1-score'] for m in model_names],
    'Accuracy': [results[m]['report']['accuracy'] for m in model_names],
}
comp_df = pd.DataFrame(metrics, index=model_names)
print(comp_df.round(4))

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(model_names))
w = 0.15
colors = [BLUE, GREEN, RED, ORANGE, PURPLE]
for i, (metric, vals) in enumerate(metrics.items()):
    ax.bar(x + i*w - 2*w, vals, w, label=metric, color=colors[i])
ax.set_xticks(x)
ax.set_xticklabels(model_names, fontsize=12)
ax.set_ylabel('Score')
ax.set_title('Model Performance Comparison (30-Day Readmission Prediction)', fontsize=13, fontweight='bold')
ax.legend()
ax.set_ylim(0, 1)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.axhline(y=0.5, color='gray', linestyle=':', label='Baseline')
save_fig("ml_model_comparison")

# ── ROC Curves ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
colors_roc = [BLUE, GREEN, RED]
for (name, res), color in zip(results.items(), colors_roc):
    fpr, tpr, _ = roc_curve(y_test, res['y_prob'])
    ax.plot(fpr, tpr, color=color, lw=2, label=f"{name} (AUC={res['roc_auc']:.3f})")
ax.plot([0,1],[0,1],'--', color='gray', label='Random Classifier')
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate (Recall)', fontsize=12)
ax.set_title('ROC Curves – 30-Day Readmission Prediction', fontsize=13, fontweight='bold')
ax.legend(loc='lower right')
ax.grid(alpha=0.3)
save_fig("ml_roc_curves")

# ── Confusion Matrix – Best Model (Random Forest) ────────────
fig, ax = plt.subplots(figsize=(6, 5))
cm = confusion_matrix(y_test, y_pred_rf)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Not Readmitted','Readmitted <30d'])
disp.plot(ax=ax, cmap='Blues', colorbar=False)
ax.set_title('Confusion Matrix – Random Forest', fontsize=13, fontweight='bold')
save_fig("ml_confusion_matrix_rf")

# ── Feature Importance (Random Forest) ───────────────────────
feature_names = NUM_FEATURES + CAT_FEATURES
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False).head(15)
print("\nTop 15 Feature Importances (Random Forest):")
print(importance_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(importance_df['feature'][::-1], importance_df['importance'][::-1], color=BLUE)
ax.set_title('Top 15 Feature Importances – Random Forest', fontsize=13, fontweight='bold')
ax.set_xlabel('Importance Score')
ax.grid(axis='x', linestyle='--', alpha=0.5)
save_fig("ml_feature_importance")

print("\n── Healthcare Recall vs Precision Trade-off ──")
print("""
   In a healthcare readmission prediction context:
   
   - RECALL (Sensitivity) = Of all actual readmissions, how many did the model identify?
     HIGH RECALL = Fewer missed readmissions (fewer false negatives)
     A patient missed (FN) = not identified as at-risk, potentially readmitted without intervention
     This is the PRIMARY metric for clinical usefulness.
   
   - PRECISION = Of all patients flagged as high-risk, what proportion were actually readmitted?
     LOW PRECISION = More false alarms (unnecessary interventions but less harm)
   
   - In healthcare: a FALSE NEGATIVE (missed readmission) is generally more costly than
     a FALSE POSITIVE (unnecessary follow-up), so we prioritize RECALL over PRECISION.
   
   - The trade-off should be discussed with clinical teams to set appropriate threshold.
""")

# ==============================================================
# 5.2 – PATIENT SEGMENTATION (K-MEANS CLUSTERING)
# ==============================================================
print("\n" + "="*60)
print("5.2 – PATIENT SEGMENTATION (K-MEANS)")
print("="*60)

# Features for clustering: healthcare utilization
cluster_features = [
    'time_in_hospital', 'num_lab_procedures', 'num_procedures',
    'num_medications', 'number_outpatient', 'number_emergency',
    'number_inpatient', 'number_diagnoses'
]

X_cluster = df[cluster_features].copy().fillna(df[cluster_features].median())
scaler_cl = StandardScaler()
X_scaled = scaler_cl.fit_transform(X_cluster)

# Elbow method
print("\nRunning Elbow Method to find optimal K...")
inertias = []
k_range = range(2, 9)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(f"   K={k}: Inertia={km.inertia_:.0f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(k_range, inertias, 'o-', color=BLUE, linewidth=2, markersize=8)
ax.set_xlabel('Number of Clusters (K)')
ax.set_ylabel('Inertia (Within-cluster Sum of Squares)')
ax.set_title('Elbow Method for Optimal K', fontsize=13, fontweight='bold')
ax.grid(linestyle='--', alpha=0.5)
save_fig("kmeans_elbow")

# Fit with K=4 (good practical segmentation for hospital use)
K_OPTIMAL = 4
print(f"\nFitting K-Means with K={K_OPTIMAL}...")
km_final = KMeans(n_clusters=K_OPTIMAL, random_state=42, n_init=10)
df['patient_segment'] = km_final.fit_predict(X_scaled)

# Analyze segments
seg_analysis = df.groupby('patient_segment').agg(
    count=('encounter_id','count'),
    avg_los=('time_in_hospital','mean'),
    avg_lab=('num_lab_procedures','mean'),
    avg_procedures=('num_procedures','mean'),
    avg_medications=('num_medications','mean'),
    avg_outpatient=('number_outpatient','mean'),
    avg_emergency=('number_emergency','mean'),
    avg_inpatient=('number_inpatient','mean'),
    avg_diagnoses=('number_diagnoses','mean'),
    readmit_rate=('readmitted_binary','mean')
).reset_index()
seg_analysis['readmit_pct'] = (seg_analysis['readmit_rate'] * 100).round(2)
print("\nSegment Summary:")
print(seg_analysis.round(2).to_string(index=False))

# Business-friendly segment labels
seg_labels = {}
for _, row in seg_analysis.iterrows():
    seg = int(row['patient_segment'])
    if row['avg_emergency'] > 0.5 and row['readmit_pct'] > 12:
        seg_labels[seg] = f"Seg {seg}: High-Risk / Emergency-Prone"
    elif row['avg_inpatient'] > 1.5:
        seg_labels[seg] = f"Seg {seg}: Complex / Chronic Patients"
    elif row['avg_medications'] > 20:
        seg_labels[seg] = f"Seg {seg}: High Medication Burden"
    else:
        seg_labels[seg] = f"Seg {seg}: Low-Acuity / Stable Patients"

print("\nBusiness-Friendly Segment Labels:")
for seg, label in seg_labels.items():
    row = seg_analysis[seg_analysis['patient_segment'] == seg].iloc[0]
    print(f"\n   {label}")
    print(f"      Patients      : {row['count']:,}")
    print(f"      Avg LOS       : {row['avg_los']:.1f} days")
    print(f"      Avg Meds      : {row['avg_medications']:.1f}")
    print(f"      Avg Diagnoses : {row['avg_diagnoses']:.1f}")
    print(f"      Prior Emerg   : {row['avg_emergency']:.2f}")
    print(f"      Prior Inpatient: {row['avg_inpatient']:.2f}")
    print(f"      Readmit Rate  : {row['readmit_pct']:.2f}%")

# PCA for visualization
print("\nGenerating segment visualization...")
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

fig, ax = plt.subplots(figsize=(10, 7))
colors_seg = [BLUE, RED, GREEN, ORANGE]
for seg in range(K_OPTIMAL):
    mask = df['patient_segment'] == seg
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
               s=5, alpha=0.3, color=colors_seg[seg],
               label=seg_labels[seg])
ax.set_title('Patient Segments (K-Means, K=4) – PCA View', fontsize=13, fontweight='bold')
ax.set_xlabel(f'PCA Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)')
ax.set_ylabel(f'PCA Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)')
ax.legend(loc='upper right', fontsize=8)
ax.grid(alpha=0.2)
save_fig("kmeans_segments_pca")

# Segment readmission bar chart
fig, ax = plt.subplots(figsize=(10, 5))
seg_names = [seg_labels[i] for i in range(K_OPTIMAL)]
bars = ax.bar(range(K_OPTIMAL), seg_analysis['readmit_pct'], color=colors_seg, edgecolor='white')
for bar, val in zip(bars, seg_analysis['readmit_pct']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.2, f'{val:.1f}%', ha='center', va='bottom')
ax.set_xticks(range(K_OPTIMAL))
ax.set_xticklabels(seg_names, rotation=15, ha='right', fontsize=9)
ax.set_title('30-Day Readmission Rate by Patient Segment', fontsize=13, fontweight='bold')
ax.set_ylabel('Readmission Rate (%)')
ax.grid(axis='y', linestyle='--', alpha=0.5)
save_fig("kmeans_segment_readmit")

# ==============================================================
# 5.3 – FINANCIAL IMPACT
# ==============================================================
print("\n" + "="*60)
print("5.3 – FINANCIAL IMPACT")
print("="*60)
print("""
   NOT AVAILABLE: The dataset does not contain any cost, revenue,
   billing, or insurance reimbursement fields.
   
   Financial impact analysis would require:
   - Hospital cost per encounter
   - Insurance reimbursement data
   - Cost of readmission penalties (e.g., CMS HRRP program)
   - Length-of-stay cost estimates
   
   NOTE: Inventing hospital costs would be misleading and unethical.
   Only real cost data from hospital billing records would be appropriate here.
   
   For portfolio purposes, this limitation should be clearly stated in
   the project documentation.
""")

# ==============================================================
# 5.4 – SOCIAL DETERMINANTS
# ==============================================================
print("\n" + "="*60)
print("5.4 – SOCIAL DETERMINANTS")
print("="*60)
print("""
   PARTIAL: Only demographic data is available (race, gender, age).
   
   True social determinants of health (SDOH) require:
   - Socioeconomic status / income level
   - Education level
   - Housing stability
   - Food security
   - Geographic access to care
   - Health literacy
   
   WHAT CAN BE OBSERVED from this dataset:
   - Racial and gender differences in readmission rates are visible but SMALL
   - These differences cannot be causally attributed to race or gender
   - They may reflect unequal access to care, insurance coverage gaps,
     or unmeasured comorbidities
   
   IMPORTANT CAUTION:
   Do not draw causal conclusions about race/gender and health outcomes
   from this dataset without accounting for confounding variables.
   
   Responsible recommendation: Supplement with SDOH data for deeper analysis.
""")

print("\n\nPhase 5 Advanced Analytics Complete!")
print("All plots saved to:", PLOT_DIR)

# Save segment info to CSV
seg_analysis['segment_label'] = seg_analysis['patient_segment'].map(seg_labels)
seg_analysis.to_csv(f"{PLOT_DIR}/patient_segments.csv", index=False)

# Save model metrics
metrics_out = []
for name, res in results.items():
    metrics_out.append({
        'Model': name,
        'ROC_AUC': round(res['roc_auc'], 4),
        'Accuracy': round(res['report']['accuracy'], 4),
        'Precision_1': round(res['report']['1']['precision'], 4),
        'Recall_1': round(res['report']['1']['recall'], 4),
        'F1_1': round(res['report']['1']['f1-score'], 4),
    })
metrics_df = pd.DataFrame(metrics_out)
metrics_df.to_csv(f"{PLOT_DIR}/model_metrics.csv", index=False)
print(f"\nModel metrics saved: {PLOT_DIR}/model_metrics.csv")
print(f"Patient segments saved: {PLOT_DIR}/patient_segments.csv")
