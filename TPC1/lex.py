import re
import ply.lex as lex

# Ex: + [ 1.0   :9.0 ]  [15.5 :19.0]   .

tokens = (
    'PLUS',
    'MINUS',
    'ESQ',
    'DIR',
    'COLON',
    'NUMBER',
    'DOT')

t_PLUS = r'\+'
t_MINUS = r'-'
t_ESQ = r'\['
t_DIR = r'\]'
t_COLON = r':'
t_DOT = r'\.'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
lexer = lex.lex()

