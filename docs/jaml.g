        file ::= class_dcl | interface_dcl

        class_dcl ::= class_mods class_dcl_rest | class_dcl_rest

        class_dcl_rest ::= CLASS ID class_body
                           | CLASS ID EXTENDS ID class_body
                           | CLASS ID IMPLEMENTS implements class_body
                           | CLASS ID EXTENDS ID IMPLEMENTS implements class_body

        class_mods ::= ABSTRACT | FINAL

        implements ::= implements_list

        implements_list ::= ID | implements_list , ID

        class_body ::= { class_body_dcl } | { }

        class_body_dcl ::= constructor_dcl | method_dcl | field_dcl
                           | class_body_dcl constructor_dcl
                           | class_body_dcl method_dcl
                           | class_body_dcl field_dcl

        field_dcl ::= field_mods field_dcl_rest | field_dcl_rest

        field_dcl_rest ::= type ID ;
                           | type array_brackets ID ;
                           | type ID array_brackets ;
                           | type ID ASSIGN_OP literal ;

        field_mods ::= PRIVATE | static_final_mods | PRIVATE static_final_mods

        static_final_mods ::= FINAL | STATIC

        constructor_dcl ::= ID formal_param block

        method_dcl ::= ABSTRACT abs_method_dcl
                       | method_mods method_dcl_rest
                       | method_dcl_rest

        method_dcl_rest ::= type ID formal_param block
                            | VOID ID formal_param block

        method_dcl_rest ::= type array_brackets ID formal_param block

        method_mods ::= PRIVATE | static_final_mods | PRIVATE static_final_mods

        formal_param ::= ( param_list ) | ( )

        param_list ::= type ID | type array_brackets ID | type ID array_brackets
                       | param_list , type ID
                       | param_list , type array_brackets ID
                       | param_list , type ID array_brackets

        block ::= { block_stmt } | { }

        block_stmt ::= stmt | var_dcl | block_stmt stmt | block_stmt var_dcl

        var_dcl ::= type ID ; | array_brackets ID ; | type ID array_brackets ;
                    | type ID ASSIGN_OP expr ;
                    | type array_brackets ID ASSIGN_OP expr ;
                    | type ID array_brackets ASSIGN_OP expr ;

        array_brackets ::= array_brackets [ ] | [ ]

        type ::= ID | TYPE

        stmt ::= if_stmt | while_stmt | for_stmt
                 | RETURN ; | RETURN expr ;
                 | expr ; | block
                 | SUPER ( ) ; | SUPER ( args_list ) ; | ;

        if_stmt ::= IF ( expr ) block
                    | IF ( expr ) block ELSE block
                    | IF ( expr ) block ELSE if_stmt

       while_stmt ::= WHILE ( expr ) block

       for_stmt ::= FOR ( var_dcl expr ; expr ) block

       expr ::= cond_or_expr | cond_or_expr ASSIGN_OP cond_or_expr

       cond_or_expr ::= cond_and_expr | cond_or_expr OR_OP cond_and_expr

       cond_and_expr ::= equality_expr | cond_and_expr AND_OP equality_expr

       equality_expr ::= relation_expr | equality_expr EQ_OP relation_expr

       relation_expr ::= add_expr | relation_expr REL_OP add_expr

       add_expr ::= mul_expr | add_expr ADD_OP mul_expr

       mul_expr ::= unary_expr | mul_expr MUL_OP unary_expr

       unary_expr ::= primary INC_OP | unary_prefix primary | primary
                      | NOT_OP | ADD_OP | INC_OP

       primary ::= ID | method_call | field_ref
                   | array_element | matrix_element
                   | literal | creator | ( expr )

       method_call ::= ID ( ) | ID ( args_list )
                       | ID method_call_rest ( )
                       | ID method_call_rest ( args_list )
                       | SUPER method_call_rest ( )
                       | SUPER method_call_rest ( args_list )

       method_call_rest ::= . ID | method_call_rest . ID

       args_list ::= args

       args ::= expr | args , expr

       field_ref ::= ID . ID | SUPER . ID

       array_element ::= ID array_suffix

       array_suffix ::= [ expr ] | array_suffix [ expr ]

       matrix_element ::= ID MAT_BRACKET expr , expr MAT_BRACKET

       literal ::= STR_L | CHAR_L | INT_L | LONG_L | FLOAT_L | DOUBLE_L
                   | TRUE_L | FALSE_L | NULL_L

       creator ::= NEW type ( ) | NEW type ( args_list )
                   | NEW type array_suffix | MAT_BRACKET expr , expr MAT_BRACKET

       interface_dcl ::= INTERFACE ID interface_body
                         | INTERFACE ID EXTENDS ID interface_body"""

       interface_body ::= { interface_body_dcl } | { }

       interface_body_dcl ::= abs_method_dcl | interface_body_dcl abs_method_dcl
       abs_method_dcl ::= type ID formal_param ;
                          | VOID ID formal_param ;
                          | type array_brackets ID formal_param ;