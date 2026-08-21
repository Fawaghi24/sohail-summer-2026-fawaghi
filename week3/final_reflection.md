# Final Reflection — Week 3, Day 5

## 2.1 The Full Journey

On Day 1 I wrote that I hadn't used Python since high school, and that was genuinely true I could follow logic and structure, but syntax, libraries, and tooling were all rusty. My supervisor's Day 1 feedback confirmed exactly that: solid object-oriented thinking on Task 3, but shaky fundamentals everywhere else, and even my Technical Inventory used the wrong rating scale because I wasn't yet thinking in those terms.

Three weeks later, the gap has closed in a real, demonstrable way, not just a felt way. I went from writing top-level scripts with no error handling to structuring code into functions, using `pathlib` instead of hardcoded paths, and wrapping file access in `try/except`. I went from not knowing pandas at all to using `groupby`, `pivot_table`, `crosstab`, and `.corr()` fluently enough to run a full exploratory analysis on a real, messy dataset. I built and evaluated three regression models, understood why Linear Regression outperformed a Random Forest instead of just accepting the result, and shipped a working Streamlit dashboard that a non-technical person could actually use.

What changed most is not just knowledge but discipline checking for data leakage before trusting a good score, re-reading a spec against my own deliverable, documenting why a decision was made instead of just making it.

What hasn't fully changed: I'm still faster at reasoning about structure and logic than at recalling Python syntax from memory, and I still lean on documentation more than I'd like. That's an honest gap, not a solved one, and it's the right thing to keep working on next.

---

## 2.2 Skills Inventory — Final

| Technology                                                  | Day 1 Level                                | Final Level                | Changed?     |
| ----------------------------------------------------------- | ------------------------------------------ | -------------------------- | ------------ |
| Python core syntax                                          | Beginner (rusty, unused since high school) | Working knowledge          | ✅ Improved  |
| Object-oriented design (classes)                            | Working knowledge                          | Confident                  | ✅ Improved  |
| pandas                                                      | Not rated (not yet introduced)             | Working knowledge          | ✅ New skill |
| matplotlib / seaborn                                        | Not rated (not yet introduced)             | Working knowledge          | ✅ New skill |
| scikit-learn (regression, classification, CV, GridSearchCV) | Not rated (not yet introduced)             | Working knowledge          | ✅ New skill |
| Streamlit                                                   | Not rated (not yet introduced)             | Beginner–Working knowledge | ✅ New skill |
| Git & GitHub workflow                                       | Beginner                                   | Working knowledge          | ✅ Improved  |
| Markdown documentation                                      | Working knowledge                          | Confident                  | ✅ Improved  |
| Data cleaning & missing-value strategy                      | Not rated (not yet introduced)             | Working knowledge          | ✅ New skill |

---

## 2.3 What I Built

- **Week 1 diagnostic scripts** (`task1.py`, `task2.py`, `task3.py`) — data handling on a student CSV, a text-analysis function, and an OOP course/enrollment system.
- **`week1/day2_pandas_basics.py`** — reproduced the Day 1 analysis using pandas instead of manual loops, plus new grouped/aggregated statistics.
- **`week1/day3_cleaning.py` + `titanic_clean.csv` + cleaning report** — cleaned the real, messy Titanic dataset: missing values, type fixes, duplicates, and three engineered features (`title`, `age_group`, `family_size`).
- **`week1/week1_reflection.md`** — first weekly self-assessment.
- **`week2/day5_eda.py` + findings.md** — full univariate/bivariate/multivariate exploratory analysis on the cleaned Titanic data.
- **`week2/day6_visuals.py` + visual report** — eight labelled, finding-titled charts using matplotlib and seaborn.
- **`week2/project/load_data.py`, `clean_data.py`, `DATA_DICTIONARY.md`** — acquisition and cleaning pipeline for real Premier League 2023-24 data (865 players, 20 clubs), plus a merged, feature-engineered dataset (`players_clean.csv`) with 8 new metrics.
- **`week2/project/analysis.py` + `visuals.py` + `ANALYSIS_REPORT.md`** — full positional, club, and value analysis with eight charts and a professional written report.
- **`week2/week2_reflection.md`** — midpoint self-assessment with week-on-week comparison.
- **`week2/project/model.py` / `model_v2.py`** — Linear Regression, Decision Tree, and tuned Random Forest models predicting `total_points`, with leakage exclusion, cross-validation, GridSearchCV tuning, and a classification model for "high performer" players.
- **`week3/day10_model_notes.md` + `day11_model_evaluation.md`** — full model comparison, feature importance, and precision/recall reasoning.
- **`week2/project/app.py`** — a working, interactive Streamlit dashboard with filters, player comparison, visual analysis, and a live prediction tool.
- **This document** — the final reflection.
  The piece I'm most proud of is the Streamlit dashboard, since it's the only deliverable that ties every other piece: cleaning, analysis, the model into something a non-technical person could actually open and use.

---

## 2.4 The Hardest Thing

The hardest thing across the whole programme was keeping track of everything as the scope grew in Weeks 2 and 3, by that point I was managing multiple scripts, datasets, and reports across a single ongoing project instead of one self-contained daily task, and it took real effort to keep the structure organized and know exactly where each piece of the pipeline stood. This was made harder by the pace at which new material arrived: some areas, particularly the machine learning and dashboard-building concepts, were introduced quickly, and I would have benefited from more practice with the fundamentals before immediately applying them to the project. I worked through it by leaning more heavily on documentation, breaking the project into smaller functions and files so each piece was easier to reason about on its own, and revisiting earlier days' code when I needed a refresher. I'd say this is mostly resolved rather than fully resolved, I can now navigate a multi-file project confidently, but I'm still building the deeper comfort that would let me do it without leaning on notes and documentation as much as I currently do.

---

## 2.5 What I Would Do Differently

1. **Refresh the core fundamentals before Day 1 rather than during the programme.** I would have practiced the baseline Python, pandas, and general programming skills needed for the early tasks in advance, so I could start each new topic at full speed instead of feeling behind while still rebuilding basics.
2. **Preview each week's upcoming topics ahead of time.** Knowing in advance that Week 2 introduced visualization and a full project pipeline, and Week 3 introduced machine learning and Streamlit, would have let me pace my learning instead of absorbing new concepts and applying them in the same day.
3. **Set aside dedicated practice time separate from deliverable time.** Rather than learning a new library while simultaneously trying to produce that day's graded output, I would have benefited from a short, separate block purely for practicing a new concept before using it for real.

---

## 2.6 Feedback to the Programme

**Task that taught the most:** Day 3 of Week 1 the real-world data cleaning task on the Titanic dataset was the first time textbook-clean data was replaced with genuinely messy data, and it taught me the most because it forced real judgment calls, not just following steps. Day 3 of Week 3, building the interactive dashboard, taught me the most on the applied/engineering side, since it was the first time all the earlier pieces had to work together as one usable product.

**Task that taught the least:** The very first diagnostic task on Day 1, working with the self-created student dataset. It was useful for getting the environment and workflow set up, but since the data was synthetic and simple, it didn't teach as much as the tasks that came later with real, messy datasets.

**Was the pace appropriate?** In Week 1, yes the pace felt manageable and well matched to what I actually knew. From Week 2 onward it became too fast at points, particularly once machine learning and dashboard-building were introduced in quick succession.

**What was missing:** Short supplementary video walkthroughs for the newer, trickier concepts especially machine learning and Streamlit before diving straight into the applied task. Written material alone made some of the faster-paced days harder than they needed to be.

---

## 2.7 Next Steps

**Three skills to keep developing after 21 August, and how:**

- **SQL** — practice by querying real, larger datasets rather than CSV files, since most real analytics work lives in databases.
- **scikit-learn** — go deeper by working on additional projects and open datasets (for example, Kaggle competitions) to build models beyond what a single internship project required.
- **Streamlit** — build and properly deploy additional dashboards, rather than only running them locally, to get comfortable with the full path from analysis to a shareable product.

**Did this programme confirm or change your interest in Data Analysis and AI?** It confirmed it. Three weeks of hands-on, real-dataset work made the interest concrete rather than theoretical.

**Where you want to be professionally in twelve months:** Working professionally in Data Analysis and AI, building on the pipeline skills: cleaning, analysis, modeling, and presentation developed during this programme.
