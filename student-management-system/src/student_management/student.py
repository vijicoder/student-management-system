"""Student model."""

from .person import Person
from .exceptions import ValidationError


class Student(Person):
    """A student with a department and a list of marks."""

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        department: str,
        marks: list[float] | None = None,
    ):
        super().__init__(student_id, name, email)
        department = str(department).strip()
        if not department:
            raise ValidationError("Department cannot be empty.")
        self.__department = department
        self.__marks: list[float] = []
        for mark in marks or []:
            self.add_mark(mark)

    @property
    def student_id(self) -> str:
        return self.person_id

    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValidationError("Department cannot be empty.")
        self.__department = value

    @property
    def marks(self) -> tuple[float, ...]:
        """Return an immutable view so callers cannot change marks directly."""
        return tuple(self.__marks)

    def add_mark(self, mark: float) -> None:
        try:
            value = float(mark)
        except (TypeError, ValueError) as exc:
            raise ValidationError("Mark must be a number.") from exc
        if not 0 <= value <= 100:
            raise ValidationError("Mark must be between 0 and 100.")
        self.__marks.append(value)

    @property
    def average(self) -> float:
        return round(sum(self.__marks) / len(self.__marks), 2) if self.__marks else 0.0

    def display_details(self) -> str:
        return (
            f"Student | ID: {self.student_id} | Name: {self.name} | "
            f"Email: {self.email} | Department: {self.department} | "
            f"Average: {self.average:.2f}"
        )

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "marks": list(self.marks),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        required = {"student_id", "name", "email", "department"}
        if not isinstance(data, dict) or not required.issubset(data):
            raise ValidationError("Student record is missing required fields.")
        marks = data.get("marks", [])
        if not isinstance(marks, list):
            raise ValidationError("Marks must be provided as a list.")
        return cls(
            data["student_id"], data["name"], data["email"],
            data["department"], marks
        )
