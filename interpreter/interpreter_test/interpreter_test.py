"""The test class for the module interpreter.py."""
import os
import sys
import cStringIO
import unittest
from interpreter.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
	"""Test class where tests to be run are the methods."""
	# Get an interpreter object for convenience
	inter = Interpreter()
	
	def test_var_dcl(self):
		"""Test variable declarations."""
		p = "{int x = 1; print x;}"
		self.check_output(p, "1")
	
	def test_if(self):
		"""Test a simple if statement."""
		p = '{int x = 2; if (x > 2) {print "fail";} else {print "pass";}}'
		self.check_output(p, "pass")
	
	def test_nested_if(self):
		"""Test nested if statements."""
		p = '{string s = "hello"; int x = 2; if (x > = 3) {print "fail";} else if (s == "hi") {print "fail2";} else {print "pass";}}'
		self.check_output(p, "pass")
	
	def  test_while(self):
		"""Test a while statement that incriments an int and prints out it's value."""
		p = "{int i = 1; while (i <= 10) {print i; i = i + 1;}}"
		# The \n are needed because each new print statement has a new line character after it
		self.check_output(p, "1\n2\n3\n4\n5\n6\n7\n8\n9\n10")
	
	def  test_for(self):
		"""Test a for loop which loops fice times, each time printing out "s"."""
		p = '{string s = "s"; for (int i = 0; i <5; i = i + 1) {print s;}}'
		self.check_output(p, "s\ns\ns\ns\ns")
	
	def test_or(self):
		"""Test the boolean or oporator by including it in an if statement where only one side is true."""
		p = '{ int x = 1; if (x != 1 || x == 1) { print "pass";}}'
		self.check_output(p, "pass")
		
	def test_and(self):
		"""Test the boolean and oporator by including it in an if statement where both sides are true."""
		p = '{ int x = 1; if (x != 1 && x == 1) { print "fail";} else {print "pass";}}'
		self.check_output(p, "pass")
	
	#Equality and relational oporators already tested in previous tests.
	
	def test_add(self):
		"""Test simple addition in a print statement."""
		p = "{print 1 + 1;}"
		self.check_output(p, "2")
	
	def test_sub(self):
		"""Test simple subtraction in a print statement."""
		p = "{print 1 - 1;}"
		self.check_output(p, "0")
	
	def test_mul(self):
		"""Test simple multiplication in a print statement."""
		p = "{print 2*2;}"
		self.check_output(p, "4")
	
	def test_div(self):
		"""Test simple division in a print statement."""
		p = "{print 4/2;}"
		self.check_output(p, "2")
	
	def test_not(self):
		"""Test that the not oporator inverts the boolean expression: true."""
		p = "{print !true;}"
		self.check_output(p, "False")
	
	def test_neg(self):
		"""Test that the negative oporator makes the expression negative"""
		p = "{print -(2+2);}"
		self.check_output(p, "-4")
	
	def test_pos(self):
		"""Test that the positive oporator has no effect on the expressions sign."""
		p = "{print +(-2);}"
		self.check_output(p, "-2")
	
	def test_inc(self):
		"""Test that the increment oporator increments by 1."""
		p = "{int x = 1; x++; print x;}"
		self.check_output(p, "2")
	
	def test_inc(self):
		"""Test that the decrement oporator decrements by 1."""
		p = "{int x = 1; --x; print x;}"
		self.check_output(p, "0")
	
	def test_brackets(self):
		"""Test precidence rules are followed when parentheses are used."""
		p = "{print (1+1)/1;}"
		self.check_output(p, "2")
	
	def check_output(self, program, exptd_result):
		"""Checks the program was interpreted corrently.
		
		Given a program to run the interpreter on, 
		this method checks the result printed by the interpreter matches the exptd_result.
		"""
		# Used to send print request to StringIO, rather than the terminal - this is so the results can be retrieved later
		import sys
		# Backup old output (the terminal)
		prev_out = sys.stdout
		del sys; import sys
		sys.stdout = cStringIO.StringIO()
		
		# Run the interpreter with the program
		self.inter.run_interpreter(program)
		
		# Get results printed out to the StringIO, remove the trailing new line created by printing
		output = sys.stdout.getvalue().rstrip()
		#Revert the output back to the terminal
		sys.stdout.close()
		sys.stdout = prev_out
		
		#Check the printed results match the expected result
		self.assertEqual(output, exptd_result)