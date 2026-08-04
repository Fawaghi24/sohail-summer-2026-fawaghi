import csv

file_path = "data/students.csv"
students = []

# Read student records from CSV file
with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Convert string numbers to float/int
        row["gpa"] = float(row["gpa"])
        row["credits_completed"] = int(row["credits_completed"])
        students.append(row)

# Check if file has data to prevent errors
if len(students) == 0:
    print("No student data found.")
else:
    # 1. Total number of students
    print("Total number of students:", len(students))

    # 2. Average GPA calculation
    total_gpa = 0
    for student in students:
        total_gpa += student["gpa"]

    average_gpa = total_gpa / len(students)
    print("Average GPA:", round(average_gpa, 2))

    # 3. Find highest GPA student per major
    highest_by_major = {}

    for student in students:
        major = student["major"]

        if major not in highest_by_major:
            highest_by_major[major] = student
        elif student["gpa"] > highest_by_major[major]["gpa"]:
            highest_by_major[major] = student

    print("\nHighest GPA student per major:")
    for major, student in highest_by_major.items():
        print(major, "-", student["name"], "(", student["gpa"], ")")

    # 4. Count students with more than 60 credits
    count = 0
    for student in students:
        if student["credits_completed"] > 60:
            count += 1

    print("\nStudents with more than 60 credits:", count)