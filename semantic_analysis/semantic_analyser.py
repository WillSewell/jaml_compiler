"""This module allows for type checking to be performed to check the program is
semantically correct.
"""
import os
import subprocess
from parser_.parser_ import Parser
from symbols import ArraySymbol, VarSymbol, LibMethodSymbol
import parser_.tree_nodes as nodes
from environments import TopEnvironment, Environment
from class_interface_method_scanner import ClassInterfaceMethodScanner
from exceptions import (NotInitWarning, NoReturnError, SymbolNotFoundError,
                        MethodSignatureError, DimensionsError,
                        ConstructorError, ClassSignatureError, AssignmentError,
                        VariableNameError, StaticError, ObjectCreationError,
                        FinalError)
from utilities.utilities import (ArrayType, camel_2_underscore, get_full_type,
                                 is_main, get_jvm_type)
from semantic_analysis.symbols import LibFieldSymbol, LibConsSymbol

# TODO: SPLIT LIB CLASSES INTO LIB CLASSES AND INTERFACES!

class TypeChecker(object):
        """This class allows for type checking of a particular program.
        Also tags nodes in the AST with type information if applicable."""

        def __init__(self):
                # Get the possible classes from java.lang and create a top
                # level environment
                lib_classes = self._scan_lib_classes()
                self._t_env = TopEnvironment(lib_classes)
                # Provides a more convenient way of calling these commonly
                # used methods
                self._get_class_s = self._t_env.get_class_s
                self._get_interface_s = self._t_env.get_interface_s
                # Used to make sure there aren't two main methods
                self._seen_main = False
                
        def analyse(self, program):
                """Type check a given program as a string, or a program as a
                text file.
                """
                p = Parser('file')
                asts = p.run_parser(program, self._t_env.lib_classes)
                # Add all global entities (classes and their methods) to the top level
                # environment
                self._scanner = ClassInterfaceMethodScanner(self._t_env)
                self._scanner.scan(asts)
                for ast in asts:
                        env = Environment(None)
                        self._visit(ast, env)
                return asts, self._t_env
        
        def _scan_lib_classes(self):
                """Scan classes which can be used from the java library."""
                root = os.path.dirname(__file__)
                class_list_path = os.path.join(root, 'classlist')
                class_list = open(class_list_path)
        
                java_lang_classes = {}
                class_ = class_list.readline()
                while class_ != '':
                        if ('java/lang' in class_ or 'java/io' in class_ or
                            'java/util' in class_):
                                name = class_[class_.rfind('/') + 1:class_.find('\n')]
                                # Remove trailing \n and add to the dict
                                java_lang_classes[name] = class_[:-1]
                        class_ = class_list.readline()
                return java_lang_classes

        def _visit(self, node, env):
                """Perform a type check on the abstract syntax tree.
                This function 

                """
                method = None
                for class_ in node.__class__.__mro__:
                        method_name = '_visit' + class_.__name__
                        method_name = camel_2_underscore(method_name)
                        method = getattr(self, method_name, None)
                        if method:
                                break
                if not method:
                        # Some nodes do not need to be type checked - for
                        # example, interfaces
                        return
                return method(node, env)

        def _visit_class_node(self, node, env):
                """Check a class declaration node."""
                # Update the current class
                class_s = self._get_class_s(node.children[0].value)
                env.cur_class = class_s
                # Visit extends and implements nodes (if they're there)
                self._visit(node.children[1], env)
                self._visit(node.children[2], env)
                # Read the large comment in the method below for an explanation
                # of this:
                if (isinstance(node.children[3], nodes.EmptyNode) and 
                    self._does_super_have_params(class_s)):
                        msg = ('There must be a constructor which ' +
                               'invokes the super classes constructor!')
                        raise ConstructorError(msg)
                self._seen_main = False
                # Visit the body
                self._visit(node.children[3], env)

        def _visit_class_body_node(self, node, env):
                """If the node has a class body, create a new environment to
                pass to the child nodes and type check the children.
                """
                prev_table = env
                env = Environment(prev_table)
                # Sort the children in this order: fields, constructor, methods
                # This is so that all the fields will be in the symbol table
                # before they are used (and initialised in the constructor)
                sorted_children = sorted(node.children)
                # If the super class has a constructor with arguments, this
                # class must have a constructor that calls the super classes
                # constructor
                # At this stage we just check if the current class has a
                # constructor at all, in the code or constructor nodes, we
                # we check the call to the super constructor is actually made
                # Set to true when the constructor in this class is seen
                seen_cons = False
                # Set to true if the super classes constructor takes parameters
                super_has_params = self._does_super_have_params(env.cur_class)
                for child in sorted_children:
                        if isinstance(child, nodes.ConstructorDclNode):
                                if seen_cons == False:
                                        seen_cons = True
                                else:
                                        # There was more than one constructor,
                                        # so error
                                        msg = 'Only one constructor allowed!'
                                        raise ConstructorError(msg)
                        self._visit(child, env)
                # If we have looked at all the children, without seeing
                # a constructor when we should have done, error
                if super_has_params and not seen_cons:
                        msg = ('There must be a constructor which ' +
                               'invokes the super classes constructor!')
                        raise ConstructorError(msg)
        
        def _does_super_have_params(self, class_s):
                """Returns whether or not the constructor of the super class of
                class_s has parameters.
                """
                has_params = False
                try:
                        super_s = self._get_class_s(class_s.super_class)
                        super_cons = super_s.constructor
                        if super_cons is not None and len(super_cons.params) != 0:
                                has_params = True
                except SymbolNotFoundError:
                        # No explicit super class
                        pass
                return has_params
        
        def _visit_field_dcl_node(self, node, env):
                self._visit(node.children[1], env)
                node.type_ = self._visit(node.children[0], env)
                return node.type_
        
        def _visit_field_dcl_assign_node(self, node, env):
                """Final fields are declared with an assignment to a literal
                value (number or String).
                """ # TODO: ALL THIS CURRENTLY DOESN'T WORK BECAUSE THE CODE GENERATOR NEEDS TO CREATE ASSIGNMENT CODE IN THE CONSTRUCTOR - DO IF I HAVE TIME! OTHERWISE REMOVE.
                # TODO: THERE IS A BUG IN JASMIN WHERE IT CONVERTS DOUBLES TO FLOATS, SO JAVA ERRORS WHEN A DOUBLE VALUE IS ASSIGNED TO IT HERE!
                if ('final' not in node.modifiers and
                    'static' not in node.modifiers):
                        msg = ('Assignment with a field declaration can ' +
                               'only be performed on final and final fields!')
                        raise FinalError(msg)
                self._visit(node.children[1].children[0], env)
                node.type_ = self._visit(node.children[0], env)
                # Check the variable initialisation
                rh_type = self._visit(node.children[1].children[1], env)
                try:
                        self._check_num_types(node.type_, rh_type);
                except TypeError:
                        # It has to be a String
                        if (node.type_ != 'java/lang/String' or 
                            rh_type != 'java/lang/String'):
                                msg = ('Assignment with a field declaration ' +
                                       'must be of a numerical or string type!')
                                raise TypeError(msg)
                return node.type_
        
        def _visit_constructor_dcl_node(self, node, env):
                # Update the current method
                env.cur_method = env.cur_class.constructor
                # Check the name is the same as the class name
                if node.children[0].value != env.cur_class.name:
                        msg = 'Constructor name does not match class name!'
                        raise MethodSignatureError(msg)
                # Check the parameter's types are legitimate
                self._visit(node.children[1], env)
                # If the class extends one which has a constructor which takes
                # arguments, it must be called with the super keywords on the
                # first line of this constructor
                try:
                        super_s = self._get_class_s(env.cur_class.super_class)
                        super_cons = super_s.constructor
                        if super_cons != None and len(super_cons.params) != 0:
                                super_node = None
                                try:
                                        super_node = node.children[2].children[0]
                                except AttributeError:
                                        # The constructor had no body
                                        pass
                                if not isinstance(super_node,
                                                  nodes.SuperConstructorCallNode):
                                        msg = ('The super classes constructor must ' +
                                               'be invoked on the first line!')
                                        raise ConstructorError(msg)
                                # Check the types of the arguments match
                                self._check_method_args(super_cons,
                                                        super_node.children[0],
                                                        env)
                except SymbolNotFoundError:
                        # No explicit super class
                        pass
                # Type check the body
                self._visit(node.children[2], env)

        def _visit_method_dcl_node(self, node, env):
                """For method declarations, check the formal params, as well as
                checking the type matches the method's return type.
                """
                # Update the current method
                name = node.children[0].value
                env.cur_method = env.cur_class.get_method(name)
                # If there are two main methods, error
                if is_main(env.cur_method):
                        if self._seen_main == True:
                                msg = 'There can only be one main method!'
                                raise MethodSignatureError(msg)
                        else:
                                self._seen_main = True
                # Check it doesn't override a final method
                self._check_override(name, env)
                # Check the return type is legitimate (and tag the node's type)
                node.type_ = self._visit(node.children[1], env)
                # Check the parameter's types are legitimate
                self._visit(node.children[2], env)
                # Type check the body
                self._visit(node.children[3], env)
                # Check the method has a return statement
                self._check_method_return(node, env)
                        
        def _visit_method_dcl_array_node(self, node, env):
                """Like above, but the method returns an array."""
                # Update the current method
                name = node.children[0].value
                env.cur_method = env.cur_class.get_method(name)
                # Check it doesn't override a final method
                self._check_override(name, env)
                # Check the return type is legitimate (and tag the node's type)
                type_ = self._visit(node.children[1], env)
                node.type_ = ArrayType(type_, node.children[2].value)
                # Check the parameter's types are legitimate
                self._visit(node.children[3], env)
                # Type check the body
                self._visit(node.children[4], env)
                # Check the method has a return statement
                self._check_method_return(node, env)
        
        def _check_override(self, name, env):
                """Checks if a method overrides one in the super class, if it
                does - check that it's not "final"."""
                try:
                        super_s = self._get_class_s(env.cur_class.super_class)
                        super_method = super_s.get_method(name)
                        if 'final' in super_method.modifiers:
                                msg = ('Method "' + name + '" cannot ' +
                                       'override a final method!')
                                raise MethodSignatureError(msg)
                except (SymbolNotFoundError, AttributeError):
                        # It does not override a method
                        # Or there was no superclass
                        # (that wasn't a library class)
                        pass

        def _visit_param_list_node(self, node, env):
                """The types of the parameters must be checked (in case they
                are of a class type which doesn't exist).
                """
                for param in node.children:
                        self._visit(param, env)
        
        def _visit_param_dcl_node(self, node, env):
                """Tag with the correct type."""
                node.type_ = self._visit(node.children[0], env)
                return node.type_
                
        def _check_method_return(self, node, env):
                """Check a type checked method has a return statement"""
                # Check the method has a return statement if it has a ret type
                if node.children[1].value != 'void':
                        if not env.cur_method.has_ret:
                                msg = ('Method "' + node.children[0].value +
                                       '" has no return!')
                                raise NoReturnError(msg)

        def _visit_block_node(self, node, env):
                """For block, handle the env in the same way as class body."""
                prev_table = env
                env = Environment(prev_table)
                for child in node.children:
                        self._visit(child, env)

        def _visit_var_dcl_node(self, node, env):
                """ If the node is a variable declaration, add the variable to
                the environment.
                """
                var_s = self._gen_var_s(node, env)
                env.put_var_s(var_s)
                # Tag the type
                node._type = var_s.type_
                return var_s.type_
        
        def _visit_var_dcl_assign_node(self, node, env):
                """This is like the above method, but where there is an
                assignment which must also be checked.
                """
                var_s = self._gen_var_s_assign(node, env)
                # Set variable to initialised
                var_s.is_init = True
                env.put_var_s(var_s)
                # Tag the type
                node.type_ = var_s.type_
                # Type check the expression
                self._visit(node.children[1], env)
                return var_s.type_
        
        def _gen_var_s(self, node, env):
                """Helper method to generate a variable symbol from a variable
                declaration statement.  Used by field declarations, local 
                variable declarations, and parameters definitions.
                """
                # Get the explicitly stated type
                type_ = self._visit(node.children[0], env)
                if type_ in self._t_env.lib_classes.keys():
                        type_ = self._t_env.lib_classes[type_]
                name = ''
                var_s = None
                try:
                        # Try and treat it like an array declaration
                        # Get its name and dimensions
                        name = node.children[1].children[0].value
                        dimensions = node.children[1].children[1].value
                        # Set the array _name node's type
                        type_ = ArrayType(type_, dimensions)
                        var_s = ArraySymbol(name, type_, dimensions)
                except AttributeError:
                        # It must be a regular variable declaration
                        name = node.children[1].value
                        var_s = VarSymbol(name, type_)
                # Check the variable does not have the same name as a type,
                # field or parameter
                self._check_var_name(name, env)
                return var_s
        
        def _gen_var_s_assign(self, node, env):
                """Like above, but works for variable declaration with
                assignment nodes.
                """
                # Get the explicitly stated type
                type_ = self._visit(node.children[0], env)
                if type_ in self._t_env.lib_classes.keys():
                        type_ = self._t_env.lib_classes[type_]
                name = ''
                var_s = None
                try:
                        # Try and treat it like an array declaration
                        # Get its name and dimensions
                        array_node = node.children[1].children[0]
                        name = array_node.children[0].value
                        dimensions = array_node.children[1].value
                        # Set the array node's type
                        type_ = ArrayType(type_, dimensions)
                        var_s = ArraySymbol(name, type_, dimensions)
                except AttributeError:
                        # It must be a regular variable declaration
                        name = node.children[1].children[0].value
                        var_s = VarSymbol(name, type_)
                # Check the variable does not have the same name as a type,
                # field or parameter
                self._check_var_name(name, env)
                return var_s
        
        def _check_var_name(self, name, env):
                """Check the local variable does not have the same name as
                a field, a parameter, a type, or another local variable.
                """
                msg = ('Variable "' + name + '" cannot have the ' +
                       'same name as a type, field or parameter!')
                try:
                        env.cur_class.get_field(name)
                        raise VariableNameError(msg)
                except SymbolNotFoundError:
                        # No field had the same name
                        pass
                for param in env.cur_method.params:
                        if name == param.name:
                                raise VariableNameError(msg)
                if name in self._t_env.types:
                        raise VariableNameError(msg)

        def _visit_if_node(self, node, env):
                """
                Type check all child nodes, it is only important that the
                first child returns a boolean.
                """
                if self._visit(node.children[0], env) != 'boolean':
                        msg = ('Type error in if node, first child was not ' +
                               '"boolean"!')
                        raise TypeError(msg)
                self._visit(node.children[1], env)
                if len(node.children) == 3:
                                self._visit(node.children[2], env)

        def _visit_while_node(self, node, env):
                """Check a while statement, similar to if statement."""
                if self._visit(node.children[0], env, ) != 'boolean':
                        msg = ('Type error in while node, first child was ' +
                               'not "boolean"!')
                        raise TypeError(msg)
                self._visit(node.children[1], env)

        def _visit_for_node(self, node, env): #TODO: BUG - THE VARIABLE (i) IS IN THE SCOPE OUTSIDE THE BODY OF THE LOOP - SHOULD BE ON THE INSIDE!
                """Check a for statement, similar to if statement."""
                self._visit(node.children[0], env)
                if self._visit(node.children[1], env) != 'boolean':
                        msg = ('Type error in for node, first child was not ' +
                               '"boolean"!')
                        raise TypeError(msg)
                self._visit(node.children[2], env)
                self._visit(node.children[3], env)

        def _visit_return_node(self, node, env):
                """Checks a return statement.  """
                ret_type =  self._visit(node.children[0], env)
                # Check the return type matches methods signature ret type
                sig_type = env.cur_method.type_
                # The same rules of assignment apply to returning
                self._check_is_assignable(sig_type, ret_type, env)
                # Tag the method as having a return statement
                env.cur_method.has_ret = True
                return ret_type

        def _visit_assign_node(self, node, env): # TODO: CAN'T ASSIGN TO A FIELD IN ANOTHER CLASS (CAN'T INC IT TOO)
                """Make sure both sides are of the same type"""
                # Update the variable to initialised
                name = node.children[0].value
                symbol = None
                if name != '':
                        # It's a regular identifier
                        symbol = self._get_var_s_from_id(name, env, False)
                        symbol.is_init = True
                else:
                        # For array elements
                        name = node.children[0].children[0].value
                        symbol = self._get_var_s_from_id(name, env, False)
                        # Check array has been initialised
                        if symbol.is_init == False:
                                msg = ('Array "' + symbol.name +
                                       '" not initialised!')
                                raise NotInitWarning(msg)
                # Check the variable being assigned to is not final
                self._check_final(symbol)
                # Check the types are compatible
                l_child_type = self._visit(node.children[0], env)
                r_child_type = self._visit(node.children[1], env)
                self._check_is_assignable(l_child_type, r_child_type, env)
                node.type_ = l_child_type
                return l_child_type
        
        def _check_final(self, symbol):
                """Checks if a given variable that is being assigned to is
                not final, if it is - this produces an error."""
                try:
                        if 'final' in symbol.modifiers:
                                msg = ('Cannot assign to final field "' +
                                       symbol.name + '"!')
                                raise AssignmentError(msg)
                except AttributeError:
                        # It's not a field
                        pass

        def _check_is_assignable(self, type1, type2, env):
                """Checks if it's possible to assign type2 to type1."""
                # Check dimensions match, if arrays
                try:
                        dimensions1 = type1.dimensions
                        try:
                                dimensions2 = type2.dimensions
                                if dimensions1 != dimensions2:
                                        msg = ('Number of array dimensions ' +
                                               'incorrect!')
                                        raise DimensionsError(msg)
                                # Set the types to the array's type
                                type1 = type1.type_
                                type2 = type2.type_
                        except AttributeError:
                                msg = ('Type being assigned or returned ' +
                                       'must be an array!')
                                raise TypeError(msg)
                except AttributeError:
                        # Check the other side isn't an array type
                        if isinstance(type2, ArrayType):
                                msg = ('Type being assigned or returned ' +
                                       'cannot be an array!')
                                raise TypeError(msg)
                # First check for numerical types
                if type1 in self._t_env.nums:
                        self._check_num_types(type1, type2)
                elif type1 == 'boolean':
                        if type2 != 'boolean':
                                msg = 'The method must return a boolean!'
                                raise TypeError(msg)
                elif not self._is_equal_types(type1, type2):
                        if not self._is_implemented_by(type1, type2):
                        # If it's not the same class or subclass, or an
                        # instantiation
                                msg = ('Type "' + type2 + '" incompatible ' +
                                       'for assignment or returning.')
                                raise TypeError(msg)

        def _check_num_types(self, type1, type2):
                """
                Check if numerical type2 can be assigned to, or returned in a
                method of type1.
                """
                try:
                        # Numbers that can hold a greater value can have a
                        # type which holds less assigned to them.  Types
                        # with a lower index value in the list of numbers
                        # can be assigned to ones with a higher index.
                        l_child_idx = self._t_env.nums.index(type1)
                        r_child_idx = self._t_env.nums.index(type2)
                        if l_child_idx < r_child_idx and type2 != 'int':
                                raise TypeError('Method must return ' + type2 +
                                                '!')
                # If the right hand side is not in nums
                except ValueError:
                        raise TypeError('The method must return a number!')

        def _is_equal_types(self, lh_type, rh_type):
                """Helper method for _check_is_assignable.  Checks if the right
                hand type is the same type, or a sub type of the left hand type
                (used to check assignment statements) for objects and arrays
                of objects.
                """
                if lh_type == rh_type:
                        return True
                else:
                        rh_class = self._get_class_s(rh_type)
                        if rh_class.super_class != 'java/lang/Object':
                                super_name = rh_class.super_class
                                return self._is_equal_types(lh_type, super_name)
                        else:
                                # No super class
                                return False
        
        def _is_implemented_by(self, lh_type, rh_type):
                """Checks to see whether the rh type implements the lh type or
                one of its super interfaces works in much the same way as the
                above method.
                """
                if lh_type == rh_type:
                        return True
                else:
                        rh_class = self._get_class_s(rh_type)
                        if len(rh_class.interfaces) != 0:
                                for interface in rh_class.interfaces:
                                        return self._is_equal_types(lh_type, 
                                                                    interface)
                        else:
                                # Does not implement an interface
                                return False

        def _visit_cond_node(self, node, env):
                """Check that and expression is applied to boolean types."""
                if self._visit(node.children[0], env) != 'boolean':
                        msg = ('Type error in conditional expression node, ' +
                               'first child was not "boolean"!')
                        raise TypeError(msg)
                if self._visit(node.children[1], env) != 'boolean':
                        msg = ('Type error in conditional expression node, ' +
                               'second child was not "boolean"!')
                        raise TypeError(msg)
                node.type_ = 'boolean'
                return node.type_

        def _visit_eq_node(self, node, env):
                """Check that equality expression is applied to """
                l_child_type = self._visit(node.children[0], env)
                r_child_type = self._visit(node.children[1], env)
                # Check primitives for comparable types
                _is_assignable = self._check_is_assignable
                if l_child_type in self._t_env.nums:
                        if r_child_type not in self._t_env.nums:
                                msg = ('Type error in equality node, second ' +
                                       'child was not a number!')
                                raise TypeError(msg)
                elif l_child_type == 'boolean' and r_child_type != 'boolean':
                        msg = ('Type error in equality node, second child ' +
                               'was not "boolean"!')
                        raise TypeError(msg)
                # For non primitive types (objects arrays) it's about whether
                # the reference is the same, we can't just check the types are
                # the same because the same object reference could be of a base
                # type on one side and a super type on the other.  We must
                # check if one is assignable to the others type and vice versa;
                # if either isn't, there's no way the object references could
                # be equal
                elif _is_assignable(l_child_type, r_child_type, env):
                        if _is_assignable(r_child_type, l_child_type, env):
                                pass
                        else:
                                msg = ('Type error in equality node, object ' +
                                       'types are not comparable!')
                                raise TypeError(msg)
                node.type_ = 'boolean'
                return node.type_

        def _visit_rel_node(self, node, env):
                """
                Check the type of the node with regex because there is a
                number of possibilities.
                """
                nums = self._t_env.nums
                if self._visit(node.children[0], env) not in nums:
                        msg = ('Type error in relational node, left child ' +
                               'is not a number!')
                        raise TypeError(msg)
                if self._visit(node.children[1], env) not in nums:
                        msg = ('Type error in relational node, right child ' +
                               'is not a number!')
                        raise TypeError(msg)
                node.type_ = 'boolean'
                return node.type_

        def _visit_add_node(self, node, env):
                """
                These nodes are similar but require their child nodes to be
                of type int.  + Can also be applied to two strings.
                """
                lh_type = self._visit(node.children[0], env)
                rh_type = self._visit(node.children[1], env)
                # First check for numerical operations
                if lh_type == 'matrix':
                        if rh_type != 'matrix':
                                msg = ('Type error in additive node, right ' +
                                       'child must be a matrix!')
                                raise TypeError(msg)
                        else:
                                node.type_ = 'matrix'
                elif lh_type in self._t_env.nums:
                        if rh_type not in self._t_env.nums:
                                msg = ('Type error in additive node, right ' +
                                       'child is not a number!')
                                raise TypeError(msg)
                        else:
                                get_type = self._num_operator_type
                                node.type_ =  get_type(node.children[0],
                                                       node.children[1])
                # If it's used to concatenate strings, check they match
                elif lh_type == 'java/lang/String':
                        if rh_type != 'java/lang/String':
                                msg = ('Type error in additive node, right ' +
                                       'child is not "String"!')
                                raise TypeError(msg)
                        node.type_ = 'java/lang/String'
                else:
                        msg = ('Type error in + node, type must be String ' +
                               'or a number!')
                        raise TypeError(msg)
                return node.type_

        def _visit_mul_node(self, node, env):
                """Check both sides are numerical."""
                lh_type = self._visit(node.children[0], env)
                rh_type = self._visit(node.children[1], env)
                # Matrix type only allowed for multiplication, not division
                if node.value == '*' and lh_type == 'matrix':
                        if rh_type != 'matrix':
                                msg = ('Type error at *, right child must ' +
                                       'be a matrix!')
                                raise TypeError(msg)
                        else:
                                node.type_ = 'matrix'
                elif (lh_type not in self._t_env.nums or 
                      rh_type not in self._t_env.nums):
                        msg = ('Type error in multiplicative node - both ' +
                               'children must be numbers are matrices!')
                        raise TypeError(msg)
                else:
                        # Tag the correct type
                        node.type_ = self._num_operator_type(node.children[0],
                                                        node.children[1])
                return node.type_

        def _num_operator_type(self, l_child, r_child):
                """
                Helper method for _visit_add _visit_mul.  Get the type of the
                numerical operator for given child nodes.
                """
                # Work out each numbers index in the list of numbers, lower
                # index numbers can be assigned to ones of a higher index
                lh_idx = self._t_env.nums.index(l_child.type_)
                rh_idx = self._t_env.nums.index(r_child.type_)
                
                if l_child.type_ == r_child.type_:
                        # If they are the same, return type of either children
                        return l_child.type_
                elif  lh_idx > rh_idx:
                        # Otherwise, return the type of whatever is higher up
                        # in the list of possible numerical types
                        return l_child.type_
                else:
                        return r_child.type_

        def _visit_not_node(self, node, env):
                """Check the type is boolean."""
                if self._visit(node.children[0], env) != 'boolean':
                        msg = 'Type error in not node, child is not "boolean"!'
                        raise TypeError(msg)
                node.type_ = 'boolean'
                return 'boolean'

        def _visit_pos_node(self, node, env):
                """Check the type is numerical."""
                nums = self._t_env.nums
                if self._visit(node.children[0], env) not in nums:
                        msg = 'Type error in pos node, child is not "int"!'
                        raise TypeError(msg)
                # Tag the type
                node.type_ =  node.children[0].type_
                return node.type_

        def _visit_inc_node(self, node, env):
                """Check the type is numerical."""
                nums = self._t_env.nums
                if self._visit(node.children[0], env) not in nums:
                        msg = 'Type error in inc node, child is not a number!'
                        raise TypeError(msg)
                # Check the variable being assigned to is not final
                try:
                        field_name = node.children[0].value
                        is_static = False
                        if 'static' in env.cur_method.modifiers:
                                is_static = True
                        symbol = self._find_field(env.cur_class.name,
                                                  field_name, is_static, env)
                        self._check_final(symbol)
                except SymbolNotFoundError:
                        # It was not a field
                        pass
                # Tag the type
                node.type_ =  node.children[0].type_
                return node.type_

        def _visit_array_dcl_node(self, node, env):
                """Simply return the array's type."""
                symbol = self._get_var_s_from_id(node.children[0].value, env,
                                                 False)
                node.type_ = symbol.type_
                # Set children's types
                for child in node.children:
                        child.type_ = node.type_.type_
                return node.type_

        def _visit_array_element_node(self, node, env):
                """Check the array has been declared, and the number of
                dimensions match.
                """
                # First check it has been declared by looking it up in
                # env (also getting its type)
                symbol = self._get_var_s_from_id(node.children[0].value, env,
                                                 True)
                # Check the dimensions are equal to the dimensions
                # stored in env
                if symbol.dimensions != len(node.children) - 1:
                        msg = ('Array "' + node.children[0].value +
                               '" does not have ' +
                               str(len(node.children) - 1) + ' dimensions!')
                        raise TypeError(msg)
                # Return the type part of the list use to represent the
                # type of the whole array because this is a reference to
                # an instance of an array
                node.type_ = symbol.type_.type_
                # Set children's types
                node.children[0].type_ = symbol.type_
                for child in node.children[1:]:
                        idx_type = self._visit(child, env)
                        if idx_type != 'int':
                                msg = ('The indices into arrays must be of ' +
                                       'an integer type!')
                                raise TypeError(msg)
                return node.type_
        
        def _visit_matrix_element_node(self, node, env):
                """Check the matrix has been declared, and the number of
                dimensions match.
                """
                # First check it has been declared by looking it up in
                # env (also getting its type)
                self._get_var_s_from_id(node.children[0].value, env, True)
                # The type is double since each cell stores a double number
                node.type_ = 'double'
                # Check index types are int
                for child in node.children[1:]:
                        idx_type = self._visit(child, env)
                        if idx_type != 'int':
                                msg = ('The indices into arrays must be of ' +
                                       'an integer type!')
                                raise TypeError(msg)
                return node.type_

        def _visit_method_call_node(self, node, env):
                """Check the method exists, the types are the same, and the
                argument's match the method's signature.
                """
                # Look up the method in this class, or a super class
                node.type_ = self._find_method(env.cur_class.name, node,
                                               False, env)
                return node.type_

        def _visit_method_call_long_node(self, node, env):
                """Works in much the same way has the above method, but this
                must look up methods in other classes.
                """
                # First get the name of the class (the type) in order to get the
                # correct class symbol
                class_name = ''
                is_static = False
                id_node = node.children[0]
                if id_node.value in self._t_env.types:
                        # It's an invocation of a static method
                        class_name = id_node.value
                        # Get the full class name (for lib classes)
                        class_name = get_full_type(class_name, self._t_env)
                        is_static = True
                else:
                        # It's an instance method
                        self._visit(id_node, env)
                        var_s = self._get_var_s_from_id(id_node.value, env,
                                                        True)
                        class_name = var_s.type_
                # Look up the method in this class, or a super class,
                # and tag the node's type
                node.type_ = self._find_method(class_name, node, is_static, env)
                return node.type_
        
        def _visit_method_call_super_node(self, node, env):
                """Uses the _find_method method to search for the method in the
                super classes.
                """
                super_ = env.cur_class.super_class
                node.type_ = self._find_method(super_, node, False, env)
                return node.type_
        
        def _find_method(self, class_, node, is_static, env):
                """Recursively search for a given method in the full inheritance
                tree for a particular class.  Returns the methods return type.
                """
                #TODO: Could be changed to return a symbol if it is done in the same way for fields - Not sure if needed
                class_s = None
                try:
                        class_s = self._get_class_s(class_)
                except SymbolNotFoundError:
                        try:
                                # See if it's an interface (can't be static)
                                if not is_static:
                                        class_s = self._get_interface_s(class_)
                                else:
                                        raise SymbolNotFoundError
                        except SymbolNotFoundError:
                                # The super class must be a Java library class
                                return self._check_lib_method(class_, node, env)
                try:
                        # Try and find the method in the class provided
                        # If the class is the current class, private
                        # methods can also be looked up
                        method_s = None
                        # Name is stored in 2nd or 3rd child depending on if
                        # the method is in the current class or external
                        method = node.children[0].value
                        if len(node.children) == 3:
                                method = node.children[1].value
                        try:
                                if class_ == env.cur_class.name:
                                        method_s = class_s.get_method(method)
                                else:
                                        method_s = class_s.get_public_method(method)
                        except AttributeError:
                                # For interfaces
                                method_s = class_s.get_method(method)
                        # Check static
                        self._check_static(method_s, is_static)
                        # Check the arguments
                        try:
                                self._check_method_args(method_s,
                                                        node.children[2], env)
                        except IndexError:
                                # It's a method in the same class (so params
                                # are second child
                                self._check_method_args(method_s,
                                                        node.children[1], env)
                        return method_s.type_
                except SymbolNotFoundError:
                        try:
                                # See if it is in a super class
                                return self._find_method(class_s.super_class,
                                                         node, is_static, env)
                        except AttributeError:
                                # Or super interface
                                super_ = class_s.super_interface
                                return self._find_method(super_, node,
                                                         is_static, env)
        
        def _check_static(self, symbol, is_static):
                """For a given method or field, this throws an error if it is
                not static when it should have been, and vice versa.
                """
                if is_static and 'static' not in symbol.modifiers:
                        msg = ('Cannot access non static method/field in a ' +
                               'static way!')
                        raise StaticError(msg)
                elif not is_static and 'static' in symbol.modifiers:
                        msg = 'Method/field must be referenced in a static way!'
                        raise StaticError(msg)

        def _check_method_args(self, method_s, args_list, env):
                """Helper method for _visit_method_call.  Checks the number and
                types of the arguments match.
                """
                try:
                        # If the method call has arguments
                        self._check_method_args_types(method_s,
                                                      args_list, env)
                except AttributeError:
                        # The method was called with no arguments
                        if len(method_s.params) > 0:
                                # The method should have been called with args
                                msg = (method_s.name + ' has ' +
                                       str(len(method_s.params)) +
                                       ' parameters!')
                                raise MethodSignatureError(msg)

        def _check_method_args_types(self, method_s, args_list, env):
                """Helper method for _check_method_args.  Checks the types of
                the arguments in a method call match the method's signature.
                """
                # Get the parameters from the method's signature
                if len(method_s.params) != len(args_list.children):
                        msg = (method_s.name + ' has ' + str(len(method_s.params)) +
                               ' parameters!')
                        raise MethodSignatureError(msg)
                for idx, param in enumerate(method_s.params):
                        arg_type = self._visit(args_list.children[idx],
                                                   env)
                        # Check types are compatible
                        self._check_is_assignable(param.type_, arg_type, env)
        
        def _check_lib_method(self, class_, node, env):
                """Uses the library class checker to check the method exists
                with the argument types provided.
                """
                # The / delimiters must be converted to .s for the Java program
                dotted_name = class_.replace('/', '.')
                arg_types = self._get_arg_types(node, env)
                dotted_arg_types = []
                for type_ in arg_types:
                        dotted_arg_types.append(type_.replace('/', '.'))
                # Super method calls and others have the name in diff locations
                method_name = node.children[0].value
                if len(node.children) == 3:
                        method_name = node.children[1].value
                check = self._run_lib_checker
                # TODO: CURRENT LIBARY METHODS CAN ONLY BE CALLED WIH THE SAME TYPE ARGUMENTS - SUB-TYPES WON'T WORK
                ret_type, parent_class, is_static = check(['-method',
                                                           dotted_name,
                                                           method_name] +
                                                          dotted_arg_types)
                if ret_type[0] == '[':
                        # It's an array, so must be converted to the array class
                        convert = self._convert_jvm_array_type_to_class
                        ret_type = convert(ret_type)
                # Create a symbol and add it to the t_env for the code
                # generator to use later
                symbol = LibMethodSymbol(method_name, ret_type, arg_types,
                                         class_, parent_class, is_static)
                if is_static:
                        symbol.modifiers = ['static']
                else:
                        symbol.modifiers = []
                self._t_env.add_lib_method(symbol)
                return ret_type
        
        def _get_arg_types(self, node, env):
                """Used by _check_lib_method and _check_lib_cons to get a list
                of the argument's types from the root node.
                """
                # Build list of argument types
                arg_types = []
                args = None
                try:
                        try:
                                # Tag the arguments with types
                                self._visit(node.children[2], env)
                                args = node.children[2].children
                        except IndexError:
                                # Simple method call, so args are second child
                                self._visit(node.children[1], env)
                                args = node.children[1].children
                        for arg in args:
                                type_ = arg.type_
                                try:
                                        # Array types need to be converted to
                                        # JVM type representation
                                        type_.type_
                                        get_jvm_type(type_)
                                except AttributeError: pass
                                arg_types.append(type_)
                except AttributeError:
                        # No arguments
                        pass
                return arg_types

        def _visit_object_creator_node(self, node, env):
                """Check the parameters match the constructor."""
                # Check the args match the constructor parameters
                try:
                        class_s = self._get_class_s(node.children[0].value)
                        if 'abstract' in class_s.modifiers:
                                msg = ('Abstract class "' + class_s.name +
                                       '" cannot be instantiated!')
                                raise ObjectCreationError(msg)
                        cons_s = class_s.constructor
                        try:
                                self._check_method_args(cons_s, node.children[1], env)
                        except IndexError:
                                # No arguments
                                pass
                except SymbolNotFoundError:
                        # Check if it's a library class
                        self._check_lib_cons(node, env)
                node.type_ = get_full_type(node.children[0].value, self._t_env)
                return node.type_
        
        def _check_lib_cons(self, node, env):
                """Uses the library class checker to check the constructor
                arguments are correct.
                """
                class_ = node.children[0].value
                full_class_name = get_full_type(class_, self.t_env)
                dotted_name = full_class_name.replace('/', '.')
                arg_types = self._get_arg_types(node, env)
                for idx, type_ in enumerate(arg_types):
                        arg_types[idx] = type_.replace('/', '.')
                self._run_lib_checker(['-cons', dotted_name] + arg_types)
                # Generate a symbol for it and at it to _t_env
                symbol = LibConsSymbol(class_, arg_types)
                self._t_env.add_lib_cons(symbol)
                # TODO: ADD A WAY TO CHECK ABSTRACT?  IN THE SAME WAY AS STATIC IS CHECKED FOR METHODS.
        
        def _visit_args_list_node(self, node, env):
                """Tag the type of each argument."""
                for arg in node.children:
                        self._visit(arg, env)
        
        def _visit_field_ref_node(self, node, env):
                """Check the field exists in the class, and tag and return the
                type.
                """
                # First get the name of the class in order to get the
                # correct class symbol that the field belongs to
                class_name = ''
                is_static = False
                id_node = node.children[0]
                if id_node.value in self._t_env.types:
                        # It's a static field
                        class_name = id_node.value
                        is_static = True
                else:
                        # It's an instance method
                        self._visit(id_node, env)
                        var_s = self._get_var_s_from_id(id_node.value, env,
                                                        True)
                        class_name = var_s.type_
                field_name = node.children[1].value
                # If it's an array or matrix type, make sure the field is
                # length
                if isinstance(class_name, ArrayType):
                        if field_name in 'length':
                                msg = ('Arrays have no fields other than ' +
                                       'length!')
                                raise SymbolNotFoundError(msg)
                        else:
                                node.type_ = 'int'
                elif class_name == 'matrix':
                        if field_name not in ['rowLength', 'colLength']:
                                msg = ('Matrices have no fields other than ' +
                                       'rowLength and colLength!')
                                raise SymbolNotFoundError(msg)
                        else:
                                node.type_ = 'int'
                else:
                        # Regular field reference
                        # Look up the method in this class, or a super class
                        field_s = self._find_field(class_name, field_name,
                                                   is_static, env)
                        node.type_ = field_s.type_
                return node.type_
        
        def _visit_field_ref_super_node(self, node, env):
                # Get the type (the class) of the super class
                super_ = env.cur_class.super_class
                field_name = node.children[1].value
                # Look up the method in this class, or a super class
                field_s = self._find_field(super_, field_name, env)
                # Add type info
                try:
                        node.type_ = field_s.type_
                except AttributeError:
                        # It was a library class
                        pass
                return node.type_

        def _visit_array_init_node(self, node, env):
                """Check the indices and return the type."""
                type_ = self._visit(node.children[0], env)
                dimensions = len(node.children) - 1
                node.type_ =  ArrayType(type_, dimensions)
                # Set the types of the children
                node.children[0].type_ = node.type_
                for child in node.children[1:]:
                        size_type = self._visit(child, env)
                        if size_type != 'int':
                                msg = ('The sizes of array dimensions must ' +
                                       'be specified by an integer!')
                                raise TypeError(msg)
                return node.type_
        
        def _visit_matrix_init_node(self, node, env):
                """Check the indices and return the type."""
                for child in node.children:
                        size_type = self._visit(child, env)
                        if size_type != 'int':
                                msg = ('The sizes of matrix dimensions must ' +
                                       'be specified by an integer!')
                                raise TypeError(msg)
                node.type_ = 'matrix'
                return node.type_
        
        def _visit_extends_node(self, node, env):
                """Check code for an extends node - the class or interface that
                is extended from must exist.
                """
                # Check that the super class exists
                node.type_ = get_full_type(node.value, self._t_env)
                # Check it does not extend a final class
                try:
                        if env.cur_class != None:
                                # Don't check for interfaces
                                super_s = self._get_class_s(node.value)
                                if 'final' in super_s.modifiers:
                                        msg = ('You cannot subclass a final ' +
                                               'class!')
                                        raise ClassSignatureError(msg)
                except SymbolNotFoundError:
                        # It was in a library class
                        msg = 'Subclassing library classes is unsupported!'
                        raise ClassSignatureError(msg)
        
        def _visit_implements_list_node(self, node, env):
                """Check each interface that is implemented exists."""
                for interface in node.children:
                        # Check that the interface exists
                        interface.type_ = get_full_type(interface.value,
                                                        self._t_env)
                        # It can't be a library class, this has already been
                        # Checked in class_interface_method_scanner
                        
        def _visit_id_node(self, node, env):
                """If it's an identifier the type needs to be looked up in env.
                This will also look check if it is a reference to a parameter
                by looking up the method symbol.
                """
                var_s = self._get_var_s_from_id(node.value, env, True)
                node.type_ = var_s.type_
                return var_s.type_
        
        def _get_var_s_from_id(self, name, env, check_init):
                """Get's a variable, parameter or field symbol, given its name.
                Gives an error if the variable/field has not been initialised,
                and check_init is true.
                """
                symbol = None
                try:
                        # Raise a warning if it has not been initialised
                        if check_init and env.get_var_s(name).is_init == False:
                                msg = ('Variable "' + name +
                                       '" used without being initialised!')
                                raise NotInitWarning(msg)
                        symbol = env.get_var_s(name)
                except SymbolNotFoundError:
                        # See if it's a field of the class
                        is_static = False
                        try:
                                if 'static' in env.cur_method.modifiers:
                                        # Static methods cannot access non
                                        # static fields
                                        is_static = True
                        except AttributeError:
                                # Not in a method
                                pass
                        try:
                                try:
                                        # Initially attempt to retrieve the
                                        # Symbol in case it's a static variable
                                        # declaration - _find_field won't
                                        # work if it is
                                        symbol = env.cur_class.get_field(name)
                                        if 'static' in symbol.modifiers:
                                                is_static = True
                                except SymbolNotFoundError: pass
                                cname = env.cur_class.name
                                symbol = self._find_field(cname, name,
                                                          is_static, env)
                        except SymbolNotFoundError:
                                # See if it's a parameter of the current method
                                # First search for the method symbol
                                params = env.cur_method._get_params()
                                # If there are no parameters, it is neither a
                                # var nor a parameter, so error
                                if len(params) == 0:
                                        msg = ('Variable "' + name +
                                               '" undeclared in current scope!')
                                        raise SymbolNotFoundError(msg)
                                # Search through the parameters for one with
                                # the matching name
                                found = False
                                for param in params:
                                        if name == param.name:
                                                found = True
                                                symbol = param
                                if not found:
                                        # If it's not a parameter
                                        msg = ('Variable "' + name +
                                               '" undeclared in current scope!')
                                        raise SymbolNotFoundError(msg)
                return symbol
        
        def _find_field(self, class_, field, is_static, env):
                """Recursively search for a given field in the full inheritance
                tree for a particular class.  Returns the field's type.
                """
                class_s = None
                try:
                        class_s = self._get_class_s(class_)
                except SymbolNotFoundError:
                        # The super class must be a Java library class
                        type_ = self._check_lib_field(class_, field, env)
                        field_s = VarSymbol(field, type_)
                        field_s.is_init = True
                        return field_s
                try:
                        field_s = None
                        if class_s.name == env.cur_class.name:
                                field_s = class_s.get_field(field)
                        else:
                                field_s = class_s.get_public_field(field)
                        self._check_static(field_s, is_static)
                        return field_s
                except SymbolNotFoundError:
                        # See if it is in a super class
                        return self._find_field(class_s.super_class, field,
                                                is_static, env)
        
        def _check_lib_field(self, class_, field, env):
                """Uses the library class checker to check the field exists."""
                full_class_name = get_full_type(class_, self._t_env)
                dotted_name = full_class_name.replace('/', '.')
                check = self._run_lib_checker
                type_, containing_class, is_static = check(['-field',
                                                            dotted_name, field])
                if type_[0] == '[':
                        # It's an array, so must be converted to the array class
                        convert = self._convert_jvm_array_type_to_class
                        type_ = convert(type_)
                # Create a symbol for use by the code generator
                symbol = LibFieldSymbol(field, type_, class_, containing_class,
                                        is_static)
                if is_static:
                        symbol.modifiers = ['static']
                else:
                        symbol.modifiers = []
                self._t_env.add_lib_field(symbol)
                return type_
                        

        def _visit_literal_node(self, node, env):
                """Returns the literal's type."""
                # Convert the node class name into a string description of the
                # type of the node
                node_name = node.__class__.__name__
                type_upper = node_name.split('L', 1)[0]
                if node_name == 'LongLNode':
                        # Splitting at the L will not work for longs
                        type_upper = 'Long'
                type_ = type_upper.lower()
                if type_ == 'string':
                        # String's need full type
                        type_ = 'java/lang/String'
                node.type_ = type_
                return type_

        def _visit_boolean_literal_node(self, node, env):
                """Returns the literal's type."""
                node.type_ = 'boolean'
                return node.type_

        def _visit_return_void_node(self, node, env):
                """Check the method returns void that this belongs to."""
                if env.cur_method.type_ != 'void':
                        raise TypeError('Method must return "void"!')
                return 'void'
        
        def _visit_empty_node(self, node, env):
                """Simply return."""
                return

        def _visit_type_node(self, node, env):
                """Simply return the value."""
                return node.value
        
        def _visit_class_type_node(self, node, env):
                """Checks that the type is valid."""
                return get_full_type(node.value, self._t_env)

        #######################################################################
        ## Interface checks
        #######################################################################
        
        def _visit_interface_node(self, node, env):
                """Check an interface declaration node."""
                # Update the current interface
                interface = node.children[0].value
                interface_s = self._t_env.get_interface_s(interface)
                env.cur_interface = interface_s
                # Check what it extends, if any
                self._visit(node.children[1], env)
                # Visit the body to check method return types and param types
                self._visit(node.children[2], env)
        
        def _visit_interface_body_node(self, node, env):
                """Simply check each method definition."""
                for child in node.children:
                        self._visit(child, env)
        
        def _visit_abs_method_dcl_node(self, node, env):
                """Check return type and parameter's types."""
                if env.cur_class != None:
                        # It's an abstract method of a class, so the class
                        # must be abstract
                        class_s = env.cur_class
                        if 'abstract' not in class_s.modifiers:
                                msg = ('Class "' + class_s.name + '" must ' +
                                       'declared abstract because it ' +
                                       'contains an abstract method!')
                                raise ClassSignatureError(msg)
                # Check the return type is legitimate
                self._visit(node.children[1], env)
                # Check the parameter's types are legitimate
                self._visit(node.children[2], env)
        
        def _visit_abs_method_dcl_array_node(self, node, env):
                """Check return type and parameter's types."""
                # Check the return type is legitimate
                self._visit(node.children[1], env)
                # Check the parameter's types are legitimate
                self._visit(node.children[3], env)
                
        def _run_lib_checker(self, args):
                """Run the library class type checker program with the
                specified arguments.
                """
                file_dir = os.path.dirname(__file__)
                checker_dir = os.path.join(file_dir, 'lib_checker')
                cmd = (['java', '-cp', checker_dir, 'LibChecker'] + 
                       args)
                process = subprocess.Popen(cmd, stdout = subprocess.PIPE)
                output = process.communicate()[0]
                output = output.rstrip(os.linesep)
                # Check for an error
                if output[0] == 'E':
                        # Remove leading "E - " from the output
                        raise SymbolNotFoundError(output[4:])
                else:
                        # Return output where packages are delimited by /
                        output = output.replace('.', '/')
                        if args[0] in ['-method', '-field']:
                                # The checker prints both the type, and the
                                # containing class for methods and fields -
                                # these need to be extracted here
                                split = output.split('|')
                                # Convert string representation of whether or
                                # not it's static to Python boolean type
                                if split[2] == 'true':
                                        return split[0], split[1], True
                                else:
                                        return split[0], split[1], False
                        else:
                                return output
        
        def _convert_jvm_array_type_to_class(self, jvm_type):
                """Converts a JVM style array type (returned from checking
                java library classes) into the array type representation used
                in this program.
                """
                # Check number of dimensions - denoted by [s
                num_d = 0
                while jvm_type[0] != '[':
                        jvm_type = jvm_type[1:]
                        num_d += 1
                type_ = ''
                if jvm_type == 'Z':
                        type_ = 'boolean'
                elif jvm_type == 'B':
                        type_ = 'byte'
                elif jvm_type == 'C':
                        type_ = 'char'
                elif jvm_type == 'D':
                        type_ = 'double'
                elif jvm_type == 'F':
                        type_ = 'float'
                elif jvm_type == 'I':
                        type_ = 'int'
                elif jvm_type == 'J':
                        type_ = 'long'
                elif jvm_type == 'S':
                        type_ = 'short'
                else:
                        # It's a class type
                        # Remove the leading L and trailing ;
                        type_ = jvm_type[1:-1]
                return ArrayType(type_, num_d)