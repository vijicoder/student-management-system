import pytest

from student_management.student import Student
from student_management.storage import StudentStorage
from student_management.exceptions import ValidationError, DuplicateStudentError


def sample_students():
    return [
        Student("S1", "Asha", "asha@example.com", "AIDS", [80, 90]),
        Student("S2", "Kumar", "kumar@example.com", "IT", [75]),
    ]


def test_json_round_trip(tmp_path):
    path = tmp_path / "students.json"
    StudentStorage.save_json(sample_students(), path)
    loaded = StudentStorage.load_json(path)
    assert [s.to_dict() for s in loaded] == [s.to_dict() for s in sample_students()]


def test_csv_round_trip(tmp_path):
    path = tmp_path / "students.csv"
    StudentStorage.export_csv(sample_students(), path)
    loaded = StudentStorage.import_csv(path)
    assert [s.to_dict() for s in loaded] == [s.to_dict() for s in sample_students()]


def test_invalid_json_is_reported(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValidationError):
        StudentStorage.load_json(path)


def test_duplicate_ids_in_json_are_rejected(tmp_path):
    path = tmp_path / "duplicates.json"
    StudentStorage.save_json([sample_students()[0], sample_students()[0]], path)
    with pytest.raises(DuplicateStudentError):
        StudentStorage.load_json(path)
