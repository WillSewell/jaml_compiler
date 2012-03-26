from symbols import (ClassSymbol, InterfaceSymbol, MethodSymbol,
                     ConstructorSymbol, ArraySymbol, VarSymbol, FieldSymbol)
from utilities.utilities import ArrayType, camel_2_underscore, get_full_type
from exceptions import (MethodNotImplementedError, VariableNameError)

class ClassInterfaceMethodScanner(object):
        """Provides an initial sweep through the higher level nodes in the ast
        looking for classes / interfaces / methods so symbols can be created, 
        and can be added to the top environment.
        """
        def __init__(self, t_env):
                """Set the top level environment."""
                self._t_env = t_env
                self._field_names = []

        def scan(self, asts):
                """Main method to initiate the scanning."""
                # First build up list of all possible types for use by the rest
                # of the type checking process
                for ast in asts:
                        self._t_env.add_type(ast.children[0].value)
                # Next visit the top level nodes - class or interface dcls
                for ast in asts:
                        self._visit(ast)
                # If a class implements an interface, check it implements it
                # correctly
                self._verify_implementations(asts)

        def _visit(self, node):
                method = None
                for class_ in node.__class__.__mro__:
                        method_name = '_visit' + class_.__name__
                        method_name = camel_2_underscore(method_name)
                        method = getattr(self, method_name, None)
                        if method:
                                break
                if not method:
                        return None
                return method(node)

        def _visit_class_node(self, node):
                """Create a class symbol and add methods to it."""
                self._cur_class = node.children[0].value
                class_s = ClassSymbol(node.children[0].value)
                class_s.modifiers = node.modifiers
                self._add_members(class_s, node)
                self._t_env.put_class_s(class_s)
                # Check if the class 'extends' or implements another
                # If it extends
                parent = node.children[1].value
                if parent != '':
                        # Add subclass to super class
                        class_s.super_class = parent
                else:
                        # Set parent to Object, which is the implicit super
                        class_s.super_class = 'Object'
                # If it implements
                try:
                        interfaces = node.children[2].children
                        if interfaces != []:
                                for interface in interfaces:
                                        # Add this interface to the cur class
                                        class_s.add_interface(interface.value)
                except AttributeError:
                        # It does not implement an interface
                        pass

        def _visit_interface_node(self, node):
                """Create an interface symbol and add methods to it."""
                interface_s = InterfaceSymbol(node.children[0].value)
                self._add_members(interface_s, node)
                self._t_env.put_interface_s(interface_s)
                # If it extends another interface
                parent = node.children[1].value
                if parent != '':
                        # Add subclass to super class
                        interface_s.super_interface = parent
        
        def _add_members(self, symbol, node):
                """For a class or interface symbol, and it's corresponding
                ast node, add it's method and field symbols to the class or
                interface (methods only for interface) symbol.
                """
                dcls = None
                try:
                        dcls = node.children[3].children
                except IndexError:
                        # It's an interface
                        dcls = node.children[2].children
                except AttributeError:
                        # The class body was empty
                        return
                for dcl in sorted(dcls):
                        # Sorted causes the field dcls to appear first, so
                        # after, the parameters can be checked for name
                        # clashes
                        dcl_s = self._visit(dcl)
                        if dcl_s != None:
                                if isinstance(dcl_s, MethodSymbol):
                                        symbol.add_method(dcl_s)
                                elif isinstance(dcl_s, ConstructorSymbol):
                                        symbol.constructor = dcl_s
                                else:
                                        # It's a field
                                        self._check_field_name(dcl_s)
                                        symbol.add_field(dcl_s)
        
        def _check_field_name(self, field_s):
                """Checks a field has a name that isn't the same as the name
                of a type.
                """
                if field_s.name in self._t_env.types:
                        msg = ('field "' + field_s.name + '" cannot have the' +
                               'same name as a type!')
                        raise VariableNameError(msg)
        
        def _visit_field_dcl_node(self, node):
                """Helper method for scan_classes_methods which scans
                properties of the method, create a symbol for it, and returns
                it.
                """
                try:
                        # For arrays
                        name = node.children[1].children[0].value
                        type_ = get_full_type(node.children[0].value,
                                              self._t_env)
                        dimensions = node.children[1].children[1].value
                        type_ = ArrayType(type_, dimensions)
                except AttributeError:
                        # Regular variables
                        name = node.children[1].value
                        type_ = get_full_type(node.children[0].value,
                                              self._t_env)
                # Build up list of the names
                self._field_names.append(name)
                # Create and return the symbol
                field_s = FieldSymbol(name, type_)
                field_s.modifiers = node.modifiers
                return field_s
        
        def _visit_field_dcl_assign_node(self, node):
                try:
                        # For arrays
                        array_node = node.children[1].children[0]
                        name = array_node.children[0].value
                        type_ = get_full_type(node.children[0].value,
                                              self._t_env)
                        dimensions = array_node.children[1].value
                        type_ = ArrayType(type_, dimensions)
                except AttributeError:
                        # Regular variables
                        name = node.children[1].children[0].value
                        type_ = get_full_type(node.children[0].value,
                                              self._t_env)
                field_s = FieldSymbol(name, type_)
                field_s.modifiers = node.modifiers
                return field_s

        def _visit_method_dcl_node(self, node):
                return self._scan_method(node)
        
        def _visit_abs_method_dcl_node(self, node):
                return self._scan_method(node)
        
        def _scan_method(self, node):
                """Helper method for scan_classes_methods which scans
                properties of the method, create a symbol for it, and returns it
                """
                name = node.children[0].value
                type_ = self._get_method_node_type(node)
                # Create variable symbols for each parameter, and add them to
                # the method symbol
                params = self._visit(node.children[2])
                if params == None: 
                        params = [] 
                method_s = MethodSymbol(name, type_, params)
                try:
                        method_s.modifiers = node.modifiers
                except AttributeError:
                        # Abstract methods do not have modifiers
                        pass
                return method_s

        def _visit_method_dcl_array_node(self, node):
                return self._scan_method_array(node)
                
        def _visit_abs_method_dcl_array_node(self, node):
                return self._scan_method_array(node)
        
        def _scan_method_array(self, node):
                """Create a method symbol for a method which returns an array
                type.
                """
                name = node.children[0].value
                type_ = self._get_method_node_type(node)
                type_ = ArrayType(type_, node.children[2].value)
                params = self._visit(node.children[3])
                if params == None: 
                        params = [] 
                method_s = MethodSymbol(name, type_, params)
                method_s.modifiers = node.modifiers
                return method_s

        def _get_method_node_type(self, node):
                """Gets the return type of a particular method."""
                type_node = node.children[1]
                type_ = 'void'
                if type_node.value != 'void':
                        type_ = get_full_type(type_node.value, self._t_env)
                return type_
        
        def _visit_constructor_dcl_node(self, node):
                """Creates a constructor symbol in much the same way as regular
                methods.  The difference is constructors do not have return
                types.
                """
                name = node.children[0].value
                # Create variable symbols for each parameter, and add them to
                # the method symbol
                params = self._visit(node.children[1])
                if params == None: 
                        params = [] 
                constructor_s = ConstructorSymbol(name, params)
                constructor_s.modifiers = node.modifiers
                return constructor_s

        def _visit_param_list_node(self, node):
                """Go through the method parameters and create a variable
                symbol for each one - these are returned as a list.
                """
                params = []
                for param in node.children:
                        id_node = param.children[1]
                        p_type = get_full_type(param.children[0].value,
                                               self._t_env)
                        # Check if it's an array or a simple identifier
                        p_name = ''
                        try:
                                # Treat it like an array
                                p_name = id_node.children[0].value
                                dimensions = id_node.children[1].value
                                p_type = ArrayType(p_type, dimensions)
                                params.append(ArraySymbol(p_name, p_type,
                                                          dimensions))
                        except AttributeError:
                                # It's a regular variable
                                p_name = id_node.value
                                params.append(VarSymbol(p_name, p_type))
                        # Check the name does not clash with a type
                        # or field name
                        self._check_param_name(p_name)
                return params
        
        def get_param_symbols(self, node):
                """A public facing interface to the above method for use by
                the semantic analyser.
                """
                return self._visit_param_list_node(node)
        
        def _check_param_name(self, name):
                """Check the local variable does not have the same name as
                a field or a type.
                """
                if (name in self._field_names 
                    or name in self._t_env.types):
                        msg = ('Parameter "' + name + '" cannot have the' +
                       'same name as a type, field or parameter!')
                        raise VariableNameError(msg)

        def _verify_implementations(self, asts):
                """Verify all classes implementing interfaces do so correctly.
                """
                for ast in asts:
                        if len(ast.children) == 4:
                                # It's a class
                                if ast.children[1] != '':
                                        # It implements an interface
                                        self._check_correctly_implemented(ast)
        
        def _check_correctly_implemented(self, class_node):
                """Checks if a particular class node implements correctly all
                the methods from the interface(s) it implements.
                """
                class_s = self._t_env.get_class_s(class_node.children[0].value)
                interfaces = class_s.interfaces
                # Get all the implemented interfaces
                interfaces_s = []
                for interface in interfaces:
                        interface_s = self._t_env.get_interface_s(interface)
                        interfaces_s.append(interface_s)
                        # Add any super interfaces
                        interfaces_s = self._add_super_interfaces(interface_s,
                                                                  interfaces_s)
                # For each implemented interface, make sure each method is
                # implemented by the class.
                for interface_s in interfaces_s:
                        for i_method in interface_s.methods:
                                res = self._search_c_methods(i_method, class_s)
                                if res == False:
                                        msg = ('Method "' + i_method.name +
                                               '" not implemented!')
                                        raise MethodNotImplementedError(msg)
        
        def _add_super_interfaces(self, cur_interface, interfaces_s):
                """Adds any super interface (and their super interfaces) to
                the list of super interface symbols.
                """
                has_super = True
                super_ = cur_interface.super_interface
                while has_super:
                        if super_ != '':
                                super_s = self._t_env.get_interface_s(super_)
                                interfaces_s.append(super_s)
                                super_ = super_s.super_interface
                        else:
                                has_super = False
                return interfaces_s
                                                
        def _search_c_methods(self, i_method, class_s):
                """Searches through all methods of class_s for one with the
                same signature as i_method.
                """
                for c_method in class_s.methods:
                        if c_method == i_method:
                                return True
                return False