"""Business logic for managing student records."""

from .student import Student
from .exceptions import DuplicateStudentError, StudentNotFoundError, ValidationError


class StudentManager:
    """In-memory student data management engine."""

    def __init__(self):
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        if not isinstance(student, Student):
            raise ValidationError("Only Student objects can be added.")
        if student.student_id in self._students:
            raise DuplicateStudentError(
                f"Student ID '{student.student_id}' already exists."
            )
        self._students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        key = str(student_id).strip()
        if key not in self._students:
            raise StudentNotFoundError(f"Student '{key}' was not found.")
        return self._students[key]

    def list_students(self) -> list[Student]:
        return sorted(self._students.values(), key=lambda item: item.student_id)

    def update_student(self, student_id: str, *, name=None, email=None, department=None) -> Student:
        student = self.get_student(student_id)
        if name is not None:
            student.name = name
        if email is not None:
            student.email = email
        if department is not None:
            student.department = department
        return student

    def delete_student(self, student_id: str) -> None:
        student = self.get_student(student_id)
        del self._students[student.student_id]

    def to_records(self) -> list[dict]:
        return [student.to_dict() for student in self.list_students()]

    def replace_all(self, students: list[Student]) -> None:
        """Replace records only after validating the complete incoming collection."""
        new_records: dict[str, Student] = {}
        for student in students:
            if not isinstance(student, Student):
                raise ValidationError("Imported records must be Student objects.")
            if student.student_id in new_records:
                raise DuplicateStudentError(
                    f"Duplicate student ID '{student.student_id}' in imported data."
                )
            new_records[student.student_id] = student
        self._students = new_records
