# 02-Deliverables.md - Data Collection & Cleaning

## Phase: 1 - Data Collection & Cleaning

**Deadline: End of Week 2**

---

## Overview

This phase focuses on acquiring datasets, cleaning data, and performing initial exploratory analysis.

---

## Team Assignments

| Member | Name | GitHub | Task |
|-------|------|--------|------|
| **Member 1** | lBebol (Abdelrahman Yasser Hassan Zaky) | lBebol | Project Lead - Coordinate & Review |
| **Member 2** | tarek0026 | github.com/tarek0026 | Q1: Download & Clean Green Space + Air Quality Data |
| **Member 3** | Yehia312 | github.com/Yehia312 | Q2: Download & Clean Temperature + Electricity Data |
| **Member 4** | koka-gamal | github.com/koka-gamal | Q3: Download & Clean Air Quality Time Series Data |
| **Member 5** | Loaay Ahmed Mohammed (221001621) | — | Verify all data files, Create data dictionary |

---

## Tasks by Member

### Member 2 [tarek0026] - Research Q1 Data
- [ ] Download air quality data (PM2.5, PM10, NO2) for target cities
- [ ] Download green space coverage data
- [ ] Merge datasets by city name
- [ ] Handle missing values
- [ ] Save cleaned data to `data/q1_green_space_air_quality/cleaned_data.csv`
- [ ] Create initial EDA notebook in `notebooks/q1_green_space_air_quality/q1_eda.ipynb`

### Member 3 [Yehia312] - Research Q2 Data
- [ ] Download temperature data for major cities
- [ ] Download electricity consumption data
- [ ] Merge datasets by city/year
- [ ] Handle missing values
- [ ] Save cleaned data to `data/q2_temperature_electricity/cleaned_data.csv`
- [ ] Create initial EDA notebook in `notebooks/q2_temperature_electricity/q2_eda.ipynb`

### Member 4 [koka-gamal] - Research Q3 Data
- [ ] Download hourly/daily air quality data
- [ ] Extract day of week from dates
- [ ] Categorize as weekend/weekday
- [ ] Handle missing values
- [ ] Save cleaned data to `data/q3_weekend_weekday_pollution/cleaned_data.csv`
- [ ] Create initial EDA notebook in `notebooks/q3_weekend_weekday_pollution/q3_eda.ipynb`

### Member 5 [Loaay Ahmed Mohammed] - Data Verification
- [ ] Review all cleaned datasets
- [ ] Create `docs/data-dictionary.md` documenting all variables
- [ ] Verify data quality and consistency

---

## Branch Workflow

| Member | Branch Name | Deliverables |
|--------|-------------|--------------|
| Member 2 | `phase1/q1-data` | `data/q1_green_space_air_quality/cleaned_data.csv`, `notebooks/q1_green_space_air_quality/q1_eda.ipynb` |
| Member 3 | `phase1/q2-data` | `data/q2_temperature_electricity/cleaned_data.csv`, `notebooks/q2_temperature_electricity/q2_eda.ipynb` |
| Member 4 | `phase1/q3-data` | `data/q3_weekend_weekday_pollution/cleaned_data.csv`, `notebooks/q3_weekend_weekday_pollution/q3_eda.ipynb` |
| Member 5 | `phase1/verify` | `docs/data-dictionary.md` |

---

## PR & Merge Rules

1. Create a branch: `phase1/member-X-task`
2. Work on your deliverable(s)
3. Push and create Pull Request to `main`
4. **Member 1 (You) must approve** before merge

---

## Verification Checklist

- [ ] Member 2: `data/q1_green_space_air_quality/cleaned_data.csv` and `notebooks/q1_green_space_air_quality/q1_eda.ipynb` complete
- [ ] Member 3: `data/q2_temperature_electricity/cleaned_data.csv` and `notebooks/q2_temperature_electricity/q2_eda.ipynb` complete
- [ ] Member 4: `data/q3_weekend_weekday_pollution/cleaned_data.csv` and `notebooks/q3_weekend_weekday_pollution/q3_eda.ipynb` complete
- [ ] Member 5: `docs/data-dictionary.md` complete
- [ ] All PRs merged to `main`

---

## Next Steps

After this phase closes, **03-deliverables.md** will release with Phase 2 tasks:
- Statistical Analysis
- Visualization Creation

---

**Phase 1 Deadline: End of Week 2**