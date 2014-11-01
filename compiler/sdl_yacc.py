# -*- coding: utf-8 -*-

import ply.yacc as yacc
import types
import sys

current_lev = 0

# Lex のサンプルを参照する
from tc_lex import *

#各モジュールの読込
from node import *

def p_program(p):
    '''program : external_declaration
               | program external_declaration'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('PROGRAM', [p[1], p[2]])


def p_external_declaration(p):
    '''external_declaration : declaration
                            | function_definition'''

    p[0] = Node('EXT_DECTN', [p[1]])

def p_declaration(p):
    'declaration : INT declarator_list SEMICOLON'

    p[0] = Node('INT', [p[2]])

def p_declarator_list(p):
    '''declarator_list : declarator
                       | declarator_list COMMA declarator'''

    if len(p) == 2:
        p[0] = make_decl(p[1], current_lev)
    else:
        p[0] = Node('DECTR_LIST', [p[1], make_decl(p[3], current_lev)] )

def p_declarator(p):
    'declarator : IDENTIFIER'

    p[0] = make_obst(p[1], current_lev)


def p_function_definition(p):
    '''function_definition : INT function_declarator LPAREN lev_inc parameter_type_list RPAREN func_compound_statement
                           | INT function_declarator LPAREN lev_inc RPAREN func_compound_statement'''
    
    #declaratorにして構文木生成でmake_fun_def呼び出すと すべて展開したあとに呼ばれるので関数が終わるまで関数呼び出せない→再帰無理
    if len(p) == 8:
        p[0] = Node('FUN_DEF', [Node('INT', [p[2]]), p[5], p[7]] )
    else:
        p[0] = Node('FUN_DEF', [Node('INT', [p[2]]), p[6]])

def p_function_declarator(p):
    'function_declarator : IDENTIFIER'

    p[0] = make_fun_def(make_obst(p[1], current_lev))

def p_parameter_type_list(p):
    '''parameter_type_list : parameter_declaration
                           | parameter_type_list COMMA parameter_declaration'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('PARAM_LIST', [p[1], p[3]] )


def p_parameter_declaration(p):
    'parameter_declaration : INT declarator'

    p[0] = Node('INT', [make_param_decl(p[2], current_lev)])
    #p[0] = Node('INT', [p[2]])

def p_statement(p):
    '''statement : SEMICOLON
                 | expression SEMICOLON
                 | compound_statement
                 | IF LPAREN expression RPAREN statement
                 | IF LPAREN expression RPAREN statement ELSE statement
                 | WHILE LPAREN expression RPAREN statement
                 | FOR LPAREN for_expression SEMICOLON for_expression SEMICOLON for_expression RPAREN statement
                 | RETURN expression SEMICOLON
                 | CONT SEMICOLON
                 | BREAK SEMICOLON'''

    if len(p) == 2 and p[1] == t_SEMICOLON:
        p[0] = []
    elif len(p) == 3:
        if p[1] == t_BREAK:
            p[0] = Node('BRK', [])
        elif p[1] == t_CONT:
            p[0] = Node('CONT', [])
        else:
            p[0] = p[1]
    elif len(p) == 2 and p[1] != t_SEMICOLON:
        p[0] = p[1]
    elif len(p) == 6 and p[1] == t_IF:
        p[0] = Node('IF', [p[3], p[5]] )
    elif len(p) == 8 and p[1] == t_IF:
        p[0] = Node('IFELSE', [p[3], p[5], p[7]] )
    elif len(p) == 6 and p[1] == t_WHILE:
        p[0] = Node('WHILE', [p[3], p[5]] )
    elif len(p) == 4:
        p[0] = Node('RTN', [p[2]] )
    elif len(p) == 10:
        p[0] = Node('FOR', [p[3], p[5],p[7],p[9]] )

#関数の場合はパラメータ宣言で1深くなるので2浅くする
def p_func_compound_statement(p):
    '''func_compound_statement : LBRACE lev_inc declaration_list statement_list lev_dec lev_dec RBRACE
                               | LBRACE lev_inc statement_list lev_dec lev_dec RBRACE
                               | LBRACE lev_inc declaration_list lev_dec lev_dec RBRACE
                               | LBRACE RBRACE'''

    if len(p) == 8:
        p[0] = Node('COMP', [p[3], p[4]])
    elif len(p) == 7:
        p[0] = Node('COMP', [p[3]])
    else:
        p[0] = Node('COMP', [])

def p_compound_statement(p):
    '''compound_statement : LBRACE lev_inc declaration_list statement_list lev_dec RBRACE
                          | LBRACE lev_inc statement_list lev_dec RBRACE
                          | LBRACE lev_inc declaration_list lev_dec RBRACE
                          | LBRACE RBRACE'''

    if len(p) == 7:
        p[0] = Node('COMP', [p[3], p[4]])
    elif len(p) == 6:
        p[0] = Node('COMP', [p[3]])
    else:
        p[0] = Node('COMP', [])
        
def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('DECTN_LIST', [p[1], p[2]] )

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('STMT_LIST', [p[1], p[2]] )

def p_for_expression(p):
    '''for_expression : empty
                      | not_expr
                      | for_expression COMMA not_expr'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('EXPR', [p[1], p[3]] )

def p_expression(p):
    '''expression : not_expr
                  | expression COMMA not_expr'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('EXPR', [p[1], p[3]] )

def p_not_expr(p):
    '''not_expr : assign_expr
                | NOT LPAREN assign_expr RPAREN'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('!',  [p[3]] )

def p_assign_expr(p):
    '''assign_expr : logical_or_expr
                   | IDENTIFIER EQUAL assign_expr'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('=', [ref_var(make_obst(p[1], current_lev)), p[3]])

def p_logical_or_expr(p):
    '''logical_or_expr : logical_and_expr
                       | logical_or_expr OR logical_and_expr'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('||', [p[1], p[3]])

def p_logical_and_expr(p):
    '''logical_and_expr : equality_expr
                        | logical_and_expr AND equality_expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('&&', [p[1], p[3]])

def p_equality_expr(p):
    '''equality_expr : relational_expr
                     | equality_expr EQUALCOMP relational_expr
                     | equality_expr EQUALNOT relational_expr'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[2] == t_EQUALCOMP:
        p[0] = Node('==', [p[1], p[3]])
    elif len(p) == 4 and p[2] == t_EQUALNOT:
        p[0] = Node('!=', [p[1], p[3]])

def p_relational_expr(p):
    '''relational_expr : add_expr
                       | relational_expr LT add_expr
                       | relational_expr GT add_expr
                       | relational_expr ELT add_expr
                       | relational_expr EGT add_expr'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[2] == t_LT:
        p[0] = Node('<', [p[1], p[3]])
    elif len(p) == 4 and p[2] == t_GT:
        p[0] = Node('>', [p[1], p[3]])
    elif len(p) == 4 and p[2] == t_ELT:
        p[0] = Node('<=', [p[1], p[3]])
    elif len(p) == 4 and p[2] == t_EGT:
        p[0] = Node('>=', [p[1], p[3]])

def p_add_expr(p):
    '''add_expr : mult_expr
                | add_expr PLUS mult_expr
                | add_expr MINUS mult_expr'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[2] == '+':
        p[0] = Node('+', [p[1], p[3]])
    elif len(p) == 4 and p[2] == '-':
        p[0] = Node('-', [p[1], p[3]])


def p_mult_expr(p):
    '''mult_expr : unary_expr
                 | mult_expr TIMES unary_expr
                 | mult_expr DIVIDE unary_expr'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[2] == '*':
        p[0] = Node('*', [p[1], p[3]])
    elif len(p) == 4 and p[2] == t_DIVIDE:
        p[0] = Node('/', [p[1], p[3]])

def p_unary_expr(p):
    '''unary_expr : postfix_expr
                  | MINUS unary_expr'''

    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 3:
        p[0] = Node('NEG', [p[2]])
        
def p_postfix_expr(p):
    '''postfix_expr : primary_expr
                    | IDENTIFIER LPAREN argument_expression_list RPAREN
                    | IDENTIFIER LPAREN RPAREN'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        arg_num = count_argnum(p[3])
        p[0] = Node('POST', [ref_fun(make_obst(p[1], current_lev), arg_num), p[3]])
    elif len(p) == 4:
        p[0] = Node('POST', [ref_fun(make_obst(p[1], current_lev), 0)])

def count_argnum(node):
    if isinstance(node,Node) and node.op == "ARG":
        return 1 + count_argnum(node.children[0])
    else:
        return 1


def p_primary_expr(p):
    '''primary_expr : IDENTIFIER
                    | CONSTANT
                    | LPAREN expression RPAREN'''

    if len(p) == 2 and isinstance(p[1], str):
        p[0] = ref_var(make_obst(p[1], current_lev))
    elif len(p) == 2 and isinstance(p[1], int):
        p[0] = Node('CONST', [p[1]])
    elif len(p) == 5:
        p[0] = p[2]

def p_argument_expression_list(p):
    '''argument_expression_list : assign_expr
                                | argument_expression_list COMMA assign_expr'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('ARG', [p[1], p[3]])

def p_lev_inc(p):
    'lev_inc :'

    global current_lev
    current_lev += 1

def p_lev_dec(p):
    'lev_dec :'

    global current_lev

    #スタック先頭から見ていって現在の深さの物をすべてポップ
    while Obst.stack[0].lev == current_lev:
        unit = Obst.stack.pop(0)
        #ぽっぷされすぎてoffsetが20とかになる
        if unit.kind == "VAR":
            Obst.var_alloc += 4
            
    current_lev -= 1

    if current_lev == 0:
        Obst.param_alloc = 4
        Obst.var_alloc = 0
        Obst.stack = [unit for unit in Obst.stack if unit.kind != "PARAM"]

    #Obst.display_stack() #スタック表示したければコメント外す

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Syntax error in input"

# 構文解析器の構築
parser = yacc.yacc()

if __name__ == '__main__':  
    
    while True:
        try:
            s = raw_input('tcperser > ')

        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        result.display(0)

    
    """
    s = ""
    for line in sys.stdin:
        s += line.strip("\n") 

    result = parser.parse(s)

    #result.display(0)

    #print ""
    print_code()
    #write_code()
    """
    
