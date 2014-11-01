# -*- coding: utf-8 -*-
import ply.lex as lex 
import re
import sys

# トークンリスト 常に必須
tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'EQUAL',
    'NOT',
    'SEMICOLON',
    'OR',
    'AND',
    'LT',
    'GT',
    'ELT',
    'EGT',
    'EQUALCOMP',
    'EQUALNOT',
    'CONSTANT',
    'IDENTIFIER'
]

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'int' : 'INT',
    'while' : 'WHILE',
    'return' : 'RETURN',
    'break' : 'BREAK',
    'continue' : 'CONT',
    'for' : 'FOR'
}

tokens = tokens + list(reserved.values())

# 正規表現による簡単なトークンのルール
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_COMMA = r'\,'

t_EQUAL = r'='
t_NOT = r'\!'
t_SEMICOLON = r';'
t_OR = r'\|\|'
t_AND = r'&&'
t_LT = r'<'
t_GT = r'>'
t_ELT = r'<='
t_EGT = r'>='
t_EQUALCOMP = r'=='
t_EQUALNOT = r'!='

t_IF = r'if'
t_INT = r'int'
t_RETURN = r'return'
t_BREAK = r'break'
t_CONT = r'continue'
t_WHILE = r'while'
t_FOR = r'for'


# 正規表現とアクションコード
def t_CONSTANT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 正規表現とアクションコード
def t_DIGIT(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
# 行番号をたどれるように
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 識別子と予約後
def t_IDENTIFIER(t):
    r'[a-zA-Z]\w*'

    #予約語の場合は予約語の中身を、そうでなければ識別子を返す
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t
 

# スペースおよびタブは無視
t_ignore = ' \t'

# エラーハンドリングルール
def t_error(t):
    print u"不正な文字 '%s'" % t.value[0]

# lexer を構築
lexer = lex.lex()

if __name__ == '__main__':  

    # コマンドラインから読み込んだ文字列でテスト
    lexer.input(sys.argv[1])
    
    while True:
        tok = lexer.token()
        if not tok:  
            # これ以上トークンはない
            break

        # タイプ、バリュー、行番号、入力データ中の相対位置の順で返す
        #print tok
        print "%s, %s" % (tok.type, tok.value)
