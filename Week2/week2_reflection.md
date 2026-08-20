# Week 2 Reflection

_Sohail Smart Solutions Summer Training Programme 2026_

---

## 1. Technical Growth

This week I made real progress in several areas. For exploratory data analysis and descriptive statistics, I had an advantage because I studied statistics last semester, so concepts like mean, skewness, and correlation were not new to me, this week I learned how to apply them directly to a real dataset instead of just knowing the theory. For data visualisation, I learned the difference between matplotlib, which gives full manual control over a chart, and seaborn, which is faster and more automatic for common statistical plots. I also understood why a well-designed chart helps a reader reach a conclusion much faster than a table of numbers. For merging datasets, I learned there are four types of joins (inner, left, right, outer), and that the correct way to check if a merge worked is to compare the number of rows before and after the merge, and check for unexpected missing values. For feature engineering, I learned why raw numbers can be misleading, for example, comparing a player who only played the last 15 minutes of a match to one who played the full 90 minutes is unfair unless the stats are normalised per 90 minutes. Finally, for domain reasoning, I understood why a 900-minute threshold is used to filter players before ranking them: it removes small, unreliable samples (like a single 45-minute game) from skewing the results. I also learned that when a player's actual goals are higher than their expected goals (xG), this can be a sign of luck or unusually good finishing, not necessarily a repeatable skill.

---

## 2. Project Checkpoint

I am genuinely pleased to be working on this project, mainly because I chose the topic myself, which makes it easier to stay motivated. What is still weak is the depth of some parts of the analysis, mainly because of the time pressure this week, which forced me to move faster than I would have liked through some sections. The most interesting thing I found was how a chart that clearly communicates a finding can be produced with just a few lines of code once the data is already cleaned it made me appreciate how much of the real work happens before the visualisation step. One thing that challenged an assumption I had was noticing that a player's cost does not always match their output, some lower-cost players produced better value-per-point than some of the most expensive players in the dataset, which was not what I expected before running the numbers.

---

## 3. Biggest Challenge

My biggest challenge this week was not a specific coding concept but the schedule itself. Week 2's tasks were only assigned on Tuesday, which meant I had to complete an entire week of material, plus the start of Week 3, in only two to three days. To manage this, I used AI assistance to speed up writing correct code syntax, while making sure I still understood the logic behind every script rather than just copying output. I tried to focus my limited time on understanding the reasoning why a threshold is used, why a join is verified, why a feature is normalised rather than only producing the deliverables. I believe this approach worked reasonably well, but I know some sections were rushed, and I would want to revisit them more carefully if I had normal time. I do not think this is fully resolved yet, mainly because I have not had the chance to slow down and review everything at a comfortable pace.

---

## 4. Self-Assessment

| Area                                            | Week 1              | Week 2 | Moved?        | Justification                                                                                                                                                                               |
| ----------------------------------------------- | ------------------- | ------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python syntax and core language features        | 3                   | 4.5    | Yes           | I watched tutorials and practiced actively, which made the syntax feel much more natural than last week.                                                                                    |
| Writing clean, structured, reusable code        | 3                   | 4      | Yes           | I structured my scripts into functions with comments and docstrings, added error handling, and used pathlib for file paths, this made my code easier to read and reuse.                     |
| pandas: selecting, filtering, grouping, merging | 4                   | 4      | No            | My pandas skills were already solid from Week 1. This week's tasks (merging datasets, grouping with transform) were harder, but my confidence stayed at the same level rather than jumping. |
| Data cleaning and handling missing values       | 4                   | 4      | No            | I reused the cleaning approach from Week 1's Titanic dataset on the new football dataset, so this felt like applying an existing skill rather than gaining a new one.                       |
| EDA and statistical interpretation              | Not rated last week | 4.5    | New this week | This is a new skill area for me this week, and my background in statistics made it easier to pick up than I expected.                                                                       |
| Data visualisation and chart selection          | Not rated last week | 4      | New this week | Also new this week, I understand which chart fits which question, but I still want more practice choosing the best chart quickly.                                                           |
| Communicating findings in writing               | 2                   | 4      | Yes           | Using the Finding / Evidence / Interpretation / Caveat structure gave my writing much more clarity than I had in Week 1.                                                                    |
| Git and GitHub workflow                         | 5                   | 5      | No            | I was already confident with Git from Week 1, and this week did not introduce anything new to that workflow.                                                                                |

**A note on AI use:** I used AI to help write correct code syntax more quickly, especially under this week's time pressure. However, I made sure to understand the logic and reasoning behind every function I used, I can explain what each script does and why, not just that it runs.

---

## 5. Direction for the Final Week

I am interested in both prediction problems, redicting a player's total points and classifying high versus low performers, because I think each teaches a different way of thinking about the same data. The part of my project I most want to strengthen is the prediction stage itself, since that is the newest and most technically demanding part for me. The one skill I most want to leave the programme with is a genuinely solid understanding of the fundamentals, rather than just being able to produce correct output without fully understanding why it works.

---

## 6. Time & Process

Week 2's tasks were not assigned until Tuesday, which meant both the full seven days of Week 2 work and the start of Week 3 had to be completed within roughly two to three days, while the final submission deadline of 21 August stayed the same.

To manage this compressed timeline, I prioritised understanding the logic and theory behind each task properly, and used AI assistance to speed up writing correct code syntax so that the pace of the schedule did not come at the cost of my actual learning. Honestly, the workload was too heavy for the time given not because the material itself was too hard, but because a week's worth of learning does not fit naturally into two or three days without cutting corners somewhere.
