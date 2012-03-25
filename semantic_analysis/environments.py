from exceptions import SymbolNotFoundError
from semantic_analysis.exceptions import VariableNameError

class TopEnvironment(object):
        """This environment is used to store all the symbols publicly
        available to all code.  This is essentially all the classes (which in
        turn store their methods).  This also stores the possible types.
        """
        def __init__(self, lib_classes):
                self._class_table = dict()
                self._interface_table = dict()
                # Stores all numerical types
                self._nums = ['byte', 'char', 'short', 'int', 'long', 'float',
                              'double']
                # Stores all possible types
                self._types = ['boolean'] + self._nums + lib_classes.keys()
                # Stores all library classes (currently only from java.lang)
                self._lib_classes = lib_classes
                # Stores signatures of library methods/constructors/fields
                self._lib_method_sigs = {}
                self._lib_field_sigs = {}
                self._lib_cons_sigs = {}

        def put_class_s(self, symbol):
                """Adds a class symbol to the dict."""
                self._class_table[symbol._name] = symbol

        def get_class_s(self, name):
                """Gets the requested class symbol, or returns an error if
                it does not exist.
                """
                try:
                        return self._class_table[name]
                except KeyError:
                        msg = 'Class "' + name + '" does not exist!'
                        raise SymbolNotFoundError(msg)

        def get_classes(self):
                """Returns all class symbols."""
                return self._class_table

        def put_interface_s(self, symbol):
                """Adds an interface symbol to the dict."""
                self._interface_table[symbol._name] = symbol

        def get_interface_s(self, name):
                """Gets the requested interface symbol, or returns an error if
                it does not exist.
                """
                try:
                        return self._interface_table[name]
                except KeyError:
                        msg = 'Interface "' + name + '" does not exist!'
                        raise SymbolNotFoundError(msg)
        
        def get_class_or_interface_s(self, name):
                """Returns a class or interface symbol."""
                try:
                        return self._class_table[name]
                except KeyError:
                        try:
                                return self._interface_table[name]
                        except KeyError:
                                msg = ('Class or interface does "' + name +
                                       '" not exist!')
                                raise SymbolNotFoundError(msg)

        def _get_interfaces(self):
                """Returns all interface symbols."""
                return self._interface_table

        def get_lib_classes(self):
                """Return the list of library classes."""
                return self._lib_classes

        def add_type(self, type_):
                self._types.append(type_)

        def get_types(self):
                return self._types

        def get_nums(self):
                return self._nums
        
        def get_lib_method_sig(self, name):
                return self._lib_method_sigs
        
#        def add_lib_method_sig(self, class_, name, arg_types, ret_type):
#                sig = name
#                if len(arg_types) == 0:
#                        # If there are no parameters
#                        method_spec = '()' + self._get_jvm_type(method_s)
#                else:
#                        # It has params, so add them to the method_spec
#                        method_spec = '('
#                        for param in method_s.params:
#                                method_spec += self._get_jvm_type(param)
#                        method_spec += ')' + ret_type
#                self._lib_method_sigs[[class_, name] + arg_types]

        classes = property(get_classes)
        interfaces = property(_get_interfaces)
        lib_classes = property(get_lib_classes) # TODO: also need lib_interfaces!
        types = property(get_types)
        nums = property (get_nums)
#        lib_method_sigs
#        lib_field_sigs
#        lib_cons_sigs

class Environment(object):
        """Environment which represents the symbol table and other
        information, such as current meothd, of the current block.
        It holds a pointer to the environment of the outer block.
        """
        def __init__(self, env):
                """Creates a new Environment, env is the parent environment."""
                # _prev_table stores the environment of the outer block
                self._prev_table = env
                # _var_table stores a dict where keys are all declared
                # identifiers seen so far, and the values are their types
                self._var_table = dict()
                # Stores the symbol of the current method
                self._method = None
                # Holds the symbol of the current class
                self._class = None
                if self._prev_table is not None:
                        self._class = self._prev_table.cur_class
                        self._method = self._prev_table.cur_method
        
        def put_var_s(self, symbol):
                """Adds a variable or array symbol to the variable current
                symbol table.
                """
                # Check to see if it already exists
                try:
                        # If one can get the variable with the same name, it
                        # already exists
                        self.get_var_s(symbol.name)
                        msg = 'A variable with the name already exists!'
                        raise VariableNameError(msg)
                except SymbolNotFoundError:
                        self._var_table[symbol.name] = symbol

        def get_var_s(self, symbol):
                """Gets a symbol from any of the symbol tables in the current
                scope. None is returned if it is not in the table."""
                env = self
                while env is not None:
                        try:
                                found = env._var_table[symbol]
                                return found
                        except KeyError:
                                pass
                        env = env._prev_table
                msg = ('Variable "' + symbol +
                       '" undeclared in current scope!')
                raise SymbolNotFoundError(msg)

        def set_cur_class(self, class_):
                self._class = class_

        def get_cur_class(self):
                return self._class

        def add_parent(self, env):
                self._prev_table = env

        def set_cur_method(self, method):
                self._method = method

        def get_cur_method(self):
                return self._method

        cur_method = property(get_cur_method, set_cur_method)
        cur_class = property(get_cur_class, set_cur_class)   