"""Base class shared by people in the university system."""

from abc import ABC, abstractmethod
from .exceptions import ValidationError


class Person(ABC):
    """Abstract parent class demonstrating encapsulation."""

    def __init__(self, person_id: str, name: str, email: str):
        person_id = str(person_id).strip()
        name = str(name).strip()
        email = str(email).strip()

        if not person_id:
            raise ValidationError("ID cannot be empty.")
        if not name:
            raise ValidationError("Name cannot be empty.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Enter a valid email address.")

        self.__person_id = person_id
        self.__name = name
        self.__email = email

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValidationError("Name cannot be empty.")
        self.__name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        value = str(value).strip()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValidationError("Enter a valid email address.")
        self.__email = value

    @abstractmethod
    def display_details(self) -> str:
        """Return a human-readable description of this person."""
