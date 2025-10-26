"""Domain exceptions.

This module defines the foundational exception classes for all domain-level errors.
"""


class DomainException(Exception):
    """Domain exception for domain-level errors.

    This exception serves as the foundation for all domain-specific exceptions.
    It provides a consistent structure with error_code, message and context for error handling.

    Attributes:
        error_code: A machine-readable error code identifying the exception type.
        message: A human-readable error message describing the exception.
        context: Additional contextual information about the error.
    """

    def __init__(
        self, error_code: str, message: str, context: dict[str, str] | None = None
    ) -> None:
        """Initialize the domain exception.

        Args:
            error_code: A machine-readable error code.
            message: A human-readable error message.
            context: Optional dictionary with additional error context.
        """
        self.error_code = error_code
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the exception."""
        return f"{self.__class__.__name__} [{self.error_code}]: {self.message}"


class NotFoundException(DomainException):
    """Exception raised when an entity is not found.

    This is a base exception for all not-found scenarios across domains.

    Attributes:
        entity_type: The type of entity that was not found (e.g., "Restaurant", "User").
        entity_id: The identifier used to search for the entity.
    """

    def __init__(self, entity_type: str, entity_id: str) -> None:
        """Initialize not found exception.

        Args:
            entity_type: Type of the entity that was not found
            entity_id: Identifier of the entity that was not found
        """
        super().__init__(
            error_code=f"{entity_type.upper()}_NOT_FOUND",
            message=f"{entity_type} with ID '{entity_id}' not found",
            context={"entity_type": entity_type, "entity_id": entity_id},
        )
        self.entity_type = entity_type
        self.entity_id = entity_id


class AlreadyExistsException(DomainException):
    """Exception raised when attempting to create a duplicate entity.

    This is a base exception for all duplicate-entity scenarios across domains.

    Attributes:
        entity_type: The type of entity that already exists (e.g., "Restaurant", "User").
        identifier: The identifier that caused the duplicate conflict.
    """

    def __init__(self, entity_type: str, identifier: str) -> None:
        """Initialize already exists exception.

        Args:
            entity_type: Type of the entity that already exists
            identifier: Identifier causing the conflict
        """
        super().__init__(
            error_code=f"{entity_type.upper()}_ALREADY_EXISTS",
            message=f"{entity_type} with identifier '{identifier}' already exists",
            context={"entity_type": entity_type, "identifier": identifier},
        )
        self.entity_type = entity_type
        self.identifier = identifier


class ValidationException(DomainException):
    """Exception raised when domain validation fails.

    This is a base exception for all validation errors across domains.

    Attributes:
        field: The field that failed validation.
        value: The value that failed validation.
    """

    def __init__(
        self, message: str, field: str | None = None, value: str | None = None
    ) -> None:
        """Initialize validation exception.

        Args:
            message: Human-readable validation error message
            field: Optional field name that failed validation
            value: Optional value that failed validation
        """
        context: dict[str, str] = {}
        if field:
            context["field"] = field
        if value:
            context["value"] = value

        super().__init__(
            error_code="VALIDATION_ERROR",
            message=message,
            context=context,
        )
        self.field = field
        self.value = value
