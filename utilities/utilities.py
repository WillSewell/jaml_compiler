"""An assortment of classes and scripts used throughout the program."""
import re

class ArrayType(object):
        """A special type representing arrays."""
        def __init__(self, type_, dimensions):
                self._type = type_
                self._dimensions = dimensions

        def __eq__(self, other):
                """This is so the attributes can be compared with another array
                type.
                """
                if isinstance(other, ArrayType):
                        if self.type_ == other.type_:
                                if self.dimensions == other.dimensions:
                                        return True
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
        
def camel_2_underscore(string):
        """Converts a CamelCase string to one where the words are
        separated_by_underscores.
        From: http://stackoverflow.com/a/1176023/1018290
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_full_type(type_, t_env):
        """This gets the full _name of the type, given the type information
        held in a top level environment.
        """
        if type_ not in t_env.types:
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

