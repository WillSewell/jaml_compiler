import sys
from code_generation.code_generator import CodeGenerator
from interpreter.interpreter import Interpreter

if __name__ == "__main__":
	if len(sys.argv) == 3:
		if sys.argv[1] == "-i":
			Interpreter().run_interpreter(sys.argv[2])
		elif sys.argv[1] == "-c":
			CodeGenerator().compile(sys.argv[2])
		else:
			print 'First argument must be either "-i" or "-c"'
	else:
		print "Usage: jamlcomp <-i | -c> <file>"
	