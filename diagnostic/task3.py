class Student:
    """Class to represent a student."""

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return f"{self.name} (ID: {self.student_id})"


class Course:
    """Class to represent an academic course with enrollment management."""

    def __init__(self, code, title, credit_hours, capacity):
        self.code = code
        self.title = title
        self.credit_hours = credit_hours
        self.capacity = capacity
        self.enrolled_students = []

    def get_enrollment_count(self):
        """Returns the current number of enrolled students."""
        return len(self.enrolled_students)

    def enroll_student(self, student):
        """Enrolls a student if the course capacity has not been reached."""
        # Edge Case: Check if course is already at full capacity
        if self.get_enrollment_count() >= self.capacity:
            print(
                f"Error: Cannot enroll {student.name} in {self.code}. Course is full!"
            )
            return False

        # Edge Case: Check if student is already enrolled
        if student in self.enrolled_students:
            print(f"{student.name} is already enrolled in {self.code}.")
            return False

        self.enrolled_students.append(student)
        print(f"Successfully enrolled {student.name} in {self.code}.")
        return True

    def drop_student(self, student):
        """Drops a student if they are currently enrolled in the course."""
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)
            print(f"Successfully dropped {student.name} from {self.code}.")
            return True
        else:
            print(f"Error: {student.name} is not enrolled in {self.code}.")
            return False


# Demonstration Section
if __name__ == "__main__":
    # Create two sample courses with low capacity to test checks
    course1 = Course("CS101", "Introduction to Computer Science", 3, capacity=2)
    course2 = Course("MATH201", "Linear Algebra", 4, capacity=30)

    # Create students
    student1 = Student("S101", "Fawaghi")
    student2 = Student("S102", "Ali")
    student3 = Student("S103", "Salim")

    print("Demonstrating Course Enrollment")
    # Student 1 enrolling in two courses 
    course1.enroll_student(student1)
    course2.enroll_student(student1)

    print("\nTesting Edge Cases")
    # Attempting duplicate enrollment
    course1.enroll_student(student1)

    # Filling capacity on Course 1
    course1.enroll_student(student2)
    # Exceeding capacity on Course 1
    course1.enroll_student(student3)

    print("\nCurrent Enrollment Summary")
    print(
        f"{course1.code} Count: {course1.get_enrollment_count()}/{course1.capacity}"
    )
    print(
        f"{course2.code} Count: {course2.get_enrollment_count()}/{course2.capacity}"
    )

    print("\nTesting Drop Functionality")
    course1.drop_student(student1)
    print(
        f"{course1.code} Count after drop: {course1.get_enrollment_count()}/{course1.capacity}"
    )