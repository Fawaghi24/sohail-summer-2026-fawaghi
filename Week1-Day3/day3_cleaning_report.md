# Day 3 Data Cleaning & Profiling Report: Titanic Dataset

## 1. Summary of Identified Data Issues & Cleaning Actions

| Feature / Column          | Problem Identified                                               | Action Taken                                                                    |
| :------------------------ | :--------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **Column Names**          | Non-standard casing and formats (e.g., `PassengerId`, `Pclass`). | Converted all names to lowercase `snake_case`.                                  |
| **`age`**                 | 177 missing values (~19.87% of records).                         | Imputed missing values using median grouped by `pclass` and `sex`.              |
| **`embarked`**            | 2 missing values (<0.25% of records).                            | Imputed missing values using dataset mode (`'s'`).                              |
| **`cabin`**               | 687 missing values (~77.10% of records).                         | Dropped entire column due to structural sparsity.                               |
| **Text Fields**           | Potential trailing/leading whitespace and inconsistent casing.   | Applied `.str.strip()` and `.str.lower()` to string columns.                    |
| **Duplicate Rows**        | Evaluated dataset for duplicate passenger entries.               | Executed `.drop_duplicates()` (0 duplicates found).                             |
| **`survived` / `pclass`** | Encoded as arbitrary numbers (`0/1` and `1/2/3`).                | Mapped to human-readable categories (`Died/Survived` and `First/Second/Third`). |

---

## 2. Justification for Key Cleaning Decisions

### Age Imputation Choice

Imputing missing `age` values using a single global median or mean distorts the natural demographic distribution across economic tiers. On the Titanic, passengers in First Class were significantly older on average than passengers in Third Class. Furthermore, female and male age distributions differed within classes. Utilizing a **group-based median stratified by `pclass` and `sex`** preserves intra-group variance and provides realistic estimates (e.g., an unaged First Class male receives a First Class male median age rather than a global average skewed by Third Class children).

### Cabin Column Treatment

The `cabin` variable is missing for over **77%** of total passengers. Imputing more than three-quarters of a column introduces artificial bias and unreliable noise into downstream exploratory analysis. Because the missingness pattern is severe and non-random, dropping the `cabin` column entirely is the most defensible choice. Socio-economic cabin position is already effectively captured by `pclass` and `fare`.

---

## 3. Five Key Insights & Interpretations

1. **Survival Rate by Passenger Class:**
   - **First Class:** 62.96% | **Second Class:** 47.28% | **Third Class:** 24.24%
   - _Interpretation:_ Passengers in higher socio-economic classes had drastically higher survival rates, likely due to proximity to lifeboats on upper decks.
2. **Survival Rate by Sex:**
   - **Female:** 74.20% | **Male:** 18.89%
   - _Interpretation:_ The "women and children first" evacuation policy was strictly enforced onboard.
3. **Survival Rate by Age Group:**
   - **Child (0–12):** 57.97% | **Teen (13–19):** 40.26% | **Adult (20–59):** 36.42% | **Senior (60+):** 22.73%
   - _Interpretation:_ Children were prioritized for rescue, whereas senior passengers suffered the lowest survival rate among age brackets.
4. **Average Fare by Passenger Class:**
   - **First Class:** $84.15 | **Second Class:** $20.66 | **Third Class:** $13.68
   - _Interpretation:_ First Class tickets were significantly more expensive than lower tiers, creating a stark economic gradient across deck levels.
5. **Survival Rate by Title (Custom Insight):**
   - **Mrs:** 79.20% | **Miss:** 69.78% | **Master:** 57.50% | **Mr:** 15.67%
   - _Interpretation:_ Adult males (`Mr`) had by far the lowest survival rates, while boys (`Master`) were given priority alongside women (`Mrs` / `Miss`).

---

## 4. Surprising Finding in the Data

What stood out most during profiling was the survival rate of young boys holding the title **`Master` (57.50%)** compared to adult men holding the title **`Mr` (15.67%)**. While adult males suffered the worst mortality rate across the ship, young boys were actively prioritized alongside women, demonstrating that age-based chivalry overrode gender penalties for young children during the emergency evacuation.
