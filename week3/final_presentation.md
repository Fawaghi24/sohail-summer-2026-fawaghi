# Final Presentation — Premier League Player Analytics

## 1. The Problem and Why It Matters (1 min)

**On screen:** Title slide / project README hero image.

**Speaker notes:**
"Fantasy football managers, scouts, and analysts all face the same question every season: which players are actually worth their price tag? Raw stats alone don't answer this a striker with 20 goals in 3000 minutes and one with 3 goals in 90 minutes look completely different once you account for playing time. My project builds a full pipeline that cleans real Premier League data, normalizes it fairly, and ends in an interactive tool that lets anyone not just someone who can code explore this question themselves."

---

## 2. The Data and What Cleaning It Required (1.5 min)

**On screen:** A quick look at the raw vs. cleaned data shape, or the DATA_DICTIONARY.md.

**Speaker notes:**
"The data comes from the public Fantasy Premier League dataset real 2023-24 season data covering 865 players across 20 clubs. The raw file has 88 columns, most of which I didn't need, so the first stage was selecting the 20 relevant ones, merging in club names from a separate teams file, and fixing data types, several of the expected-goals columns were stored as text instead of numbers. I engineered 8 new features on top of that: per-90 rates like goals-per-90, so playing time is accounted for fairly, plus value metrics like points-per-million and difference metrics like actual-minus-expected goals. Every step is guarded against divide-by-zero errors, so a player with 0 minutes doesn't crash the pipeline."

---

## 3. Three Most Interesting Findings (3 min)

**On screen:** Embed the corresponding chart for each finding as you talk.

**Finding A — Expensive doesn't mean valuable.**
_(Chart: `04_cost_vs_points.png`)_
"There's zero overlap between my top 10 'best value' players by points-per-million and my top 10 highest-cost players. Not one player appears on both lists. That's a genuinely useful, non-obvious insight it means picking players by reputation or price tag alone is a bad strategy."

**Finding B — Points are heavily skewed toward a small group of stars.**
_(Chart: `01_points_distribution.png`)_
"The average player scored about 36 points, but the median was only 13 meaning most players scored well below the average, and a small number of standout performers pulled that average up. That's a right-skewed distribution, and it's a good example of when the mean can genuinely mislead you if you don't also check the median."

**Finding C — Position changes how a player earns points entirely.**
_(Chart: `02_points_per_90_by_position.png`)_
"Forwards earn points mainly through goals, midfielders balance goals and assists, and defenders and goalkeepers earn points mostly through clean sheets. This is why any fair player comparison has to happen within a position group, not across the whole league comparing a goalkeeper's goal tally to a striker's is meaningless."

---

## 4. The Model, Its Performance, and Its Limits (2 min)

**On screen:** Your model comparison table, or the feature importance chart.

**Speaker notes:**
"I tested three regression models to predict a player's season points from their in-game stats Linear Regression, a Decision Tree, and a tuned Random Forest using 5-fold cross-validation to make sure the results were stable, not just lucky on one split. Linear Regression won clearly: it explains about 96% of the variation in points, with a typical error of around 6 points, and it was the most consistent model across every fold. Interestingly, the simpler model beat both tree-based models here.

I also built a classifier to flag 'high performer' players top 25% by points. It's deliberately conservative: when it predicts someone is a high performer, it's right 100% of the time, but it misses about 18% of genuine high performers. That's a real trade-off I had to reason about, not just a number I concluded that in a scouting context, missing a good player is actually more costly than a false alarm, so a future version should be tuned to prioritize recall over precision.

The most important thing I want to be upfront about: this is a single season of data, expected-goals is itself an estimate not a fact, and fantasy points are a proxy for real performance, not a direct measure of skill. This model is a screening tool, not a replacement for human judgment."

---

## 5. Live Dashboard Demonstration (2 min)

**On screen:** `streamlit run app.py`, live.

**Speaker notes / demo script:**

1. "Here's the dashboard everything you just saw in charts is now interactive." _(Show the Overview metrics.)_
2. "I can filter to just forwards, or just one club, and every number updates live." _(Apply a filter.)_
3. "The Player Explorer table is sortable and exportable as CSV." _(Click a column header, show the download button.)_
4. "I can compare any two players side by side." _(Pick two players in Section 4.)_
5. "And finally, the prediction tool I can enter a hypothetical player's stats and get a predicted points total, with a clear caveat that this is an estimate, not a forecast." _(Run one prediction.)_

---

## 6. What I Learned and What I'd Do Next (0.5 min)

**Speaker notes:**
"This project took me from barely knowing Python three weeks ago to building a full pipeline cleaning, analysis, visualization, a trained and evaluated model, and a working interactive app. If I continued, I'd want to bring in multiple seasons of data so predictions aren't limited to a single year, and I'd tune the classifier's threshold to catch more genuine high performers, even at the cost of a few more false alarms."

---

## Anticipated Questions and Prepared Answers

**Q1: "Why did the simpler Linear Regression model beat the more complex Random Forest?"**
_A: "My cross-validation showed Linear Regression had both the highest mean R² and the lowest variation across folds. My best guess is that the relationship between raw stats goals, assists, minutes and total points is fairly linear and additive by design, since FPL points are literally calculated with a points-per-goal, points-per-assist formula. A more complex model doesn't have an advantage when the underlying relationship is already close to linear; it just has more room to overfit."_

**Q2: "How do you know your model isn't just leaking the answer through one of its features?"**
_A: "I explicitly excluded four columns bonus, bps, points_per_game, and points_per_million because they're mathematically derived from total_points itself. I also watched for the classic warning sign: if my R² had come out above 0.98, that would have been suspicious on a dataset this size. My actual result, 0.96, is high but not suspiciously perfect, which is consistent with a real relationship rather than a leaked one."_

**Q3: "If a club actually used your classifier to decide who to scout, what's the risk?"**
_A: "The current model is tuned to avoid false alarms when it says 'high performer,' it's always right. But that comes at the cost of missing about 18% of genuine high performers, and in scouting, missing a good player who then signs with a rival club is a more expensive mistake than wasting a bit of scouting time on an average player. So as it stands, I'd recommend adjusting the model to prioritize recall over precision before using it for real scouting decisions that's a clear next step, not a hidden flaw I'm unaware of."_
