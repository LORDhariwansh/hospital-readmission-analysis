"""
==============================================================
HOSPITAL READMISSION ANALYSIS
Summary Dashboard Chart (Phase 9 - Final Visualization)
All numbers are actual values from the UCI dataset
==============================================================
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

PLOT_DIR = "C:/Users/hariv/Downloads/files/hospital_project/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# ── Color Palette ─────────────────────────────────────────────
BLUE    = '#2980B9'
RED     = '#E74C3C'
GREEN   = '#27AE60'
ORANGE  = '#E67E22'
PURPLE  = '#8E44AD'
TEAL    = '#16A085'
DARK    = '#2C3E50'
LIGHT   = '#ECF0F1'

def save_fig(name):
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/{name}.png", dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {name}.png")

# ==============================================================
# CHART 1: Executive Summary Dashboard (4-panel)
# ==============================================================
fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor('#F8F9FA')
gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.4)

# ── KPI Strip ─────────────────────────────────────────────────
kpi_ax = fig.add_subplot(gs[0, :])
kpi_ax.set_facecolor(DARK)
kpi_ax.set_xlim(0, 6); kpi_ax.set_ylim(0, 1)
kpi_ax.axis('off')

kpis = [
    ("101,766", "Total Encounters"),
    ("71,518", "Unique Patients"),
    ("11,357", "30-Day Readmissions"),
    ("11.16%", "Readmission Rate"),
    ("4.40 Days", "Avg Length of Stay"),
    ("16.02", "Avg Medications"),
]
for i, (val, label) in enumerate(kpis):
    x = 0.08 + i * 0.97
    kpi_ax.text(x, 0.65, val, ha='center', va='center', fontsize=16,
                fontweight='bold', color='white')
    kpi_ax.text(x, 0.22, label, ha='center', va='center', fontsize=9,
                color='#BDC3C7')
    if i < len(kpis) - 1:
        kpi_ax.axvline(x=0.56 + i*0.97, color='#4A5568', linewidth=1, alpha=0.5)

kpi_ax.set_title("Hospital Readmission Analysis – Executive Dashboard | UCI Diabetes 130-US Hospitals",
                 fontsize=14, fontweight='bold', color=DARK, pad=12, loc='left')

# ── Panel 1: Readmission by Age ───────────────────────────────
ax1 = fig.add_subplot(gs[1, :2])
ages  = ['[0-10)','[10-20)','[20-30)','[30-40)','[40-50)',
         '[50-60)','[60-70)','[70-80)','[80-90)','[90-100)']
rates = [1.86, 5.79, 14.24, 11.23, 10.60, 9.67, 11.13, 11.77, 12.08, 11.10]
colors_age = [RED if r > 12 else (ORANGE if r > 11 else BLUE) for r in rates]
bars = ax1.bar(ages, rates, color=colors_age, edgecolor='white', width=0.7)
for bar, r in zip(bars, rates):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{r:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')
ax1.set_title('30-Day Readmission Rate by Age Group', fontweight='bold', fontsize=11)
ax1.set_ylabel('Readmission Rate (%)', fontsize=9)
ax1.set_ylim(0, 18)
ax1.tick_params(axis='x', rotation=30, labelsize=8)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.axhline(y=11.16, color=RED, linestyle='--', linewidth=1.2, label='Avg: 11.16%')
ax1.legend(fontsize=8)

# ── Panel 2: Emergency Visits vs Readmission ──────────────────
ax2 = fig.add_subplot(gs[1, 2:])
emerg_cats = ['0 Visits', '1 Visit', '2 Visits', '3 Visits', '4+ Visits']
emerg_rates = [10.47, 14.35, 18.27, 20.28, 28.54]
emerg_counts = [90383, 7677, 2042, 725, 939]
ax2b = ax2.twinx()
b = ax2.bar(emerg_cats, emerg_counts, color=BLUE, alpha=0.5, label='Patient Count')
l, = ax2b.plot(emerg_cats, emerg_rates, color=RED, marker='o', linewidth=2.5,
               markersize=8, label='Readmit Rate %')
ax2.set_title('Emergency Visit History vs 30-Day Readmission', fontweight='bold', fontsize=11)
ax2.set_ylabel('Patient Count', color=BLUE, fontsize=9)
ax2b.set_ylabel('Readmission Rate (%)', color=RED, fontsize=9)
ax2b.set_ylim(0, 35)
ax2.grid(axis='y', linestyle='--', alpha=0.3)
lines = [b, l]; labels = ['Patient Count', 'Readmit Rate %']
ax2.legend(lines, labels, loc='upper left', fontsize=8)
ax2b.axhline(y=11.16, color=RED, linestyle='--', linewidth=1, alpha=0.5)

# ── Panel 3: Utilization Category ────────────────────────────
ax3 = fig.add_subplot(gs[2, 0])
util_cats = ['No Prior\nUtilization', 'Low\n(1-2)', 'Moderate\n(3-5)', 'High\n(6+)']
util_rates = [8.18, 12.59, 16.39, 25.51]
util_colors = [GREEN, BLUE, ORANGE, RED]
bars3 = ax3.bar(util_cats, util_rates, color=util_colors, edgecolor='white', width=0.6)
for bar, r in zip(bars3, util_rates):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
             f'{r:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax3.set_title('Readmission by\nUtilization Category', fontweight='bold', fontsize=10)
ax3.set_ylabel('Readmission Rate (%)', fontsize=9)
ax3.set_ylim(0, 32)
ax3.grid(axis='y', linestyle='--', alpha=0.4)
ax3.axhline(y=11.16, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# ── Panel 4: Patient Segments ─────────────────────────────────
ax4 = fig.add_subplot(gs[2, 1])
seg_labels = ['Seg 0\nLow-Acuity\n(n=29,204)', 'Seg 1\nHigh Meds\n(n=21,745)',
              'Seg 2\nHigh-Risk\n(n=6,705)', 'Seg 3\nModerate\n(n=44,112)']
seg_rates = [8.09, 12.17, 24.35, 10.69]
seg_colors = [GREEN, ORANGE, RED, BLUE]
bars4 = ax4.bar(seg_labels, seg_rates, color=seg_colors, edgecolor='white', width=0.6)
for bar, r in zip(bars4, seg_rates):
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
             f'{r:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax4.set_title('Readmission by\nPatient Segment (K=4)', fontweight='bold', fontsize=10)
ax4.set_ylabel('Readmission Rate (%)', fontsize=9)
ax4.set_ylim(0, 30)
ax4.tick_params(axis='x', labelsize=7)
ax4.grid(axis='y', linestyle='--', alpha=0.4)
ax4.axhline(y=11.16, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# ── Panel 5: Medications vs LOS ──────────────────────────────
ax5 = fig.add_subplot(gs[2, 2])
med_groups = ['Low\n(1-5)', 'Moderate\n(6-15)', 'High\n(16-25)', 'Very High\n(26+)']
med_los = [2.28, 3.50, 5.04, 7.31]
med_colors_v = [GREEN, BLUE, ORANGE, RED]
bars5 = ax5.bar(med_groups, med_los, color=med_colors_v, edgecolor='white', width=0.6)
for bar, r in zip(bars5, med_los):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.08,
             f'{r:.2f}d', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax5.set_title('Avg LOS by\nMedication Count Group', fontweight='bold', fontsize=10)
ax5.set_ylabel('Avg Length of Stay (days)', fontsize=9)
ax5.set_ylim(0, 9)
ax5.grid(axis='y', linestyle='--', alpha=0.4)

# ── Panel 6: ML Model Comparison ─────────────────────────────
ax6 = fig.add_subplot(gs[2, 3])
models = ['Logistic\nRegression', 'Decision\nTree', 'Random\nForest']
auc_scores = [0.6458, 0.6618, 0.6692]
recall_scores = [0.5161, 0.5980, 0.5795]
x_pos = np.arange(len(models))
w = 0.35
b1 = ax6.bar(x_pos - w/2, auc_scores, w, label='ROC-AUC', color=BLUE, alpha=0.9)
b2 = ax6.bar(x_pos + w/2, recall_scores, w, label='Recall', color=RED, alpha=0.9)
for bar, v in zip(b1, auc_scores):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
             f'{v:.3f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
for bar, v in zip(b2, recall_scores):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
             f'{v:.3f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
ax6.set_title('ML Model Performance\n(Recall prioritized in healthcare)', fontweight='bold', fontsize=9)
ax6.set_xticks(x_pos)
ax6.set_xticklabels(models, fontsize=8)
ax6.set_ylim(0, 0.85)
ax6.legend(fontsize=8)
ax6.grid(axis='y', linestyle='--', alpha=0.4)

plt.suptitle('Hospital Readmission Analysis – DACS08 Portfolio Project | n=101,766 Encounters',
             fontsize=13, fontweight='bold', y=1.01, color=DARK)
save_fig("executive_dashboard_summary")

# ==============================================================
# CHART 2: Feature Importance (already generated, but add a better version)
# ==============================================================

fig2, ax = plt.subplots(figsize=(11, 6))
features = [
    'discharge_disposition_id', 'number_inpatient', 'num_lab_procedures',
    'time_in_hospital', 'number_emergency', 'num_medications',
    'number_diagnoses', 'admission_type_id', 'admission_source_id',
    'number_outpatient', 'num_procedures', 'age', 'race', 'gender', 'change'
]
importances = [0.148, 0.112, 0.098, 0.094, 0.087, 0.083, 0.078, 0.062,
               0.055, 0.048, 0.038, 0.035, 0.028, 0.022, 0.012]

colors_fi = [RED if v > 0.1 else (ORANGE if v > 0.07 else BLUE) for v in importances]
bars_fi = ax.barh(features[::-1], importances[::-1], color=colors_fi[::-1], edgecolor='white')
for bar, v in zip(bars_fi, importances[::-1]):
    ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
            f'{v:.3f}', va='center', fontsize=9)
ax.set_xlabel('Feature Importance Score (Random Forest)', fontsize=11)
ax.set_title('Top 15 Feature Importances – 30-Day Readmission Prediction\n(Random Forest | ROC-AUC = 0.669 | Recall = 0.58)',
             fontsize=12, fontweight='bold')
ax.set_xlim(0, 0.185)
ax.grid(axis='x', linestyle='--', alpha=0.4)
ax.axvline(x=0.1, color='gray', linestyle=':', alpha=0.5)
ax.text(0.1, -0.8, 'High\nImpact', ha='center', fontsize=8, color='gray')
save_fig("feature_importance_final")

# ==============================================================
# CHART 3: Complete Readmission Overview (donut + bars)
# ==============================================================

fig3, axes3 = plt.subplots(1, 3, figsize=(16, 6))
fig3.patch.set_facecolor('#F8F9FA')

# Donut chart - target distribution
sizes = [54864, 35545, 11357]
labels_d = ['Not Readmitted\n(NO)\n54,864 (53.9%)',
            'Readmitted >30d\n35,545 (34.9%)',
            'Readmitted <30d\n11,357 (11.2%)']
colors_d = [GREEN, ORANGE, RED]
wedges, texts = axes3[0].pie(sizes, colors=colors_d, startangle=90,
                              wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
axes3[0].legend(wedges, labels_d, loc='lower center', fontsize=8,
                bbox_to_anchor=(0.5, -0.22), ncol=1)
axes3[0].set_title('Target Variable Distribution\n(readmitted)', fontweight='bold', fontsize=11)

# Readmission by race
races  = ['Caucasian','AfricanAm.','Hispanic','Asian','Other']
rrates = [11.29, 11.22, 10.41, 10.14, 9.63]
rcolors = [BLUE, PURPLE, ORANGE, TEAL, GREEN]
bars_r = axes3[1].barh(races[::-1], rrates[::-1], color=rcolors[::-1], edgecolor='white')
for bar, v in zip(bars_r, rrates[::-1]):
    axes3[1].text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                  f'{v:.1f}%', va='center', fontsize=9, fontweight='bold')
axes3[1].axvline(x=11.16, color='gray', linestyle='--', linewidth=1.2, alpha=0.7, label='Avg: 11.16%')
axes3[1].set_xlabel('Readmission Rate (%)', fontsize=9)
axes3[1].set_title('30-Day Readmission Rate by Race\n(small differences; interpret cautiously)', fontweight='bold', fontsize=10)
axes3[1].set_xlim(0, 14)
axes3[1].legend(fontsize=8)
axes3[1].grid(axis='x', linestyle='--', alpha=0.3)

# Diagnosis burden vs readmission + LOS
diag_groups = ['Low\n(1-3)', 'Moderate\n(4-6)', 'High\n(7-9)', 'Very High\n(10+)']
diag_los  = [2.74, 3.70, 4.76, 5.10]
diag_read = [6.97, 9.44, 12.06, 14.78]
x_d = np.arange(len(diag_groups))
w_d = 0.35
ax3b = axes3[2].twinx()
b_d1 = axes3[2].bar(x_d - w_d/2, diag_los, w_d, color=BLUE, alpha=0.8, label='Avg LOS (days)')
b_d2 = ax3b.bar(x_d + w_d/2, diag_read, w_d, color=RED, alpha=0.8, label='Readmit Rate %')
for bar, v in zip(b_d1, diag_los):
    axes3[2].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
                  f'{v:.1f}d', ha='center', va='bottom', fontsize=8)
for bar, v in zip(b_d2, diag_read):
    ax3b.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
              f'{v:.1f}%', ha='center', va='bottom', fontsize=8)
axes3[2].set_xticks(x_d)
axes3[2].set_xticklabels(diag_groups)
axes3[2].set_ylabel('Avg LOS (days)', color=BLUE, fontsize=9)
ax3b.set_ylabel('Readmission Rate (%)', color=RED, fontsize=9)
axes3[2].set_title('Diagnosis Burden:\nLOS & Readmission Rate', fontweight='bold', fontsize=10)
lines_d = [b_d1, b_d2]; labels_d2 = ['Avg LOS (days)', 'Readmit Rate %']
axes3[2].legend(lines_d, labels_d2, loc='upper left', fontsize=8)
axes3[2].grid(axis='y', linestyle='--', alpha=0.3)

plt.suptitle('Hospital Readmission Analysis – Patient & Clinical Overview', fontsize=13,
             fontweight='bold', y=1.02)
save_fig("patient_clinical_overview")

print("\nAll summary charts generated!")
print("Files saved:")
print(" - executive_dashboard_summary.png")
print(" - feature_importance_final.png")
print(" - patient_clinical_overview.png")
