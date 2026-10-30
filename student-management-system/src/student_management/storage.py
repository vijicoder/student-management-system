"""JSON and CSV persistence helpers."""

import csv
import json
from pathlib import Path

from .student import Student
from .exceptions import ValidationError, DuplicateStudentError


class StudentStorage:
    """Save and load student records in JSON and CSV formats."""

    CSV_FIELDS = ["student_id", "name", "email", "department", "marks"]

    @staticmethod
    def save_json(students: list[Student], file_path: str | Path) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [student.to_dict() for student in students]
        path.write_text(json.dumps(payload, indent=4), encoding="utf-8")

    @staticmethod
    def load_json(file_path: str | Path) -> list[Student]:
        path = Path(file_path)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValidationError(f"Could not read valid JSON data: {exc}") from exc
        if not isinstance(raw, list):
            raise ValidationError("JSON file must contain a list of student records.")
        return StudentStorage._build_students(raw)

    @staticmethod
    def export_csv(students: list[Student], file_path: str | Path) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=StudentStorage.CSV_FIELDS)
            writer.writeheader()
            for student in students:
                row = student.to_dict()
                row["marks"] = json.dumps(row["marks"])
                writer.writerow(row)

    @staticmethod
    def import_csv(file_path: str | Path) -> list[Student]:
        path = Path(file_path)
        try:
            with path.open("r", newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                if reader.fieldnames is None or not set(StudentStorage.CSV_FIELDS).issubset(reader.fieldnames):
                    raise ValidationError("CSV file is missing required columns.")
                records = []
                for row in reader:
                    try:
                        row["marks"] = json.loads(row["marks"] or "[]")
                    except json.JSONDecodeError as exc:
                        raise ValidationError("CSV marks must contain a JSON list.") from exc
                    records.append(row)
        except OSError as exc:
            raise ValidationError(f"Could not read CSV file: {exc}") from exc
        return StudentStorage._build_students(records)

    @staticmethod
    def _build_students(records: list[dict]) -> list[Student]:
        students = []
        seen = set()
        for record in records:
            student = Student.from_dict(record)
            if student.student_id in seen:
                raise DuplicateStudentError(
                    f"Duplicate student ID '{student.student_id}' in file."
                )
            seen.add(student.student_id)
            students.append(student)
        return students
