"""The test class for the module jaml.py."""
import unittest
import os
from semantic_analysis import semantic_analyser
from semantic_analysis.exceptions import (NotInitWarning, NoReturnError,
                                          SymbolNotFoundError,
                                          MethodSignatureError, DimensionsError,
                                          MethodNotImplementedError,
                                          ConstructorError, VariableNameError,
                                          AssignmentError, ObjectCreationError,
                                          ClassSignatureError)

class TestSemanticAnalyser(unittest.TestCase):
        this_file_path = os.path.dirname(__file__)
        file_dir = os.path.join(this_file_path, 'test_files')

        def test_scan_classes_methods(self):
                """Test that all referenced classes are scanned properly, and
                returned.
                """
                asts = self.analyse_file('test_scan_classes_methods.jml')
                self.assertEqual(asts[0][0].children[0].value,
                                 'test_scan_classes_methods')
                self.assertEqual(asts[0][1].children[0].value,
                                 'test_scan_classes_methods2')
        
        def test_extends_pass(self):
                """Test a subclass can be assigned to a superclass."""
                self.analyse_file('test_extends_pass.jml')
        
        def test_extends_fail(self):
                """Test an error thrown when a superclass is assigned to a
                subclass.
                """
                self.assertRaises(TypeError, self.analyse_file,
                                  'test_extends_fail.jml')
        
        def test_class_extends_final_fail(self):
                """Test error thrown when a final class is attempted to be
                extended."""
                self.assertRaises(ClassSignatureError, self.analyse_file,
                                  'test_class_extends_final_fail.jml')
        
        def test_implements_pass(self):
                """Test that no errors thrown when a class implements more than
                one interface correctly.
                """
                self.analyse_file('test_implements_pass.jml')
        
        def test_implements_not_exists_fail(self):
                """Test the case where the interface does not exist."""
                self.assertRaises(SymbolNotFoundError,
                                  semantic_analyser.analyse,
                                  'class X implements Y {}')
        
        def test_not_implemented_fail(self):
                """Test the case where a class does not correctly implement
                all methods in an interface."""
                self.assertRaises(MethodNotImplementedError, self.analyse_file,
                                  'test_not_implemented_fail.jml')
                
        def test_env_pass(self):
                """Test that a variable is correctly looked up when it's used in
                a nested block.
                """
                self.analyse_stmt('int x = 4;if (x == 5){ x = 3;}')
        
        def test_env_fail(self):
                """Test that an exception is raised when a variable is
                referenced that was declared in an inner block.
                """
                self.assertRaises(SymbolNotFoundError, self.analyse_stmt,
                                  'if ("y" != "x"){float x = 10L;}x = 15L;')
        
        def test_class_scope_fail(self):
                """Test exception thrown when variable is referenced from
                another method.
                """
                self.assertRaises(SymbolNotFoundError,
                                  semantic_analyser.analyse, 
                                  'class X { void x() { int x = 3; } ' +
                                  'void y() { x = 4;}}')
        
        def test_param_pass(self):
                """Test parameters can be used within the method body."""
                semantic_analyser.analyse('class X { void x(int y) ' +
                                          '{int x = y;}}')
        
        def test_param_fail(self):
                """Test parameters of one method are not accessible 
                elsewhere.
                """
                self.assertRaises(SymbolNotFoundError,
                                  semantic_analyser.analyse,
                                  'class x { void x(int y) {} ' +
                                  'void z(){int w = y;}}')
        
        def test_super_cons_params_no_cons_fail(self):
                """Test that an error is thrown when a class does not have
                a constructor, when the super class has a constructor that
                takes parameters.
                """
                self.assertRaises(ConstructorError, self.analyse_file,
                                  'test_super_cons_params_no_cons_fail.jml')
        
        def test_super_cons_params_no_params(self):
                """Test that an error is thrown when the super class has a
                constructor which takes parameters, and the sub class has
                a constructor, but it does not call the super classes
                constructor.
                """
                self.assertRaises(ConstructorError, self.analyse_file,
                                  'test_super_cons_params_no_params.jml')
        
        def test_multi_constructors_fail(self):
                """Test an error is thrown when a class contains multiple
                constructors."""
                self.assertRaises(ConstructorError, semantic_analyser.analyse,
                                  'class X { X() {} X() {} }')
        
        def test_method_call_pass(self):
                """Test that there is no error when a call is made to another
                method within the same class.
                """
                semantic_analyser.analyse('class X {void x() {y();} ' +
                                          'void y(){} }')
        
        def test_method_call_fail(self):
                """Test an error is thrown when a method is called which doesn't
                exist.
                """
                self.assertRaises(SymbolNotFoundError,
                                  semantic_analyser.analyse,
                                  'class X {void x() {z();} void y(){} }')
        
        def test_method_call_args_pass(self):
                """Test that there is no error when the arguments match the
                method signature.
                """
                semantic_analyser.analyse('class X {void x() ' +
                                          '{long w = 5; y(w + 5);} ' +
                                          'void y(long z){} }')
        
        def test_method_call_args_length_fail(self):
                """Test an error is thrown when a method is called where no 
                arguments are provided when there should be one.
                """
                self.assertRaises(MethodSignatureError,
                                  semantic_analyser.analyse,
                                  'class X {void x() {y();} void y(long z){} }')
        
        def test_method_call_args_wrong_type_fail(self):
                """Test an error is thrown when a method is called where
                the arguments are of the incorrect type.
                """
                self.assertRaises(TypeError, semantic_analyser.analyse,
                                  'class X {void x() {boolean w = true; ' +
                                  'y(w);} void y(long z){} }')
        
        def test_method_return_pass(self):
                """Test that no error is raised when the correct type is
                returned.
                """
                semantic_analyser.analyse('class X {short x(){return 6;}}')
        
        def test_method_no_return_fail(self):
                """Test that an error is raised when a method does not return
                anything when it's signature states it should.
                """
                self.assertRaises(NoReturnError, semantic_analyser.analyse,
                                  'class X {short x(){}}')
        
        def test_method_wrong_return_fail(self):
                """Test that an error is raised when a method returns an
                incorrect type.
                """
                self.assertRaises(TypeError, semantic_analyser.analyse,
                                  'class X {short x(){return true;}}')
        
        def test_method_return_array_pass(self):
                """Test no error raised when a method returns an array"""
                semantic_analyser.analyse('class X {byte[][] x(){return new ' +
                                          'byte[5][5];}}')
        
        def test_method_return_array_fail(self):
                """Test error raised when array is not returned"""
                self.assertRaises(TypeError, semantic_analyser.analyse,
                                  'class X {int[] x(){return 1;}}')
        
        def test_method_call_external_pass(self):
                """Test no error thrown when a method is called from an object
                of another class."""
                self.analyse_file('test_method_call_external_pass.jml')
        
        def test_method_call_external_not_exists_fail(self):
                """Test that an error is raised when a method is called in
                another class which doesn't exist."""
                self.assertRaises(SymbolNotFoundError, self.analyse_file,
                                  'test_method_call_external_not_exists_fail' +
                                  '.jml')
        
        def test_method_call_external_wrong_type_fail(self):
                """Test that an error is raised when a method is called in
                another class which returns an incompatible type with what
                the result is being assigned to."""
                self.assertRaises(TypeError, self.analyse_file,
                                  'test_method_call_external' +
                                 '_wrong_type_fail.jml')
        
        def test_method_call_super_pass(self):
                """Test no error thrown when a method is invoked that is
                defined in a super class.
                """
                self.analyse_file('test_method_call_super_pass.jml')
        
        def test_method_override_final_fail(self):
                """Test that an error is thrown when a subclass attempts to
                override a final method in a super class.
                """
                self.assertRaises(MethodSignatureError, self.analyse_file,
                                 'test_method_override_final_fail.jml')
        
        def test_method_call_static_pass(self):
                """Test no error thrown when a static method is called from
                another class.
                """
                self.analyse_file('test_method_call_static_pass.jml')
        
        def test_method_call_static_not_static_fail(self):
                """Test an error thrown when a method is referenced in a static
                way when it is not static.
                """
                self.assertRaises(SymbolNotFoundError, self.analyse_file,
                                  'test_method_call_static_not_static_fail.jml')
        
        def test_ref_non_static_field_fail(self):
                """Test that an error is thrown when a non static field
                is referenced from a static method.
                """
                self.assertRaises(SymbolNotFoundError,
                                  semantic_analyser.analyse,
                                  'class X { int x = 5; static void x()' +
                                  '{ int y = x;}}')
        
        def test_pivate_method_pass(self):
                """Test no error thrown when a private method is called
                from within the same class.
                """
                semantic_analyser.analyse('class X { void x() {}' +
                                          'void y() { x();} }')
        
        def test_private_method_fail(self):
                """Test an error thrown when a private method is attempted to
                be accessed in another class.
                """
                self.assertRaises(SymbolNotFoundError, self.analyse_file,
                                  'test_private_method_fail.jml')
        
        def test_object_creator_fail(self):
                """Test that an error is raised when an object is assigned to a
                variable of an incorrect type."""
                self.assertRaises(TypeError, self.analyse_file,
                                  'test_object_creator_fail.jml')
        
        def test_object_creator_abstact_fail(self):
                """Test an error is thrown when an abstract class is attempted
                to be instantiated.
                """
                self.assertRaises(ObjectCreationError, self.analyse_file,
                                  'test_object_creator_abstact_fail.jml')
                
        def test_field(self):
                """Test that a field can be accessed from within a method."""
                semantic_analyser.analyse('class X { int x; ' +
                                          'void x() {x = 5;}}')
        
        def test_final_field_assign_fail(self):
                """Test error thrown when assignment is attemped with a final
                field.
                """
                self.assertRaises(AssignmentError, semantic_analyser.analyse,
                                  'class X { final short y = 5;' +
                                  'void x(){y=5;}}')
        
        def test_final_field_inc_fail(self):
                """Like above, but checks for decrementing."""
                self.assertRaises(AssignmentError, semantic_analyser.analyse,
                                  'class X { final short y = 5;' +
                                  'void x(){y--;}}')
        
        def test_field_ref_external_pass(self):
                """Test no error thrown when a field is referenced in another
                class."""
                self.analyse_file('test_field_ref_external_pass.jml')
        
        def test_field_ref_external_fail(self):
                """Test an error thrown when a field is referenced in another
                class that doesn't exist."""
                self.assertRaises(SymbolNotFoundError, self.analyse_file,
                                  'test_field_ref_external_fail.jml')

        def test_field_ref_static_pass(self):
                """Test no error thrown when a static field is referenced from
                another class.
                """
                self.analyse_file('test_field_ref_static_pass.jml')
        
        def test_field_ref_static_not_static_fail(self):
                """Test an error thrown when a field is referenced in a static
                way when it is not static.
                """
                self.assertRaises(SymbolNotFoundError, self.analyse_file,
                                  'test_field_ref_static_not_static_fail.jml')
        
        def test_field_ref_super_pass(self):
                """Test no error thrown when a field is referenced that is
                defined in a super class.
                """
                self.analyse_file('test_field_ref_super_pass.jml')
        
        def test_pivate_field_pass(self):
                """Test no error thrown when a private field is used in the
                same class.
                """
                semantic_analyser.analyse('class X { private byte x = 1;' +
                                          'void y() { byte y = x;} }')
        
        def test_private_field_fail(self):
                """Test an error thrown when a private method is attempted to
                be accessed in another class.
                """
                self.assertRaises(SymbolNotFoundError, self.analyse_file,
                                  'test_private_field_fail.jml')
        
        # There are a number of possibilities of possible name clashes -
        # these attempt to check for a few of the, but they are not
        # exhaustive tests       
        def test_name_clash_field_type(self):
                """Test an error thrown when there is a name clash between
                a type (class) name and a field name."""
                self.assertRaises(VariableNameError, semantic_analyser.analyse,
                                  'class X { short X; }')
        
        def test_name_clash_param_field(self):
                """Test an error thrown when there is a name clash between
                a parameter name and a field name."""
                self.assertRaises(VariableNameError, semantic_analyser.analyse,
                                  'class X { short x; void y(byte x){} }')
        
        def test_name_clash_local_param(self):
                """Test an error thrown when there is a name clash between
                a parameter name and a local variable name."""
                self.assertRaises(VariableNameError, semantic_analyser.analyse,
                                  'class X { void y(byte x){int x = 5;} }')
        
        def test_name_clash_local_field(self):
                """Test an error thrown when there is a name clash between
                a field name and a local variable name."""
                self.assertRaises(VariableNameError, semantic_analyser.analyse,
                                  'class X { double x; void y(){int x = 5;} }')
        
        def test_if_pass(self):
                """Test no exception thrown when there is a boolean expression 
                in the if statement.
                """
                self.analyse_stmt('if(3 > 1){}')
        
        def test_if_fail(self):
                """Test exception thrown when there is no boolean expression in
                the if statement.
                """
                self.assertRaises(TypeError, self.analyse_stmt, 'if(3 - 1){}')
        
        def test_while_pass(self):
                """Test no exception thrown when there is a boolean expression
                in the while statement.
                """
                self.analyse_stmt('while(3 > 1){}')
        
        def test_while_fail(self):
                """Test exception thrown when there is no boolean expression in
                the while statement.
                """
                self.assertRaises(TypeError, self.analyse_stmt,
                                  'while(3 - 1){}')
        
        def test_for_pass(self):
                """Test no exception thrown when there is a boolean expression
                in the for statement.
                """
                self.analyse_stmt('for(int x = 1; x < 2; x=x+1){}')
        
        def test_for_fail(self):
                """Test exception thrown when there is no boolean expression in
                the for statement.
                """
                self.assertRaises(TypeError, self.analyse_stmt,
                                  'for(int x = 1; x + 2; x=x+1){}')
        
        def test_assign_pass(self):
                """Test no exception thrown when the types of both child nodes
                are equal.
                """
                self.analyse_stmt('int x = 1;')
        
        def test_assign_undeclared_fail(self):
                """Test exception thrown when an assignment is made, but the
                variable has not been initialised.
                """
                self.assertRaises(NotInitWarning, self.analyse_stmt,
                                  'int x; int y = x;')
        
        def test_array_init_pass(self):
                """Test no exception thrown when the type and dimension of the
                array is the same.
                """
                self.analyse_stmt('int arr[] = new int[10];')
        
        def test_array_init_type_fail(self):
                """Test exception thrown when the type of an array
                initialisation is incorrent.
                """
                self.assertRaises(TypeError, self.analyse_stmt,
                                  'int arr[] = new boolean[10];')
        
        def test_array_init_dimension_fail(self):
                """Test exception thrown when the number of dimensions of an
                array initialisation is incorrent.
                """
                self.assertRaises(DimensionsError, self.analyse_stmt,
                                  'int arr[] = new int[10][5];')
        
        def test_array_element_assign_pass(self):
                """Test no exception thrown when the type and dimension of the
                array is the same.
                """
                self.analyse_stmt('int arr[] = new int[10]; arr[1] = 5;')
        
        def test_array_element_assign_type_fail(self):
                """Test exception thrown when the type of an array element
                assignment is incorrent."""
                self.assertRaises(TypeError, self.analyse_stmt,
                                  'int arr[] = new int[10]; arr[1] = "hello";')
        
        def test_array_element_assign_dimension_fail(self):
                """Test exception thrown when the number of dimensions of an
                array element assignment is incorrent.
                """
                self.assertRaises(TypeError, self.analyse_stmt,
                                  'int arr[] = new int[10]; arr[1][2] = 5;')
        
        def test_array_assign_undeclared_fail(self):
                """Test exception thrown when an array element assignment is
                made, but the array is not initialised.
                """
                self.assertRaises(NotInitWarning, self.analyse_stmt,
                                  'int arr[][]; arr[1][2] = 5;')
                
        def test_cond_pass(self):
                """Test no exception thrown when the types of both child nodes
                are boolean.
                """
                self.analyse_stmt('3 < 4 || 3 > 5;')
        
        def test_cond_fail(self):
                """Test exception thrown when the child nodes are not
                boolean.
                """
                self.assertRaises(TypeError, self.analyse_stmt, '5&&6;')
        
        def test_eq_pass(self):
                """Test no exception thrown when the types of both child nodes
                are equal.
                """
                self.analyse_stmt('"hi" != "hello";')
        
        def test_eq_fail(self):
                """Test exception thrown when the child nodes are not equal."""
                self.assertRaises(TypeError, self.analyse_stmt, '3 == true;')
        
        def test_relational_pass(self):
                """Test no exception thrown when the types of both child nodes
                are int.
                """
                self.analyse_stmt('3 <= 4;')
        
        def test_relational_fail(self):
                """Test exception thrown when the child nodes are not int."""
                self.assertRaises(TypeError, self.analyse_stmt, 'true > "x";')
        
        def test_additive_pass(self):
                """Test no exception thrown when the types of both child nodes
                are int.
                """
                self.analyse_stmt('2-1;')
        
        def test_additive_fail(self):
                """Test exception thrown when the child nodes are not int."""
                self.assertRaises(TypeError, self.analyse_stmt, 'true+"x";')
        
        def test_concat_pass(self):
                """Test that two strings can be concatenated."""
                self.analyse_stmt('"Hell" + "o";')
        
        def test_concat_fail(self):
                """Test that an error is thrown when a string is concatenated
                with a non string.
                """
                self.assertRaises(TypeError, self.analyse_stmt, '"Hell" + 1;')
        
        def test_mult_pass(self):
                """Test no exception thrown when the types of both child nodes
                are int.
                """
                self.analyse_stmt('2*1;')
        
        def test_mult_fail(self):
                """Test exception thrown when the child nodes are not int."""
                self.assertRaises(TypeError, self.analyse_stmt, 'true/"x";')
        
        def test_not_pass(self):
                """Test no exception thrown when the type of the child node is
                boolean.
                """
                self.analyse_stmt('!true;')
        
        def test_not_fail(self):
                """Test exception thrown when the child node is not boolean."""
                self.assertRaises(TypeError, self.analyse_stmt, '!3;')
        
        def test_neg_pass(self):
                """Test no exception thrown when the type of the child node is
                int.
                """
                self.analyse_stmt('-1;')
        
        def test_neg_fail(self):
                """Test exception thrown when the child node is not int."""
                self.assertRaises(TypeError, self.analyse_stmt, '-"x";')
        
        def test_inc_pass(self):
                """Test no exception thrown when the type of the child node is
                int.
                """
                self.analyse_stmt('1++;')
        
        def test_dec_fail(self):
                """Test exception thrown when the child node is not int."""
                self.assertRaises(TypeError, self.analyse_stmt, '--"x";')
        
        # The next section tests the implicit conversion of numerical primitive 
        # data types
        # It would take many tests to test this exaustively, so a representative
        # subset of the possibilities is tested below
        
        def test_convert_char_int(self):
                """Test a char can be multiplied by an int and the * node's type
                becomes int.
                """
                node = self.analyse_stmt("'a'*1;")
                self.assertEqual(self.get_type_node(node), "int")
        
        def test_convert_int_long(self):
                """Test an int can be divided by a long and the / node's type
                becomes long.
                """
                node = self.analyse_stmt('100/10L;')
                self.assertEqual(self.get_type_node(node), "long")

        def test_convert_long_float(self):
                """Test a long can be added to a float and the + node's type
                becomes float.
                """
                node = self.analyse_stmt('1L+10F;')
                self.assertEqual(self.get_type_node(node), "float")

        def test_convert_int_double(self):
                """Test a float can be subtracted by a double and the - node's
                type becomes double.
                """
                node = self.analyse_stmt('10-5.5D;')
                self.assertEqual(self.get_type_node(node), "double")
        
        ## HELPER METHODS ##
        
        def analyse_stmt(self, stmt):
                """Helper method used so that single line code can be tested
                with having to declared a class and method for it to go in.
                """
                return semantic_analyser.analyse("""
                                                  class X {
                                                        void x() {
                                                                """ +
                                                                stmt +
                                                                """
                                                        }
                                                  }
                                                 """)
        
        def analyse_file(self, file_name):
                """Helper method to allow the semantic analyser to be run on a
                particular file in the test_files folder.
                """
                path = os.path.join(self.file_dir, file_name)
                return semantic_analyser.analyse(path)
        
        def get_type_node(self, root):
                """Helper method for use by the conversion tests to get the
                type node from the AST.
                Must get the correct child of these nodes:
                class
                class_body
                method_dcl
                block
                <numerical op node>
                <the left child of that>
                """
                block_node = root[0][0].children[3].children[0].children[3]
                return block_node.children[0].type_