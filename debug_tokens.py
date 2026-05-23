from translator import Lexer
s = open('ab.yl', 'r', encoding='utf-8').read()
for t in Lexer(s).tokens():
    print((t.type, t.value, t.line, t.col))
