# -*- coding: utf-8 -*-
from Main.AnaliseSintatica import Sintatica

class Semantica:

    def __init__(self, code):
        self.symbols = {}
        self.scope = "global"
        self.tree = Sintatica(code).ast
        self.ultimo_tipo = None
        self.programa(self.tree)
        self.verify_main(self.symbols)
        self.var_used(self.symbols)
        self.func_used(self.symbols)

    '''
    Função que verifica se existe a main
    '''
    def verify_main(self, symbols):
        if "principal" not in symbols.keys():
            print("ERRO: funcao principal nao foi declarada")

    '''
    Função que verifica se alguma variável não está sendo utilizada
    '''
    def var_used(self, symbols):
        for key, values in symbols.items():
            if values[0] == "variavel":
                if values[2] is False:
                    scope = key.split("-")
                    if scope[0] != "global":
                        print("WARNING: variavel " + values[1] + " da funcao " + scope[0] + " nunca é utilizada")
                    else:
                        print("WARNING: variavel " + values[1] + " nunca é utilizada")

    '''
    Função que verifica se alguma função não está sendo utilizada
    '''
    def func_used(self, symbols):
        for (key, values) in symbols.items():
            if values[0] == "funcao" and key != "principal":
                if values[3] is False:
                    print("WARNING: a funcao " + key + " nunca é utilizada ")

    '''
    Start
    '''
    def programa(self, node):
        self.lista_declaracoes(node.child[0])

    '''
    Diferenciação pelo tamanho
    '''
    def lista_declaracoes(self, node):
        if len(node.child) == 1:
            self.declaracao(node.child[0])
        else:
            self.lista_declaracoes(node.child[0])
            self.declaracao(node.child[1])

    '''
    Diferenciação pelo tipo, pois os tamanhos são iguais
    '''
    def declaracao(self, node):
        if node.child[0].type == "declaracao_variaveis":
            self.declaracao_variaveis(node.child[0])
        elif node.child[0].type == "inicializacao_variaveis":
            self.inicializacao_variaveis(node.child[0])
        else:
            if len(node.child[0].child) == 1:
                self.scope = node.child[0].child[0].value
            else:
                self.scope = node.child[0].child[1].value

            self.declaracao_funcao(node.child[0])
            self.scope = "global"

    '''
    Verifica se a variável tem colchete, ou seja, se é vetor, e depois verifica se ja foi declarado e adiciona
    na tabela de símbolos
    '''
    def declaracao_variaveis(self, node):
        var_type = node.child[0].type
        var_name = ""
        var_remaining = "" #restante
        i = 0

        for son in self.lista_variaveis(node.child[1]):
            if "[" in son:
                for i in range(len(son)):
                    if son[i] == "[":
                        break
                    var_name += son[i]
                var_remaining = son[i:]
                son = var_name

            if self.scope + "-" + son in self.symbols.keys():
                print("ERRO: variavel '" + son + "' já foi declarada")
                exit(1)

            if "global" + "-" + son in self.symbols.keys():
                print("ERRO: variavel '" + son + "' já foi declarada")

            if son in self.symbols.keys():
                print("WARNING: funcoes com nomes iguais: " + node.value)
                                                    #classe, nome variavel, utilizacao, atribuicao, tipo, escopo
            self.symbols[self.scope + "-" + son] = ["variavel", son, False, False, var_type + var_remaining, self.scope]

    def inicializacao_variaveis(self, node):
        self.atribuicao(node.child[0])

    '''
    Cria uma lista de variáveis
    '''
    def lista_variaveis(self, node):
        list_var = []
        if len(node.child) == 1:
            if len(node.child[0].child) == 1:
                list_var.append(node.child[0].value + self.indice(node.child[0].child[0]))
            else:
                list_var.append(node.child[0].value)

            return list_var
        else:
            list_var = self.lista_variaveis(node.child[0])
            list_var.append(node.child[1].value)

            return list_var

    '''
    Verifica se uma variável foi declarada e se não possui atribuição
    '''
    def var(self, node):
        name_var = self.scope + "-" + node.value
        if name_var not in self.symbols:
            name_var = "global" + "-" + node.value
            if name_var not in self.symbols:
                print("ERRO: variavel " + node.value + " nao foi declarada")
                exit(1)

        if self.symbols[name_var][3] is False:
            print("ERRO: variavel " + node.value + " sem atribuicao")

        self.symbols[name_var][2] = True

        return self.symbols[name_var][4]

    '''
    Verifica o tipo da expressão passado dentro do colchete
    '''
    def indice(self, node):
        if len(node.child) == 1:
            tipo = self.expressao(node.child[0])
            if tipo != "inteiro":
                print("ERRO: aceita-se tamanho de vetor apenas do tipo inteiro")

            return "[]"
        else:
            var = self.indice(node.child[0])
            tipo = self.expressao(node.child[1])
            if tipo != "inteiro":
                print("ERRO: aceita-se tamanho de vetor apenas do tipo inteiro")

            return "[]" + var

    def tipo(self, node):
        if node.type == "inteiro" or node.type == "flutuante":
            return node.type
        else:
            print("ERRO: tipo " + node.type + "incorreto, espera-se apenas tipos inteiro, flutuante ou cientifico")

    '''
    Verifica se alguma função e alguma variável já foi declarada e adiciona a função na tabela de símbolos
    '''
    def declaracao_funcao(self, node):
        if len(node.child) == 1:
            tipo = "void"
            if node.child[0].value in self.symbols.keys():
                print("ERRO: função " + node.child[0].value + " ja foi declarada")

            elif "global" + "-" + node.child[0].value in self.symbols.keys():
                print("ERRO: variavel " + node.child[0].value + " ja foi declarada")

            self.symbols[node.child[0].value] = ["funcao", node.child[0].value, [], False, tipo]
            self.cabecalho(node.child[0])
        else:
            tipo = self.tipo(node.child[0])

            self.symbols[node.child[1].value] = ["funcao", node.child[1].value, [], False, tipo]
            self.cabecalho(node.child[1])

    '''
    Verifica se o tipo da função condiz com o retorno dela
    '''
    def cabecalho(self, node):
        #funcao, nome, lista parametros, usada, tipo
        list_par = self.lista_parametros(node.child[0])

        self.symbols[node.value][2] = list_par

        type_corpo = self.corpo(node.child[1])
        type_func = self.symbols[node.value][4]

        if type_corpo != type_func:
            if node.value != "principal":
                print("ERRO: a funcao " + node.value + " retorna " + type_corpo + " e deveria retornar " + type_func)
            else:
                print("WARNING: a funcao " + repr(node.value) + " retorna " + repr(type_corpo) + " e deveria retornar " + repr(type_func))

    '''
    Cria lista de parâmetros
    '''
    def lista_parametros(self, node):
        parametros = []
        if len(node.child) == 1:
            if node.child[0] is None:
                return self.vazio(node.child[0])
            else:
                parametros.append(self.parametro(node.child[0]))
                return parametros

        else:
            parametros = self.lista_parametros(node.child[0])
            parametros.append(self.parametro(node.child[1]))
            return parametros

    def parametro(self, node):
        if len(node.child) > 0 and node.child[0].type == "parametro":
            return self.parametro(node.child[0])
        else:
            if len(node.child) == 0:
                tipo = self.ultimo_tipo
            else:
                tipo = self.tipo(node.child[0])

            self.symbols[self.scope + "-" + node.value] = ["variavel", node.value, False, True, tipo, self.scope]
            self.ultimo_tipo = tipo
            return tipo

    def corpo(self, node):
        if len(node.child) == 1:
            return self.vazio(node.child[0])

        else:
            self.corpo(node.child[0])
            type_acao = self.acao(node.child[1])
            return type_acao

    def acao(self, node):
        if node.child[0].type == "expressao":
            return self.expressao(node.child[0])

        elif node.child[0].type == "declaracao_variaveis":
            return self.declaracao_variaveis(node.child[0])

        elif node.child[0].type == "se":
            return self.se(node.child[0])

        elif node.child[0].type == "repita":
            return self.repita(node.child[0])

        elif node.child[0].type == "leia":
            return self.leia(node.child[0])

        elif node.child[0].type == "escreva":
            return self.escreva(node.child[0])

        elif node.child[0].type == "retorna":
            return self.retorna(node.child[0])

        elif node.child[0].type == "error":
            return self.error(node.child[0])

    '''
    Verifica se a expressão é do tipo lógico e se as duas expressões no 'se' sao diferentes
    '''
    def se(self, node):
        see = self.expressao(node.child[0])
        if see != "logico":
            print("ERRO: a expressão " + see + " nao é do tipo logico")

        if len(node.child) == 2:
            return self.corpo(node.child[1])
        else:
            c1 = self.corpo(node.child[1])
            c2 = self.corpo(node.child[2])
            if c1 != c2:
                if c1 == "void":
                    return c2
                else:
                    return c1

            return c1

    def repita(self, node):
        repeat = self.expressao(node.child[1])
        if repeat != "logico":
            print("ERRO: a expressão " + repeat + " nao é do tipo logico")

        return self.corpo(node.child[0])

    '''
    Verifica se a variável foi declarada e se o tipo da variável condiz com o valor atribuído a ela
    '''
    def atribuicao(self, node):
        scope = self.scope + "-" + node.child[0].value
        if self.scope + "-" + node.child[0].value not in self.symbols.keys():
            scope = "global" + "-" + node.child[0].value
            if "global" + "-" + node.child[0].value not in self.symbols.keys():
                print("ERRO: variavel " + node.child[0].value + " nao foi declarada")

        tipo_before = self.symbols[scope][4]
        tipo_after = self.expressao(node.child[1])

        if tipo_before == "inteiro[]":
            tipo_before = tipo_before[:-2]

        self.symbols[scope][2] = True
        self.symbols[scope][3] = True
        if tipo_before != tipo_after:
            print("WARNING: tipo " + tipo_before + " é diferente de " + tipo_after + " var " + node.child[0].value)

        return "void"

    def leia(self, node):
        if self.scope + "-" + node.value not in self.symbols.keys():
            if "global" + "-" + node.value not in self.symbols.keys():
                print("ERRO: " + node.value + " nao foi declarada")

        return "void"

    def escreva(self, node):
        tipo_exp = self.expressao(node.child[0])

        if tipo_exp == "logico":
            print("ERRO: expressao invalida")

        return "void"

    def retorna(self, node):
        tipo_exp = self.expressao(node.child[0])

        if tipo_exp == "logico":
            print("ERRO: expressao invalida")
        return tipo_exp

    def expressao(self, node):
        if node.child[0].type == "expressao_simples":
            return self.expressao_simples(node.child[0])
        else:
            return self.atribuicao(node.child[0])

    def expressao_simples(self, node):
        if len(node.child) == 1:
            return self.expressao_aditiva(node.child[0])
        else:
            tipo1 = self.expressao_simples(node.child[0])
            self.operador_relacional(node.child[1])
            tipo2 = self.expressao_aditiva(node.child[2])
            if tipo1 == "inteiro[]":
                tipo1 = tipo1[:-2]

            if tipo2 == "inteiro[]":
                tipo2 = tipo2[:-2]

            if tipo1 != tipo2:
                print("WARNING: operacao do tipo " + tipo1 + " é diferente do tipo " + tipo2)
            return "logico"

    def expressao_aditiva(self, node):
        if len(node.child) == 1:
            return self.expressao_multiplicativa(node.child[0])
        else:
            tipo1 = self.expressao_aditiva(node.child[0])
            self.operador_soma(node.child[1])
            tipo2 = self.expressao_multiplicativa(node.child[2])

            if tipo1 == "inteiro[]":
                tipo1 = tipo1[:-2]

            if tipo2 == "inteiro[]":
                tipo2 = tipo2[:-2]

            if tipo1 != tipo2:
                print("WARNING: operacao do tipo " + tipo1 + " é diferente do tipo " + tipo2)
            if (tipo1 == "flutuante") or (tipo2 == "flutuante"):
                return "flutuante"
            else:
                return "inteiro"

    def expressao_multiplicativa(self, node):
        if len(node.child) == 1:
            return self.expressao_unaria(node.child[0])
        else:
            tipo1 = self.expressao_multiplicativa(node.child[0])
            self.operador_multiplicacao(node.child[1])
            tipo2 = self.expressao_unaria(node.child[2])

            if tipo1 == "inteiro[]":
                tipo1 = tipo1[:-2]

            if tipo2 == "inteiro[]":
                tipo2 = tipo2[:-2]

            if tipo1 != tipo2:
                print("WARNING: operacao do tipo " + tipo1 + " é diferente do tipo " + tipo2)
            if (tipo1 == "flutuante") or (tipo2 == "flutuante"):
                return "flutuante"
            else:
                return "inteiro"

    def expressao_unaria(self, node):
        if len(node.child) == 1:
            return self.fator(node.child[0])
        else:
            self.operador_soma(node.child[0])
            return self.fator(node.child[1])

    def operador_relacional(self, node):
        return node.value

    def operador_soma(self, node):
        return node.value

    def operador_multiplicacao(self, node):
        return node.value

    def fator(self, node):
        if node.child[0].type == "var":
            return self.var(node.child[0])

        if node.child[0].type == "chamada_funcao":
            return self.chamada_funcao(node.child[0])

        if node.child[0].type == "numero":
            return self.numero(node.child[0])

        else:
            return self.expressao(node.child[0])

    def numero(self, node):
        var = repr(node.value)
        if ("e" in var) or ("E" in var):
            return "cientifico"

        if "." in var:
            return "flutuante"

        else:
            return "inteiro"

    '''
    Verifica se existe uma recursão da main, se a main foi chamado em algum outro lugar e se os
    parâmetros condizem na chamada de uma função
    '''
    def chamada_funcao(self, node):
        if node.value == "principal" and self.scope == "principal":
            print("WARNING: chamada recursiva para a funcao principal")

        if node.value == "principal" and self.scope != "principal":
            print("ERRO: chamada da funcao principal na funcao " + self.scope)
            exit(1)

        if node.value not in self.symbols.keys():
            print("ERRO: funcao " + node.value + " nao foi declarada")
            exit(1)

        arg_pass = []
        arg_pass.append(self.lista_argumentos(node.child[0]))
        #print(arg_pass[0])
        if arg_pass[0] is "void":
            arg_pass = []

        elif type(arg_pass[0]) != str:
            arg_pass = arg_pass[0]

        arg_esp = self.symbols[node.value][2]

        if type(arg_esp) is str:
            arg_esp = []

        if len(arg_pass) != len(arg_esp):
            print("ERRO: argumentos invalidos. Espera-se " + repr(len(arg_esp)) + " e foi passado " + repr(len(arg_pass)))

        for i in range(len(arg_pass)):
            if arg_pass[i] != arg_esp[i]:
                print("WARNING: argumentos invalidos. Espera-se " + arg_esp[i] + "  e foi passado " + arg_pass[i])

        self.symbols[node.value][3] = True
        return self.symbols[node.value][4]

    def lista_argumentos(self, node):
        if len(node.child) == 1:
            if node.child[0] is None:
                return self.vazio(node.child[0])
            if node.child[0].type == "expressao":
                return self.expressao(node.child[0])

            else:
                return []
        else:
            list_arg = []
            list_arg.append(self.lista_argumentos(node.child[0]))
            if not (type(list_arg[0]) is str):
                list_arg = list_arg[0]

            list_arg.append(self.expressao(node.child[1]))
            return list_arg

    def vazio(self, node):
        return "void"

'''
print da árvore
'''
def print_tree(node, level="->"):
    if node is not None:
        print("%s %s %s" %(level, node.type, node.value))
        for son in node.child:
            print_tree(son, level+"->")

'''
print da tabela de símbolos
'''
def print_symbols(simbolos):
    for key, values in simbolos.items():
        print(values)

if __name__ == '__main__':
    codigo = open('C:/Users/Mateu/Desktop/UTFPR-BCC/Compiladores/geracao-codigo-testes/gencode-002.tpp')
    #r = codigo.read()
    f = Semantica(codigo.read())
    print_tree(f.tree)
    print_symbols(f.symbols)

    '''
    import sys
    codigo = open(sys.argv[1])
    f = Semantica(codigo.read())
    print_tree(f.tree)
    print_symbols(f.symbols)
    '''