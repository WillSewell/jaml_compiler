import re
from spark import GenericScanner

class Token(object):
        """A class to represent the tokens the scanner identifies."""
        def __init__(self, name, attr=None):
                """Initialise the name of the token i.e. what lexical token it
                acually corrosponds to, and the atribute if any.  For literals
                and identifies, this is the value or the word itself."""
                self._name = name
                self._attr = attr

        def __cmp__(self, obj):
                return cmp(self._name, obj)

        def __repr__(self):
                if self._attr == None:
                        return self._name
                else:
                        return self._name + ': ' + '(' + str(self._attr) + ')'
        
        def _get_name(self):
                return self._name
        
        def _get_attr(self):
                return self._attr
        
        def _set_name(self, name):
                self._name
        
        def _set_attr(self, attr):
                self._attr = attr
        
        name = property(_get_name, _set_name)
        attr = property(_get_attr, _set_attr)

class Scanner(GenericScanner):
        def __init__(self):
                GenericScanner.__init__(self)

        def tokenize(self, input_):
                self.rv = []
                GenericScanner.tokenize(self, input_)
                return self.rv
        
        def _convert_rel_op(self, op_str):
                if op_str == '<' or op_str == '>':
                        return op_str
                elif re.match(r'>\s*=', op_str) != None:
                        return '>='
                else: # It's <=
                        return '<='

        def t_whitespace(self, s):
                r'\s+'
                pass
        
        def t_if(self, s):
                r'if'
                t = Token('IF')
                self.rv.append(t)
        
        def t_else(self, s):
                r'else'
                t = Token('ELSE')
                self.rv.append(t)
        
        def t_while(self, s):
                r'while'
                t = Token('WHILE')
                self.rv.append(t)
        
        def t_for(self, s):
                r'for'
                t = Token('FOR')
                self.rv.append(t)
        
        def t_new(self, s):
                r'new'
                t = Token('NEW')
                self.rv.append(t)
        
        def t_return(self, s):
                r'return'
                t = Token('RETURN')
                self.rv.append(t)
        
        def t_class(self, s):
                r'class'
                t = Token('CLASS')
                self.rv.append(t)
        
        def t_void(self, s):
                r'void'
                t = Token('VOID')
                self.rv.append(t)
                
        def t_str_l(self, s):
                r'"([^"]*)"'
                t = Token('STR_L', eval(s))
                self.rv.append(t)
        
        def t_char_l(self, s):
                r"'.'"
                # eval() will evaluate a string, so removes the ''
                t = Token('CHAR_L', ord(eval(s)))
                self.rv.append(t)

        def t_double_float_l(self, s):
                # Doubles and floats must be in one rule because otherwise the
                # regex engine would always match 1.5F as a double and then
                # crash on the F because it's greedy.
                r'\b([0-9]*\.[0-9]+)(d|D|f|F)?|[0-9]+(d|D|f|F)\b'
                # First check for a float
                if s.find('f') != -1 or s.find('F') != -1:
                        attr = re.sub('f|F', '', s)
                        t = Token('FLOAT_L', float(attr))
                else:
                        attr = re.sub('d|D', '', s)
                        t = Token('DOUBLE_L', float(attr))
                self.rv.append(t)

        def t_long_l(self, s):
                r'\b\d+(l|L)\b'
                attr = re.sub('l|L', '', s)
                t = Token('LONG_L', long(attr))
                self.rv.append(t)

        def t_int_l(self, s):
                r'\b\d+\b'
                t = Token('INT_L', int(s))
                self.rv.append(t)

        def t_text(self, s):
                r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
                # check for reserved words
                if s in ['char', 'byte', 'short', 'int', 'long', 'float', 
                         'double', 'boolean', 'matrix']:
                        t = Token('TYPE', s)
                elif s == 'null':
                        t = Token('NULL_L', None)
                elif s == 'true':
                        t = Token('TRUE_L', True)
                elif s == 'false':
                        t = Token('FALSE_L', False)
                elif s == 'if':
                        t = Token('IF')
                elif s == 'else':
                        t = Token('ELSE')
                elif s == 'while':
                        t = Token('WHILE')
                elif s == 'for':
                        t = Token('FOR')
                elif s == 'new':
                        t = Token('NEW')
                elif s == 'return':
                        t = Token('RETURN')
                elif s == 'class':
                        t = Token('CLASS')
                elif s == 'extends':
                        t = Token('EXTENDS')
                elif s == 'interface':
                        t = Token('INTERFACE')
                elif s == 'implements':
                        t = Token('IMPLEMENTS')
                elif s == 'abstract':
                        t = Token('ABSTRACT')
                elif s == 'final':
                        t = Token('FINAL')
                elif s == 'static':
                        t = Token('STATIC')
                elif s == 'private':
                        t = Token('PRIVATE')
                elif s == 'super':
                        t = Token('SUPER')
#                elif s == 'this':
#                        t = Token('THIS')
                elif s == 'void':
                        t = Token('VOID')
                else:
                        t = Token('ID', s)
                self.rv.append(t)
        
        ########################################################################
        # These have to be grouped together because the regex engine is greedy,
        # and will therefore only ever match == as two assignment signs rather 
        # than an equality operator.  The same will happen for !=. Because of
        # this, the longer option needs to appear first in an alternation so
        # it's attempted to be matched first.
        ########################################################################
        def t_assign_eq_not_op(self, s):
                r'==|!=|=|!'
                if s == '=':
                        t = Token('ASSIGN_OP')
                elif s == '!':
                        t = Token('NOT_OP')
                else:
                        t = Token('EQ_OP', s)
                self.rv.append(t)
        
        def t_or_op(self, s):
                r'\|\|'
                t = Token('OR_OP')
                self.rv.append(t)
        
        def t_and_op(self, s):
                r'&&'
                t = Token('AND_OP')
                self.rv.append(t)
        
        def t_rel_op(self, s):
                r'(<|>)(\s*=)?'
                t = Token('REL_OP', self._convert_rel_op(s))
                self.rv.append(t)
        
        # These must be grouped into one method for the same reasons as outlined
        # for the t_assign_eq_not_op method
        def t_add_op(self, s):
                r'\+\+|--|\+|-'
                if s in ['++', '--']:
                        t = Token('INC_OP', s)
                else:
                        t = Token('ADD_OP', s)
                self.rv.append(t)
     
        def t_mul_op(self, s):
                r'\*|/'
                t = Token('MUL_OP', s)
                self.rv.append(t)
        
        def t_brackets(self, s):
                r'\(|\)|\[|\]|\{|\}|<|>'
                t = Token(s)
                self.rv.append(t)
        
        def t_punct(self, s):
                r',|\.|;'
                t = Token(s)
                self.rv.append(t)