"""The test class for the module code_geenerator.py."""
import os
import subprocess
import unittest
from code_generation.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
        """Test class where tests to be run are the methods."""
        def setUp(self):
                unittest.TestCase.setUp(self)
                # Get an interpreter object for convenience
                self._code_gen = CodeGenerator()
                # Get the directory to get test files from
                this_file_path = os.path.dirname(__file__)
                self._file_dir = os.path.join(this_file_path, 'test_files')
        
        def test_extends_field(self):
                """Test a subclass can use a field of a superclass."""
                self._check_output_file('test_extends_field.jml', '10')
        
        def test_extends_method(self):
                """Test a subclass can use a method of a superclass."""
                self._check_output_file('test_extends_method.jml', '10')
        
        def test_invoke_implemented_method(self):
                """Test the case where a class invokes a method of an interface
                which has been instantiated by a class.
                """
                self._check_output_file('test_invoke_implemented_method.jml', '10')
                
        def test_cons_param(self):
                """Test that constructor parameters can be correctly used."""
                p = ('class X { X(String x) {' + self._wrap_print('x') +
                     '} static void main(String[] args) ' +
                     '{X inst = new X("pass");}}')
                self._check_output(p, 'X', 'pass')
        
        def test_method_param(self):
                """Test that method parameters can be correctly used."""
                p = ('class X { void meth(String x){' + self._wrap_print('x') +
                     '} static void main(String[] args) {' +
                     'X inst = new X();inst.meth("pass");}}')
                self._check_output(p, 'X', 'pass')
        
        def test_super_cons_implicitly_invoked(self):
                """Test that the super constructor is implicitly invoked."""
                self._check_output_file('test_super_cons_implicitly_invoked' +
                                        '.jml', 'pass')
        
        def test_super_cons_explicitly_invoked(self):
                """Test that the super classes constructor can be explicitly
                invoked correctly.
                """
                self._check_output_file('test_super_cons_explicitly_invoked' +
                                        '.jml', 'pass')
        
        def test_method_call(self):
                """Test a simple method call to a method in the current class.
                """
                p = ('class X { void meth() { int x = meth2();' +
                     self._wrap_print('x') + '} byte meth2() {return 5;} ' +
                     'static void main(String[] args) {' +
                     'X inst = new X();inst.meth();}}')
                self._check_output(p, 'X', '5')
        
        def test_method_return_array(self):
                """Test a method in the same class correctly returns an array.
                """
                p = ('class X { void meth() { byte[][] x = meth2();' +
                     'int y = x[0][0];' + self._wrap_print('y') +
                     '} byte[][] meth2() { byte[][] arr = new byte[5][5];'
                     'arr[0][0] = 5; return arr;} ' +
                     'static void main(String[] args) {' +
                     'X inst = new X();inst.meth();}}')
                self._check_output(p, 'X', '5')
        
        def test_method_call_external(self):
                """Test that a external method call is correctly compiled."""
                self._check_output_file('test_method_call_external.jml','10.1')
        
        def test_method_call_static(self):
                """Test a static external method call."""
                self._check_output_file('test_method_call_static.jml', '10.0')
        
        def test_private_method_call(self):
                """Test an invocation of a private method in the current class.
                """
                self._check_output('class X { private void meth() {' +
                                   self._wrap_print('10') +
                                   '} static void main(String[] args) {' +
                                   'X inst = new X();inst.meth();}}',
                                   'X', '10')
        
        def test_lib_method_call(self):
                """Test a call to a library class."""
                self._check_output('class X{static void main(String[] args) ' +
                                   '{Integer i = new Integer(5);' +
                                   self._wrap_print('i.intValue()') +
                                   '}}', 'X', '5')
                
        def test_lib_method_call_params(self):
                """Test a call to a library class with parameters."""
                self._check_output('class X {static void main(String[] args)' +
                                   '{String s = new String("pass");' +
                                   self._wrap_print('s.endsWith("s")') +
                                   '}}', 'X', 'true')
                
        def test_lib_method_in_super_call(self):
                """Test a method call to a library object where the method
                is defined in its super class.
                """
                self._check_output('class X{static void main(String[] args){' +
                                   self._wrap_print('Double.isNaN(1.1)') +
                                   '}}', 'X', 'false')
        
        def test_lib_method_call_static(self):
                """Test a static method call. """
                self._check_output('class X {static void main(String[] args)' +
                                   '{GregorianCalendar x = ' +
                                   'new GregorianCalendar();' +
                                   self._wrap_print('x.isLenient()') +
                                   '}}', 'X', 'true')
        
        def test_field_access(self):
                """Test a simple field accessing in the same class."""
                p = ('class X { int f; void meth() { f = 5;' + 
                     self._wrap_print('f') + '} static void main(' +
                     'String[] args) { X inst = new X();inst.meth();}}')
                self._check_output(p, 'X', '5')
        
        def test_field_inc(self):
                """Test incrementing a field in the current class."""
                p = ('class X { int f; void meth() {f = 5;f++;' + 
                     self._wrap_print('f') + '} static void main(' +
                     'String[] args) {X inst = new X();inst.meth();}}')
                self._check_output(p, 'X', '6')
        
        def test_field_array(self):
                """Test a field of array type correctly compiles."""
                p = ('class X { int[] f; void meth() { f = new int[1];' +
                     'f[0] = 5;' + self._wrap_print('f[0]') + '} ' +
                     'static void main(String[] args) ' +
                     '{ X inst = new X();inst.meth();}}')
                self._check_output(p, 'X', '5')
        
        def test_field_ref_external(self):
                """Test access to an external field."""
                self._check_output_file('test_field_ref_external.jml', 'pass')
        
        def test_field_ref_static(self):
                """Test a reference to a static final field."""
                self._check_output_file('test_field_ref_static.jml', '10.5')
        
        def test_field_ref_super(self):
                """Test a reference to a field in the super class."""
                self._check_output_file('test_field_ref_super.jml', '10')
        
        def test_field_ref_private(self):
                """Test a reference to a private field in the current class."""
                p = ('class X { private int x; X() {x = 10;' +
                     self._wrap_print('x') + '} static void main ' +
                     '(String[] args) { new X();}}')
                self._check_output(p, 'X', '10') 
                
        def test_var_dcl(self):
                """Test variable declarations."""
                p = self._wrap_stmts('int x = 1;' + self._wrap_print('x'))
                self._check_output(p, 'X', '1')
        
        def test_if(self):
                """Test a simple if statement."""
                p = self._wrap_stmts('int x = 2; if (x > 2) {' +
                                     self._wrap_print('"fail"') +
                                     '} else {' + self._wrap_print('"pass"') +
                                     '}')
                self._check_output(p, 'X', "pass")
        
        def test_nested_if(self):
                """Test nested if statements."""
                p = self._wrap_stmts('String s = "hello";' +
                                     'int x = 2; if (x > = 3) {' +
                                     self._wrap_print('"fail"') +
                                     '} else if (s == "hi") {' +
                                     self._wrap_print('"fail2"') +
                                     '} else {' + self._wrap_print('"pass"') +
                                     '}')
                self._check_output(p, 'X', 'pass')
        
        def  test_while(self):
                """Test a while statement that increments an int and prints out
                it's value.
                """
                p = self._wrap_stmts('int i = 1; while (i <= 10) {' +
                                     self._wrap_print('i') + 'i = i + 1;}')
                # The new lines are needed because each new print statement has
                # a new line character after it
                nl = os.linesep
                self._check_output(p, 'X', '1' + nl + '2' + nl + '3' + nl +
                                   '4' + nl + '5' + nl + '6' + nl + '7' + nl +
                                   '8' + nl + '9' + nl + '10')
        
        def  test_for(self):
                """Test a for loop which loops five times, each time printing
                out "s".
                """
                p = self._wrap_stmts('String s = "s"; ' +
                                     'for (int i = 0; i <5; i = i + 1) {' +
                                     self._wrap_print('s') + '}')
                nl = os.linesep
                self._check_output(p, 'X', 's' + nl + 's' + nl + 's' + nl +
                                   's' + nl + 's')
        
        def test_or(self):
                """Test the boolean or operator by including it in an if
                statement where only one side is true.
                """
                p = self._wrap_stmts('int x = 1; if (x != 1 || x == 1) {' +
                                     self._wrap_print('"pass"') + '}')
                self._check_output(p, 'X', 'pass')
        
        def test_and(self):
                """Test the boolean and operator by including it in an if
                statement where both sides are true.
                """
                p = self._wrap_stmts('int x = 1; if (x != 1 && x == 1) {'
                                     + self._wrap_print('"fail"') +
                                     '} else {' + self._wrap_print('"pass"') +
                                     '}')
                self._check_output(p, 'X', 'pass')
        
        #Equality and relational operators already tested in previous tests.
        
        def test_add(self):
                """Test simple addition in a print statement."""
                p = self._wrap_stmts(self._wrap_print('1 + 1'))
                self._check_output(p, 'X', '2')
        
        def test_concat(self):
                """Test concatination of two strings."""
                p = self._wrap_stmts(self._wrap_print('"fst" + "snd"'))
                self._check_output(p, 'X', 'fstsnd')
        
        def test_sub(self):
                """Test simple subtraction in a print statement."""
                p = self._wrap_stmts(self._wrap_print('1 - 1'))
                self._check_output(p, 'X', '0')
        
        def test_mul(self):
                """Test simple multiplication in a print statement."""
                p = self._wrap_stmts(self._wrap_print('2*2'))
                self._check_output(p, 'X', '4')
        
        def test_div(self):
                """Test simple division in a print statement."""
                p = self._wrap_stmts(self._wrap_print('4/2'))
                self._check_output(p, 'X', '2')
        
        def test_not(self):
                """Test that the not operator inverts the boolean expression:
                true.
                """
                p = self._wrap_stmts(self._wrap_print('!true'))
                self._check_output(p, 'X', 'false')
        
        def test_neg(self):
                """Test that the negative operator makes the expression
                negative.
                """
                p = self._wrap_stmts(self._wrap_print('-(2+2)'))
                self._check_output(p, 'X', '-4')
        
        def test_pos(self):
                """Test that the positive operator has no effect on the
                expression's sign.
                """
                p = self._wrap_stmts(self._wrap_print('+(-2)'))
                self._check_output(p, 'X', '-2')
        
        def test_inc(self):
                """Test that the increment operator increments by 1."""
                p = self._wrap_stmts('int x = 1; x++;' + self._wrap_print('x'))
                self._check_output(p, 'X', '2')
        
        def test_dec(self):
                """Test that the decrement operator decrements by 1."""
                p = self._wrap_stmts('int x = 1; --x;' + self._wrap_print('x'))
                self._check_output(p, 'X', '0')
        
        def test_brackets(self):
                """Test precedence rules are followed when parentheses are
                used.
                """
                p = self._wrap_stmts(self._wrap_print('(1+1)/1'))
                self._check_output(p, 'X', '2')
        
        def test_array(self):
                """Test a simple array creation and access."""
                p = self._wrap_stmts('String[] arr = new String[5];' +
                                     'arr[0] = "Hello";' +
                                     self._wrap_print('arr[0]'))
                self._check_output(p, 'X', 'Hello')
        
        def test_multi_array(self):
                """Test creation and access of a multi-dimensional array."""
                p = self._wrap_stmts('int[][][] a = new int[5][10][1];' +
                                     'a[2][1][0] = 10;' +
                                     self._wrap_print('a[2][1][0]'))
                self._check_output(p, 'X', '10')
        
        def test_array_init_loop(self):
                """Test an array being initialised in a for loop and printed
                in a for loop.
                """
                p = self._wrap_stmts('long[] a = new long[5];' +
                                     'for (int i = 0; i < 5; i++) {' +
                                     'a[i] = i;}' +
                                     'for (int j = 4; j >= 0; j--) {' +
                                     self._wrap_print('a[j]') + '}')
                nl = os.linesep
                self._check_output(p, 'X', '4' + nl + '3' + nl + '2' + nl +
                                   '1' + nl + '0')
        
        def test_matrix(self):
                """Test a simple matrix creation and access."""
                p = self._wrap_stmts('matrix m = |1,1|;' +
                                     'm|0,0| = 10.5;' +
                                     self._wrap_print('m|0,0|'))
                self._check_output(p, 'X', '10.5')
        
        def test_matrix_mult(self):
                """Test a matrix multiplication."""
                p = self._wrap_stmts('matrix a1 = |2, 2|;' +
                                     'a1|0,0| = 1;' +
                                     'a1|0,1| = 2;' +
                                     'a1|1,0| = 3;' +
                                     'a1|1,0| = 4;' +
                                     'matrix a2 = |2, 1|;' +
                                     'a2|0,0| = 1;' +
                                     'a2|1,0| = 2;' +
                                     'matrix a3;' +
                                     'a3 = a1 * a2;' +
                                     'PrintStream ps = System.out;' +
                                     'for (int n = 0; n<a1.rowLength; n++) {' +
                                     'for (int o=0; o<a2.colLength;o++) {' +
                                     'ps.println(a3|n,o|);' +
                                     '}}')
                self._check_output(p, 'X', '5.0' + os.linesep + '4.0')
        
        def test_matrix_mult_dimension_error(self):
                """Test an exception is thrown when the inner dimensions do
                not agree.
                """
                p = self._wrap_stmts('matrix a1 = |2, 2|;' +
                                     'a1|0,0| = 1;' +
                                     'a1|0,1| = 2;' +
                                     'a1|1,0| = 3;' +
                                     'a1|1,0| = 4;' +
                                     'matrix a2 = |1, 1|;' +
                                     'a2|0,0| = 1;' +
                                     'matrix a3;' +
                                     'a3 = a1 * a2;')
                self._check_output(p, 'X', 'Exception in thread "main" ' +
                                   'java.lang.ArithmeticException: ' +
                                   'Inner matrix dimensions must match for ' +
                                   'multiplication!' + os.linesep +
                                   '\tat X.main(X.j)', check_error = True)
        
        def test_matrix_add(self):
                """Test a matrix addition."""
                p = self._wrap_stmts('matrix a1 = |2, 2|;' +
                                     'a1|0,0| = 1;' +
                                     'a1|0,1| = 2;' +
                                     'a1|1,0| = 3;' +
                                     'a1|1,1| = 4;' +
                                     'matrix a2 = |2, 2|;' +
                                     'a2|0,0| = 1;' +
                                     'a2|0,1| = 2;' +
                                     'a2|1,0| = 3;' +
                                     'a2|1,1| = 4;' +
                                     'matrix a3;' +
                                     'a3 = a1 + a2;' +
                                     'PrintStream ps = System.out;' +
                                     'for (int n = 0; n<a1.rowLength; n++) {' +
                                     'for (int o=0; o<a2.colLength;o++) {' +
                                     'ps.println(a3|n,o|);' +
                                     '}}')
                nl = os.linesep
                self._check_output(p, 'X', '2.0' + nl + '4.0' + nl + '6.0' +
                                   nl + '8.0')
        
        def test_matrix_add_dimension_error(self):
                """Test an exception is thrown when the dimensions are not the
                same for two matrices when subtracted.
                """
                p = self._wrap_stmts('matrix a1 = |2, 2|;' +
                                     'a1|0,0| = 1;' +
                                     'a1|0,1| = 2;' +
                                     'a1|1,0| = 3;' +
                                     'a1|1,0| = 4;' +
                                     'matrix a2 = |1, 1|;' +
                                     'a2|0,0| = 1;' +
                                     'matrix a3;' +
                                     'a3 = a1 - a2;')
                self._check_output(p, 'X', 'Exception in thread "main" ' +
                                   'java.lang.ArithmeticException: ' +
                                   'Matrix dimensions must be equal for ' +
                                   'addition/subtraction!' + os.linesep +
                                   '\tat X.main(X.j)', check_error = True)
        
        def test_command_line_args(self):
                """Test that command line arguments are correctly read."""
                p = ('class X {' +
                     'static void main(String[] args) {' +
                     self._wrap_print('args[0]') + '}}')
                self._check_output(p, 'X', 'arg', args = ['arg'])
        
        def _wrap_stmts(self, stmts):
                """Helper method used so lines of code can be tested
                without having to create a class and method for it to go in.
                """
                return ("""
                        class X {
                                static void main(String[] args) {
                                        """ +
                                        stmts +
                                        """
                                }
                       }
                       """)
        
        def _wrap_print(self, stmt):
                return ("""
                        PrintStream ps = System.out;
                        ps.println(""" + stmt + """);
                        """)
        
        def _check_output(self, program, class_name, exptd_result, args = [],
                          check_error = False):
                """Checks the program was compiled correctly.
                
                Given a program to run the compiler on, 
                this method checks the result printed when the JVM is run with
                the code generator's output.
                """
                output_dir = os.path.join(os.path.dirname(__file__),
                                          'bin_test_files')
                # Remove any old asm and binary files
                self._cleanup(output_dir)
                # Run the compiler with the program
                self._code_gen.compile_(program, output_dir)
                
                # Run the JVM on the compiled file
                cmd = ['java', '-cp', output_dir, class_name] + args
                process = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                           stderr = subprocess.PIPE)
                output = ''
                if not check_error:
                        output = process.communicate()[0]
                else:
                        output = process.communicate()[1]
                output = output.rstrip(os.linesep)
                
                #Check the printed results match the expected result
                self.assertEqual(output, exptd_result)
                
        def _check_output_file(self, file_name, exptd_result):
                """Helper method to allow the code generator to be run on a
                particular file, and the output checked
                """
                path = os.path.join(self._file_dir, file_name)
                # Remove the .jml extension
                class_name = file_name[:-4]
                return self._check_output(path, class_name, exptd_result)    
            
        def _cleanup(self, dir_):
                """Removes all files in the directory."""
                for file_ in os.listdir(dir_):
                        file_path = os.path.join(dir_, file_)
                        try:
                                os.remove(file_path)
                        except OSError:
                                # It was a Folder
                                pass