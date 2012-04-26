from code_generation.code_generator import CodeGenerator
#from semantic_analysis.semantic_analyser import TypeChecker
#from parser_ import parser_

def wrap_print(stmt):
    return ("""
        PrintStream ps = System.out;
        ps.println(""" + stmt + """);
        """)

if __name__ == '__main__':
#    print parser_.parse('x ~ 1 , 5 ~', 'matrix_element')
#    print parser_.parse(r"N:\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_extends_pass.jml")

#    print TypeChecker().analyse('class X {void x(){Runnable x = new Thread();  'x.run();}}')
#    print TypeChecker().analyse(r'\\smbhome.uscs.susx.ac.uk\wjs25\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_object_creator_fail.jml')[0]

#    CodeGenerator().compile_('class X {  X() {}static void main(String[] args){matrix A = |}}')
    CodeGenerator().compile_(r'C:\Users\Will\workspace\jaml_compiler\jaml_files\jaml\Perceptron.jml')