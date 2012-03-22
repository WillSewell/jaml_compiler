from code_generation.code_generator import CodeGenerator
#from semantic_analysis import semantic_analyser
#from parser_ import parser_

if __name__ == '__main__':
#        print parser_.parse(r"N:\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_extends_pass.jml")
#        print parser_.parse(r"N:\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_extends_pass.jml")

#        print semantic_analyser.analyse('class X { final short y = 5; void x(){y=5;}}')
#        print semantic_analyser.analyse(r'N:\workspace\jaml_compiler\semantic_analysis\semantic_analysis_test\test_files\test_method_call_super_pass.jml')[0]
        
        CodeGenerator().compile_('class X {void x(){PrintStream ps = System.out; ps.println(10);}}')
#        CodeGenerator().compile_(r"C:\Users\Will\workspace\jaml_compiler\jaml_files\jaml\TestArray.jml")