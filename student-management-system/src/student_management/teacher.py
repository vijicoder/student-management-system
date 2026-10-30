"""Teacher model used to demonstrate polymorphism."""

from .person import Person
from .exceptions import ValidationError


class Teacher(Person):
    """A teacher with a subject."""

    def __init__(self, teacher_id: str, name: str, email: str, subject: str):
        super().__init__(teacher_id, name, email)
        subject = str(subject).strip()
        if not subject:
            raise ValidationError("Subject cannot be empty.")
        self.__subject = subject

    @property
    def subject(self) -> str:
        return self.__subject

    def display_details(self) -> str:
        return (
            f"Teacher | ID: {self.person_id} | Name: {self.name} | "
            f"Email: {self.email} | Subject: {self.subject}"
        )
