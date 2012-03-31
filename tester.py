from code_generation.code_generator import CodeGenerator
#from semantic_analysis.semantic_analyser import TypeChecker
#from parser_ import parser_

def wrap_print(stmt):
        return ("""
                PrintStream ps = System.out;
                ps.println(""" + stmt + """);
                """)

if __name__ == '__main__':
#        print parser_.parse(r"N:\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_extends_pass.jml")
#        print parser_.parse(r"N:\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_extends_pass.jml")

#        print TypeChecker().analyse('class X { final static short y = 5; static void x(){y--;}}')
#        print TypeChecker().analyse(r'\\smbhome.uscs.susx.ac.uk\wjs25\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_object_creator_fail.jml')[0]
        
#        CodeGenerator().compile_()
        CodeGenerator().compile_(r'\\smbhome.uscs.susx.ac.uk\wjs25\workspace\jaml_compiler\code_generation\code_generation_test\test_files\test_field_ref_static.jml')