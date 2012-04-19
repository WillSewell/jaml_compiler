"""An assortment of classes and scripts used throughout the program."""
import re
import parser_.tree_nodes as nodes

class ArrayType(object):
    """A special type representing arrays."""
    def __init__(self, type_, dimensions):
        self._type = type_
        self._dimensions = dimensions

    def __eq__(self, other):
        """This is so the attributes can be compared with another array
        type.
        """
        try:
            if self._type == other.type_:
                if self._dimensions == other.dimensions:
                    return True
        except AttributeError:
            # Not an array type
            pass
        return False

    def __ne__(self, other):
        """This is for != comparisons."""
        return not self.__eq__(other)

    def _get_type(self):
        return self._type

    def _get_dimensions(self):
        return self._dimensions

    type_ = property(_get_type)
    dimensions = property(_get_dimensions)

class MatrixType(object):
    """A special type representing matrices."""
    def __init__(self, dimension1, dimension2):
        # Stores the length of each dimension
        self._dimension1 = dimension1
        self._dimension2 = dimension2

    def __eq__(self, other):
        """This is so the attributes can be compared with another matrix type
        """
        try:
            if self._dimension1 == other.dimension1:
                if self._dimension2 == other.dimension2:
                    return True
        except AttributeError:
            # Not a matrix type
            pass
        return False

    def __ne__(self, other):
        """This is for != comparisons."""
        return not self.__eq__(other)

    def _get_dimension1(self):
        return self._dimension1
    
    def _get_dimension2(self):
        return self._dimension2

    dimension1 = property(_get_dimension1)
    dimension2 = property(_get_dimension2)

def visit(source_object, node, env = None):
    """Looks up the correct method to call in source_object based on the type
    of node. TypeChecker methods also need the env.
    Code from: http://peter-hoffmann.com/2010
    extrinsic-visitor-pattern-python-inheritance.html
    """
    method = None
    # Search through super classes of the nodes type
    for class_ in node.__class__.__mro__:
        # Convert the camel case name into a underscored name prefixed with
        # _visit - this corrosponds to the method's name
        method_name = '_visit' + class_.__name__
        method_name = camel_2_underscore(method_name)
        # Get the method attribute
        method = getattr(source_object, method_name, None)
        if method:
            break
    if not method:
        # Some nodes do not need to be type checked -
        # for example, interfaces
        return None
    # Run the method with the node and return the result
    if env is not None:
        return method(node, env)
    else:
        return method(node)
    
def camel_2_underscore(string):
    """Converts a CamelCase string to one where the words are
    separated_by_underscores.
    From: http://stackoverflow.com/a/1176023/1018290
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_full_type(type_, t_env):
    """This gets the full _name of the type, given the type information held
    in a top level environment.
    """
    if type_ not in t_env.types + ['void']:
        # It might already be a full class type
        if type_ not in t_env.lib_classes.values():
            raise TypeError('No such type as: ' + type_ + '!')
    # For a library class, get its full type
    if type_ in t_env.lib_classes.keys():
        type_ = t_env.lib_classes[type_]
    return type_

def is_main(method_s):
    """For a given method, checks whether it is the main method."""
    try:
        if (method_s.name == 'main' 
            and method_s.type_ == 'void' 
            and 'static' in method_s.modifiers
            and len(method_s.params) == 1  
            and method_s.params[0].name == 'args' 
            and method_s.params[0].type_.type_ == 'java/lang/String' 
            and method_s.params[0].type_.dimensions == 1):
            return True
    except AttributeError: pass
    return False

def get_jvm_type(node_or_symbol):
    """Get's the jvm type signature for a given node, symbol, or simple
    string representation of the type.
    """
    type_ = ''
    jvm_type = ''
    # Work out if it needs array information
    try:
        try:
            # Try as if it's a method symbol
            dimensions = node_or_symbol.type_.dimensions
            for _ in range(dimensions):
                jvm_type += '['
        except AttributeError:
            try:
                # Try as an array symbol
                for _ in range(node_or_symbol.dimensions):
                    jvm_type += '['
            except AttributeError:
                # It's an ast node
                node = node_or_symbol
                if isinstance(node, nodes.ArrayDclNode):
                    for _ in range(node.children[1]):
                        jvm_type += '['
                elif isinstance(node, nodes.ArrayInitNode):
                    for _ in node.children[1:]:
                        jvm_type += '['
            # Get the type symbol
            type_ = node_or_symbol.type_
        try:
            type_ = node_or_symbol.type_.type_
        except AttributeError: pass
    except AttributeError:
        # Treat it as a string representation of the type
        type_ = node_or_symbol
    if type_ == 'boolean':
        jvm_type += 'Z'
    elif type_ == 'byte':
        jvm_type += 'B'
    elif type_ == 'char':
        jvm_type += 'C'
    elif type_ == 'short':
        jvm_type += 'S'
    elif type_ == 'int':
        jvm_type += 'I'
    elif type_ == 'long':
        jvm_type += 'J'
    elif type_ == 'float':
        jvm_type += 'F'
    elif type_ == 'double':
        jvm_type += 'D'
    elif type_ == 'void':
        jvm_type += 'V'
    else:
        # It's a class type
        jvm_type += 'L' + type_ + ';'
    return jvm_type