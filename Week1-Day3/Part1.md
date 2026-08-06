# Part 1

## 1.1 The anatomy of dirty data

### Why each dirty data problem is dangerous if left unhandled:

- Missing values: Disguised nulls like "N/A" and "unknown" are treated as plain text strings, while numeric flags like -1 are treated as real integers. If left unhandled, both will distort calculated metrics.

- Wrong data types: Incorrect data types break operations. For example, if numbers are stored as text strings, trying to add them together will concatenate (append) the text rather than performing mathematical addition.

- Duplicate records: Duplicates skew overall record counts and distort calculations (such as averages) because identical or near-identical records get counted and calculated multiple times.

- Inconsistent categories: Categories like "male", "Male", and "M" are treated as distinct values because Pandas looks for exact text matches. Grouping by gender will split your statistics into separate categories instead of grouping them together.

- Outliers: When data is entered incorrectly with extreme values that lie far outside reasonable ranges (e.g., an age of 200) it creates data-entry outliers that distort both the average and standard deviation.

- Whitespace and casing: Differences in capitalization or invisible leading/trailing spaces mean strings are not exact matches. Functions like `.groupby()` or conditional filtering will treat them as different values, silently breaking your analysis without throwing an error.
