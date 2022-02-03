######
# for loop expression context-free grammar
######
# E -> ( A ; G ; id P ) S
# A -> B | id C
# B -> int id C
# C -> = number
# 

#
# P -> op
# G -> stm
# S -> { snipt }
def S(line_iter):
    line = next(line_iter)
    token,attr,line_num,column = line.split(':')
    if token == 'L_CURLYBRACKET':
        while True:
            try:
                line = next(line_iter)
                token,attr,line_num,column = line.split(':')
                if token == 'R_CURLYBRACKET':
                    return True
            except StopIteration:
                raise RuntimeError(f'it expected to end up the statement by Right CURLYBRACKET but it did not finished {line_num}')
    else:
        raise RuntimeError(f'it expected Left CURLYBRACKET but it got {token} on line {line_num}')

def G(line_iter):
    while True:
        try:
            line = next(line_iter)
            token,attr,line_num,column = line.split(':')
            if token == 'END':
                return True
        except StopIteration:
            raise RuntimeError(f'it expected to end up the statement by ; but it did not finished {line_num}')

def P(line_iter):
    while True:
        try:
            line = next(line_iter)
            token,attr,line_num,column = line.split(':')
            if token == 'R_PARENTHESIS':
                return True
        except StopIteration:
            raise RuntimeError(f'it expected to end up the statement by ) but it did not finished {line_num}')

def for_expression(line_iter):
    line = next(line_iter)
    token,attr,line_num,column = line.split(':')

    if token == 'L_PARENTHESIS':
        if A(line_iter) ==True:
            line = next(line_iter)
            token,attr,line_num,column = line.split(':')
            if token == 'END':
                if G(line_iter) == True:
                    line = next(line_iter)
                    token,attr,line_num,column = line.split(':')
                    if token == 'ID':
                        if P(line_iter) == True:
                            if S(line_iter) == True:
                                return True;
            ############## P
            else:
                raise RuntimeError(f'it expected ; but it got {attr} on line {line_num}')
    else:
        raise RuntimeError(f'it expected ( but it got {token} on line {line_num}')

def A(line_iter):
    line = next(line_iter)
    token,attr,line_num,column = line.split(':')
    if token == 'ID':
        return C(line_iter)
    else:
        return B(line_iter,line)

def B(line_iter,line):
    token,attr,line_num,column = line.split(':')
    if token == 'int' and attr == 'int':
        line = next(line_iter)
        token,attr,line_num,column = line.split(':')
        if token == 'ID':
            return C(line_iter)
        else:
            raise RuntimeError(f'it expected to get Varible but it got {token} on line {line_num}')
    else:
        raise RuntimeError(f'it expected to get Integar declaration but it got {token} on line {line_num}')

def C(line_iter):
    line = next(line_iter)
    token,attr,line_num,column = line.split(':')
    if token == 'ASSIGN':
        line = next(line_iter)
        token,attr,line_num,column = line.split(':')
        if token == 'NUMBER':
            return True
        else:
            raise RuntimeError(f'it expected a number but it got {token} on line {line_num}')
    else:
        raise RuntimeError(f'it expected = but it got {token} on line {line_num}')


with open('tokens.dat','r')as file:
    lines_iter = iter(file.readlines())
    while True:
        try:
            line = next(lines_iter)
            token,attr,line_num,column = line.split(':')
            if token == 'for' and attr == 'for':
                if for_expression(lines_iter) == True:
                    print("the for expression is accepted")
        except StopIteration:
            break;