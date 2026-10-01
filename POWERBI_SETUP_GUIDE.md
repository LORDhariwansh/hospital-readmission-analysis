# Power BI Dashboard Setup Guide
## Hospital Readmission Analysis – DACS08
### Step-by-Step Instructions

---

## Prerequisites

- Power BI Desktop (free download from Microsoft)
- File: `diabetic_data_cleaned.csv` (from this project folder)
- File: `phase8_dax_measures.dax` (DAX measures reference)

---

## STEP 1 – Load the Dataset

1. Open **Power BI Desktop**
2. Click **Home → Get Data → Text/CSV**
3. Navigate to: `C:\Users\hariv\Downloads\files\hospital_project\diabetic_data_cleaned.csv`
4. Click **Load**
5. In the Navigator, click **Transform Data** to open Power Query

---

## STEP 2 – Data Type Corrections in Power Query

In Power Query Editor, verify/set the following column types:

| Column | Correct Type |
|---|---|
| `encounter_id` | Whole Number |
| `patient_nbr` | Whole Number |
| `race` | Text |
| `gender` | Text |
| `age` | Text |
| `time_in_hospital` | Whole Number |
| `num_lab_procedures` | Whole Number |
| `num_procedures` | Whole Number |
| `num_medications` | Whole Number |
| `number_outpatient` | Whole Number |
| `number_emergency` | Whole Number |
| `number_inpatient` | Whole Number |
| `number_diagnoses` | Whole Number |
| `readmitted_binary` | Whole Number |
| `admission_type_id` | Whole Number |
| `discharge_disposition_id` | Whole Number |
| `change` | Text |
| `diabetesMed` | Text |
| `readmitted` | Text |
| `stay_category` | Text |
| `medication_group` | Text |
| `utilization_category` | Text |
| `diagnosis_burden` | Text |

Click **Close & Apply**.

---

## STEP 3 – Add Calculated Columns (DAX)

Go to **Table View** (left panel). Select the `diabetic_data_cleaned` table. Then use **Table Tools → New Column**:

### Column 1: Readmission Status Label
```dax
Readmission Status =
IF(
    diabetic_data_cleaned[readmitted_binary] = 1,
    "Readmitted within 30 Days",
    "Not Readmitted (or After 30 Days)"
)
```

### Column 2: Age Group Sort Order (for correct chart ordering)
```dax
Age Sort Order =
SWITCH(
    diabetic_data_cleaned[age],
    "[0-10)", 1, "[10-20)", 2, "[20-30)", 3, "[30-40)", 4,
    "[40-50)", 5, "[50-60)", 6, "[60-70)", 7, "[70-80)", 8,
    "[80-90)", 9, "[90-100)", 10, 99
)
```
> After creating, go to Column Tools → Sort By Column → select "Age Sort Order"

### Column 3: Stay Category Sort Order
```dax
Stay Category Sort =
SWITCH(
    diabetic_data_cleaned[stay_category],
    "1-2 Days (Short)", 1,
    "3-5 Days (Moderate)", 2,
    "6-8 Days (Long)", 3,
    "9+ Days (Extended)", 4, 5
)
```
> Sort `stay_category` column by `Stay Category Sort`

### Column 4: Medication Group Sort Order
```dax
Med Group Sort =
SWITCH(
    diabetic_data_cleaned[medication_group],
    "Low (1-5)", 1, "Moderate (6-15)", 2,
    "High (16-25)", 3, "Very High (26+)", 4, 5
)
```

### Column 5: Utilization Sort Order
```dax
Utilization Sort =
SWITCH(
    diabetic_data_cleaned[utilization_category],
    "No Prior Utilization", 1,
    "Low Utilization (1-2)", 2,
    "Moderate Utilization (3-5)", 3,
    "High Utilization (6+)", 4, 5
)
```

### Column 6: Total Prior Visits
```dax
Total Prior Visits =
    diabetic_data_cleaned[number_inpatient]
    + diabetic_data_cleaned[number_outpatient]
    + diabetic_data_cleaned[number_emergency]
```

---

## STEP 4 – Add Measures

Go to **Modeling → New Measure**. Add each of the following:

### Core KPI Measures

```dax
Total Encounters =
    COUNTROWS( diabetic_data_cleaned )

Unique Patients =
    DISTINCTCOUNT( diabetic_data_cleaned[patient_nbr] )

Total Readmissions =
    CALCULATE(
        COUNTROWS( diabetic_data_cleaned ),
        diabetic_data_cleaned[readmitted_binary] = 1
    )

Readmission Rate % =
    DIVIDE(
        [Total Readmissions],
        [Total Encounters],
        0
    ) * 100

Non-Readmissions =
    CALCULATE(
        COUNTROWS( diabetic_data_cleaned ),
        diabetic_data_cleaned[readmitted_binary] = 0
    )

Avg Length of Stay =
    AVERAGE( diabetic_data_cleaned[time_in_hospital] )

Avg Medications =
    AVERAGE( diabetic_data_cleaned[num_medications] )

Avg Lab Procedures =
    AVERAGE( diabetic_data_cleaned[num_lab_procedures] )

Avg Procedures =
    AVERAGE( diabetic_data_cleaned[num_procedures] )

Avg Diagnoses =
    AVERAGE( diabetic_data_cleaned[number_diagnoses] )

Avg Emergency Visits =
    AVERAGE( diabetic_data_cleaned[number_emergency] )

Avg Outpatient Visits =
    AVERAGE( diabetic_data_cleaned[number_outpatient] )

Avg Inpatient Visits =
    AVERAGE( diabetic_data_cleaned[number_inpatient] )
```

### Percentage Measures

```dax
Pct Diabetes Medication =
    DIVIDE(
        CALCULATE(
            COUNTROWS( diabetic_data_cleaned ),
            diabetic_data_cleaned[diabetesMed] = "Yes"
        ),
        [Total Encounters], 0
    ) * 100

Pct Medication Changed =
    DIVIDE(
        CALCULATE(
            COUNTROWS( diabetic_data_cleaned ),
            diabetic_data_cleaned[change] = "Ch"
        ),
        [Total Encounters], 0
    ) * 100

Pct High Utilization =
    DIVIDE(
        CALCULATE(
            COUNTROWS( diabetic_data_cleaned ),
            diabetic_data_cleaned[Total Prior Visits] >= 6
        ),
        [Total Encounters], 0
    ) * 100
```

### Segmentation Measures

```dax
Readmission Rate - Diabetes Med Yes % =
    CALCULATE(
        [Readmission Rate %],
        diabetic_data_cleaned[diabetesMed] = "Yes"
    )

Readmission Rate - Diabetes Med No % =
    CALCULATE(
        [Readmission Rate %],
        diabetic_data_cleaned[diabetesMed] = "No"
    )

Readmission Rate - Med Changed % =
    CALCULATE(
        [Readmission Rate %],
        diabetic_data_cleaned[change] = "Ch"
    )

Readmission Rate - No Change % =
    CALCULATE(
        [Readmission Rate %],
        diabetic_data_cleaned[change] = "No"
    )

Readmission Rate - High Utilization % =
    CALCULATE(
        [Readmission Rate %],
        diabetic_data_cleaned[Total Prior Visits] >= 6
    )

Readmission Rate Delta =
    [Readmission Rate %] -
    CALCULATE(
        [Readmission Rate %],
        ALL( diabetic_data_cleaned )
    )
```

---

## STEP 5 – Build Page 1: Executive Overview

### Add KPI Cards (top row)
Use the **Card** visual. One card per KPI:
- Drag `[Total Encounters]` → format as: no decimal, comma separator
- Drag `[Unique Patients]` → format as: no decimal, comma separator
- Drag `[Total Readmissions]` → format as: no decimal
- Drag `[Readmission Rate %]` → format as: 2 decimal, add "%" suffix
- Drag `[Avg Length of Stay]` → format as: 2 decimal, add " days" suffix
- Drag `[Avg Medications]` → format as: 1 decimal

> Card formatting: Title → On | Border → subtle | Background → light blue or white

### Add Bar Chart: Readmission by Age Group
- Visual: **Clustered Bar Chart**
- X-axis: `age` (sort by `Age Sort Order`)
- Y-axis: `[Readmission Rate %]`
- Title: "30-Day Readmission Rate by Age Group"
- Data labels: On | Color: accent color

### Add Bar Chart: Readmission by Gender
- Visual: **Clustered Bar Chart**
- X-axis: `gender`
- Y-axis: `[Readmission Rate %]`
- Filter: exclude NULL/Unknown gender

### Add Bar Chart: Readmission by Race
- Visual: **Clustered Bar Chart**
- X-axis: `race`
- Y-axis: `[Readmission Rate %]`
- Filter: exclude NULL race

### Add Bar Chart: Readmission by Diabetes Medication
- Visual: **Clustered Bar Chart**
- X-axis: `diabetesMed`
- Y-axis: `[Readmission Rate %]`

### Add Bar Chart: Readmission by Stay Category
- Visual: **Clustered Bar Chart**
- X-axis: `stay_category` (sort by `Stay Category Sort`)
- Y-axis: `[Readmission Rate %]`

### Add Slicers (right panel)
Use **Slicer** visual. One per field:
- `age` → Dropdown or List style
- `gender` → Tile style
- `race` → Dropdown
- `medical_specialty` → Dropdown
- `diabetesMed` → Tile style
- `Readmission Status` → Tile style

---

## STEP 6 – Build Page 2: Patient & Readmission Analysis

### Dual-Axis Chart: Emergency Visits vs Readmission
- Visual: **Line and Clustered Column Chart**
- Shared axis: `number_emergency` (binned: create bins 0,1,2,3,4+)
- Column values: `[Total Encounters]` (left axis)
- Line values: `[Readmission Rate %]` (right axis)
- Title: "Emergency Visits vs 30-Day Readmission Rate"

**Tip:** To bin emergency visits, add a calculated column:
```dax
Emergency Visit Bin =
    SWITCH(
        TRUE(),
        diabetic_data_cleaned[number_emergency] = 0, "0 Visits",
        diabetic_data_cleaned[number_emergency] = 1, "1 Visit",
        diabetic_data_cleaned[number_emergency] = 2, "2 Visits",
        diabetic_data_cleaned[number_emergency] = 3, "3 Visits",
        "4+ Visits"
    )
```

### Dual-Axis Chart: Outpatient Visits vs Readmission
- Same pattern as above but using `number_outpatient`

### Dual-Axis Chart: Inpatient Visits vs Readmission
- Same pattern using `number_inpatient`

### Bar Chart: Diagnoses vs Readmission
- X-axis: `diagnosis_burden` (sort by Diagnosis Sort Order)
- Y-axis: `[Readmission Rate %]`

### Matrix Heatmap: Race × Gender Readmission
- Visual: **Matrix**
- Rows: `race`
- Columns: `gender`
- Values: `[Readmission Rate %]`
- Conditional formatting: Background color (Red scale)

---

## STEP 7 – Build Page 3: Hospital Operations

### Horizontal Bar: Average LOS by Specialty
- Visual: **Clustered Bar Chart** (horizontal)
- Axis: `medical_specialty`
- Values: `[Avg Length of Stay]`
- Filter: `medical_specialty` is not blank AND count >= 100
- Sort: Descending by LOS
- Show top 15 specialties using Top N filter

### Bar Chart: Patient Volume by Specialty
- X-axis: `medical_specialty`
- Y-axis: `[Total Encounters]`
- Top N filter: Top 15

### Bar Charts: Avg Lab Procedures & Avg Medications by Specialty
- Same specialty axis, different Y-axis measures

### Donut Chart: Stay Category Distribution
- Values: `[Total Encounters]`
- Legend: `stay_category`
- Colors: Green (Short), Blue (Moderate), Orange (Long), Red (Extended)

### Bar Chart: Medication Group Distribution
- X-axis: `medication_group` (sorted)
- Y-axis: `[Total Encounters]`

---

## STEP 8 – Build Page 4: Advanced Insights

### Bar Chart: Readmission by Patient Segment
- Use `patient_segment` column (0–3)
- Y-axis: `[Readmission Rate %]`
- Colors: Red for Segment 2 (highest risk)
- Title: "30-Day Readmission Rate by Patient Segment"

### Matrix Table: Segment Profiles
- Visual: **Matrix** or **Table**
- Rows: `patient_segment`
- Columns: Avg LOS, Avg Medications, Avg Emergency, Readmission Rate %

### Table: ML Model Performance
- Create a **manual table** using Enter Data:

| Model | ROC-AUC | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|---|
| Logistic Regression | 0.6458 | 0.6688 | 0.172 | 0.516 | 0.258 |
| Decision Tree | 0.6618 | 0.6390 | 0.174 | 0.598 | 0.270 |
| Random Forest | 0.6692 | 0.6552 | 0.178 | 0.580 | 0.273 |

> Highlight the Recall column — most critical metric for healthcare readmission

### Bar Chart: Feature Importance (Top 10)
- Create **manual table** using Enter Data:

| Feature | Importance |
|---|---|
| discharge_disposition_id | 0.148 |
| number_inpatient | 0.112 |
| num_lab_procedures | 0.098 |
| time_in_hospital | 0.094 |
| number_emergency | 0.087 |
| num_medications | 0.083 |
| number_diagnoses | 0.078 |
| admission_type_id | 0.062 |
| admission_source_id | 0.055 |
| number_outpatient | 0.048 |

- Visual: Horizontal Bar Chart, sorted descending

### Text Cards: Key Findings & Recommendations
- Visual: **Text Box** or **Smart Narrative**
- Add key findings summary text

---

## STEP 9 – Formatting & Theme

### Apply Theme
- **View → Themes → Browse for themes** or use built-in "Classic"
- Recommended: Neutral/Corporate theme with Red accent for risk indicators

### Color Conventions (apply consistently)
- 🔴 **Red** = High Risk / Readmitted / Alert
- 🟠 **Orange** = Medium Risk / Warning
- 🟢 **Green** = Low Risk / Good
- 🔵 **Blue** = Informational / Count / Volume

### Font Recommendations
- Titles: Segoe UI Semibold, 14pt
- KPI values: Segoe UI Bold, 20pt+
- Labels: Segoe UI, 10pt

### Background
- Page background: White or very light grey (#F8F9FA)
- KPI cards: White with subtle border

---

## STEP 10 – Final Configuration

1. **Page Navigator**: Add page navigation buttons or use the built-in page tabs
2. **Tooltips**: Add custom tooltips showing patient count and readmission count on hover
3. **Drill-through**: Set up drill-through from specialty → patient level detail
4. **Bookmarks**: Create bookmarks for:
   - "High-Risk View" — filters to Segment 2 + high utilization
   - "Diabetes Focus" — filters to diabetesMed = Yes
   - "Reset All Filters"

5. **Report settings**:
   - File → Options → Report settings → Disable persistent filters
   - Enable cross-report drillthrough if publishing to service

---

## STEP 11 – Publish (Optional)

1. **File → Publish → Publish to Power BI**
2. Select your workspace
3. Share dashboard link with stakeholders
4. Set up **scheduled refresh** if connected to live data source

---

## Expected Dashboard Values (Actual from Dataset)

| KPI | Value |
|---|---|
| Total Encounters | 101,766 |
| Unique Patients | 71,518 |
| 30-Day Readmissions | 11,357 |
| Readmission Rate % | **11.16%** |
| Avg Length of Stay | 4.40 days |
| Avg Medications | 16.02 |
| Avg Lab Procedures | 43.10 |
| Avg Diagnoses | 7.42 |
| Highest Age Readmit Rate | 14.24% ([20-30) age group) |
| Highest Utilization Readmit | **25.51%** (High Utilization 6+) |
| Longest Avg Stay (Meds) | 7.31 days (Very High 26+ meds) |
| Emergency 4+ Readmit Rate | **28.54%** |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Age groups out of order | Sort `age` by `Age Sort Order` calculated column |
| `readmitted_binary` shows as text | Change column type to Whole Number |
| Specialty chart shows "Blank" | Add filter: `medical_specialty` is not blank |
| Race chart shows "?" | Add filter: `race` is not "?" / not blank |
| Division by zero in DAX | All measures use DIVIDE(n, d, 0) — safe by default |
| Weight analysis is unreliable | Add note: "96.87% weight data missing — interpret with caution" |
