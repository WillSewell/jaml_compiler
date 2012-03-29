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
                self._check_output('class X { X(String x) {' +
                                   self._wrap_print('x') +
                                   '} static void main(String[] args) {' +
                                   'X inst = new X("pass");}}', 'X', 'pass')
        
        def test_method_param(self):
                """Test that method parameters can be correctly used."""
                self._check_output('class X { void meth(String x) {' +
                                   self._wrap_print('x') +
                                   '} static void main(String[] args) {' +
                                   'X inst = new X();inst.meth("pass");}}',
                                   'X', 'pass')
        
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
                self._check_output('class X { void meth() {' +
                                   'int x = meth2();' +
                                   self._wrap_print('x') +
                                   '} byte meth2() {return 5;} ' +
                                   'static void main(String[] args) {' +
                                   'X inst = new X();inst.meth();}}',
                                   'X', '5')
        
        def test_method_return_array(self):
                """Test a method in the same class correctly returns an array.
                """
                self._check_output('class X { void meth() {' +
                                   'byte[][] x = meth2();' +
                                   'int y = x[0][0];' + self._wrap_print('y') +
                                   '} byte[][] meth2() {' +
                                   'byte[][] arr = new byte[5][5];'
                                   'arr[0][0] = 5; return arr;} ' +
                                   'static void main(String[] args) {' +
                                   'X inst = new X();inst.meth();}}',
                                   'X', '5')
        
        def test_method_call_external(self):
                """Test that a external method call is correctly compiled."""
                self._check_output_file('test_method_call_external.jml','10.1')
        
        def test_method_call_static(self):
                """Test a static external method call."""
                self._check_output_file('test_method_call_static.jml', '10.0')
        
        def test_private_method_invokation(self):
                """Test an invocation of a private method in the current class.
                """
                self._check_output('class X { private void meth() {' +
                                   self._wrap_print('10') +
                                   '} static void main(String[] args) {' +
                                   'X inst = new X();inst.meth();}}',
                                   'X', '10')

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
        
        def _check_output(self, program, class_name, exptd_result):
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
                cmd = ['java', '-cp', output_dir, class_name]
                popen = subprocess.Popen(cmd, stdout = subprocess.PIPE)
                output = popen.communicate()[0]
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