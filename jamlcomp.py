"""This allows the program to be run.  It will either compile the file, or
print error information.

Usage: jamlcomp <file> [<output directory>]
"""
import sys
from code_generation.code_generator import CodeGenerator

if __name__ == '__main__':
        try:
                if len(sys.argv) == 2:
                        CodeGenerator().compile_(sys.argv[1])
                elif len(sys.argv) == 3:
                        CodeGenerator().compile_(sys.argv[1], sys.argv[2])
                else:
                        print 'Usage: jamlcomp <file> [<output directory>]'
        except Exception as error:
                print 'Compilation error! Message: "' + error + '"'