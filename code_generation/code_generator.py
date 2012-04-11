"""This module generates Jasmin assembly code from a type checked abstract
syntax tree."""
import os
import subprocess
from semantic_analysis.semantic_analyser import TypeChecker
import parser_.tree_nodes as nodes
from utilities.utilities import (camel_2_underscore, is_main, get_jvm_type,
                                 ArrayType, get_full_type)
from semantic_analysis.exceptions import SymbolNotFoundError

class FileReadError(Exception):
        """Raised when a reference to a variable is made when it has not been
        initialised.
        """
        pass

class Frame(object):
        """Used to store information regarding a method's current frame - i.e.
        local variables."""
        def __init__(self, params, is_static, ret_type):
                """Initialise the frame once visiting a new method node.
                Static methods operate differently, because the first element
                on the static is not a reference to "this".
                """
                # This stores all seen variables as keys, along with a
                # reference to their storage location
                self._var = dict()
                # Stores the method's return type
                self._ret_type = ret_type
                # This holds the reference to next free storage location for a 
                # variable
                # Start at 1, because 0 is a reference to "this" 
                # (in non static methods)
                if is_static:
                        self._next_var = 0
                else:
                        self._next_var = 1
                try:
                        for param in params.children:
                                type_node = param.children[0]
                                id_node = param.children[1]
                                name = id_node.value
                                try:
                                        # For arrays
                                        name = id_node.children[0].value
                                except AttributeError: pass
                                if type_node.value in ['long', 'double']:
                                        self.new_var(name, True)
                                else:
                                        self.new_var(name, False)
                except AttributeError:
                        # There are no parameters
                        pass

        def get_var(self, var):
                """For a given variable name, gets the location in the array of
                local variables."""
                return self._var[var]
        
        def new_var(self, var, is_long = False):
                """Creates a storage location for a new variable.  is_long is
                True for longs and doubles because they take up two storage
                locations.
                """
                self._var[var] = self._next_var
                if is_long:
                        self._next_var += 2
                else:
                        self._next_var += 1
        
        def new_matrix(self, var, d1, d2):
                """Creates a new matrix local variable."""
                self._var[var] = self._next_var
                # Work out number of elements and multiply by two because the
                # matrix elements have values of type double
                self._next_var = self._next_var + d1 * d2 * 2
        
        def _get_ret_type(self):
                return self._ret_type
        
        ret_type = property(_get_ret_type)

class CodeGenerator(object):
        """This class contains all the methods and fields to do the code
        generation.
        """
        def __init__(self):
                # Labels used in if, while, for and comparison statements need
                # to be unique for that statement, appending the value stored
                # here to the end makes it unique if it is incremented after
                # each new statement of that type has been visited
                # Should be accessed with _label_suffix
                self._next_labels = {'if': 0, 'while': 0, 'for': 0, 'comp': 0,
                                     'not': 0, 'mat_rows': 0, 'mat_a_cols': 0,
                                     'mat_b_cols': 0, 'auxiliary': 0}
                # This stores all the instructions which will be written to the
                # output file
                self._out = ''
                # The current frame keeps track of local variable locations for
                # a given method
                self._cur_frame = None
                # Stores the name of the current class
                self._cur_class = ''
                # Stores method signatures for simple retrieval when the method
                # is called.  Elements are indexed with a (class, method) tuple
                self._method_sigs = dict()
                # Stores field sigs
                self._field_sigs = dict()

        def compile_(self, source, dst = None):
                """This is the public method which takes the source file or
                string, and generates the assembly code file.
                """
                # Generate the type checked abstract syntax tree
                asts, t_env = TypeChecker().analyse(source)
                self._gen_field_method_sigs(t_env)
                self._t_env = t_env
                # Get paths to directories needed
                code_gen_root = os.path.dirname(__file__)
                project_root = os.path.dirname(code_gen_root)
                if dst is None:
                        asm_root = os.path.join(project_root, 'jaml_files',
                                                'asm')
                        bin_root = os.path.join(project_root, 'jaml_files',
                                                'bin')
                else:
                        asm_root = dst
                        bin_root = dst
                # If it's a file, check it has the correct extension
                try:
                        # This will error if it isn't a file
                        open(source) 
                        if source.find('.jml') == -1:
                                msg = ('Source file does not have the ' +
                                       'correct extension (.jml).')
                                raise FileReadError(msg)
                except:
                        pass
                # Loop through each class generating code and writing files
                for ast in asts:
                        # Generate code
                        self._reset()
                        self._visit(ast)
                        # Write/print results
                        # Get the file name by appending .j to class name
                        name = ast.children[0].value
                        output_f_name = name + '.j'
                        out_path = os.path.join(asm_root, output_f_name)
                        # Create the output file and write output to it
                        out_file = open(out_path, 'w')
                        out_file.write(self._out)
                        out_file.close()
                        # Run Jasmin
                        jasmin_file = os.path.join(project_root, 'jasmin',
                                                   'jasmin.jar')
                        subprocess.call(['java', '-jar', jasmin_file, '-d',
                                        bin_root, out_path])
                self._reset()
        
        def _gen_field_method_sigs(self, t_env):
                """Generate assembly style method signatures for all methods
                and fields using the information held in the top environment
                from the semantic analyser.
                """
                for class_s in (t_env.classes.values() +
                                t_env.interfaces.values()):
                        self._gen_method_sigs(class_s, t_env)
                        try:
                                self._gen_cons_sig(class_s, t_env)
                                self._gen_field_sigs(class_s, t_env)
                        except:
                                # Not in interfaces
                                pass
        
        def _gen_cons_sig(self, class_s, t_env):
                """Generate the signature for the constructor."""
                try:
                        cons = class_s.constructor
                        signature = class_s.name + '/'
                        if cons is not None and len(cons.params) > 0:
                                signature += '<init>'
                                signature += self._gen_method_descriptor(cons,
                                                                         True)
                        else:
                                # No explicit constructor
                                signature += '<init>()V'
                        # Store the constructor's signature
                        self._method_sigs[(class_s.name, '<init>')] = signature
                except AttributeError:
                        # It was an interface (no constructor)
                        pass
        
        def _gen_field_sigs(self, class_s, t_env):
                """Generate field signatures for a class."""
                for field in class_s.fields:
                        name = field.name
                        signature = (class_s.name + '/' + name + ' ' +
                                     get_jvm_type(field))
                        # Store the signature
                        self._field_sigs[(class_s.name, name)] = signature
        
        def _gen_method_sigs(self, class_s, t_env):
                """Generate method and a constructor signatures for a class."""
                for method in class_s.methods:
                        name = method.name
                        signature = class_s.name + '/'
                        # Check for the main method
                        if is_main(method):
                                signature += 'main([Ljava/lang/String;)V'
                        else:
                                signature += name
                                signature += self._gen_method_descriptor(method,
                                                                         False)
                        # Store the signature
                        self._method_sigs[(class_s.name, name)] = signature
        
        def _gen_method_descriptor(self, method_s, is_cons):
                """This method returns a jasmin style string which 
                represents the parameter types and return types for a method.
                """
                ret_type = ''
                if is_cons:
                        ret_type = 'V'
                else:
                        ret_type = get_jvm_type(method_s)
                method_spec = ''
                if len(method_s.params) == 0:
                        # If there are no parameters
                        method_spec = '()' + ret_type
                else:
                        # It has params, so add them to the method_spec
                        method_spec = '('
                        for param in method_s.params:
                                method_spec += get_jvm_type(param)
                        method_spec += ')' + ret_type
                return method_spec
        
        def _reset(self):
                """Reset the fields to their default values for further
                compilation.
                """
                for key in self._next_labels.iterkeys():
                        self._next_labels[key] = 0
                self._out = ''
                self._cur_frame = None

        #######################################################################
        ## Visitor methods
        #######################################################################
        # NOTE: explanations of the asm instructions can be found in the
        # string of the comment, behind the ; character
        # First check if it's an interior node so the child nodes can be
        # extracted
        
        def _visit(self, node):
                """Perform a type check on the abstract syntax tree.
                This function 
                """
                #print '---'
                #print node.node_id
                #print '---'
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
                return method(node)
        
        def _visit_class_node(self, node):
                children = node.children
                # Set the current class
                self._cur_class = children[0].value
                # Generate the class signature
                class_sig = '.class '
                for modifier in node.modifiers:
                        class_sig += modifier + ' '
                class_sig += children[0].value
                self._add_ln(class_sig)
                # Generate extends/implements code
                if children[1].value != '':
                        # It extends another class
                        self._add_ln('.super ' + children[1].value) 
                else:
                        # There was no explicitly stated superclass
                        self._add_ln('.super java/lang/Object')
                try:
                        for interface in children[2].children:
                                self._add_ln('.implements ' + 
                                             interface.value)
                except AttributeError:
                        # It does not implement an interface
                        pass
                self._visit(children[3])
        
        def _visit_class_body_node(self, node):
                prev_child = None
                added_cons = False
                for child in sorted(node.children):
                        if (not added_cons and 
                            not isinstance(prev_child, nodes.ConstructorDclNode)
                            and (isinstance(child, nodes.MethodDclNode) or 
                            isinstance(child, nodes.MethodDclArrayNode))):
                                # If a method comes straight after a field
                                # declaration, there is no constructor, so
                                # generate a default one
                                self._gen_default_constructor()
                                added_cons = True
                        if isinstance(child, nodes.ConstructorDclNode):
                                added_cons = True
                        self._visit(child)
                        prev_child = child
                if added_cons == False:
                        # If there is still no constructor, it means there is
                        # only field definitions, so generate a default one
                        self._gen_default_constructor()
        
        def _gen_default_constructor(self):
                """Generate a default constructor for when the class does not
                contain an explicit one.
                """
                # Write the signature
                self._add_ln('.method <init>()V')
                self._add_iln('.limit stack 10')
                self._add_iln('.limit locals 100')
                # Call the super constructor
                self._gen_super_constructor()
                # Generate code for the method body
                self._add_iln('return')
                self._add_ln('.end method')
        
        def _gen_super_constructor(self):
                """Generates the code to invoke a call to the super class'
                constructor.
                """
                self._add_iln('aload_0', ';Load the current object')
                super_ = self._t_env.get_class_s(self._cur_class).super_class
                self._add_iln('invokespecial ' + super_ + '/<init>()V')
        
        def _visit_field_dcl_node(self, node):
                id_node = node.children[1]
                try:
                        # Try for array fields
                        id_node = node.children[1].children[0]
                except AttributeError: pass
                name = id_node.value
                type_ = get_jvm_type(node.children[1])
                # Generate the signature
                field_sig = '.field '
                for modifier in node.modifiers:
                        field_sig += modifier + ' '
                field_sig += name + ' ' + type_
                self._add_ln(field_sig)
        
        def _visit_field_dcl_assign_node(self, node):
                id_node = node.children[1].children[0]
                try:
                        # Try for array fields
                        id_node = node.children[1].children[0].children[0]
                except AttributeError: pass
                name = id_node.value
                type_ = get_jvm_type(node.children[1].children[1])
                # Generate the signature
                field_sig = '.field '
                for modifier in node.modifiers:
                        field_sig += modifier + ' '
                # Get the value to be assigned
                value_node = node.children[1].children[1]
                value = str(value_node.value)
                if value_node.type_ == 'java/lang/String':
                        value = '"' + value_node.value + '"'
                field_sig += name + ' ' + type_ + ' = ' + value
                self._add_ln(field_sig)
        
        def _visit_constructor_dcl_node(self, node):
                """Generate a constructor definition, will also generate a
                call to to the super constructor and add a return statement
                if these are not done explicitly.
                """
                children = node.children
                name = '<init>'
                # Combine signature and spec
                class_s = self._t_env.get_class_s(self._cur_class)
                cons_s = class_s.constructor
                signature = name + self._gen_method_descriptor(cons_s, True)
                # Write the signature
                self._add_ln('.method ' + signature)
                # Create a new frame for this method
                self._cur_frame = Frame(children[1], False, 'void')
                self._add_iln('.limit stack 10')
                self._add_iln('.limit locals 100')
                # If the constructor of the super class is no explicitly called
                # in the code, it must be generated here
                not_has_body = isinstance(node.children[2], nodes.EmptyNode)
                if (not_has_body or 
                    not isinstance(node.children[2].children[0],
                                   nodes.SuperConstructorCallNode)):
                        self._gen_super_constructor()
                # Generate code for the method body
                self._visit(children[2])
                if (not_has_body or
                    not isinstance(children[2].children[-1],
                                   nodes.ReturnVoidNode)):
                        # There is no return statement at the end of the method,
                        # so one must be added
                        self._add_iln('return')
                self._add_ln('.end method')

        def _visit_method_dcl_node(self, node):
                self._gen_method_def(node)
        
        def _visit_method_dcl_array_node(self, node):
                self._gen_method_def(node)
        
        def _gen_method_def(self, node):
                """Shared code to generate a method definition and it's body
                for use by _visit_method_dcl_node and
                _visit_method_dcl_array_node.
                """
                children = node.children
                # These nodes are stored in different locations depending on
                # if the method returns an array or not, that is why they are
                # stored in these auxiliary variables
                param_node = children[2]
                body_node = children[3]
                if len(children) == 5:
                        param_node = children[3]
                        body_node = children[4]
                if children[0].value == 'main':
                        # Added public and static to main so that the JVM
                        # recognises this as the main method
                        self._add_ln('.method public static main' +
                                     '([Ljava/lang/String;)V')
                else:
                        name = children[0].value
                        # Build up the spec (parameter types and return type)
                        class_s = self._t_env.get_class_s(self._cur_class)
                        method_s = class_s.get_method(name)
                        spec = self._gen_method_descriptor(method_s, False)
                        # Combine signature and spec
                        signature = name + spec
                        # Add modifiers
                        full_sig = '.method '
                        if 'private' not in node.modifiers:
                                full_sig += 'public '
                        for modifier in node.modifiers:
                                full_sig += modifier + ' '
                        # Write the signature
                        self._add_ln(full_sig + signature)
                # Create a new frame for this method
                is_static = 'static' in node.modifiers
                self._cur_frame = Frame(param_node, is_static, node.type_)
                self._add_iln('.limit stack 10')
                self._add_iln('.limit locals 100')
                # Generate code for the method body
                self._visit(body_node)
                # If the method is not empty, check it has a return statement
                # at the end, if not, manually add one
                body_stmts = body_node.children
                if (len(body_stmts) != 0 and 
                    (not isinstance(body_stmts[-1], nodes.ReturnVoidNode) or
                     not isinstance(body_stmts[-1], nodes.ReturnNode))):
                        # There is no return statement at the end of the method,
                        # so one must be added
                        self._add_iln('return')
                self._add_ln('.end method')
                
        def _visit_block_node(self, node):
                """If it's a block, simply visit each child."""
                for child in node.children:
                        self._visit(child)
                        
        def _visit_var_dcl_node(self, node):
                """If it's a variable declaration, create a new variable in the
                frame.
                """
                var_name = node.children[1].value
                try:
                        # Do for arrays
                        var_name = node.children[1].children[0].value
                except AttributeError: pass
                is_long = self._is_long(node.children[0].value)
                self._cur_frame.new_var(var_name, is_long)
        
        def _visit_var_dcl_assign_node(self, node):
                """Create a new variable in the frame, and visit the assignment
                statement.
                """
                assign_node = node.children[1]
                var_name = assign_node.children[0].value
                try:
                        # Do for arrays
                        var_name = assign_node.children[0].children[0].value
                except AttributeError: pass
                is_long = self._is_long(node.children[1].type_)
                self._cur_frame.new_var(var_name, is_long)
                self._visit(assign_node)
        
        def _is_long(self, type_):
                """Returns whether or not a type takes up two slots in memory;
                e.i. longs and doubles.
                """
                is_long = False
                if type_ in ['long', 'double']:
                        is_long = True
                return is_long
        
        def _visit_if_node(self, node):
                children = node.children
                # Create a copy of _next_if so that the one held in this
                # recursive call does not become modified in one of the child
                # recursive method calls.
                next_if = self._label_suffix('if')
                # Generate code for the boolean expression
                self._visit(children[0])
                self._add_iln('ifeq IfFalse' + next_if,
                              ';Jump to IfFalse if if-stmt evaluates to false')
                self._visit(children[1])
                self._add_iln('goto IfEnd' + next_if)
                self._add_ln('IfFalse' + next_if + ':',
                             ';Continue from here if if_stmt was false')
                # If these is an else statement, generate the code for that
                if len(children) == 3:
                        self._visit(children[2])
                self._add_ln('IfEnd' + next_if + ':', ';End the if statement')
        
        def _visit_while_node(self, node):
                """These following statements work in much the same way as the
                if statement.
                """
                children = node.children
                next_while = self._label_suffix('while')
                self._add_ln('WhileStart' + next_while + ':',
                             ';Create an initial label to return to for ' +
                             'loop effect')
                self._visit(children[0])
                self._add_iln('ifeq WhileEnd' + next_while, 
                              ';Jump to WhileEnd if the boolean expression ' +
                              'evaluates to false to break out of loop')
                self._visit(children[1])
                self._add_iln('goto WhileStart' + next_while,
                              ';Jump back to WhileStart to create the loop ' +
                              'effect')
                self._add_ln('WhileEnd' + next_while + ':',
                             ';Exit point for he loop')
        
        def _visit_for_node(self, node):
                children = node.children
                next_for = self._label_suffix('for')
                self._visit(children[0])
                self._add_ln('ForStart' + next_for + ':',
                             ';Create an initial label to return to for ' +
                             'loop effect')
                self._visit(children[1])
                self._add_iln('ifeq ForEnd' + next_for, 
                              ';Jump to ForEnd if the boolean expression ' +
                              'evaluates to false to break out of loop')
                self._visit(children[3])
                self._visit(children[2])
                self._add_iln('goto ForStart' + next_for,
                              ';Jump back to ForStart to create the loop ' +
                              'effect')
                self._add_ln('ForEnd' + next_for + ':', ';Exit point for ' +
                             'the loop')
        
        def _visit_return_node(self, node):
                ret_expr = node.children[0]
                self._visit(ret_expr)
                # Add a convert operator is needed
                method_type = self._cur_frame.ret_type
                self._add_convert_op(method_type, ret_expr)
                self._add_iln(self._prefix(method_type) + 'return',
                             ';Return from method')
        
        def _visit_super_constructor_call_node(self, node):
                self._add_iln('aload_0', ';Load the current object')
                super_ = self._t_env.get_class_s(self._cur_class).super_class
#                if super_ == '':
#                        super_ = 'java/lang/Object'
#                else:
                # Get the arguments onto the stack
                try:
                        super_s = self._t_env.get_class_s(super_)
                        super_params = super_s.constructor.params
                        args_list = node.children[0].children
                        self._gen_args_list_node(args_list,
                                                 super_params)
                except AttributeError:
                        # No argumnts
                        pass
                sig = self._method_sigs[super_, '<init>']
                self._add_iln('invokespecial ' + sig)
        
        def _visit_assign_node(self, node):
                """For an assignment, generate code for the right hand side,
                and store this in the memory location corresponding to the 
                value in _var.
                """
                try:
                        # Try assigning into an array element
                        self._gen_array_element_assignment(node)
                except AttributeError:
                        # It's regular assignment
                        self._gen_regular_assignment(node)
        
        def _gen_regular_assignment(self, node):
                """Generate the code for regular assignment."""
                children= node.children
                try:
                        # Treat it as an array_dcl
                        var_name = children[0].children[0].value
                except AttributeError:
                        var_name = children[0].value
                # If it's a field, ref to the current object must be
                # loaded before the value to assign
                if (self._cur_class, var_name) in self._field_sigs.keys():
                        self._add_iln('aload_0', ';Load the current object ' +
                                      'to assign to field')
                self._visit(children[1])
                # Add conversion op if needed
                self._add_convert_op(children[0], children[1]) 
                # Store the value in the correct variable
                if (self._cur_class, var_name)  in self._field_sigs.keys():
                        # It's a field, so use field store syntax
                        sig = self._field_sigs[self._cur_class, var_name]
                        self._add_iln('putfield ' + sig,
                                      ';Store into field ' + children[0].value)
                else:
                        self._add_iln(self._prefix(children[0]) + 'store ' +
                                      str(self._cur_frame.get_var(var_name)), 
                                      ';Store top of stack in ' +
                                      str(self._cur_frame.get_var(var_name)) +
                                      ' (' + var_name + ')')
        
        def _gen_array_element_assignment(self, node):
                """Generate code for assigning to an array element."""
                children = node.children
                if isinstance(children[0], nodes.ArrayDclNode):
                        # If it's an array declaration node, it must
                        # be treated like a normal variable
                        raise AttributeError
                # Load the array
                self._gen_load_variable(children[0].children[0])
                for child in children[0].children[1:-1]:
                        # Load the indexes into the arrays
                        # And then load each sub array
                        self._visit(child)
                        self._add_iln('aaload')
                # Push the final index
                self._visit(children[0].children[-1])
                # Load the value to assign
                self._visit(children[1])
                # Add conversion op if needed
                self._add_convert_op(children[0], children[1])
                # Store the value
                self._add_iln(self._array_prefix(children[0]) + 'store',
                              ';Store the value in the array element')

        def _add_convert_op(self, l_child, r_child):
                """Helper method to convert one type to another before
                assignment if needed.  Works for type-tagged tree nodes, or
                string type descriptions.
                """
                l_type = l_child
                r_type = r_child
                # If either is a tree node, the type becomes the node's type
                try:
                        l_type = l_child.type_
                except AttributeError: pass
                try: 
                        r_type = r_child.type_
                except AttributeError: pass
                is_prim = self._is_prim(l_type)
                if l_type != r_type and is_prim:
                        convert_op = None
                        if l_type in ['char', 'byte', 'short', 'int']:
                                convert_op = self._convert_num_to_int(r_type)
                        elif l_type == 'long' :
                                convert_op = self._convert_num_to_long(r_type)
                        elif l_type == 'float':
                                convert_op = self._convert_num_to_float(r_type)
                        elif l_type == 'double':
                                convert_op = self._convert_num_to_double(r_type)
                        if convert_op is not None:
                                self._add_iln(convert_op, 
                                              ';Convert left hand side to ' +
                                              'match the type of the right')

        def _visit_cond_node(self, node):
                """Apply the operator to the boolean values."""
                children = node.children
                if node.value == '||':
                        self._visit(children[0])
                        self._visit(children[1])
                        self._add_iln('ior', ';OR the top two binary ' +
                                      'values on the stack')
                else:
                        #It's 'and'
                        self._visit(children[0])
                        self._visit(children[1])
                        self._add_iln('iand', ';AND the top two binary ' +
                                      'values on the stack')
        
        def _visit_eq_node(self, node):
                if node.children[0].type_ in self._t_env.nums + ['boolean']:
                        # It's a primitive type
                        self._gen_comp_code(node, False)
                else:
                        # Compare object references
                        self._gen_comp_code(node, True)
                
        def _visit_rel_node(self, node):
                """Generate code for each child - this will leave the result of
                each as the top to values on the stack.
                """
                self._gen_comp_code(node, False)
        
        def _gen_comp_code(self, node, is_object):
                """Generate code for comparisons.
                Some numerical can be implicitly converted if they are not the
                same type as the other side, the correct conversion operator
                must be looked up."""
                children = node.children
                self._visit(children[0])
                if not is_object:
                        # May need to convert primitive types
                        convert_op = self._convert_num_to_int(children[0].type_)
                        if convert_op is not None:
                                self._add_iln(convert_op, 
                                              ';Convert for comparison')
                        self._visit(children[1])
                        convert_op = self._convert_num_to_int(children[1].type_)
                        if convert_op is not None:
                                self._add_iln(convert_op,
                                              ';Convert for comparison')
                        # Generate comparison code
                        type_ = self._get_greater_type(children[0].type_,
                                                       children[1].type_)
                        self._gen_comp(node, type_)
                else:
                        self._visit(children[1])
                        self._gen_comp_object(node)                       
        
        def _get_greater_type(self, type1, type2):
                """From two primitive types, returns the one which is
                'higher up' in the list of primitive types.
                """
                prims = ['char', 'byte', 'short', 'int', 'long', 'float',
                         'double']
                return prims[max(prims.index(type1), prims.index(type2))]
        
        def _gen_comp(self, node, type_):
                """Helper method to generate code for an integer comparison
                operator.
                """
                # Create a copy of the label suffix
                next_comp = self._label_suffix('comp')
                # Create a corresponding asm instruction for the operator
                op = node.value
                if op == '>':
                        self._gen_greater_than(node, type_, next_comp)
                if op == '>=':
                        self._gen_greater_eq_to(node, type_, next_comp)
                if op == '<':
                        self._gen_less_than(node, type_, next_comp)
                if op == '<=':
                        self._gen_less_eq_to(node, type_, next_comp)
                if op == '==':
                        self._gen_eq_to(node, type_, next_comp)
                if op == '!=':
                        self._gen_not_eq_to(node, type_, next_comp)
                # Generate the remainder of the comparison code
                self._gen_comp_end(next_comp)
        
        def _gen_greater_than(self, node, type_, next_comp):
                if type_ in ['byte', 'char', 'short', 'int']:
                        self._add_iln('if_icmpgt CompTrue' + next_comp,
                                      ';If the value on the top of the ' +
                                      'stack is greater than the one below ' +
                                      'it, jump to CompTrue')
                elif type_ in ['long', 'float', 'double']:
                        self._gen_long_float_double_comp(node, type_)
                        self._add_iln('ifgt CompTrue' + next_comp, 
                                      'Jump to CompTrue if result is 1')
        
        def _gen_greater_eq_to(self, node, type_, next_comp):
                if type_ in ['byte', 'char', 'short', 'int']:
                        self._add_iln('if_icmpge CompTrue' + next_comp,
                                      ';If the value on the top of the ' +
                                      'stack is greater than or equal to ' +
                                      'the one below it, jump to CompTrue')
                elif type_ in ['long', 'float', 'double']:
                        self._gen_long_float_double_comp(node, type_)
                        self._add_iln('ifge CompTrue' + next_comp, 
                                      'Jump to CompTrue if result is 1 or 0')
        
        def _gen_less_than(self, node, type_, next_comp):
                if type_ in ['byte', 'char', 'short', 'int']:
                        self._add_iln('if_icmplt CompTrue' + next_comp,
                                      ';If the value on the top of the ' +
                                      'stack is less than the one below it,' +
                                      'jump to CompTrue')
                elif type_ in ['long', 'float', 'double']:
                        self._gen_long_float_double_comp(node, type_)
                        self._add_iln('iflt CompTrue' + next_comp, 
                                      'Jump to CompTrue if result is -1')
        
        def _gen_less_eq_to(self, node, type_, next_comp):
                if type_ in ['byte', 'char', 'short', 'int']:
                        self._add_iln('if_icmple CompTrue' + next_comp,
                                      ';If the value on the top of the ' +
                                      'stack is less than or equal to the ' +
                                      'one below it, jump to CompTrue')
                elif type_ in ['long', 'float', 'double']:
                        self._gen_long_float_double_comp(node, type_)
                        self._add_iln('ifle CompTrue' + next_comp, 
                                      'Jump to CompTrue if result is -1 or 0')

        def _gen_eq_to(self, node, type_, next_comp):
                if type_ in ['byte', 'char', 'short', 'int']:
                        self._add_iln('if_icmpeq CompTrue' + next_comp,
                                      ';If the value on the top of the ' +
                                      'stack is equal to the one below it, ' +
                                      'jump to CompTrue')
                elif type_ in ['long', 'float', 'double']:
                        self._gen_long_float_double_comp(node, type_)
                        self._add_iln('ifeq CompTrue' + next_comp, 
                                      'Jump to CompTrue if result is 0')
        
        def _gen_not_eq_to(self, node, type_, next_comp):
                if type_ in ['byte', 'char', 'short', 'int']:
                        self._add_iln('if_icmpne CompTrue' + next_comp,
                                      ';If the value on the top of the ' +
                                      'stack is is not equal o the one ' +
                                      'below it, jump to CompTrue')
                elif type_ in ['long', 'float', 'double']:
                        self._gen_long_float_double_comp(node, type_)
                        self._add_iln('ifne CompTrue' + next_comp, 
                                      'Jump to CompTrue if result is 1 or -1')
        
        def _gen_long_float_double_comp(self, node, type_):
                if type_ == 'long':
                        self._add_iln('lcmp',
                                      ';Compare two longs: 1 if var1 is ' +
                                      'greater, 0 if equal, -1 if less than')
                else:
                        self._add_iln(self._prefix(node) + 'cmpl',
                                      ';Compare the two values: 1 if var1 ' +
                                      'is greater, 0 if equal, -1 if less than')
                
        def _gen_comp_object(self, node):
                """Like _gen_comp, but only supports equal to or not equal to.
                Used for comparing object instances.
                """
                next_comp = self._label_suffix('comp')
                op = node.value
                if op == '==':
                        self._add_iln('if_acmpeq CompTrue' + next_comp,
                                      ';If the object on the top of the ' +
                                      'stack is the same instance as the ' +
                                      'one below it, jump to CompTrue')
                if op == '!=':
                        self._add_iln('if_acmpne CompTrue' + next_comp,
                                      ';If the object on the top of the ' +
                                      'stack is not the same instance as ' +
                                      'the one below it, jump to CompTrue')
                # Generate the remainder of the comparison code
                self._gen_comp_end(next_comp)
        
        def _gen_comp_end(self, next_comp):
                """Generates the rest of the code common to both comparison
                methods above.
                """
                self._add_iln('ldc 0',
                              ';Comparison was false, so load binary ' +
                              'constant 0')
                self._add_iln('goto CompEnd' + next_comp,
                              ';Jump to the end of the comparison')
                self._add_ln('CompTrue' + next_comp + ':',
                             ';End up here if the comparison was true')
                self._add_iln('ldc 1', 
                              ';Comparison was true, so load binary constant 1')
                self._add_ln('CompEnd' + next_comp + ':',
                             ';Exit point for comparison if it is false')
        
        def _visit_add_node(self, node):
                """Generate either regular addition code, string concatenation
                or matrix addition.
                """
                # For string concatination
                if node.type_ == 'java/lang/String':
                        # Load the references to the two strings, the first will
                        # be what the method will be called on, the second
                        # will be its argument
                        self._visit(node.children[0])
                        self._visit(node.children[1])
                        self._add_iln('invokevirtual java/lang/String/concat' +
                                      '(Ljava/lang/String;)Ljava/lang/String;',
                                      ';Use the built in concat method of ' +
                                      'String')
                elif node.type_ == 'matrix':
                        self._gen_matrix_operation(node)
                else:
                        # Treat it as the arithmetic operator
                        self._gen_arith(node)
        
        def _gen_matrix_operation(self, node):
                """Method to generate code common to both matrix addition and
                multiplication.  This is the setting up, and the outer loop
                through the rows.
                """
                # Note: the left hand matrix is referred to as a, and the right
                # as b
                # Create and store lengths of the dimensions
                # First visit child to gen code to load the array
                self._visit(node.children[0])
                self._add_iln('dup', ';Dup to get the rows and the columns')
                # Get First matrix column length
                self._add_iln('iconst_0', ';Index into first dimension')
                self._add_iln('aaload', ';Load second dimension')
                self._add_iln('arraylength', ';Get cols length')
                # To store columns of first matrix
                col_len_loc1 = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + col_len_loc1, ';Store length')
                # Get First matrix rows length
                self._add_iln('arraylength', ';Get rows length')
                self._add_iln('dup', ';Dup to specify dimensions ' +
                              'for the result array as well as storing')
                # To store rows of first matrix
                row_len_loc1 = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + row_len_loc1, ';Store length')
                # Load second matrix
                self._visit(node.children[1])
                self._add_iln('dup', ';Dup to get the rows and the columns')
                # Get Second matrix row length
                self._add_iln('arraylength', ';Get rows length')
                row_len_loc2 = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + row_len_loc2, ';Store length')
                # Get Second matrix column length
                self._add_iln('iconst_0', ';Index into first dimension')
                self._add_iln('aaload', ';Load second dimension')
                self._add_iln('arraylength', ';Get cols length')
                self._add_iln('dup', ';Dup to specify dimensions ' +
                              'for the result array as well as storing')
                # To store columns of second matrix
                col_len_loc2 = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + col_len_loc2, ';Store length')
                # Gen code to throw an exception if dimensions are incompatible
                if node.value == '*':
                        self._gen_check_matrix_mult_dimensions(col_len_loc1,
                                                               row_len_loc2)
                else:
                        self._gen_check_matrix_add_dimensions(row_len_loc1,
                                                              col_len_loc1,
                                                              row_len_loc2,
                                                              col_len_loc2)
                # Create an array to store the result in
                self._add_iln('multianewarray [[D 2',
                              ';Construct a new array to store result')
                result_mat_loc = str(self._get_auxillary_var_loc())
                self._add_iln('astore ' + result_mat_loc,
                              ';Store the result array') 
                # Create and store the indices for rows
                self._add_iln('iconst_0', ';Load 0')
                idx1_loc = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + idx1_loc, ';Store index')
                # Create local variables of label suffixes so they
                # can't be updated in child nodes
                next_mat_rows = self._label_suffix('mat_rows')
                next_mat_cols_b = self._label_suffix('mat_b_cols')
                # Start outer loop
                self._add_ln('MatRowStart' + next_mat_rows + ':',
                             ';Start of loop through rows')
                self._add_iln('iload ' + idx1_loc, ';Load index')
                self._add_iln('iload ' + row_len_loc1, ';Get row length')
                self._add_iln('if_icmpge MatRowEnd' + next_mat_rows,
                              ';Check if idx has reached the size ' +
                              'of the rows')
                if node.value == '*':
                        self._gen_matrix_multiplication(node, col_len_loc1,
                                                        col_len_loc2,
                                                        result_mat_loc,
                                                        idx1_loc,
                                                        next_mat_cols_b)
                else:
                        self._gen_matrix_addition(node, col_len_loc2,
                                                  result_mat_loc,
                                                  idx1_loc, next_mat_cols_b)
                self._add_iln('iinc ' + idx1_loc + ' 1',
                              ';Increment the index')
                self._add_iln('goto MatRowStart' + next_mat_rows,
                              ';Return to start of inner loop')
                self._add_ln('MatRowEnd' + next_mat_rows + ':',
                             ';End of the inner loop')
                self._add_iln('aload ' + result_mat_loc,
                              ';Leave the result matrix on the stack')
        
        def _gen_check_matrix_mult_dimensions(self, col_len_loc1, row_len_loc2):
                """Generate code to check matrices dimensions are compatible
                for multiplcation.
                """
                next_comp = self._label_suffix('comp')
                self._add_iln('iload ' + col_len_loc1,
                              ";Load first array's columns")
                self._add_iln('iload ' + row_len_loc2,
                              ";Load second array's rows")
                self._add_iln('if_icmpeq CompTrue' + next_comp,
                              ';Check dimensions match')
                self._add_iln('new java/lang/ArithmeticException',
                              ';Create a new exception')
                self._add_iln('dup',
                              ';Dup in order to call constructor, and throw')
                self._add_iln('ldc "Inner matrix dimensions must match ' +
                              'for multiplication!"', ';Load error message')
                self._add_iln('invokespecial java/lang/ArithmeticException/' +
                              '<init>(Ljava/lang/String;)V',
                              ";Invoke the exception's constructor")
                self._add_iln('athrow', ';Throw the exception')
                self._add_ln('CompTrue' + next_comp + ':',
                             ';Exit check here if no exception thrown')
        
        def _gen_check_matrix_add_dimensions(self, row_len_loc1, col_len_loc1,
                                             row_len_loc2, col_len_loc2):
                """Generate code to check matrices dimensions are compatible
                for addition/subtraction.
                """
                next_comp1 = self._label_suffix('comp')
                next_comp2 = self._label_suffix('comp')
                # Compare rows
                self._add_iln('iload ' + row_len_loc1,
                              ";Load first array's rows")
                self._add_iln('iload ' + row_len_loc2,
                              ";Load second array's rows")
                self._add_iln('if_icmpne CompTrue' + next_comp1,
                              ";If dimensions don't match, jump to " +
                              'exception throwing section')
                # Compare columns
                self._add_iln('iload ' + col_len_loc1,
                              ";Load first array's cols")
                self._add_iln('iload ' + col_len_loc2,
                              ";Load second array's cols")
                self._add_iln('if_icmpeq CompTrue' + next_comp2,
                              ';Check dimensions match')
                self._add_ln('CompTrue' + next_comp1 + ':',
                             ';First check failed')
                self._add_iln('new java/lang/ArithmeticException',
                              ';Create a new exception')
                self._add_iln('dup',
                              ';Dup in order to call constructor, and throw')
                self._add_iln('ldc "Matrix dimensions must be equal for ' +
                              'addition/subtraction!"', ';Load error message')
                self._add_iln('invokespecial java/lang/ArithmeticException/' +
                              '<init>(Ljava/lang/String;)V',
                              ";Invoke the exception's constructor")
                self._add_iln('athrow', ';Throw the exception')
                self._add_ln('CompTrue' + next_comp2 + ':',
                             ';Exit check here if no exception thrown')
        
        def _gen_matrix_addition(self, node, col_len_loc, result_mat_loc,
                                 idx1_loc, next_mat_cols):
                # Create and store columns index
                self._add_iln('iconst_0', ';Load 0')
                idx2_loc = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + idx2_loc, ';Set loop index to 0')
                # Start inner loop
                self._add_ln('MatColStart' + next_mat_cols + ':',
                             ';Start of loop through rows')
                self._add_iln('iload ' + idx2_loc, ';Load index')
                self._add_iln('iload ' + col_len_loc, ';Get row len')
                self._add_iln('if_icmpge MatColEnd' + next_mat_cols,
                              ';Check if idx has reached the size ' +
                              'of the cols')
                # Do the addition
                # Load the result matrix
                self._add_iln('aload ' + result_mat_loc,
                              ';Load the result matrix')
                self._add_iln('iload ' + idx1_loc, ';Load row index')
                self._add_iln('aaload', ';Load matrix row')
                self._add_iln('iload ' + idx2_loc, ';Load col index')
                # Load matrix 1 and get element
                self._visit(node.children[0]) 
                self._add_iln('iload ' + idx1_loc, ';Load row index')
                self._add_iln('aaload', ';Load matrix row')
                self._add_iln('iload ' + idx2_loc, ';Load col index')
                self._add_iln('daload', ';Load current matrix element')
                # Load matrix 2 and get element
                self._visit(node.children[1])
                self._add_iln('iload ' + idx1_loc, ';Load row index')
                self._add_iln('aaload', ';Load matrix row')
                self._add_iln('iload ' + idx2_loc, ';Load col index')
                self._add_iln('daload', ';Load current matrix element')
                # Add elements and store in result matrix cell
                if node.value == '+':
                        self._add_iln('dadd', ';Add element values')
                else:
                        self._add_iln('dsub', ';Sub element values')
                self._add_iln('dastore', ';Store result in new array')
                # End the loops
                self._add_iln('iinc ' + idx2_loc + ' 1',
                              ';Increment the index')
                self._add_iln('goto MatColStart' + next_mat_cols,
                              ';Return to start of inner loop')
                self._add_ln('MatColEnd' + next_mat_cols + ':',
                             ';End of the inner loop')
        
        def _get_auxillary_var_loc(self):
                """If a auxillary local variable needs to be created by the
                code generator, this will create it in the frame and return
                its location in memory.
                """
                result_mat_name = 'aux' + self._label_suffix('auxiliary')
                self._cur_frame.new_var(result_mat_name, False)
                return self._cur_frame.get_var(result_mat_name)

        def _visit_mul_node(self, node):
                if node.type_ == 'matrix':
                        self._gen_matrix_operation(node)
                else:
                        self._gen_arith(node)
                        
        def _gen_matrix_multiplication(self, node, col_len_loc1, col_len_loc2,
                                       result_mat_loc, idx1_loc,
                                       next_mat_b_cols):
                # Create label suffix for the cell loop labels
                next_mat_a_cols = self._label_suffix('mat_a_cols')
                # Set the middle loop index to 0
                self._add_iln('iconst_0', ';Load 0')
                idx2_loc = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + idx2_loc, ';Set loop index to 0')
                # Start loop through matrix b columns
                self._add_ln('MatBColStart' + next_mat_b_cols + ':',
                             ';Start of loop through rows')
                self._add_iln('iload ' + idx2_loc, ';Load index')
                self._add_iln('iload ' + col_len_loc2, ';Get row len')
                self._add_iln('if_icmpge MatBColEnd' + next_mat_b_cols,
                              ';Check if idx has reached the size ' +
                              'of the cols')
                # Set the inner loop index to 0
                self._add_iln('iconst_0', ';Load 0')
                idx3_loc = str(self._get_auxillary_var_loc())
                self._add_iln('istore ' + idx3_loc, ';Set loop index to 0')
                # Start (innermost) loop through matrix a columns
                self._add_ln('MatAColStart' + next_mat_a_cols + ':',
                             ';Start of loop through rows')
                self._add_iln('iload ' + idx3_loc, ';Load index')
                self._add_iln('iload ' + col_len_loc1, ';Get row len')
                self._add_iln('if_icmpge MatAColEnd' + next_mat_a_cols,
                              ';Check if idx has reached the size ' +
                              'of the cols')
                # Do the Multiplication
                # Load the result matrix
                self._add_iln('aload ' + result_mat_loc,
                              ';Load the result matrix')
                self._add_iln('iload ' + idx1_loc, ';Load row index')
                self._add_iln('aaload', ';Load matrix row')
                self._add_iln('iload ' + idx2_loc, ';Load col index')
                self._add_iln('dup2', ';Duplicate the array and its index ' +
                              'so that one can be used to load the element' +
                              'and one can be used to store into at the end')
                self._add_iln('daload', ';Load the array element to add to ' +
                              'the result of the multiplication')
                # Load matrix 1 and get element
                self._visit(node.children[0]) 
                self._add_iln('iload ' + idx1_loc, ';Load row index')
                self._add_iln('aaload', ';Load matrix row')
                self._add_iln('iload ' + idx3_loc, ';Load col index')
                self._add_iln('daload', ';Load current matrix element')
                # Load matrix 2 and get element
                self._visit(node.children[1])
                self._add_iln('iload ' + idx3_loc, ';Load row index')
                self._add_iln('aaload', ';Load matrix row')
                self._add_iln('iload ' + idx2_loc, ';Load col index')
                self._add_iln('daload', ';Load current matrix element')
                # Multiply the two elements and then add them to what is
                # already in the cell of the new matrix
                self._add_iln('dmul', ';Mul element values')
                self._add_iln('dadd', ';Add multiplied values to what is ' +
                              'already in the result array')
                self._add_iln('dastore', ';Store result in new array')
                # End matrix a column loop
                self._add_iln('iinc ' + idx3_loc + ' 1',
                              ';Increment the index')
                self._add_iln('goto MatAColStart' + next_mat_a_cols,
                              ';Return to start of inner loop')
                self._add_ln('MatAColEnd' + next_mat_a_cols + ':',
                             ';End of the inner loop')
                # End matrix b column loop
                self._add_iln('iinc ' + idx2_loc + ' 1',
                              ';Increment the index')
                self._add_iln('goto MatBColStart' + next_mat_b_cols,
                              ';Return to start of middle loop')
                self._add_ln('MatBColEnd' + next_mat_b_cols + ':',
                             ';End of the middle loop')

        def _gen_arith(self, node):
                """For arithmetic nodes."""
                # Apply a conversion operator if needed
                self._convert_num(node.children[0], node.children[1])
                # Simply apply appropriate asm instruction to the values on the
                # top of the stack
                op = ''
                if node.value == '+':
                        op = self._prefix(node) + 'add'
                elif node.value == '-':
                        op = self._prefix(node) + 'sub'
                elif node.value == '*':
                        op = self._prefix(node) + 'mul'
                elif node.value == '/':
                        op = self._prefix(node) + 'div'
                self._add_iln(op, ';Apply ' + node.value + 
                              ' to the values on the top of the stack')

        def _convert_num(self, l_child, r_child):
                """Write the correct numerical conversion oporator for the
                given child nodes of an arithmatic operator if needed.
                """
                self._visit(l_child)
                convert_op = None
                # First check if the left hand side needs to be converted to
                # match the type of the right hand side
                if l_child.type_ in ['char', 'byte', 'short', 'int']:
                        convert_op = self._convert_num_from_int(r_child.type_)
                elif l_child.type_ == 'long' :
                        convert_op = self._convert_num_from_long(r_child.type_)
                elif l_child.type_ == 'float':
                        convert_op = self._convert_num_from_float(r_child.type_)
                # If it does need to be converted, write out the correct
                # conversion operator
                if convert_op is not None:
                        self._add_iln(convert_op,
                                      ';Convert left hand side to match the ' +
                                      'type of the right')
                # Generate the code for the right child, and add a conversion
                # operator if needed in the same way as before.
                self._visit(r_child)
                convert_op = None
                if r_child.type_ in ['char', 'byte', 'short', 'int']:
                        convert_op = self._convert_num_from_int(l_child.type_)
                elif r_child.type_ == 'long' :
                        convert_op = self._convert_num_from_long(l_child.type_)
                elif r_child.type_ == 'float':
                        convert_op = self._convert_num_from_float(l_child.type_)
                if convert_op is not None:
                        self._add_iln(convert_op,
                                      ';Convert left hand side to match the ' +
                                      'type of the right')
        
        def _convert_num_from_int(self, type_):
                """Get the asm instruction to convert from an int to a given
                type_.
                """
                if type_ == 'long':
                        return 'i2l'
                elif type_ == 'float':
                        return 'i2f'
                elif type_ == 'double':
                        return 'i2d'
        
        def _convert_num_from_long(self, type_):
                """Get the asm instruction to convert from long to a given
                type_.
                """
                if type_ == 'float':
                        return 'l2f'
                elif type_ == 'double':
                        return 'l2d'
        
        def _convert_num_from_float(self, type_):
                """Get the asm instruction to convert from a float to a given
                type_.
                """
                if type_ == 'double':
                        return 'f2d'
        
        def _convert_num_to_int(self, type_):
                """Get the asm instruction to convert to an int from a given
                type_.
                """
                if type_ == 'long':
                        return 'l2i'
                elif type_ == 'float':
                        return 'f2i'
                elif type_ == 'double':
                        return 'd2i'
        
        def _convert_num_to_long(self, type_):
                """Get the asm instruction to convert to a long from a given
                type_.
                """
                if type_ in ['char', 'byte', 'short', 'int']:
                        return 'i2l'
                elif type_ == 'float':
                        return 'f2l'
                elif type_ == 'double':
                        return 'd2l'
        
        def _convert_num_to_float(self, type_):
                """Get the asm instruction to convert to a float from a given
                type_.
                """
                if type_ in ['char', 'byte', 'short', 'int']:
                        return 'i2f'
                elif type_ == 'long':
                        return 'l2f'
                elif type_ == 'double':
                        return 'd2f'
        
        def _convert_num_to_double(self, type_):
                """Get the asm instruction to convert to a double from a given
                type_.
                """
                if type_ in ['char', 'byte', 'short', 'int']:
                        return 'i2d'
                elif type_ == 'long':
                        return 'l2d'
                elif type_ == 'float':
                        return 'f2d'
        
        def _visit_not_node(self, node):
                """'Not' the top of the stack - if it's 0, convert to 1, if
                it's 1, convert to 0.
                """
                self._visit(node.children[0])
                next_not = self._label_suffix('not')
                self._add_iln('ifeq IsFalse' + next_not,
                              ';If its 0, go to the code to change it to 1')
                self._add_iln('iconst_0', ';It was 1, so change to 0')
                self._add_iln('goto NotEnd' + next_not, ';Exit the not code')
                self._add_ln('IsFalse' + next_not + ':',
                             ';Start here to change to 1')
                self._add_iln('iconst_1', ';Change to 1')
                self._add_ln('NotEnd' + next_not + ':', ';Exit the not code')

        def _visit_pos_node(self, node):
                """Simply apply the neg operator to the top of the stack."""
                self._visit(node.children[0])
                if node.value == '-':
                        self._add_iln(self._prefix(node.children[0]) + 'neg',
                                      ';Negates the integer on the top of ' +
                                      'the stack')
        
        def _visit_inc_node(self, node):
                """Used to increment or decrement a numerical variable or array
                element.  Whether it is an inc or dec is determined by type.
                """
                children = node.children
                op = ''
                if node.value == '--':
                        op = '-'
                try:
                        # Try for array elements
                        # First get the element of the array to store into
                        # on the stack
                        var_name = children[0].children[0].value
                        self._add_iln('aload ' +
                                      str(self._cur_frame.get_var(var_name)),
                                      ';Load the array to store into')
                        for child in children[0].children[1:-1]:
                                # Load the indexes into the arrays
                                # And then load each sub array
                                self._visit(child)
                                self.add_iln('aaload')
                        # Push the final index
                        self._visit(children[0].children[-1])

                        # Next get the element of the array again, this time
                        # to retrieve and increment the value
                        self._add_iln('aload ' +
                                      str(self._cur_frame.get_var(var_name)),
                                      ';Load the array to store into')
                        for child in children[0].children[1:-1]:
                                # Load the indexes into the arrays
                                # And then load each sub array
                                self._visit(child)
                                self.add_iln('aaload')
                        # Push the final index
                        self._visit(children[0].children[-1])
                        # Load the value from the array cell
                        self._add_iln(self._prefix(children[0]) + 'aload',
                                      ';Retrieve the value stored in the '
                                      'array cell')
                        self._add_iln('ldc ' + op + '1',
                                      ';Push 1 or -1 onto the stack')
                        self._add_iln(self._prefix(children[0]) + 'add',
                                      ';Add the 1 to the value')
                        
                        # Store the new value back in the cell originally
                        # pushed on the stack
                        self._add_iln(self._prefix(children[1]) + 'astore',
                                      ';Store the value in the array element')
                except AttributeError:
                        try:
                                # Incrementing is far simpler for variables
                                name = children[0].value
                                var = str(self._cur_frame.get_var(name))
                                self._add_iln(self._prefix(children[0]) +
                                              'inc ' + var + ' ' + op + '1',
                                              ';Increments variable ' + var +
                                              ' (' + name + ')')
                        except KeyError:
                                # It's a field
                                # Ref to the current object must be loaded
                                # before the value to assign
                                self._add_iln('aload_0', ';Load the current ' +
                                              'object to assign to field')
                                self._gen_load_variable(children[0])
                                self._add_iln('ldc ' + op + '1',
                                      ';Push 1 or -1 onto the stack')
                                self._add_iln(self._prefix(children[0]) + 'add',
                                      ';Add the 1 to the value')
                                sig = self._field_sigs[self._cur_class,
                                                       children[0].value]
                                self._add_iln('putfield ' + sig,
                                              ';Store into field ' +
                                              children[0].value)
                                
                
        def _visit_array_dcl_node(self, node):
                var = str(self._cur_frame.get_var(node.children[0].value))
                self._add_iln(self._get_load_op(node.type_) + ' ' + var,
                              ';Load value stored in ' + var + ' (' +
                              node.children[0].value + ')')
        
        def _visit_array_element_node(self, node):
                """Get the value held in the array element."""
#                var_name = node.children[0].value
#                self._add_iln('aload ' + str(self._cur_frame.get_var(var_name)),
#                              ';Load the array to store into')
                self._gen_load_variable(node.children[0])
                for child in node.children[1:-1]:
                        # Load the indexes into the arrays
                        # And then load each sub array
                        self._visit(child)
                        self._add_iln('aaload')
                # Push the final index
                self._visit(node.children[-1])
                # Load the value
                self._add_iln(self._array_prefix(node.children[0].type_) +
                              'load')
                
        def _visit_matrix_element_node(self, node):
                """Get the value held in the matrix element."""
                self._gen_load_variable(node.children[0])
                self._visit(node.children[1])
                self._add_iln('aaload', ';Load inner array')
                self._visit(node.children[2])
                self._add_iln('daload', ';Load the value')
                
        def _visit_method_call_node(self, node):
                """Generate code to call a method in the current class, or a
                superclass.
                """
                self._add_iln('aload_0 ', ';Load the local variable in ' +
                              'location 0, which is a reference to the ' +
                              'current object')
                class_s = self._t_env.get_class_s(self._cur_class)
                method_name = node.children[0].value
                # Search for the method
                try:
                        class_s, method_s = self._find_method_s(class_s,
                                                                method_name)
                except SymbolNotFoundError:
                        # Must be in a library class
                        method_s = self._find_lib_method_s(self._cur_class,
                                                           method_name,
                                                           node.children[1])
                # Get the results from what the arguments are on the top of the
                # stack
                try:
                        self._gen_args_list_node(node.children[1].children,
                                                 method_s.params)
                except AttributeError:
                        # No args
                        pass
                # Invoke the method
                try:
                        method_sig = self._method_sigs[(class_s.name, method_s.name)]
                        # If it's a call to a private method, or a method in a super
                        # class, invokespecial must be used
                        op = 'invokevirtual'
                        if 'private' in method_s.modifiers:
                                op = 'invokespecial'
                        self._add_iln(op + ' ' + method_sig)
                except KeyError:
                        # Do for lib methods
                        self._add_iln('invokevirtual ' + method_s.sig)
        
        def _visit_method_call_long_node(self, node):
                """Generate code for a extended method call where the method
                is held in another class.
                """
                children = node.children
                class_name = children[0].value
                method_name = children[1].value
                args_list = children[-1]
                # Load the object, if it's not static
                is_static = True
                if children[0].value not in self._t_env.types:
                        class_name = children[0].type_
                        self._gen_load_variable(children[0])
                        is_static = False
                else:
                        class_name = get_full_type(class_name, self._t_env)
                class_s = None
                method_s = None
                try:
                        # Search for the method
                        get_class = self._t_env.get_class_or_interface_s
                        class_s = get_class(class_name)
                        class_s, method_s = self._find_method_s(class_s,
                                                                method_name)
                        # Get the results from what the arguments are on the 
                        # top of the stack
                        try:
                                self._gen_args_list_node(args_list.children, # TODO: NOT NEEDED FOR LIB CLASSES BECAUSE SUB CLASSES OF ARGS ARE NOT SUPPORTED SO FAR
                                                         method_s.params)
                        except AttributeError:
                                # No args
                                pass
                except SymbolNotFoundError:
                        # It was a library class
                        method_s = self._find_lib_method_s(class_name,
                                                           method_name,
                                                           args_list)
                # Invoke the method
                # First need to get the correct operator, then need to check
                # if it's an interface or class type
                op = 'invokevirtual'
                if is_static:
                        op = 'invokestatic'
                elif method_s is not None and 'private' in method_s.modifiers:
                        op = 'invokespecial'
                try:
                        method_sig = self._method_sigs[(class_s.name,
                                                        method_s.name)]
                        self._add_iln(op + ' ' + method_sig)
                except (KeyError, AttributeError):
                        try:
                                # It could be an object of type interface
                                # Interfaces need the number of arguments too
                                # This is num_args + 1, since the first is the
                                # ref to the current object
                                num_args = 1
                                try:
                                        args = node.children[-1].children
                                        num_args = len(args) + 1
                                except AttributeError:
                                        # No args
                                        pass
                                self._add_iln('invokeinterface ' +
                                              self._method_sigs[(class_s.name,
                                                                method_s.name)]
                                              + ' ' + str(num_args))
                        except (KeyError, AttributeError):
                                # Arg types need to be worked out in order to
                                # get the library class signature
                                sig = method_s.sig
                                self._add_iln(op + ' ' + sig)
                        
        
        def _visit_method_call_super_node(self, node):
                """Generate code for a call to a method in a super class."""
                self._add_iln('aload_0 ',
                              ';Load the local variable in location ' +
                              '0, which is a reference to the ' +
                              'current object')
                # Get the class and method symbols of the method
                class_s = self._t_env.get_class_or_interface_s(self._cur_class)
                cur_class_s = class_s
                method_name = node.children[0].value
                try:
                        super_s = self._t_env.get_class_s(class_s.super_class)
                        # Search for the method
                        class_s, method_s = self._find_method_s(super_s, method_name)
                except SymbolNotFoundError:
                        method_s = self._find_lib_method_s(self._cur_class,
                                                           method_name,
                                                           node.children[1])
                        class_s = None
                # Get the results from what the arguments are on the top of the
                # stack
                try:
                        self._gen_args_list_node(node.children[-1],
                                                 method_s.params)
                except AttributeError:
                        # No args
                        pass
                # The operator needs to be invoke special if there is a
                # method with the same name in the current class
                op = 'invokevirtual'
                if method_name in [meth_s.name for meth_s in cur_class_s.methods]:
                        op = 'invokespecial'
                # Invoke the method
                try:
                        method_sig = self._method_sigs[(class_s.name, method_s.name)]
                        self._add_iln(op + ' ' + method_sig)
                except AttributeError:
                        # It's a library method
                        self._add_iln(op + ' ' + method_s.sig)
        
        def _find_method_s(self, class_s, name):
                """Find a method symbol by searching in the full inheritance
                tree.
                """
                method_s = None
                try:
                        method_s = class_s.get_method(name)
                        return class_s, method_s
                except SymbolNotFoundError:
                        # Method not in current class, so look in super
                        super_name = ''
                        try:
                                super_name = class_s.super_class
                        except AttributeError:
                                # It was actually an interface
                                super_name = class_s.super_interface
                        super_s = self._t_env.get_class_s(super_name)
                        # Recursively search in the super class
                        return self._find_method_s(super_s, name)
        
        def _find_lib_method_s(self, class_name, method_name, args_list):
                """Get a library method symbol from the class of the object it
                was invoked on, it's name, and the arguments used.
                """
                # If the class provided is not the name of a library class,
                # recursively look through its super classes until a library
                # class is reached
                try:
                        super_name = ''
                        class_s = self._t_env.get_class_s(class_name)
                        try:
                                super_name = class_s.super_class
                        except AttributeError:
                                # It was actually an interface
                                super_name = class_s.super_interface
                        return self._find_lib_method_s(super_name, method_name,
                                                       args_list)
                except SymbolNotFoundError:
                        # The class is a library class
                        arg_types = []
                        # Add args if any
                        try:
                                args = args_list.children
                                arg_types = self._get_arg_types(args)
                                # Generate the arguments
                                for arg in args_list.children:
                                        self._visit(arg)
                        except AttributeError: pass
                        class_name = get_full_type(class_name, self._t_env)
                        return self._t_env.get_lib_method(class_name,
                                                          method_name,
                                                          arg_types)

        def _gen_args_list_node(self, args, params):
                """Generate code for the arguments.  It takes the parameters
                of the method that the arguments are being passed into, to
                check if any type conversions are required.
                """
                for idx, child in enumerate(args):
                        self._visit(child)
                        # Add convertion op if needed
                        self._add_convert_op(params[idx], child)
        
        def _get_arg_types(self, args_list):
                """From a list of args, produces a list of the argument's
                types.
                """
                types = []
                for arg in args_list:
                        types.append(arg.type_)
                return types

        def _visit_object_creator_node(self, node):
                """Create a new object reference and invoke its constructor."""
                name = node.children[0].value
                self._add_iln('new ' + get_full_type(name, self._t_env),
                              ';Create a new instance of the class')
                self._add_iln('dup', ';Duplicate the reference')
                
                try:
                        class_s = self._t_env.get_class_s(name)
                        cons_s = class_s.constructor
                        # Add the arguments
                        try:
                                args_list = node.children[1].children
                                self._gen_args_list_node(args_list,
                                                         cons_s.params)
                        except IndexError:
                                # No arguments
                                pass
                        sig = self._method_sigs[name, '<init>']
                except SymbolNotFoundError:
                        # Library class
                        args_list = []
                        # Get args if any
                        try:
                                args_list = node.children[1].children
                        except IndexError: pass
                        arg_types = self._get_arg_types(args_list)
                        full_name = get_full_type(name, self._t_env)
                        cons_s = self._t_env.get_lib_cons(full_name, arg_types)
                        # Generate the arguments
                        for arg in args_list:
                                self._visit(arg)
                        sig = cons_s.sig
                # Invoke the constructor
                self._add_iln('invokespecial ' + sig, ';Call the constructor')
        
        def _visit_field_ref_node(self, node):
                """Get a reference to the class of the field, and get the
                field's value.
                """
                field_name = node.children[1].value
                class_name = node.children[0].value
                is_static = True
                if class_name not in self._t_env.types:
                        # Load reference to the object held in the variable
                        self._visit(node.children[0])
                        class_name = node.children[0].type_
                        is_static = False
                # If it's a matrix or array, the field must be length, whose
                # value is accessed differently
                if class_name == 'matrix' or isinstance(class_name, ArrayType):
                        if field_name == 'colLength':
                                # Need to get columns
                                self._add_iln('iconst_0',
                                              ';Index into first element')
                                self._add_iln('aaload', ';Load 2nd dimension')
                        self._add_iln('arraylength', ";Get the array's length")
                                
                else:
                        sig = self._get_field_sig(class_name, field_name)
                        op = 'getfield'
                        if is_static:
                                op = 'getstatic'
                        self._add_iln(op + ' ' + sig, ';Get the fields value')
        
        def _get_field_sig(self, cname, fname):
                """For a given current class name and field name, search
                through the full inheritance tree for the correct signature
                for the field.
                """
                try:
                        class_s = self._t_env.get_class_s(cname)
                        try:
                                field_s = class_s.get_field(fname)
                                return self._field_sigs[class_s.name, fname]
                        except SymbolNotFoundError:
                                # Field not in current class, so look in super
                                super_name = class_s.super_class
                                # Recursively search in the super class
                                return self._get_field_sig(super_name, fname)
                except SymbolNotFoundError:
                        # It's in a library class
                        field_s = self._t_env.get_lib_field(cname, fname)
                        return field_s.sig
                        
        def _visit_array_init_node(self, node):
                """Constructs a new array, or multi-dimensional array."""
                if len(node.children) == 2:
                        # It has one dimension
                        self._visit(node.children[1])
                        if self._is_prim(node.type_):
                                # If the node is a primitive type
                                self._add_iln('newarray ' + node.type_.type_,
                                             ';Construct new array')
                        else:
                                self._add_iln('anewarray ' + node.type_.type_,
                                             ';Construct new array')
                else:
                        # It's multi-dimensional
                        for child in node.children[1:]:
                                # Get the sizes of each dimenion on the stack
                                self._visit(child)
                        self._add_iln('multianewarray ' +
                                      get_jvm_type(node) + ' ' +
                                      str(len(node.children[1:])),
                                      ';Construct a new multidimensional array')
        
        def _visit_matrix_init_node(self, node):
                for child in node.children:
                        # Get the sizes of each dimenion on the stack
                        self._visit(child)
                self._add_iln('multianewarray [[D 2',
                              ';Construct a new multidimensional array')
                
        def _visit_id_node(self, node):
                """If it's an identifier, load the value from memory - the
                correct location is optained from _var.
                """
                self._gen_load_variable(node)
        
        def _gen_load_variable(self, node):
                """Generate code to load a variable, be it a local variable,
                or a field.
                """
                try:
                        # Use local variable load syntax
                        var = str(self._cur_frame.get_var(node.value))
                        self._add_iln(self._prefix(node) + 'load ' + var,
                                      ';Load value stored in ' + var + ' (' +
                                      node.value + ')')
                except KeyError:
                        # It must be a field
                        self._add_iln('aload_0', ';Load "this" in order to ' +
                                      'access the field')
                        # Find the field (could be in superclass)
                        fname = node.value
                        cname = self._cur_class
                        sig = self._get_field_sig(cname, fname)
                        self._add_iln('getfield ' + sig,
                                      ";Get the field's value")
        
        def _visit_literal_node(self, node):
                """If it's a literal, pop it onto the stack."""
                if node.type_ == 'byte':
                        self._add_iln('bipush ' +  str(node.value),
                                      ';Load constant numerical byte ' +
                                      str(node.value))
                elif node.type_ == 'short':
                        self._add_iln('sipush ' +  str(node.value),
                                      ';Load constant numerical short ' +
                                      str(node.value))
                if node.type_ in ['char', 'int', 'float']:
                        self._add_iln('ldc ' +  str(node.value),
                                      ';Load constant numerical value ' +
                                      str(node.value))
                elif node.type_ in ['long', 'double']:
                        self._add_iln('ldc2_w ' +  str(node.value),
                                      ';Load constant numerical value ' +
                                      str(node.value))
                elif node.type_ == 'java/lang/String':
                        self._add_iln('ldc "' + node.value + '"',
                                      ';Load constant string "' + node.value +
                                      '" (creates a new String object)')
                else: # If it's a boolean, convert the value to 1 or 0
                        if node.value == True:
                                self._add_iln('iconst_1',
                                              ';Load constant boolean value 1')
                        else:
                                self._add_iln('iconst_0',
                                              ';Load constant boolean value 0')
        
        def _gen_return_void(self, node):
                self._add_iln('return', ';Return from the void method')
        
        def _visit_interface_node(self, node):
                children = node.children
                # Set the current class as the interface
                self._cur_class = children[0].value
                # Generate the code
                self._add_ln('.interface ' + children[0].value)
                self._cur_class = children[0].value
                if children[1].value != '':
                        # It extends another inteface
                        self._add_ln('.super ' + children[1].value)
                else:
                        # Hack because there is no top-level interface, yet
                        # Jasmin requires one
                        self._add_ln('.super java/lang/Object')
                self._visit(children[2])
        
        def _visit_interface_body_node(self, node):
                for child in node.children:
                        self._visit(child)
        
        def _visit_abs_method_dcl_node(self, node):
                self._gen_interface_method(node)
        
        def _visit_abs_method_dcl_array_node(self, node):
                self._gen_interface_method(node)
                
        def _gen_interface_method(self, node):
                children = node.children
                name = children[0].value
                interface_s = self._t_env.get_interface_s(self._cur_class)
                method_s = interface_s.get_method(name)
                signature = name
                signature += self._gen_method_descriptor(method_s, False)
                # Write the signature
                self._add_ln('.method public abstract ' + signature)
                self._add_ln('.end method')
        
        def _prefix(self, node):
                """Get's the correct instruction prefix given the type of the
                provided node (or a string representation of a type).
                """
                # Assume it's a string representation of a type
                type_ = node
                try:
                        # If it was a node that was passed in
                        if not isinstance(type_, ArrayType):
                                type_ = node.type_
                except AttributeError: pass
                jvm_type = ''
                if type_ in ['boolean', 'byte', 'char', 'short', 'int']:
                        jvm_type += 'i'
                elif type_ == 'long':
                        jvm_type += 'l'
                elif type_ == 'float':
                        jvm_type += 'f'
                elif type_ == 'double':
                        jvm_type += 'd'
                else:
                        # It's a class type or array
                        jvm_type += 'a'
                return jvm_type

        def _array_prefix(self, type_):
                """Like above, but works for the type of array elements."""
                # Assume it's a string representation of a type
                type_ = type_.type_
                jvm_type = ''
                if type_ in ['byte', 'boolean']:
                        jvm_type += 'ba'
                elif type_ == 'char':
                        jvm_type += 'ca'
                elif type_ == 'short':
                        jvm_type += 'sa'
                elif type_ == 'int':
                        jvm_type += 'ia'
                elif type_ == 'long':
                        jvm_type += 'la'
                elif type_ == 'float':
                        jvm_type += 'fa'
                elif type_ == 'double':
                        jvm_type += 'da'
                else:
                        # It's a class type or array
                        jvm_type += 'aa'
                return jvm_type
        
        def _is_prim(self, type_):
                """Returns whether or not a type is a primitive type."""
                try:
                        # If it's an array type - get the type of that
                        type_ = type_.type_
                except AttributeError: pass
                if type_ in ['boolean', 'byte', 'char', 'short', 'int',
                                 'long', 'float', 'double']:
                        return True
                return False
        
        def _label_suffix(self, key):
                """Gets the current label suffix, and automatically increments.
                """
                val = self._next_labels[key]
                self._next_labels[key] += 1
                return str(val)
        
        def _add_iln(self, line, comment = None):
                """Adds and indented line to the output."""
                if comment is None:
                        self._out += '\t' + line + '\n'
                else:
                        self._out += ('\t' + line + self._get_tab_len(line) +
                                      comment + '\n')

        def _add_ln(self, line, comment = None):
                """Adds a regular line to the output."""
                if comment is None:
                        self._out += line + '\n'
                else:
                        self._out += (line + self._get_tab_len(line) + '\t' +
                                      comment + '\n')
        
        def _get_tab_len(self, line):
                """Get the amount of tabs needed to indent the comment part 20
                characters.
                """
                length = len(line)
                if length < 8:
                        return '\t\t\t\t'
                elif length < 15:
                        return '\t\t\t'
                elif length < 22:
                        return '\t\t'
                elif length < 32:
                        return '\t'
                else: # It's 32 or greater - just make it a space
                        return ' '