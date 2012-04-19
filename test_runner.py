"""Module to run all the test cases as a single test suite."""
import unittest
from parser_.parser_test.parser_test import TestParser
from semantic_analysis.semantic_analysis_test.semantic_analyser_test \
    import TestSemanticAnalyser
from code_generation.code_generation_test.code_generator_test \
    import TestCodeGenerator

if __name__ == '__main__':
    # Create suites from all test cases
    parser_suite = unittest.makeSuite(TestParser, 'test')
    semantic_analyser_suite = unittest.makeSuite(TestSemanticAnalyser, 
                             'test')
    code_generator_suite = unittest.makeSuite(TestCodeGenerator, 'test')
    # Combine all the suites into one suite
    all_suites = unittest.TestSuite((parser_suite, semantic_analyser_suite,
                     code_generator_suite))
    # Create a runner and use it to run all the tests in all the combined 
    # suites
    runner = unittest.TextTestRunner()
    runner.run(all_suites)