class NotInitWarning(Exception):
        """Raised when a reference to a variable is made when it has not been
        initialised.
        """
        pass

class NoReturnError(Exception):
        """Raised when a method does not have a return statement."""
        pass

class SymbolNotFoundError(Exception):
        """Raised when a symbol is used which is not in the symbol table."""
        pass

class MethodSignatureError(Exception):
        """Raised when a method is called with incorrect number of arguments."""
        pass

#class FieldError(Exception):
#        """Raised when a field definition is not valid."""
#        pass

class DimensionsError(Exception):
        """Raised when the incorrect number of dimensions is used when
        referencing an array.
        """
        pass

class MethodNotImplementedError(Exception):
        """Raised when a class does not correctly implement an interface."""
        pass

class ConstructorError(Exception):
        """Raised when there is an issue with the constructor."""
        pass

class VariableNameError(Exception):
        """Thrown when there is a conflict with a variable's name."""
        pass

class ClassSignatureError(Exception):
        """Raised when there is an issue with a class signature."""
        pass

class MethodInvokationError(Exception):
        """Raised when their is an issue with a call to a method."""
        pass

class AssignmentError(Exception):
        """Raised when there's a problem with an assignment statement."""
        pass

class ObjectCreationError(Exception):
        """Raised when there is an issue with the instantiation of a class."""
        
class StaticError(Exception):
        """Raised when a static method/field is not referenced correctly."""