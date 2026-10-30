import pytest

from student_management.manager import StudentManager
from student_management.student import Student
from student_management.exceptions import (
    DuplicateStudentError, StudentNotFoundError, ValidationError
)


def make_student(student_id="S1"):
    return Student(student_id, "Asha", "asha@example.com", "AIDS", [90])


def test_add_and_get_student():
    manager = StudentManager()
    manager.add_student(make_student())
    assert manager.get_student("S1").name == "Asha"


def test_duplicate_id_is_rejected():
    manager = StudentManager()
    manager.add_student(make_student())
    with pytest.raises(DuplicateStudentError):
        manager.add_student(make_student())


def test_missing_student_is_rejected():
    with pytest.raises(StudentNotFoundError):
        StudentManager().get_student("missing")


def test_update_and_delete_student():
    manager = StudentManager()
    manager.add_student(make_student())
    manager.update_student("S1", name="Anu")
    assert manager.get_student("S1").name == "Anu"
    manager.delete_student("S1")
    with pytest.raises(StudentNotFoundError):
        manager.get_student("S1")


def test_only_student_objects_can_be_added():
    with pytest.raises(ValidationError):
        StudentManager().add_student("not a student")
