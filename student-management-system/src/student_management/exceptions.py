"""Custom exceptions used by the student management system."""


class StudentManagementError(Exception):
    """Base exception for this application."""


class ValidationError(StudentManagementError):
    """Raised when supplied data is invalid."""


class DuplicateStudentError(StudentManagementError):
    """Raised when a student ID already exists."""


class StudentNotFoundError(StudentManagementError):
    """Raised when a requested student does not exist."""
