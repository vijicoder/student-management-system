import pytest

from student_management.student import Student
from student_management.teacher import Teacher
from student_management.person import Person
from student_management.exceptions import ValidationError


def test_student_inherits_person_and_calculates_average():
    student = Student("S1", "Asha", "asha@example.com", "AIDS", [80, 90])
    assert isinstance(student, Person)
    assert student.average == 85
    assert student.student_id == "S1"


def test_marks_are_validated():
    student = Student("S1", "Asha", "asha@example.com", "AIDS")
    with pytest.raises(ValidationError):
        student.add_mark(101)


def test_marks_are_encapsulated():
    student = Student("S1", "Asha", "asha@example.com", "AIDS", [75])
    assert student.marks == (75.0,)
    with pytest.raises(AttributeError):
        student.marks.append(90)


def test_polymorphic_display_methods():
    people = [
        Student("S1", "Asha", "asha@example.com", "AIDS"),
        Teacher("T1", "Ravi", "ravi@example.com", "Python"),
    ]
    output = [person.display_details() for person in people]
    assert "Student" in output[0]
    assert "Teacher" in output[1]


def test_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        Student("S1", "Asha", "not-an-email", "AIDS")
