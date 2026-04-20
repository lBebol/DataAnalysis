# 01-Deliverables.md - Project Initialization

## Phase: 0 - Documentation & Setup

**Deadline: End of Week 1**

---

## Overview

This phase focuses on setting up the project foundation, researching each research question, and preparing data sources for analysis.

---

## Team Assignments

| Member | Name | GitHub | Task |
|-------|------|--------|------|
| **Member 1** | **[You]** | - | Repository Setup - Create GitHub repo, folder structure, `.gitignore`, `README.md` |
| **Member 2** | tarek0026 | github.com/tarek0026 | Research Q1 Documentation - Green Space & Air Quality |
| **Member 3** | Yehia312 | github.com/Yehia312 | Research Q2 Documentation - Temperature & Electricity |
| **Member 4** | koka-gamal | github.com/koka-gamal | Research Q3 Documentation - Weekend vs Weekday Pollution |
| **Member 5** | **[Unknown]** | - | Data Sourcing Guide |

---

## Folder Structure

```
/DataAnalysis/
├── docs/
│   ├── 01-deliverables.md     ← Member 1
│   ├── 02-deliverables.md     ← (Phase 1)
│   ├── 03-deliverables.md    ← (Phase 2)
│   ├── 04-deliverables.md    ← (Phase 3)
│   ├── research-q1.md         ← Member 2
│   ├── research-q2.md        ← Member 3
│   ├── research-q3.md        ← Member 4
│   └── data-sources.md       ← Member 5
├── data/
├── notebooks/
├── src/
├── results/
├── .gitignore
└── README.md
```

---

## Branch Workflow

Each member creates a branch and works on their deliverable:

| Member | Branch Name | Task | Deliverable |
|--------|-------------|------|--------------|
| Member 1 | `phase0/setup` | Repository setup, create this file | `docs/01-deliverables.md` |
| Member 2 | `phase0/research-q1` | Research question 1 documentation | `docs/research-q1.md` |
| Member 3 | `phase0/research-q2` | Research question 2 documentation | `docs/research-q2.md` |
| Member 4 | `phase0/research-q3` | Research question 3 documentation | `docs/research-q3.md` |
| Member 5 | `phase0/data-sources` | Data sourcing guide | `docs/data-sources.md` |

---

## Research Doc Template

Each research document (`research-qX.md`) should include:

1. **Research Question** - The exact question being investigated
2. **Hypothesis** - Expected relationship between variables
3. **Literature Review** - 2-3 relevant studies or articles
4. **Proposed Data Sources** - Specific datasets to use
5. **Variables Required** - What data fields are needed for analysis
6. **Methodology** - Statistical approach planned

---

## Data Sources Doc Template

`data-sources.md` should include for each research question:

| Research Question | Dataset Name | Source Link | Description |
|------------------|-------------|-------------|-------------|
| Q1 | - | - | - |
| Q2 | - | - | - |
| Q3 | - | - | - |

Include: download instructions, licensing, and last updated date.

---

## PR & Merge Rules

1. Create a branch: `phase0/member-X-task`
2. Work on your deliverable
3. Push and create Pull Request to `main`
4. **Member 1 (You) must approve** before merge
5. All members can review but approval is limited to Member 1

---

## Verification Checklist (Pre-Merge)

- [ ] Repository created on GitHub
- [ ] All folders created in project directory
- [ ] `.gitignore` includes Python, Jupyter, data, and IDE patterns
- [ ] `README.md` has project overview and team
- [ ] `01-deliverables.md` created and complete
- [ ] `research-q1.md` complete
- [ ] `research-q2.md` complete
- [ ] `research-q3.md` complete
- [ ] `data-sources.md` complete (or pending Member 5)
- [ ] All PRs merged to `main`

---

## Next Steps

After this phase closes, **02-deliverables.md** will release with Phase 1 tasks:
- Data Collection & Cleaning
- Initial Exploratory Analysis

---

**Phase 0 Deadline: End of Week 1**