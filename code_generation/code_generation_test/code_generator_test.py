"""The test class for the module code_geenerator.py."""
import os
import subprocess
import unittest
from code_generation.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
        """Test class where tests to be run are the methods."""
        # Get an interpreter object for convenience
        code_gen = CodeGenerator()

        def test_var_dcl(self):
                """Test variable declarations."""
                p = '{int x = 1; print x;}'
                self._check_output(p, '1')
        
        def test_if(self):
                """Test a simple if statement."""
                p = '{int x = 2; if (x > 2) {print "fail";} else {print "pass";}}'
                self._check_output(p, "pass")
        
        def test_nested_if(self):
                """Test nested if statements."""
                p = '{string s = "hello"; int x = 2; if (x > = 3) {print "fail";} else if (s == "hi") {print "fail2";} else {print "pass";}}'
                self._check_output(p, 'pass')
        
        def  test_while(self):
                """Test a while statement that incriments an int and prints out it's value."""
                p = '{int i = 1; while (i <= 10) {print i; i = i + 1;}}'
                # The new lines are needed because each new print statement has a new line character after it
                nl = self.nl
                self._check_output(p, '1' + nl + '2' + nl + '3' + nl + '4' + nl + '5' + nl + '6' + nl + '7' + nl + '8' + nl + '9' + 
                						 nl + '10')
        
        def  test_for(self):
                """Test a for loop which loops fice times, each time printing out "s"."""
                p = '{string s = "s"; for (int i = 0; i <5; i = i + 1) {print s;}}'
                nl = self.nl
                self._check_output(p, 's' + nl + 's' + nl + 's' + nl + 's' + nl + 's')
        
        def test_or(self):
                """Test the boolean or oporator by including it in an if statement where only one side is true."""
                p = '{ int x = 1; if (x != 1 || x == 1) { print "pass";}}'
                self._check_output(p, 'pass')
        
        def test_and(self):
                """Test the boolean and oporator by including it in an if statement where both sides are true."""
                p = '{ int x = 1; if (x != 1 && x == 1) { print "fail";} else {print "pass";}}'
                self._check_output(p, 'pass')
        
        #Equality and relational oporators already tested in previous tests.
        
        def test_add(self):
                """Test simple addition in a print statement."""
                p = self._wrap_stmt('{print 1 + 1;}')
                self._check_output(p, '2')
        
        def test_sub(self):
                """Test simple subtraction in a print statement."""
                p = self._wrap_stmt('{print 1 - 1;}')
                self._check_output(p, '0')
        
        def test_mul(self):
                """Test simple multiplication in a print statement."""
                p = self._wrap_stmt('{print 2*2;}')
                self._check_output(p, '4')
        
        def test_div(self):
                """Test simple division in a print statement."""
                p = self._wrap_stmt('{print 4/2;}')
                self._check_output(p, '2')
        
        def test_not(self):
                """Test that the not operator inverts the boolean expression: true."""
                p = self._wrap_stmt('{print !true;}')
                self._check_output(p, 'false')
        
        def test_neg(self):
                """Test that the negative operator makes the expression negative."""
                p = self._wrap_stmt('{print -(2+2);}')
                self._check_output(p, '-4')
        
        def test_pos(self):
                """Test that the positive operator has no effect on the expression's sign."""
                p = self._wrap_stmt('{print +(-2);}')
                self._check_output(p, '-2')
        
        def test_inc(self):
                """Test that the increment operator increments by 1."""
                p = self._wrap_stmt('{int x = 1; x++; print x;}')
                self._check_output(p, '2')
        
        def test_dec(self):
                """Test that the decrement operator decrements by 1."""
                p = self._wrap_stmt('{int x = 1; --x; print x;}')
                self._check_output(p, '0')
        
        def test_brackets(self):
                """Test precedence rules are followed when parentheses are used."""
                p = self._wrap_stmt('{print (1+1)/1;}')
                self._check_output(p, '2')
        
        def _wrap_print_stmt(self, stmt):
                """Helper method used so that single line code can be tested
                without having to create a class and method for it to go in.
                """
                return ("""
                      class X {
                                void x() {
                                        Console c = System.console();
                                        PrintWriter out = c.writer();
                                        out.println(
                                                """ +
                                                stmt +
                                                """
                                                );
                                }
                     }
                     """)
        
        def _check_output(self, program, exptd_result):
                """Checks the program was compiled correctly.
                
                Given a program to run the compiler on, 
                this method checks the result printed when the JVM is run with the code generator's output.
                """
                # Run the compiler with the program
                self.code_gen.compile_(program, os.path.join(os.path.dirname(__file__), 'bin_test_files'))
                
                # Run the JVM on the compiled file
                file_dir = os.path.join(os.path.dirname(__file__), 'bin_test_files')
                cmd = ['java', '-cp', file_dir, 'Default']
                output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].rstrip(os.linesep)
                
                #Check the printed results match the expected result
                self.assertEqual(output, exptd_result)