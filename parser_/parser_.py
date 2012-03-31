import os
from spark import GenericParser
from scanner import Scanner
import tree_nodes as nodes

class Parser(GenericParser):
        def __init__(self, start):
                GenericParser.__init__(self, start)

        def p_file(self, args):
                """
                file ::= class_dcl
                file ::= interface_dcl
                """
                return args[0]
        
        def p_class_dcl(self, args):
                """
                class_dcl ::= class_mods class_dcl_rest
                class_dcl ::= class_dcl_rest
                """
                # Used to distinguish between classes with, and without,
                # modifiers
                try:
                        args[1].modifiers = args[0]
                        return args[1]
                except IndexError:
                        return args[0]

        def p_class_dcl_rest(self, args):
                """ class_dcl_rest ::= CLASS ID class_body """
                root = nodes.ClassNode()
                root.add_child(nodes.IdNode(args[1].attr))
                root.add_children([nodes.EmptyNode(), nodes.EmptyNode()])
                root.add_child(args[2])
                return root
        def p_class_dcl_extends_rest(self, args):
                """ class_dcl_rest ::= CLASS ID EXTENDS ID class_body"""
                root = nodes.ClassNode()
                root.add_child(nodes.IdNode(args[1].attr))
                root.add_child(nodes.ExtendsNode(args[3].attr))
                root.add_children([nodes.EmptyNode(), args[4]])
                return root
        def p_class_dcl_implements_rest(self, args):
                """ class_dcl_rest ::= CLASS ID IMPLEMENTS implements class_body"""
                root = nodes.ClassNode()
                root.add_child(nodes.IdNode(args[1].attr))
                root.add_children([nodes.EmptyNode(), args[3], args[4]])
                return root
        def p_class_dcl_extends_implements_rest(self, args):
                """ class_dcl_rest ::= CLASS ID EXTENDS ID IMPLEMENTS implements class_body """
                root = nodes.ClassNode()
                root.add_child(nodes.IdNode(args[1].attr))
                root.add_child(nodes.ExtendsNode(args[3].attr))
                root.add_children([args[5], args[6]])
                return root
        
        def p_class_modifiers(self, args):
                """
                class_mods ::= ABSTRACT
                class_mods ::= FINAL
                """
                # Return the list ['abstract'] or ['final']
                return [args[0].name.lower()]

        def p_implements(self, args):
                """ implements ::= implements_list """
                root = nodes.ImplementsListNode()
                for implements in args[0]:
                        root.add_child(implements)
                return root

        def p_implements_list_base(self, args):
                """ implements_list ::= ID """
                return [nodes.ImplementsNode(args[0].attr)]
        def p_implements_list(self, args):
                """ implements_list ::= implements_list , ID """
                return args[0] + [nodes.ImplementsNode(args[2].attr)]

        def p_class_body(self, args):
                """ class_body ::= { class_body_dcl } """
                root = nodes.ClassBodyNode()
                for dcl in args[1]:
                        root.add_child(dcl)
                return root

        def p_class_body_empty(self, args):
                """ class_body ::= { } """
                root = nodes.EmptyNode()
                return root

        def p_class_body_dcl_constructor_base(self, args):
                """ class_body_dcl ::= constructor_dcl """
                return [args[0]]
        def p_class_body_dcl_method_base(self, args):
                """ class_body_dcl ::= method_dcl """
                return [args[0]]
        def p_class_body_dcl_var_base(self, args):
                """ class_body_dcl ::= field_dcl """
                return [args[0]]
        def p_class_body_dcl_constructor(self, args):
                """ class_body_dcl ::= class_body_dcl constructor_dcl """
                return args[0] + [args[1]]
        def p_class_body_dcl_method(self, args):
                """ class_body_dcl ::= class_body_dcl method_dcl """
                return args[0] + [args[1]]
        def p_class_body_dcl_var(self, args):
                """ class_body_dcl ::= class_body_dcl field_dcl """
                return args[0] + [args[1]]
        
        def p_field_dcl(self, args):
                """
                field_dcl ::= field_mods field_dcl_rest
                field_dcl ::= field_dcl_rest
                """
                try:
                        args[1].modifiers = args[0]
                        return args[1]
                except IndexError:
                        return args[0]
        
        def p_field_dcl_rest(self, args):
                """ field_dcl_rest ::= type ID ; """
                root = nodes.FieldDclNode()
                root.add_children([args[0], nodes.IdNode(args[1].attr)])
                return root
        def p_field_dcl_array1_rest(self, args):
                """ field_dcl_rest ::= type array_brackets ID ; """
                root = nodes.FieldDclNode()
                root.add_child(args[0])
                root.add_child(nodes.create_array_dcl(args[2].attr, args[1]))
                return root
        def p_field_dcl_array2_rest(self, args):
                """ field_dcl_rest ::= type ID array_brackets ; """
                root = nodes.FieldDclNode()
                root.add_child(args[0])
                root.add_child(nodes.create_array_dcl(args[1].attr, args[2]))
                return root

        def p_field_dcl_assign(self, args):
                """ field_dcl_rest ::= type ID ASSIGN_OP literal ; """
                return self._var_dcl_assign_node('field', args)
#        def p_field_dcl_array_init1(self, args):
#                """ field_dcl_rest ::= type array_brackets ID ASSIGN_OP literal ; """
#                return self._var_dcl_array_init_node('field', args)
#        def p_field_dcl_array_init2(self, args):
#                """ field_dcl_rest ::= type ID array_brackets ASSIGN_OP literal ; """
#                return self._var_dcl_array_init_node('field', args)
        
        def p_field_modifiers(self, args):
                """
                field_mods ::= PRIVATE
                field_mods ::= static_final_mods
                field_mods ::= PRIVATE static_final_mods
                """
                # Return the list of modifiers, possibly with private
                try:
                        return [args[0].name.lower()] + args[1]
                except (IndexError, AttributeError):
                        try:
                                return [args[0].name.lower()]
                        except AttributeError:
                                return args[0]
        
        def p_static_final_mods1(self, args):
                """
                static_final_mods ::= FINAL STATIC
                static_final_mods ::= STATIC FINAL
                """
                # These methods are used to return the list of static and/or
                # final modifiers
                return [args[0].name.lower(), args[1].name.lower()]
        def p_static_final_mods2(self, args):
                """
                static_final_mods ::= FINAL
                static_final_mods ::= STATIC
                """
                return [args[0].name.lower()]

        def p_constructor_dcl(self, args):
                """ constructor_dcl ::= ID formal_param block """
                root = nodes.ConstructorDclNode()
                root.add_child(nodes.IdNode(args[0].attr))
                root.add_children(args[1:3])
                return root
        
        def p_method_dcl(self, args):
                """
                method_dcl ::= ABSTRACT abs_method_dcl
                method_dcl ::= method_mods method_dcl_rest
                method_dcl ::= method_dcl_rest
                """
                try:
                        if args[0].name == 'ABSTRACT':
                                return args[1]
                except AttributeError:
                        try:
                                args[1].modifiers = args[0]
                                return args[1]
                        except IndexError:
                                return args[0]

        def p_method_dcl_rest(self, args):
                """
                method_dcl_rest ::= type ID formal_param block
                method_dcl_rest ::= VOID ID formal_param block
                """
                root = nodes.MethodDclNode()
                root.add_child(nodes.IdNode(args[1].attr))
                try:
                        if args[0].name == 'VOID':
                                root.add_child(nodes.TypeNode('void'))
                except AttributeError:
                        root.add_child(args[0])
                root.add_children(args[2:4])
                return root

        def p_method_dcl_array_rest(self, args):
                """
                method_dcl_rest ::= type array_brackets ID formal_param block
                """
                # Like above, but this one returns an array
                root = nodes.MethodDclArrayNode()
                root.add_child(nodes.IdNode(args[2].attr))
                root.add_children([args[0], nodes.DimensionsNode(args[1])])
                root.add_children(args[3:5])
                return root
        
        def p_method_modifiers(self, args):
                """
                method_mods ::= PRIVATE
                method_mods ::= static_final_mods
                method_mods ::= PRIVATE static_final_mods
                """
                # Return the list of modifiers, possibly with private
                try:
                        return [args[0].name.lower()] + args[1]
                except (IndexError, AttributeError):
                        try:
                                return [args[0].name.lower()]
                        except AttributeError:
                                return args[0]

        def p_formal_param1(self, args):
                """ formal_param ::= ( param_list ) """
                root = nodes.ParamListNode()
                for param in args[1]:
                        root.add_child(param)
                return root

        def p_formal_param2(self, args):
                """ formal_param ::= ( ) """
                return nodes.EmptyNode()

        def p_param_list_base(self, args):
                """ param_list ::= type ID """
                root = nodes.ParamDclNode()
                root.add_children([args[0], nodes.IdNode(args[1].attr)])
                return [root]
        def p_param_list_array_base1(self, args):
                """ param_list ::= type array_brackets ID """
                root = nodes.ParamDclNode()
                root.add_child(args[0])
                root.add_child(nodes.create_array_dcl(args[2].attr, args[1]))
                return [root]
        def p_param_list_array_base2(self, args):
                """ param_list ::= type ID array_brackets """
                root = nodes.ParamDclNode()
                root.add_child(args[0])
                root.add_child(nodes.create_array_dcl(args[1].attr, args[2]))
                return [root]
        def p_param_list(self, args):
                """ param_list ::= param_list , type ID """
                root = nodes.ParamDclNode()
                root.add_children([args[2], nodes.IdNode(args[3].attr)])
                return args[0] + [root]
        def p_param_list_array1(self, args):
                """ param_list ::= param_list , type array_brackets ID """
                root = nodes.ParamDclNode()
                root.add_child(args[2])
                root.add_child(nodes.create_array_dcl(args[4].attr, args[3]))
                return args[0] + [root]
        def p_param_list_array2(self, args):
                """ param_list ::= param_list , type ID array_brackets """
                root = nodes.ParamDclNode()
                root.add_child(args[2])
                root.add_child(nodes.create_array_dcl(args[3].attr, args[4]))
                return args[0] + [root]

        def p_block(self, args):
                """ block ::= { block_stmt } """
                root = nodes.BlockNode()
                for stmt in args[1]:
                        root.add_child(stmt)
                return root
        def p_block_empty(self, args):
                """ block ::= { } """
                root = nodes.EmptyNode()
                return root

        def p_block_stmt_base(self, args):
                """ block_stmt ::= stmt """
                return [args[0]]
        def p_block_stmt_var_base(self, args):
                """ block_stmt ::= var_dcl """
                return [args[0]]
        def p_block_stmt_stmt(self, args):
                """ block_stmt ::= block_stmt stmt """
                return args[0] + [args[1]]
        def p_block_stmt_var(self, args):
                """ block_stmt ::= block_stmt var_dcl """
                return args[0] + [args[1]]

        def p_var_dcl_simple(self, args):
                """ var_dcl ::= type ID ; """
                root = nodes.VarDclNode()
                root.add_children([args[0], nodes.IdNode(args[1].attr)])
                return root
        def p_var_dcl_array1(self, args):
                """ var_dcl ::= type array_brackets ID ; """
                root = nodes.VarDclNode()
                root.add_child(args[0])
                root.add_child(nodes.create_array_dcl(args[2].attr, args[1]))
                return root
        def p_var_dcl_array2(self, args):
                """ var_dcl ::= type ID array_brackets ; """
                root = nodes.VarDclNode()
                root.add_child(args[0])
                root.add_child(nodes.create_array_dcl(args[1].attr, args[2]))
                return root

        def p_var_dcl_assign(self, args):
                """ var_dcl ::= type ID ASSIGN_OP expr ; """
                return self._var_dcl_assign_node('local', args)
        def p_var_dcl_array_init1(self, args):
                """ var_dcl ::= type array_brackets ID ASSIGN_OP expr ; """
                return self._var_dcl_array_init_node('local', args)
        def p_var_dcl_array_init2(self, args):
                """ var_dcl ::= type ID array_brackets ASSIGN_OP expr ; """
                return self._var_dcl_array_init_node('local', args)
        
        def _var_dcl_assign_node(self, type_, args):
                root = None
                if type_ == 'field':
                        root = nodes.FieldDclAssignNode()
                elif type_ == 'local':
                        root = nodes.VarDclAssignNode()
                root.add_child(args[0])
                assign_node = nodes.AssignNode()
                assign_node.add_children([nodes.IdNode(args[1].attr), args[3]])
                root.add_child(assign_node)
                return root

        def _var_dcl_array_init_node(self, type_, args):
                root = None
                if type_ == 'field':
                        root = nodes.FieldDclAssignNode()
                elif type_ == 'local':
                        root = nodes.VarDclAssignNode()
                root.add_child(args[0])
                assign_node = nodes.AssignNode()
                array_node = None
                try:
                        array_node = nodes.create_array_dcl(args[1].attr,
                                                            args[2])
                except AttributeError:
                        array_node = nodes.create_array_dcl(args[2].attr,
                                                            args[1])
                assign_node.add_child(array_node)
                assign_node.add_child(args[4])
                root.add_child(assign_node)
                return root

        # For brackets after a type or id in an array declaration, we want to
        # count the number of brackets to get the array dimensions
        def p_array_brackets1(self, args):
                """ array_brackets ::= array_brackets [ ] """
                return args[0] + 1
        def p_array_brackets2(self, args):
                """ array_brackets ::= [ ] """
                return 1

        def p_type(self, args):
                """
                type ::= ID
                type ::= TYPE
                """
                if args[0].name == 'ID':
                        return nodes.ClassTypeNode(args[0].attr)
                else:
                        return nodes.TypeNode(args[0].attr)

        def p_stmt1(self, args):
                """ stmt ::= if_stmt """
                return args[0]
        def p_stmt2(self, args):
                """ stmt ::= while_stmt """
                return args[0]
        def p_stmt3(self, args):
                """ stmt ::= for_stmt """
                return args[0]
        def p_stmt4(self, args):
                """ stmt ::= RETURN ; """
                return nodes.ReturnVoidNode()
        def p_stmt5(self, args):
                """ stmt ::= RETURN expr ; """
                root = nodes.ReturnNode()
                root.add_child(args[1])
                return root
        def p_stmt6(self, args):
                """ stmt ::= expr ; """
                return args[0]
        def p_stmt7(self, args):
                """ stmt ::= block """
                return args[0]
        def p_stmt8(self, args):
                """ stmt ::= SUPER ( ) ; """
                return nodes.SuperConstructorCallNode()
        def p_stmt9(self, args):
                """ stmt ::= SUPER ( args_list ) ; """
                root = nodes.SuperConstructorCallNode()
                root.add_child(args[2])
                return root
        def p_stmt10(self, args):
                """ stmt ::= ; """
                return nodes.EmptyNode()

        def p_if_stmt1(self, args):
                """ if_stmt ::= IF ( expr ) block """
                root = nodes.IfNode()
                root.add_children([args[2], args[4]])
                return root
        def p_if_stmt2(self, args):
                """ if_stmt ::= IF ( expr ) block ELSE block """
                root = nodes.IfNode()
                root.add_children([args[2], args[4], args[6]])
                return root
        def p_if_stmt3(self, args):
                """ if_stmt ::= IF ( expr ) block ELSE if_stmt """
                root = nodes.IfNode()
                root.add_children([args[2], args[4], args[6]])
                return root

        def p_while_stmt(self, args):
                """while_stmt ::= WHILE ( expr ) block"""
                root = nodes.WhileNode()
                root.add_children([args[2], args[4]])
                return root

        def p_for_stmt(self, args):
                """for_stmt ::= FOR ( var_dcl expr ; expr ) block"""
                root = nodes.ForNode()
                root.add_children([args[2], args[3], args[5], args[7]])
                return root

        def p_expr(self, args):
                """
                expr ::= cond_or_expr
                expr ::= cond_or_expr ASSIGN_OP cond_or_expr
                """
                if len(args) == 3:
                        root = nodes.AssignNode()
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]

        def p_cond_or_expr(self, args):
                """
                cond_or_expr ::= cond_and_expr
                cond_or_expr ::= cond_or_expr OR_OP cond_and_expr
                """
                # TODO: SAY HOW DID cond_or_expr OR_OP cond_and_expr  rather than:
                # cond_and_expr OR_OP cond_or_expr because the parser
                # algorithm favours it: see wikipedia

                #ALSO CREATE A FUNCTION TO DO ALL THESE DUPLICATED THING???
                if len(args) == 3:
                        root = nodes.CondNode('||')
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]

        def p_cond_and_expr(self, args):
                """
                cond_and_expr ::= equality_expr
                cond_and_expr ::= cond_and_expr AND_OP equality_expr
                """
                if len(args) == 3:
                        root = nodes.CondNode('&&')
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]

        def p_equality_expr(self, args):
                """
                equality_expr ::= relation_expr
                equality_expr ::= equality_expr EQ_OP relation_expr
                """
                if len(args) == 3:
                        root = nodes.EqNode(args[1].attr)
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]

        def p_relation_expr(self, args):
                """
                relation_expr ::= add_expr
                relation_expr ::= relation_expr rel_op add_expr
                """
                if len(args) == 3:
                        root = nodes.RelNode(args[1])
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]
        
        def p_relation_op(self, args):
                """
                rel_op ::= > 
                rel_op ::= <
                rel_op ::= > ASSIGN_OP
                rel_op ::= < ASSIGN_OP
                """
                # These cannot be grouped as single tokens because <, > and =
                # characters are used in other syntactic areas
                if len(args) == 1:
                        return args[0].name
                else:
                        return args[0].name + '='
                
        def p_add_expr(self, args):
                """
                add_expr ::= mul_expr
                add_expr ::= add_expr ADD_OP mul_expr
                """
                if len(args) == 3:
                        root = nodes.AddNode(args[1].attr)
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]

        def p_mul_expr(self, args):
                """
                mul_expr ::= unary_expr
                mul_expr ::= mul_expr MUL_OP unary_expr
                """
                if len(args) == 3:
                        root = nodes.MulNode(args[1].attr)
                        root.add_children([args[0], args[2]])
                        return root
                else:
                        return args[0]

        def p_unary_expr1(self, args):
                """ unary_expr ::= primary INC_OP """
                root = nodes.IncNode(args[1].attr)
                root.add_child(args[0])
                return root
        def p_unary_expr2(self, args):
                """ unary_expr ::= unary_prefix primary """
                root = args[0]
                root.add_child(args[1])
                return root
        def p_unary_expr3(self, args):
                """ unary_expr ::= primary """
                return args[0]

        def p_unary_op(self, args):
                """
                unary_prefix ::= NOT_OP
                unary_prefix ::= ADD_OP
                unary_prefix ::= INC_OP
                """
                if args[0].name == 'NOT_OP':
                        return nodes.NotNode()
                elif args[0].name == 'ADD_OP':
                        return nodes.PosNode(args[0].attr)
                elif args[0].name == 'INC_OP':
                        return nodes.IncNode(args[0].attr)

        def p_primary_id(self, args):
                """ primary ::= ID """
                return nodes.IdNode(args[0].attr)
        def p_primary_method_call(self, args):
                """ primary ::= method_call """
                return args[0]
        def p_primary_field_ref(self, args):
                """ primary ::= field_ref """
                return args[0]
        def p_primary_array(self, args):
                """ primary ::= array_element """
                return args[0]
        def p_primary_matrix(self, args):
                """ primary ::= matrix_element """
                return args[0]
        def p_primary_literal(self, args):
                """ primary ::= literal """
                return args[0]
        def p_primary_creator(self, args):
                """ primary ::= creator """
                return args[0]
        def p_primary_brackets(self, args):
                """ primary ::= ( expr ) """
                return args[1]

        def p_method_call_simple(self, args):
                """ method_call ::= ID ( ) """
                root = nodes.MethodCallNode()
                root.add_child(nodes.IdNode(args[0].attr))
                root.add_child(nodes.EmptyNode())
                return root
        def p_method_call_simple_args(self, args):
                """ method_call ::= ID ( args_list ) """
                root = nodes.MethodCallNode()
                root.add_children([nodes.IdNode(args[0].attr), args[2]])
                return root
        def p_method_call_long(self, args):
                """ method_call ::= ID method_call_rest ( ) """
                root = nodes.MethodCallLongNode()
                root.add_child(nodes.IdNode(args[0].attr))
                for id_ in args[1]:
                        root.add_child(id_)
                root.add_child(nodes.EmptyNode())
                return root
        def p_method_call_long_args(self, args):
                """ method_call ::= ID method_call_rest ( args_list ) """
                root = nodes.MethodCallLongNode()
                root.add_child(nodes.IdNode(args[0].attr))
                for id_ in args[1]:
                        root.add_child(id_)
                root.add_child(args[3])
                return root

        def p_method_call_super(self, args):
                """ method_call ::= SUPER method_call_rest ( ) """
                root = nodes.MethodCallSuperNode()
                for id_ in args[1]:
                        root.add_child(id_)
                root.add_child(nodes.EmptyNode())
                return root
        def p_method_call_super_args(self, args):
                """ method_call ::= SUPER method_call_rest ( args_list ) """
                root = nodes.MethodCallSuperNode()
                for id_ in args[1]:
                        root.add_child(id_)
                root.add_child(args[3])
                return root

        def p_method_call_rest_base(self, args):
                """ method_call_rest ::= . ID """
                leaf = nodes.IdNode(args[1].attr)
                return [leaf]
        def p_method_call_rest(self, args):
                """ method_call_rest ::= method_call_rest . ID """
                leaf = nodes.IdNode(args[2].attr)
                return args[0] + [leaf]

        def p_args_list(self, args):
                """ args_list ::= args """
                root = nodes.ArgsListNode()
                for arg in args[0]:
                        root.add_child(arg)
                return root
                
        def p_args_base(self, args):
                """ args ::= expr """
                return [args[0]]
        def p_args(self, args):
                """ args ::= args , expr """
                return args[0] + [args[2]]
        
        def p_field_ref(self, args):
                """ field_ref ::= ID . ID """
                root = nodes.FieldRefNode()
                root.add_child(nodes.IdNode(args[0].attr))
                root.add_child(nodes.IdNode(args[2].attr))
                return root
        
        def p_field_ref_super(self, args):
                """field_ref ::= SUPER . ID """
                root = nodes.FieldRefSuperNode()
                root.add_child(nodes.IdNode(args[2].attr))
                return root

        def p_array_element(self, args):
                """ array_element ::= ID array_suffix """
                root = nodes.ArrayElementNode()
                root.add_child(nodes.IdNode(args[0].attr))
                for index in args[1]:
                        root.add_child(index)
                return root

        def p_array_suffix1(self, args):
                """ array_suffix ::= [ expr ] """
                return [args[1]]
        def p_array_suffix2(self, args):
                """ array_suffix ::= array_suffix [ expr ]  """
                return args[0] + [args[2]]
        
        def p_matrix_element(self, args):
                """ matrix_element = ID < expr , expr > """
                root = nodes.MatrixElementNode()
                root.add_children([args[0], args[2], args[4]])
                return root

        def p_sting_l(self, args):
                """ literal ::= STR_L """
                return nodes.StringLNode(args[0].attr)
        def p_char_l(self, args):
                """ literal ::= CHAR_L """
                return nodes.CharLNode(args[0].attr)
        def p_int_l(self, args):
                """ literal ::= INT_L """
                return nodes.IntLNode(args[0].attr)
        def p_long_l(self, args):
                """ literal ::= LONG_L """
                return nodes.LongLNode(args[0].attr)
        def p_float_l(self, args):
                """ literal ::= FLOAT_L """
                return nodes.FloatLNode(args[0].attr)
        def p_double_l(self, args):
                """ literal ::= DOUBLE_L """
                return nodes.DoubleLNode(args[0].attr)
        def p_true_l(self, args):
                """ literal ::= TRUE_L """
                """ literal ::= FALSE_L """
                return nodes.BooleanLNode(args[0].attr)
        def p_null_l(self, args):
                """ literal ::= NULL_L """
                return nodes.NullLNode(args[0].attr)

        def p_creator_object(self, args):
                """ creator ::= NEW type ( ) """
                root = nodes.ObjectCreatorNode()
                root.add_child(args[1])
                return root
        def p_creator_object_args(self, args):
                """ creator ::= NEW type ( args_list ) """
                root = nodes.ObjectCreatorNode()
                root.add_children([args[1], args[3]])
                return root
        def p_creator_array(self, args):
                """ creator ::= NEW type array_suffix """
                root = nodes.ArrayInitNode()
                root.add_child(args[1])
                for index in args[2]:
                        root.add_child(index)
                return root
        def p_creator_matrix(self, args):
                """ creator ::= < expr , expr > """
                root = nodes.MatrixInitNode()
                root.add_children([args[1], args[3]])
                return root

################################################################################
## RULES FOR INTERFACES
################################################################################

        def p_inteface_dcl(self, args):
                """ interface_dcl ::= INTERFACE ID interface_body """
                root = nodes.InterfaceNode()
                root.add_child(nodes.IdNode(args[1].attr))
                root.add_children([nodes.EmptyNode(), args[2]])
                return root

        def p_interface_dcl_extends(self, args):
                """ interface_dcl ::= INTERFACE ID EXTENDS ID interface_body"""
                root = nodes.InterfaceNode()
                root.add_child(nodes.IdNode(args[1].attr))
                root.add_children([nodes.ExtendsNode(args[3].attr), args[4]])
                return root

        def p_interface_body(self, args):
                """ interface_body ::= { interface_body_dcl } """
                root = nodes.InterfaceBodyNode()
                for dcl in args[1]:
                        root.add_child(dcl)
                return root

        def p_interface_body_empty(self, args):
                """ interface_body ::= { } """
                root = nodes.EmptyNode()
                return root

        def p_interface_body_dcl_method_base(self, args):
                """ interface_body_dcl ::= abs_method_dcl """
                return [args[0]]
        def p_interface_body_dcl_method(self, args):
                """ interface_body_dcl ::= interface_body_dcl abs_method_dcl """
                return args[0] + [args[1]]

        def p_abs_method_dcl(self, args):
                """
                abs_method_dcl ::= type ID formal_param ;
                abs_method_dcl ::= VOID ID formal_param ;
                """
                root = nodes.AbsMethodDclNode()
                root.add_child(nodes.IdNode(args[1].attr))
                try:
                        if args[0].name == 'VOID':
                                root.add_child(nodes.TypeNode('void'))
                except AttributeError:
                        root.add_child(args[0])
                root.add_child(args[2])
                return root

        def p_abs_method_dcl_array(self, args):
                """
                abs_method_dcl ::= type array_brackets ID formal_param ;
                """
                # Like above, but this one returns an array
                root = nodes.AbsMethodDclArrayNode()
                root.add_child(nodes.IdNode(args[2].attr))
                root.add_children([args[0], nodes.DimensionsNode(args[1])])
                root.add_child(args[3])
                return root

def parse(f, start = 'file', lib_classes = None):
        """parses a jml file and returns a list of abstract syntax trees, or
        parses a string containing JaML code.
        """
        scanner = Scanner()
        parser = Parser(start)
        # Try and parse a file, if this fails, parse a sting of JaML code
        try:
                # This is to see if it's a file or not
                open(f)
                # Stores the directory of the main class
                dir_ = os.path.dirname(f)
                # Add the name of the main class to begin with
                file_name = os.path.basename(f)
                class_name = file_name.replace('.jml', '')
                # 'seen' stores names of all already seen class references
                seen = [class_name]
                # Stores classes to parse
                to_parse = [class_name]
                # Stores the ASTs of parsed classes
                parsed = nodes.ProgramASTs()
                while to_parse:
                        # Append file information to the class names
                        file_name = os.path.join(dir_, to_parse[0] + '.jml')
                        # Get the raw input
                        raw = open(file_name)
                        input_ = raw.read()
                        # Scan and parse the file
                        tokens = scanner.tokenize(input_)
#                        print tokens
                        ast = parser.parse(tokens)
                        # Check the class and file are named the same
                        if to_parse[0] != ast.children[0].value:
                                raise NameError('Class name and file name ' +
                                                'do not match!')
                        to_parse.pop(0)

                        parsed.append(ast)
                        # Fined classes reference from the one just parsed
                        if lib_classes == None:
                                lib_classes = {}
                        refed_classes = find_refed_classes(ast, seen, [],
                                                           lib_classes, dir_)
                        seen += refed_classes
                        to_parse += refed_classes
                return parsed
        except IOError:
                # Simply parse the program held in the string
                tokens = scanner.tokenize(f)
#                print tokens
                ast = parser.parse(tokens)
                ast_wrapper = nodes.ProgramASTs()
                ast_wrapper.append(ast)
                return ast_wrapper

def find_refed_classes(node, seen, new, lib_classes, cur_dir):
        """Gets the names of all referenced classes in the abstract syntax tree.
        """
        # Uses a depth first search looking for var_dcl, object_creator and
        # extends nodes
        try:
                # The try will fail if it's a leaf
                children = node.children
                # Need to check object_creator nodes because subclasses
                # that are assigned to variables of type superclass
                # must also be parsed.  Also, extends nodes must be
                # checked.
                if isinstance(node, nodes.ObjectCreatorNode):
                        class_name = children[0].value
                        if class_name not in seen:
                                new.append(class_name)
                        # Search in the arguments (if any)
                        try:
                                new += find_refed_classes(node.children[1],
                                                          seen, [], lib_classes,
                                                          cur_dir)
                        except IndexError: pass
                elif (isinstance(node, nodes.MethodCallLongNode) or
                      isinstance(node, nodes.FieldRefNode)):
                        # Check if the first child is a static reference to
                        # a class, if it is, add the class to parse
                        id_node = node.children[0]
                        if check_static_ref(id_node, cur_dir):
                                new.append(id_node.value)
                        try:
                                # Search in the arguments for methods calls
                                new += find_refed_classes(node.children[2],
                                                          seen, [], lib_classes,
                                                          cur_dir)
                        except IndexError: pass
                else:
                        # Keep searching through the AST
                        for child in children:
                                new += find_refed_classes(child, seen, [],
                                                          lib_classes, cur_dir)
        except AttributeError:
                if node.value not in seen:
                        is_class1 = isinstance(node, nodes.ClassTypeNode) 
                        is_class = is_class1 and node.value not in lib_classes.keys()
                        is_extends = isinstance(node, nodes.ExtendsNode)
                        is_implements = isinstance(node, nodes.ImplementsNode)
                        if is_class or is_extends or is_implements:
                                seen.append(node.value)
                                new.append(node.value)
        return new

def check_static_ref(id_node, cur_dir):
        """For a given identifier, this checks if it is a static reference to
        a class by searching for files in the same folder as the current
        class from one with the matching name.
        """
        listing = os.listdir(cur_dir)
        for file_name in listing:
                # Remove .jml extension from file name to get class name
                if id_node.value == file_name[:-4]:
                        return True
        return False