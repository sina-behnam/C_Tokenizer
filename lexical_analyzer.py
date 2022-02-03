from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

keyword_keys = ['return', 'for', 'while', 'if', 'else', 'do', 'switch', 'case', 'default', 'break', 'continue', 'goto', 'void', 'main', 'extern', 'static', 'struct', 'typedef', 'enum', 'union', 'sizeof', 'const', 'volatile', 'register', 'auto', 'signed', 'unsigned', 'short', 'long', 'inline', 'restrict', 'int', 
'float', 'char', 'string']

def tokenize(code):
    keywords = keyword_keys
    token_specification = [
        ('NUMBER',          r'\d+(\.\d*)?'),    # Integer or decimal number
        ('ASSIGN',          r'='),              # Assignment operator
        ('END',             r';'),              # Statement terminator
        ('ID',              r'[A-Za-z]+'),      # Identifiers
        ('OP',              r'[+\-*<>/]'),      # Arithmetic operators
        ('L_PARENTHESIS',   r'\('),             # Left PARENTHESIS
        ('R_PARENTHESIS',   r'\)'),             # Right PARENTHESIS
        ('L_CURLYBRACKET',  r'{'),
        ('R_CURLYBRACKET',  r'}'),
        ('NEWLINE',         r'\n'),             # Line endings
        ('SKIP',            r'[ \t]+'),         # Skip over spaces and tabs
        ('HEADER',          r'#include([ ]*)<[a-z]+.h?>'),
        ('MISMATCH',        r'.'),               # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    line_num = 1
    line_start = 0

    iter_flag = False    

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)


input_file = open('sample.c','r')
statements = input_file.read()
input_file.close()

f = open('tokens.dat','w')
f.write('')
f.close()

with open('tokens.dat','a+') as file:
    for token in tokenize(statements):
        print(token)
        file.write(str(token.type) +':'+ str(token.value) +':'+ str(token.line) +':'+ str(token.column)+'\n')