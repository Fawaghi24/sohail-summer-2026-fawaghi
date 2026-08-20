# Titanic Exploratory Data Analysis Findings

## Key Findings

### 1. Survival Disparity by Gender

- **Finding:** Female passengers had a significantly higher survival rate than male passengers across all ticket classes.
- **Evidence:** Overall survival for First-class females was 96.81% versus 36.89% for First-class males. In Third-class, females had a 50.0% survival rate while males had only 13.54%.
- **Interpretation:** This strongly reflects the enforcement of the historic "women and children first" evacuation policy during lifeboat loading.
- **Caveat:** This statistical gap does not prove that every individual crew member prioritized women, nor does it account for physical locations on the ship when the emergency began.

### 2. Socioeconomic Status and Survival

- **Finding:** Passengers in higher class accommodations experienced higher survival probabilities.
- **Evidence:** First-class passengers achieved survival rates of 96.81% (female) and 36.89% (male), whereas Third-class survival dropped to 50.0% (female) and 13.54% (male).
- **Interpretation:** First-class passengers likely had better access to lifeboats due to proximity to the upper decks, clearer emergency communication, and social privilege.
- **Caveat:** Ticket class alone cannot prove direct discrimination by crew; structural layout and proximity to exit routes played a major role.

### 3. Age Prioritization During Evacuation

- **Finding:** Children had the highest likelihood of survival among age groups, while elderly passengers had the lowest.
- **Evidence:** Children (0–12 years) recorded a 57.97% survival rate, whereas Seniors (60+ years) recorded a 22.73% survival rate.
- **Interpretation:** Rescue efforts prioritized younger passengers, whereas elderly individuals may have faced mobility limitations during the chaos.
- **Caveat:** Binned age groups do not capture family unit dynamics, such as whether a child survived because they were accompanied by a First-class parent.

### 4. High Skewness and Outliers in Fare Distribution

- **Finding:** Ticket fares are extremely right-skewed with significant high-value outliers.
- **Evidence:** The mean fare ($32.20) is more than double the median fare ($14.45), with a skewness score of 4.787 and 116 IQR outliers (up to $512.33).
- **Interpretation:** Most passengers purchased inexpensive Third-class tickets, while a small luxury group purchased extremely expensive suites.
- **Caveat:** High fare values do not always mean a single luxury ticket; some high fares represent group or family bookings purchased under a single ticket number.

### 5. Correlation Between Fare and Survival

- **Finding:** Higher fare prices show a positive correlation with survival status.
- **Evidence:** Fare holds the strongest positive Pearson correlation with survival (`+0.257`) among all numeric features.
- **Interpretation:** Paying a higher fare granted access to First-class cabins located closer to the lifeboat deck.
- **Caveat:** Correlation does not mean wealth itself directly caused survival; fare is a proxy for cabin location and deck level.

---

## Correlation vs. Causation Warning

**Spurious Correlation:** A careless analyst might look at the positive correlation between `fare` and `survived_num` (`+0.257`) and conclude that paying more money directly caused a passenger to survive.

**Real Underlying Driver:** Higher fare is a proxy for **passenger class (`pclass`) and physical deck location**. Passengers who paid higher fares were located on upper decks with direct access to lifeboats and were given priority during the evacuation. The physical location and evacuation protocol were the true drivers of survival, not the money itself.
