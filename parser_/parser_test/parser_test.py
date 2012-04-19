"""The test class for the module yapps_parser.py."""
import unittest
from parser_.parser_ import Parser
import parser_.tree_nodes as nodes

class TestParser(unittest.TestCase):
    """Test class where tests to be run are the methods."""
    # First tests are for the lexer
    def test_id_mixed_case_num(self):
        """Test mixed case IDs with numbers and an underscore."""
        # Error will be thrown if iDEntif1er_ is not recognised as an ID
        output = Parser('primary').run_parser('iDEntif1er_')
        # Check it is an ID
        self.assertEqual(output[0].value, 'iDEntif1er_')

    def test_id_whitespace(self):
        """Whitespace should be ignored, check no error thrown."""
        output = Parser('primary').run_parser('  iDEntif1er ')
        # Check whitespace removed
        self.assertEqual(output[0].value, "iDEntif1er")

    def test_id_start_with_upper(self):
        """Test ID recognised when it starts with an upper case letter.
        """
        Parser('primary').run_parser('Hi')

    def test_id_contains_reserved_word(self):
        """ Test that ID is still recognised when it contains a
        reserved word.
        """
        Parser('primary').run_parser('whiler')

    def test_id_error_reserved_word(self):
        """Test an exception is thrown when a reserved word is used as
        an ID.
        """
        self.assertRaises(SystemExit, Parser('primary').run_parser,
                  'while')

    def test_id_error_start_with_num(self):
        """Test exception thrown when ID starts with a number."""
        self.assertRaises(SystemExit, Parser('primary').run_parser,
                  '1test')

    # NOTE - Newer version of PyUnit now has assertIsInstance(), for now we
    # must make do with self.assertTrue(isinstance())
    def test_int_recognised(self):
        """Test that integer is recognised."""
        node = Parser('literal').run_parser('1234')
        self.assertTrue(isinstance(node[0], nodes.IntLNode))

    def test_long_recognised(self):
        """Test that longs are recognised."""
        node = Parser('literal').run_parser('1234L')
        self.assertTrue(isinstance(node[0], nodes.LongLNode))

    def test_float_recognised(self):
        """Test that floats are recognised."""
        node = Parser('literal').run_parser('1234f')
        self.assertTrue(isinstance(node[0], nodes.FloatLNode))

    def test_double_recognised(self):
        """Test that doubles are recognised."""
        node = Parser('literal').run_parser('12.34D')
        self.assertTrue(isinstance(node[0], nodes.DoubleLNode))

    def test_double_recognised_no_d(self):
        """Test that doubles are recognised when the literal has a
        decimal point, but no 'd' or 'D'.
        """
        node = Parser('literal').run_parser('12.34')
        self.assertTrue(isinstance(node[0], nodes.DoubleLNode))

    def test_string_recognised(self):
        """Test that strings are recognised"""
        node = Parser('literal').run_parser('"this IS a string 123"')
        self.assertTrue(isinstance(node[0], nodes.StringLNode))

    def test_char_recognised(self):
        """Test that chars are recognised."""
        node = Parser('literal').run_parser("'x'")
        self.assertTrue(isinstance(node[0], nodes.CharLNode))

    def test_bool_recognised(self):
        """Test that boolean literals are recognised."""
        node = Parser('literal').run_parser('true')
        # Check the node is a boolean
        self.assertTrue(isinstance(node[0], nodes.BooleanLNode))

    def test_nl_tab(self):
        """Test new lines and tabs are correctly ignored."""
        Parser('block').run_parser('{x\n\r=\t\t2\n;}')

    ########################################################################
    ## TEST PARSER RULES
    ##
    ## Where there are multiple rules with the same LHS, and the starting
    ## rule is one of thse, the first of those rules that appears in the
    ## is used by the parser generator.  This is why, when on of these rules
    ## needs to be used that isn't the first one, the block statement is
    ## used as the firt node.
    ########################################################################

    # It was considered unecessary to explicitly test things like simple
    # class definitions / methods since these all must work aleady for the
    # other tests to pass

    def test_class_extends(self):
        """Test a class which extends another is correctly parsed."""
        node_ids = [nodes.ClassNode, nodes.IdNode, nodes.ExtendsNode,
                nodes.EmptyNode, nodes.EmptyNode]
        node = Parser().run_parser('class X extends Y {}')
        self.check_ast(node, node_ids, 0)

    def test_class_implements(self):
        """Test a class which implements an interface is correctly
        parsed.
        """
        node_ids = [nodes.ClassNode, nodes.IdNode, nodes.EmptyNode,
                nodes.ImplementsListNode, nodes.ImplementsNode,
                nodes.EmptyNode]
        node = Parser().run_parser('class X implements Y {}')
        self.check_ast(node, node_ids, 0)

    def test_class_multi_implements(self):
        """Test a class which implements more than one
        interface is correctly parsed.
        """
        node_ids = [nodes.ClassNode, nodes.IdNode, nodes.EmptyNode,
                nodes.ImplementsListNode, nodes.ImplementsNode,
                nodes.ImplementsNode, nodes.EmptyNode]
        node = Parser().run_parser('class X implements Y, Z {}')
        self.check_ast(node, node_ids, 0)

    def test_class_extends_implements(self):
        """Test a class which extends a class and implements and
        interface is correctly parsed.
        """
        node_ids = [nodes.ClassNode, nodes.IdNode, nodes.ExtendsNode,
                nodes.ImplementsListNode, nodes.ImplementsNode,
                nodes.EmptyNode]
        node = Parser().run_parser('class X extends Y implements Z{}')
        self.check_ast(node, node_ids, 0)

    def test_class_modifier(self):
        """Test that a class modifier is correctly added."""
        node = Parser().run_parser('abstract class X {}')
        self.assertEqual(node[0].modifiers, ['abstract'])

    def test_interface(self):
        """Test an interface definition with an abstract method."""
        node_ids = [nodes.InterfaceNode, nodes.IdNode, nodes.EmptyNode,
                nodes.InterfaceBodyNode, nodes.AbsMethodDclNode,
                nodes.IdNode, nodes.ClassTypeNode,
                nodes.ParamListNode, nodes.ParamDclNode,
                nodes.ClassTypeNode, nodes.IdNode]
        node = Parser().run_parser('interface X {Type X(Type2 y);}')
        self.check_ast(node, node_ids, 0)
        
    def test_field_modifier(self):
        """Test that field modifiers are correctly added."""
        node = Parser().run_parser('class X { ' +
                       'private static final int x;}')
        self.assertEqual(node[0].children[3].children[0].modifiers,
                 ['private', 'static', 'final'])
    
    def test_field_assignment(self):
        """Test that a field with assignment parses."""
        node_ids = [nodes.ClassNode, nodes.IdNode, nodes.EmptyNode,
                nodes.EmptyNode, nodes.ClassBodyNode,
                nodes.FieldDclAssignNode, nodes.TypeNode,
                nodes.AssignNode, nodes.IdNode, nodes.IntLNode]
        node = Parser().run_parser('class X { static final int x = 5;}')
        self.check_ast(node, node_ids, 0)
    
    def test_constructor(self):
        """Test a constructor is correctly parsed."""
        node_ids = [nodes.ClassNode, nodes.IdNode, nodes.EmptyNode,
                nodes.EmptyNode, nodes.ClassBodyNode,
                nodes.ConstructorDclNode, nodes.IdNode,
                nodes.ParamListNode, nodes.ParamDclNode,
                nodes.TypeNode, nodes.IdNode, nodes.EmptyNode]
        node = Parser().run_parser('class X {X(int y){}}')
        self.check_ast(node, node_ids, 0)

    def test_method_array(self):
        """Test that a method that returns an array is correctly parsed.
        """
        node_ids = [nodes.MethodDclArrayNode, nodes.IdNode,
                nodes.TypeNode, nodes.DimensionsNode,
                nodes.ParamListNode, nodes.ParamDclNode,
                nodes.TypeNode, nodes.IdNode,
                nodes.ParamDclNode, nodes.TypeNode,
                nodes.IdNode, nodes.EmptyNode]
        node = Parser('method_dcl').run_parser('byte[][] ' +
                               'X(int x, char z){}')
        self.check_ast(node, node_ids, 0)

    def test_method_param_array(self):
        """Test the case where a method has an array parameter is
        correctly parsed.
        """
        node_ids = [nodes.MethodDclNode, nodes.IdNode,
                nodes.TypeNode, nodes.ParamListNode,
                nodes.ParamDclNode, nodes.TypeNode,
                nodes.ArrayDclNode, nodes.ArrayIdNode,
                nodes.DimensionsNode, nodes.EmptyNode]
        node = Parser('method_dcl').run_parser('byte X(int x[][][]) {}')
        self.check_ast(node, node_ids, 0)
    
    def test_abstract_method(self):
        """Test an abstract method in a class."""
        node = Parser().run_parser('abstract class X { ' +
                     'abstract int x();}')[0]
        self.assertTrue(isinstance(node.children[3].children[0],
                       nodes.AbsMethodDclNode))
    
    def test_method_modifier(self):
        """Test that field modifiers are correctly added."""
        node = Parser().run_parser('class X { ' +
                       'final static int x(){}}')[0]
        self.assertEqual(node.children[3].children[0].modifiers,
                 ['final', 'static'])

    def test_empty_block_stmt(self):
        """Test an empty block statement parses."""
        node_ids = [nodes.EmptyNode]
        node = Parser('block').run_parser('{}')
        # Check there are no children of the block
        self.check_ast(node, node_ids, 0)


    def test_var_dcl_simple(self):
        """Test a simple variable declaration statement parses."""
        # Note: Generally all parser tests will work like so:
        # Create a list of types of nodes one should see in the AST,
        # in the order they would appear from a pre order tree traversal
        node_ids = [nodes.BlockNode, nodes.VarDclNode, nodes.TypeNode,
                nodes.IdNode]
        # Parse the Java code
        node = Parser('block').run_parser('{int x;}')
        # Check the AST against the list of node_ids
        self.check_ast(node, node_ids, 0)

    def test_var_dcl_comp(self):
        """Test the variable declaration statement with assignment."""
        node_ids = [nodes.BlockNode, nodes.VarDclAssignNode,
                nodes.TypeNode, nodes.AssignNode, nodes.IdNode,
                nodes.IntLNode]
        node = Parser('block').run_parser('{int x = 10;}')
        self.check_ast(node, node_ids, 0)

    def test_array_dcl(self):
        """Test a simple array declartion."""
        node_ids = [nodes.BlockNode, nodes.VarDclNode, nodes.TypeNode,
                nodes.ArrayDclNode, nodes.ArrayIdNode,
                nodes.DimensionsNode]
        node = Parser('block').run_parser('{int x[];}')
        self.check_ast(node, node_ids, 0)

    def test_array_init(self):
        """Test an array declaration with an initialisation."""
        node_ids = [nodes.BlockNode, nodes.VarDclAssignNode,
                nodes.TypeNode, nodes.AssignNode,
                nodes.ArrayDclNode, nodes.ArrayIdNode,
                nodes.DimensionsNode, nodes.ArrayInitNode,
                nodes.TypeNode, nodes.IntLNode, nodes.AddNode,
                nodes.IntLNode, nodes.IntLNode]
        node = Parser('block').run_parser('{boolean x[][] = ' +
                          'new boolean[5][10-1];}')
        self.check_ast(node, node_ids, 0)
    
    def test_matrix_init(self):
        """Test an matrix declaration with an initialisation."""
        node_ids = [nodes.BlockNode, nodes.VarDclAssignNode,
                nodes.TypeNode, nodes.AssignNode, nodes.IdNode,
                nodes.MatrixInitNode, nodes.IntLNode,
                nodes.AddNode, nodes.IntLNode, nodes.IntLNode]
        node = Parser('block').run_parser('{matrix x = |5, 10-1|;}')
        self.check_ast(node, node_ids, 0)

    def test_stmt_empty(self):
        """Test the case where there is an empy line of code."""
        node_ids = [nodes.BlockNode, nodes.EmptyNode]
        node = Parser('block').run_parser('{;}')
        self.check_ast(node, node_ids, 0)

    def test_stmt_expr(self):
        """Test for the case where there is just one, simple,
        expression.
        """
        node_ids = [nodes.BlockNode, nodes.AssignNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x = y;}')
        self.check_ast(node, node_ids, 0)

    def test_if_stmt(self):
        """Test a simple if statement."""
        node_ids = [nodes.IfNode, nodes.RelNode, nodes.IdNode,
                nodes.IdNode, nodes.BlockNode, nodes.AddNode,
                nodes.IdNode, nodes.IntLNode]
        node = Parser('if_stmt').run_parser('if (x > y) {x - 1;}')
        self.check_ast(node, node_ids, 0)

    def test_if_else_stmt(self):
        """Test an if statement with an else clause."""
        node_ids = [nodes.BlockNode, nodes.IfNode, nodes.RelNode,
                nodes.IdNode, nodes.IdNode, nodes.BlockNode,
                nodes.AddNode, nodes.IdNode, nodes.IntLNode,
                nodes.BlockNode,nodes.AddNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{if (x > y) {x - 1;} ' +
                          'else {x - y;}}')
        self.check_ast(node, node_ids, 0)

    def test_nested_if_stmts(self):
        """Test two nested if statements."""
        node_ids = [nodes.BlockNode, nodes.IfNode, nodes.RelNode,
                nodes.IdNode, nodes.IdNode, nodes.BlockNode,
                nodes.AddNode, nodes.IdNode, nodes.IntLNode,
                nodes.IfNode, nodes.EqNode, nodes.IdNode,
                nodes.IntLNode, nodes.BlockNode,
                nodes.AssignNode, nodes.IdNode,
                nodes.IntLNode, nodes.BlockNode,
                nodes.AddNode, nodes.IdNode, nodes.IntLNode]
        node = Parser('block').run_parser('{if (x > y) {x - 1;} ' +
                          'else if (y == 3){y = 3;} ' +
                          'else{y + 2;}}')
        self.check_ast(node, node_ids, 0)

    def test_while_stmt(self):
        """Test a while statement, also test with no whitespace in the
        code.
        """
        node_ids = [nodes.WhileNode, nodes.EqNode, nodes.IdNode,
                nodes.IntLNode, nodes.BlockNode,
                nodes.AddNode, nodes.IdNode, nodes.IntLNode]
        node = Parser('while_stmt').run_parser('while(x==1){x+10;}')
        self.check_ast(node, node_ids, 0)

    def test_for_stmt(self):
        """Test a regular for statement."""
        node_ids = [nodes.ForNode, nodes.VarDclAssignNode,
                nodes.TypeNode, nodes.AssignNode, nodes.IdNode,
                nodes.IntLNode, nodes.RelNode, nodes.IdNode,
                nodes.IntLNode, nodes.IncNode, nodes.IdNode,
                nodes.BlockNode, nodes.AddNode, nodes.IdNode,
                nodes.IntLNode]
        node = Parser('for_stmt').run_parser('for (int x = 1; ' +
                             'x < 2; x++){y + 1;}')
        self.check_ast(node, node_ids, 0)

    def test_assign(self):
        """Test a simple assigment expression."""
        node_ids = [nodes.BlockNode, nodes.AssignNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x = y;}')
        self.check_ast(node, node_ids, 0)    

    def test_array_assign(self):
        """Test an array initialisation."""
        node_ids = [nodes.BlockNode, nodes.AssignNode, nodes.IdNode,
                nodes.ArrayInitNode, nodes.TypeNode,
                nodes.IntLNode]
        node = Parser('block').run_parser('{x = new float[5];}')
        self.check_ast(node, node_ids, 0)

    def test_array_element_assign(self):
        """Test an assignment of an array element."""
        node_ids = [nodes.BlockNode, nodes.AssignNode,
                nodes.ArrayElementNode, nodes.IdNode,
                nodes.IntLNode, nodes.IntLNode,
                nodes.BooleanLNode]
        node = Parser('block').run_parser('{x[4][5] = true;}')
        self.check_ast(node, node_ids, 0)
    
    def test_matrix_assign(self):
        """Test an matrix initialisation."""
        node_ids = [nodes.BlockNode, nodes.AssignNode, nodes.IdNode,
                nodes.MatrixInitNode, nodes.IntLNode,
                nodes.IntLNode]
        node = Parser('block').run_parser('{x = |5, 5|;}')
        self.check_ast(node, node_ids, 0)

    def test_matrix_element_assign(self):
        """Test an assignment of an matrix element."""
        node_ids = [nodes.BlockNode, nodes.AssignNode,
                nodes.MatrixElementNode, nodes.IdNode,
                nodes.IntLNode, nodes.IntLNode, nodes.IntLNode]
        node = Parser('block').run_parser('{x|1 , 5| = 5;}')
        self.check_ast(node, node_ids, 0)

    def test_cond_expr(self):
        """Test a simple conditional expression."""
        node_ids = [nodes.BlockNode, nodes.CondNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x || y;}')
        self.check_ast(node, node_ids, 0)

    def test_eq_expr(self):
        """Test a simple equality expression."""
        node_ids = [nodes.BlockNode, nodes.EqNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x != y;}')
        self.check_ast(node, node_ids, 0)

    def test_rel_expr(self):
        """Test a simple relation expression."""
        node_ids = [nodes.BlockNode, nodes.RelNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x >= y;}')
        self.check_ast(node, node_ids, 0)

    def test_add_expr(self):
        """Test a simple additive expression."""
        node_ids = [nodes.BlockNode, nodes.AddNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x + y;}')
        self.check_ast(node, node_ids, 0)

    def test_mul_expr(self):
        """Test a simple multiplicative expression."""
        node_ids = [nodes.BlockNode, nodes.MulNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x / y;}')
        self.check_ast(node, node_ids, 0)

    def test_unary_expr(self):
        """Test a simple unary expression with a additive expression to
        check a proper distinction is made.
        """
        node_ids = [nodes.BlockNode, nodes.AddNode, nodes.PosNode,
                nodes.IntLNode, nodes.IntLNode]
        node = Parser('block').run_parser('{-1 + 2;}')
        self.check_ast(node, node_ids, 0)

    def test_unary_expr_prefix(self):
        """Test the unary expression where a minus sign prefixes the
        literal.
        """
        node_ids = [nodes.BlockNode, nodes.PosNode,
                nodes.IntLNode]
        node = Parser('block').run_parser('{-1;}')
        self.check_ast(node, node_ids, 0)

    def test_unary_expr_inc_prefix(self):
        """Test the unary expression where an increment operator
        prefixes the literal.
        """
        node_ids = [nodes.BlockNode, nodes.IncNode,
                nodes.IntLNode]
        node = Parser('block').run_parser('{++1;}')
        self.check_ast(node, node_ids, 0)

    def test_unary_expr_dec_suffix(self):
        """Test the unary expression where a decrement operator suffixes
        the unary expression.
        """
        node_ids = [nodes.BlockNode, nodes.IncNode,
                nodes.IntLNode]
        node = Parser('block').run_parser('{1--;}')
        self.check_ast(node, node_ids, 0)

    def test_paran(self):
        """Test a primary production, which involves testing
        parenthesis/precedence.
        """
        node_ids = [nodes.BlockNode, nodes.MulNode, nodes.MulNode,
                nodes.IdNode, nodes.AddNode, nodes.IdNode,
                nodes.IdNode, nodes.AddNode, nodes.IdNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{x * (y + z) * (y - x);}')
        self.check_ast(node, node_ids, 0)

    def test_method_call_long(self):
        """Test a call to a method in another class parses."""
        node_ids = [nodes.BlockNode, nodes.MethodCallLongNode,
                nodes.IdNode, nodes.IdNode, nodes.EmptyNode]
        node = Parser('block').run_parser('{x.y();}')
        self.check_ast(node, node_ids, 0)
    
    def test_method_call_super(self):
        """Test a call to a method in the super class."""
        node_ids = [nodes.BlockNode, nodes.MethodCallSuperNode,
                nodes.IdNode, nodes.ArgsListNode, nodes.IdNode]
        node = Parser('block').run_parser('{super.y(x);}')
        self.check_ast(node, node_ids, 0)
    
    def test_field_ref(self):
        """Test a reference to a field in another class."""
        node_ids = [nodes.BlockNode, nodes.FieldRefNode,
                nodes.IdNode, nodes.IdNode]
        node = Parser('block').run_parser('{x.y;}')
        self.check_ast(node, node_ids, 0)
    
    def test_field_ref_super(self):
        """Test a reference to a field in the super class."""
        node_ids = [nodes.BlockNode, nodes.FieldRefSuperNode,
                nodes.IdNode]
        node = Parser('block').run_parser('{super.y;}')
        self.check_ast(node, node_ids, 0)
        
    def check_ast(self, nodel, node_types, index):
        """Checks the ast against the node ids provided.

        node is the current root of the tree.
        node_ids is the list of node_ids the tree should contain,
        in pre-order.
        index is the number of nodes visit so far, and the index into
        the list of node_ids.
        """
        # Remove the node from the list it will be in
        node = nodel[0]
        self.check_ast_rest(node, node_types, index)

    def check_ast_rest(self, node, node_types, index):
        """Pre order traversal of the AST, checking each node's node_id
        as they are visited."""
        self.assertTrue(isinstance(node, node_types[index]))
        try:
            # Recursively call the method for each children
            children = node.children
            for child in children:
                index += 1
                index = self.check_ast_rest(child,
                                node_types,
                                index)
        except AttributeError:
            # It was a leaf node; without children
            pass
        return index