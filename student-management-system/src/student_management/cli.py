"""Simple interactive command-line interface."""

from pathlib import Path

from .manager import StudentManager
from .student import Student
from .storage import StudentStorage
from .exceptions import StudentManagementError

DATA_DIR = Path("data")
JSON_FILE = DATA_DIR / "students.json"
CSV_FILE = DATA_DIR / "students.csv"


def main() -> None:
    manager = StudentManager()
    print("=== Student Management System ===")
    while True:
        print(
            "\n1. Add student\n2. List students\n3. Find student\n"
            "4. Update student\n5. Delete student\n6. Add mark\n"
            "7. Save JSON\n8. Load JSON\n9. Export CSV\n"
            "10. Import CSV\n0. Exit"
        )
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                student = Student(
                    input("Student ID: "), input("Name: "), input("Email: "),
                    input("Department: ")
                )
                manager.add_student(student)
                print("Student added.")
            elif choice == "2":
                students = manager.list_students()
                if not students:
                    print("No student records found.")
                for student in students:
                    print(student.display_details())
            elif choice == "3":
                print(manager.get_student(input("Student ID: ")).display_details())
            elif choice == "4":
                student_id = input("Student ID: ")
                name = input("New name (blank to keep): ").strip()
                email = input("New email (blank to keep): ").strip()
                department = input("New department (blank to keep): ").strip()
                manager.update_student(
                    student_id,
                    name=name or None,
                    email=email or None,
                    department=department or None,
                )
                print("Student updated.")
            elif choice == "5":
                manager.delete_student(input("Student ID: "))
                print("Student deleted.")
            elif choice == "6":
                student = manager.get_student(input("Student ID: "))
                student.add_mark(input("Mark (0-100): "))
                print("Mark added.")
            elif choice == "7":
                StudentStorage.save_json(manager.list_students(), JSON_FILE)
                print(f"Saved to {JSON_FILE}")
            elif choice == "8":
                manager.replace_all(StudentStorage.load_json(JSON_FILE))
                print(f"Loaded from {JSON_FILE}")
            elif choice == "9":
                StudentStorage.export_csv(manager.list_students(), CSV_FILE)
                print(f"Exported to {CSV_FILE}")
            elif choice == "10":
                manager.replace_all(StudentStorage.import_csv(CSV_FILE))
                print(f"Imported from {CSV_FILE}")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Choose a valid menu option.")
        except (StudentManagementError, ValueError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
