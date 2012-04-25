"""This module stores the various exceptions that can be thrown by the type
checker.
"""

class JamlException(Exception):
    """Generic exception type for this project."""
    pass

class NotInitWarning(JamlException):
    """Raised when a reference to a variable is made when it has not been
    initialised.
    """
    pass

class NoReturnError(JamlException):
    """Raised when a method does not have a return statement."""
    pass

class SymbolNotFoundError(JamlException):
    """Raised when a symbol is used which is not in the symbol table."""
    pass

class MethodSignatureError(JamlException):
    """Raised when a method is called with incorrect number of arguments."""
    pass

class FinalError(JamlException):
    """Raised when a final field or method is not used correctly."""
    pass

class DimensionsError(JamlException):
    """Raised when the incorrect number of dimensions is used when
    referencing an array.
    """
    pass

class MethodNotImplementedError(JamlException):
    """Raised when a class does not correctly implement an interface."""
    pass

class ConstructorError(JamlException):
    """Raised when there is an issue with the constructor."""
    pass

class VariableNameError(JamlException):
    """Thrown when there is a conflict with a variable's name."""
    pass

class ClassSignatureError(JamlException):
    """Raised when there is an issue with a class signature."""
    pass

class MethodInvokationError(JamlException):
    """Raised when their is an issue with a call to a method."""
    pass

class AssignmentError(JamlException):
    """Raised when there's a problem with an assignment statement."""
    pass

class ObjectCreationError(JamlException):
    """Raised when there is an issue with the instantiation of a class."""

class StaticError(JamlException):
    """Raised when a static method/field is not referenced correctly."""