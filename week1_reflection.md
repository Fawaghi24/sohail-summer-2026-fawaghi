# Week 1 Reflection: Learning the Basics & Working with Data

## 1. What I Learned This Week
This week, I learned how to set up a proper coding environment and start analyzing data with Python. First, I learned about virtual environments (`venv`). They help keep each project's packages separate so things don't break. I would use a virtual environment at the start of any new project. Next, I started using `pandas` for working with tables. Instead of writing long loops in Python, `pandas` lets me inspect data quickly with functions like `.info()` and `.describe()`, filter specific rows, and group data together using `.groupby()`. I would use `pandas` whenever I need to work with CSV files or spreadsheets. Finally, I learned how to clean dirty data. Datasets often have missing numbers, wrong text formats, or repeated rows. I learned how to handle missing values safely for example, replacing missing ages with the median age of a group instead of using a simple average that could be ruined by extreme values. Cleaning the data first is important because wrong data leads to wrong results.

## 2. What I Built
* **`PROFILE.md` & `README.md`**: Files in my GitHub repository where I wrote about my background, my skills, and instructions on how to run my code.
* **`diagnostic/task1.py`**: A basic Python script that reads a student CSV file to count total students, find the average GPA, and filter credits.
* **`diagnostic/task2.py`**: A script that takes a paragraph of text and counts the words, characters, and most common words.
* **`diagnostic/task3.py`**: A script where I built `Course` and `Student` classes to practice object-oriented programming, like enrolling students and setting class capacity limits.
* **`diagnostic/data/students.csv`**: A dataset I created and later expanded to 30 rows with extra information like active status and enrollment year.
* **`week1/day2_pandas_basics.py`**: A script where I redid the student analysis using `pandas` commands instead of manual loops, making the code much shorter and cleaner.
* **`week1/day3_cleaning.py`**: A complete script that downloads raw Titanic passenger data, fixes missing values, standardizes column names, and creates new columns like age groups and titles.
* **`week1/day3_cleaning_report.md`**: A report explaining why I chose specific cleaning steps and listing five key findings from the Titanic dataset.

## 3. My Biggest Challenge
My biggest challenge this week was translating what I understood conceptually into actual working code. Sometimes I knew what a command was supposed to do, but when I tried to run it in the terminal or in Python, I realized I needed extra subcommands or extra steps that I had never seen before. For example, knowing a general Git command wasn't enough; I had to learn the specific subcommands and flags to make it work correctly without breaking things. The same thing happened when working with file paths in `pathlib`. To get through this, I had to slow down, read error messages carefully, and test small commands one by one before putting them into my main file. I feel better about it now, but I still need more practice so these subcommands become natural to me.

## 4. Honest Self-Assessment
* **Python syntax and core language features (3/5):** The last time I used Python was back in high school, so I feel like I need a refresher from the beginning. However, knowing C++ and Java makes it easier for me to understand the general logic.
* **Writing clean, structured, reusable code (3/5):** I can organize my code into functions and classes fine, but making it look really clean and professional takes me extra time.
* **pandas — loading, selecting, and filtering data (4/5):** I feel good about opening CSV files, picking specific columns, and filtering rows with conditions.
* **pandas — grouping and aggregation (4/5):** I understand how `.groupby()` works for basic things, but doing more complex summaries is still a bit tricky for me.
* **Data cleaning and handling missing values (4/5):** I feel confident finding missing data, removing bad rows, and filling in missing numbers using medians.
* **Git and GitHub workflow (5/5):** I feel very confident using Git commands, making commits, pushing code to GitHub, and using `.gitignore`.
* **Reading official documentation independently (2/5):** I find reading long technical text documentation hard. I actually prefer watching video tutorials to learn new technical concepts visually.

## 5. What I Want From Next Week
* **Which specific sport or dataset would you like to work with, and why?** Football, because it is my main area of interest and I really want to analyze player stats.
* **Which of this week's topics do you want revisited before we move on?** Basic Python syntax and common subcommands or methods, so I can write code faster without getting stuck on small syntax details.
* **Which single skill do you most want to have gained by the end of next week?** Data visualization learning how to make clear graphs and charts so I can turn raw numbers into visual pictures.

## 6. Time & Process
* **Overall Assessment:** The workload throughout the week was appropriate. 
