from abc import ABC, abstractmethod  # ABC module is used for abstract base classes
import re  # Regular expression module for email validation

class InvalidEmailError(Exception):
    """Exception raised for invalid email format."""
    def __init__(self, email):
        """Initialize InvalidEmailError."""
        self.email = email
        super().__init__(f"Invalid email format: {email}")

class Person:
    """Base class representing a person."""
    def __init__(self, name, email):
        """Initialize a Person object."""
        self.name = name
        if not self.validate_email(email):
            raise InvalidEmailError(email)
        self.email = email

    @staticmethod
    def validate_email(email):
        """Validate email address format."""
        return re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email) is not None

class Course(ABC):
    """Abstract base class representing a course."""
    def __init__(self, course_id, name, instructor, duration, capacity):
        """Initialize a Course object."""
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.duration = duration
        self.capacity = capacity
        self.students = []

    @abstractmethod
    def add_student(self, student):
        """Add a student to the course."""
        pass

    def get_students(self):
        """Get the list of enrolled students in the course."""
        return self.students

    def get_course_info(self):
        """Get information about the course."""
        return f"Course: {self.name}\nInstructor: {self.instructor}\nDuration: {self.duration} weeks\nCapacity: {self.capacity}\nEnrolled Students: {len(self.students)}"

class AcademicCourse(Course):
    """Class representing an academic course."""
    def add_student(self, student):
        """Add a student to the academic course."""
        if len(self.students) < self.capacity:
            self.students.append(student)
            print(f"Enrollment Successful: {student.name} has enrolled in {self.name}")
        else:
            raise CourseCapacityReachedError()

class PhysicalEducationCourse(Course):
    """Class representing a physical education course."""
    def add_student(self, student):
        """Add a student to the physical education course."""
        if len(self.students) < self.capacity:
            self.students.append(student)
            print(f"Enrollment Successful: {student.name} has enrolled in {self.name}")
        else:
            raise CourseCapacityReachedError()

class Student(Person):
    """Class representing a student."""
    def __init__(self, name, email, student_id):
        """Initialize a Student object."""
        super().__init__(name, email)
        self.student_id = student_id
        self.courses_enrolled = []

    def add_course(self, course):
        """Add a course to the student's enrolled courses."""
        self.courses_enrolled.append(course)

class CourseCapacityReachedError(Exception):
    """Exception raised when the course capacity is reached."""
    def __init__(self, message="Course capacity reached. Enrollment failed."):
        """Initialize CourseCapacityReachedError."""
        super().__init__(message)

class CourseNotFoundError(Exception):
    """Exception raised when a course is not found."""
    def __init__(self, message="Course not found."):
        """Initialize CourseNotFoundError."""
        super().__init__(message)

class Platform:
    """Class representing a platform for managing courses and enrollments."""
    def __init__(self):
        """Initialize a Platform object."""
        self.courses = {}

    def add_course(self, course):
        """Add a course to the platform."""
        self.courses[course.course_id] = course

    def enroll_student(self, course_id, student):
        """Enroll a student in a course."""
        course = self.courses.get(course_id)
        if not course:
            raise CourseNotFoundError()
        try:
            course.add_student(student)
            student.add_course(course)
            return True
        except CourseCapacityReachedError as e:
            print(f"Enrollment Failed: {e}")
            return False

    def display_course_info(self, course_id):
        """Display information about a course."""
        course = self.courses.get(course_id)
        if not course:
            raise CourseNotFoundError()
        print(course.get_course_info())

    def list_courses(self):
        """List available courses."""
        print("Available Courses:")
        for course_id, course in self.courses.items():
            print(f"{course_id}: {course.name} - {course.instructor}")

    def add_new_course(self):
        """Add a new course to the platform."""
        print("\nAdd New Course")
        course_id = input("Enter course ID: ")
        name = input("Enter course name: ")
        instructor = input("Enter instructor name: ")
        duration = int(input("Enter course duration (in weeks): "))
        capacity = int(input("Enter course capacity: "))
        new_course = AcademicCourse(course_id, name, instructor, duration, capacity)
        self.add_course(new_course)
        print(f"Course '{name}' added successfully!")

class Application:
    """Class representing the application."""
    def __init__(self):
        """Initialize the Application object."""
        self.platform = Platform()
        self.add_default_courses()

    def add_default_courses(self):
        """Add default courses."""
        courses = [
            ("MDE134", "Turkish Language 4 (A2 level)", "Aigerim Raissova", 15, 15),
            ("MDE153", "Module of Social and Political Knowledge (Cultural Studies)", "Aida Baigaraeva", 7, 25),
            ("MDE154", "Module of Social and Political Knowledge (Psychology)", "Yelnura Autalipova", 7, 25),
            ("MDE172", "Philosophy", "Yerzhan Chongarov", 12, 20),
            ("MDE197", "Foreign Language", "Kundyzai Omirzak", 15, 15),
            ("MDE294", "Physical Education 4", "unknown", 4, 50),
        ]
        for course_id, name, instructor, duration, capacity in courses:
            self.platform.add_course(AcademicCourse(course_id, name, instructor, duration, capacity))

    def display_menu(self):
        """Display the main menu."""
        print("\nWelcome to Course Management System")
        print("1. Enroll student")
        print("2. Add new course")
        print("3. Display course information")
        print("4. List available courses")
        print("5. Exit")

    def run(self):
        """Run the application."""
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.enroll_student()
            elif choice == "2":
                self.add_new_course()
            elif choice == "3":
                self.display_course_info()
            elif choice == "4":
                self.list_courses()
            elif choice == "5":
                print("the session is over")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def enroll_student(self):
        """Enroll a student in a course."""
        print("\nEnroll Student")
        student_name = input("Enter student name: ")
        student_email = input("Enter student email: ")
        student_id = input("Enter student ID: ")

        student = Student(student_name, student_email, student_id)

        print("Currently Available Courses:")
        self.platform.list_courses()
        course_id = input("Enter course ID to enroll student: ")

        try:
            if self.platform.enroll_student(course_id, student):
                print("Student enrollment successful.")
        except (CourseNotFoundError, InvalidEmailError) as e:
            print(f"Error: {e}")

    def add_new_course(self):
        """Add a new course to the platform."""
        self.platform.add_new_course()

    def display_course_info(self):
        """Display information about a course."""
        print("\nDisplay Course Information")
        course_id = input("Enter course ID: ")

        try:
            self.platform.display_course_info(course_id)
        except CourseNotFoundError as e:
            print(f"Error: {e}")

    def list_courses(self):
        """List available courses."""
        print("\nList of Available Courses:")
        self.platform.list_courses()

if __name__ == "__main__":
    app = Application()
    app.run()
