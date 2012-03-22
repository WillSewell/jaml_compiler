import semantic_analyser
from exceptions import VariableNameError, SymbolNotFoundError

class Symbol(object):
        """
        Represents a symbol to be stored in the Environment.  Using a class
        rather than a simpler data structure, such as a list of symbol
        attributes allows for easier code modification.
        """
        def __init__(self, name):
                self._name = name

        def _get_name(self):
                return self._name

        name = property(_get_name)

class ClassInterfaceSymbol(Symbol):
        """Generic symbol which represents both classes and interfaces."""
        def __init__(self, name):
                super(ClassInterfaceSymbol, self).__init__(name)
                self._methods = []

        def _get_methods(self):
                return self._methods
        
        def _get_symbol(self, name, list_):
                """Used by other methods to get fields/methods of the class."""
                for member in list_:
                        if member._name == name:
                                return member
                msg = ('Class member "' + name + '" does not exist in ' +
                       'class "' + self._name + '".')
                raise semantic_analyser.SymbolNotFoundError(msg)

        def get_method(self, name):
                return self._get_symbol(name, self._methods)
        
        def add_method(self, method):
                self._methods.append(method)

        methods = property(_get_methods)

class ModiferContainer(object):
        """Subclasses are those which can have modifiers."""
        def _get_modifiers(self):
                return self._modifiers

        def _set_modifiers(self, value):
                self._modifiers = value
        
        modifiers = property(_get_modifiers, _set_modifiers)

class ClassSymbol(ClassInterfaceSymbol, ModiferContainer):
        """Symbol that represent classes."""
        def __init__(self, name):
                super(ClassSymbol, self).__init__(name)
                self._super_class = None
                self._interfaces = []
                self._constructor = None
                self._fields = []
        
        def _get_super_class(self):
                return self._super_class

        def _set_super_class(self, super_class):
                self._super_class = super_class

        def _get_interfaces(self):
                return self._interfaces

        def add_interface(self, interface):
                self._interfaces.append(interface)
        
        def _get_constructor(self):
                return self._constructor
        
        def _set_constructor(self, constructor):
                self._constructor = constructor
        
        def _get_fields(self):
                return self._fields
        
        def _get_public_fields(self):
                return [field for field in self._fields
                        if not 'private' in field.modifiers]

        def get_field(self, name):
                return self._get_symbol(name, self._fields)
        
        def get_public_field(self, name):
                return self._get_symbol(name, self._get_public_fields())
        
        def add_field(self, field):
                try:
                        # If one can get the variable with the same name, it
                        # already exists
                        self.get_field(field.name)
                        msg = 'A field with the name already exists!'
                        raise VariableNameError(msg)
                except SymbolNotFoundError:
                        self._fields.append(field)
        
        def _get_public_methods(self):
                return [method for method in self._methods
                        if 'private' not in method.modifiers]
        
        def get_public_method(self, name):
                return self._get_symbol(name, self._get_public_methods())
        
        super_class = property(_get_super_class, _set_super_class)
        interfaces = property(_get_interfaces)
        constructor = property(_get_constructor, _set_constructor)
        fields = property(_get_fields)
        public_methods = property(_get_public_methods)

class InterfaceSymbol(ClassInterfaceSymbol):
        def __init__(self, name):
                super(InterfaceSymbol, self).__init__(name)
                self._sub_interfaces = None
                self._super_interface = ''
                
        def _get_super_interface(self):
                return self._super_interface
        
        def _set_super_interface(self, super_interface):
                self._super_interface = super_interface

        super_interface = property(_get_super_interface, _set_super_interface)

class SymbolWithType(Symbol):
        """Represents symbols that have a type associated with them."""
        def __init__(self, name, type_):
                super(SymbolWithType, self).__init__(name)
                self._type = type_

        def _get_type(self):
                return self._type

        type_ = property(_get_type)

class MethodSymbol(SymbolWithType, ModiferContainer):
        """Symbol that represent declared methods."""
        def __init__(self, name, type_, params):
                super(MethodSymbol, self).__init__(name, type_)
                # Used by the type checker to make sure it has a return
                # Statement
                self._has_ret = False
                self._params = params
                
        def __eq__(self, other):
                """This is so the attributes can be compared with another method
                symbol.  Needed to compare class method signatures with 
                interface method signatures.
                """
                try:
                        if self._name != other._name:
                                return False
                        if self._name != other._name:
                                return False
                        for idx, param in enumerate(self.params):
                                if param != other.params[idx]:
                                        return False
                except AttributeError:
                        # It was the same type of symbol
                        return False
                return True

        def __ne__(self, other):
                """This is for != comparisons."""
                return not self.__eq__(other)

        def add_param(self, param):
                try:
                        # If one can get the variable with the same name, it
                        # already exists
                        self.get_var_s(param.name)
                        msg = 'A parameter with the name already exists!'
                        raise VariableNameError(msg)
                except SymbolNotFoundError:
                        self._fields.append(param)
                
        def _get_params(self):
                return self._params
        
        def _get_has_ret(self):
                return self._has_ret
        
        def _set_has_ret(self, val):
                self._has_ret = val

        params = property(_get_params)
        has_ret = property(_get_has_ret, _set_has_ret)

class ConstructorSymbol(Symbol):
        """A special symbol for a class' constructor."""
        def __init__(self, name, params):
                super(ConstructorSymbol, self,).__init__(name)
                self._params = params
        
        # Note - the params code is duplicated, but this was done to avoid
        # avoid diamond multiple inheritance, which introduces problems with
        # super() when __init__ has different signatures in super classes
        def _get_params(self):
                return self._params

        params = property(_get_params)

class SymbolWithInit(SymbolWithType):
        """Represents symbols that must be initialised before they are used."""
        def __init__(self, name, type_):
                super(SymbolWithInit, self).__init__(name, type_)
                self.is_init = False

        def _get_is_init(self):
                return self._is_init

        def _set_is_init(self, is_init):
                self._is_init = is_init

        is_init = property(_get_is_init, _set_is_init)

class ArraySymbol(SymbolWithInit):
        """A special type of symbol for arrays which additionally stores the
        number of dimensions.
        """
        def __eq__(self, other):
                """This is so the attributes can be compared with another array
                symbol.  Needed when comparing method parameters
                """
                try:
                        if self._name != other._name:
                                return False
                        if self._name != other._name:
                                return False
                        if self.dimensions != other.dimensions:
                                return False
                except AttributeError:
                        # It was the same type of symbol
                        return False
                return True

        def __ne__(self, other):
                """This is for != comparisons."""
                return not self.__eq__(other)
        
        def __init__(self, name, type_, dimensions):
                super(ArraySymbol, self).__init__(name, type_)
                self._dimensions = dimensions

        def _get_dimensions(self):
                return self._dimensions

        dimensions = property(_get_dimensions)

class VarSymbol(SymbolWithInit):
        """Represents standard variable symbols."""
        def __eq__(self, other):
                """This is so the attributes can be compared with another var
                symbol.  Needed when comparing method parameters
                """
                try:
                        if self._name != other._name:
                                return False
                        if self._name != other._name:
                                return False
                except AttributeError:
                        # It was the same type of symbol
                        return False
                return True

        def __ne__(self, other):
                """This is for != comparisons."""
                return not self.__eq__(other)

class FieldSymbol(VarSymbol, ModiferContainer):
        """A special case of normal variables which can have modifiers."""
        pass