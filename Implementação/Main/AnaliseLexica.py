# coding=UTF-8
import ply.lex as lex
import sys
# coding: UTF-8
class Lexica(object):
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    pr = {
        u'até' : 'ATE',
        u'se' : 'SE',
        u'senão' : 'SENAO',
        u'então' : 'ENTAO',
        u'fim' : 'FIM',
        u'repita' : 'REPITA',
        u'flutuante' : 'FLUTUANTE',
        u'retorna' : 'RETORNA',
        u'leia' : 'LEIA',
        u'escreva' : 'ESCREVA',
        u'inteiro' : 'INTEIRO',

    }
    # lista de tokens
    tokens = [
        'PLUS',
        'MINUS',
        'VEZES',
        'DIVIDE',
        'IGUAL',
        'VIRGULA',
        'DOISPONTOS',
        'LCOLCH',
        'RCOLCH',
        'NEGACAO',
        'LPAREN',
        'RPAREN',
        'MAIOR',
        'MENOR',
        'MENOREQ',
        'MAIOREQ',
        'ATRIBUICAO',
        'ELOGICO',
        'DIF',
        'ID',
        'NUM_FLUTUANTE',
        'COMENTARIO',
        'NUM_CIENTIFICA',
       'NUM_INTEIRO',
        'COMENTARIO_INCOMPLETO',

    ] + list(pr.values())


    # expressões regulares

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_VEZES   = r'\*'
    t_DIVIDE  = r'/'
    t_IGUAL   = r'\='
    t_VIRGULA = r','
    t_DOISPONTOS = r'\:'
    t_LCOLCH = r'\['
    t_RCOLCH = r'\]'
    t_NEGACAO = r'\!'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_MAIOR = r'\>'
    t_MENOR = r'\<'
    t_MENOREQ = r'\<='
    t_MAIOREQ = r'\>='
    t_ATRIBUICAO = r'(\?<\!<|>|:|=)=(?!=)'
    t_ELOGICO = r'&&'
    t_DIF = r'<>'

    # função que trata a quebra de linha
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # função que trata os comentários
    def t_COMENTARIO(self, t):
        r'\{[^}]*[^{]*\}'

    def t_COMENTARIO_INCOMPLETO(self, t):
        r'({)'

    # função que trata os espaços
    #def t_SPACE(t):
    #    r'\ '
    #    pass

    # função que trata as palavras reservadas da linguagem
    def t_PR(self, t):
        r'se\b|então\b|senão\b|fim\b|repita\b|flutuante\b|retorna\b|até\b|leia\b|escreva\b|inteiro\b'
        t.type = self.pr.get(t.value)
        return t

    # função que trata qualquer ID que aparecer
    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z_0-9]*'
        t.type = self.pr.get(t.value, 'ID')
        return t

    # função que trata notação científica
    def t_NUM_CIENTIFICA(self, t):
        r'([+-]?(\d+)(.\d+)([eE][+|-]?(\d+)))'
        return t

    # função que trata números pontos flutuantes
    def t_NUM_FLUTUANTE(self, t):
        r'([+-]?\d+)?(\.(\d)+)|((\d)\.)'
        return t

    # função qu trata números inteiros
    def t_NUM_INTEIRO(self, t):
        r'([+-]?\d+)'
        return t

    # função que trata os símbolos da linguagem
    #def t_SB(t):
    #    r'\+|\-|\*|/|\=|,|(\?<\!<|>|:|=)=(?!=)|\<|\>|\<=\b|\>=\b|\(|\)|\:|\[|\]|&&|\!'
    #    return t

    #def t_NUMBER(t):
    #    r'\d+'
    #    t.value = int(t.value)
    #    return t

    # ignora espaço
    t_ignore = ' \t'

    # função que trata quando encontra um caracter ilegal
    def t_error(self, t):
        print("Illegal character '%s', linha %d" % (t.value[0], t.lineno))
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


# Tokenize
if __name__ == '__main__':
    codigo = open('C:/Users/Mateu/Desktop/UTFPR-BCC/Compiladores/lexica-testes/fat.tpp')
    r = codigo.read()
    lexerTest = Lexica()
    lexerTest.build()

    # Carrega os dados
    lexerTest.lexer.input(r)

    # Percorre o arquivo e imprime os tokens
    while True:
        tok = lexerTest.lexer.token()
        if not tok:
            break
        print("<" + tok.type + ", " + tok.value + ">")