from llvmlite import ir
from Main.AnaliseSintatica import Sintatica
from Main.AnaliseSemantica import Semantica

class GenCode:
    def __init__(self, code):
        self.tree = Sintatica(code).ast
        self.module = ir.Module('program')
        self.symbols = Semantica(code).symbols
        self.scope = "global"
        self.builder = None
        self.func = None
        self.programa(self.tree)

    def programa(self, node):
        self.lista_declaracoes(node.child[0])

    def lista_declaracoes(self, node):
        if len(node.child) == 1:
            self.declaracao(node.child[0])
        else:
            self.lista_declaracoes(node.child[0])
            self.declaracao(node.child[1])

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

    def declaracao_variaveis(self, node):
        var_type = node.child[0].type
        var_name = ""
        var_r = ""  # restante
        i = 0

        for son in self.lista_variaveis(node.child[1]):
            if "[" in son:
                for i in range(len(son)):
                    if son[i] == "[":
                        break
                    var_name += son[i]
                var_r = son[i:]
                son = var_name
            if self.scope == "global":
                if var_type == "inteiro":
                    var = ir.GlobalVariable(self.module, ir.IntType(32), son)
                    var.initializer = ir.Constant(ir.IntType(32), 0)
                    var.linkage = "common"
                    var.align = 4
                if var_type == "flutuante":
                    var = ir.GlobalVariable(self.module, ir.FloatType(), son)
                    var.initializer = ir.Constant(ir.FloatType(), 0)
                    var.linkage = "common"
                    var.align = 4
            else:
                if var_type == "inteiro":
                    var = self.builder.alloca(ir.IntType(32), name=son)
                    var.align = 4
                    num1 = ir.Constant(ir.IntType(32), 0)
                    self.builder.store(num1, var)
                if var_type == "flutuante":
                    var = self.builder.alloca(ir.FloatType(), name=son)
                    var.align = 4
                    num1 = ir.Constant(ir.FloatType(), 0)
                    self.builder.store(num1, var)

            self.symbols[self.scope + "-" + son] = ["variavel", son, False, False, var_type + var_r, self.scope, var]

    def inicializacao_variaveis(self, node):
        self.atribuicao(node.child[0])

    def lista_variaveis(self, node):
        print("bbbbbbbbbb")
        list_var = []
        if len(node.child) == 1:
            if len(node.child[0].child) == 1:
                list_var.append(node.child[0].value + self.indice(node.child[0].child[0]))
            else:
                list_var.append(node.child[0].value)

            return list_var

        else:
            list_var = self.lista_variaveis(node.child[0])

            if len(node.child[1].child) == 1:
                list_var.append(node.child[1].value) + self.indice(node.child[1].child[0])
            else:
                list_var.append(node.child[1].value)

            print("asf " + list_var)
            return list_var

    def var(self, node):
        name_var = self.scope + "-" + node.value
        if name_var not in self.symbols:
            name_var = "global" + "-" + node.value
            if name_var not in self.symbols:
                print("ERRO: variavel " + node.value + " nao foi declarada")
                exit(1)

        if self.symbols[name_var][3] is False:
            print("ERRO: variavel " + node.value + " sem atribuicao")

        self.symbols[name_var][2] = True  # seta ID com valor utilizado
        return self.symbols[name_var][4]

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
        print("asdfasd")
        print(node)
        if node == "inteiro":
            return ir.IntType(32)
        elif node == "flutuante":
            return ir.FloatType()
        else:
            # Caso type
            if node.type == "inteiro":
                return ir.IntType(32)
            else:
                return ir.FloatType()

    def declaracao_funcao(self, node):
        if len(node.child) == 1:
            tipo = "void"
            if self.symbols[node.child[0].value][2] is None:
                param = ir.VoidType()
            else:
                param = self.symbols[node.child[0].value][2]
            self.scope = node.child[0].value
            #tipo_return = ir.VoidType()
            tipo_param = ()
            if param != "void":
                for i in param:
                    if i == "inteiro":
                        tipo_param = ir.IntType(32) + tipo_param
                    if i == "flutuante":
                        tipo_param = ir.FloatType() + tipo_param
            tipo_return = ir.VoidType()
            tipo_func = ir.FunctionType(tipo_return, tipo_param)
            func = ir.Function(self.module, tipo_func, name=node.child[0].value)

            entryBlock = func.append_basic_block('entry')
            exitBasicBlock = func.append_basic_block('exit')

            self.builder = ir.IRBuilder(entryBlock)
            self.symbols[node.child[0].value] = ["funcao", node.child[0].value, [], tipo, 0, self.scope]
            self.cabecalho(node.child[0])
        else:
            print("ccccc")
            tipo = self.tipo(node.child[0])
            print(tipo)
            if self.symbols[node.child[1].value][2] is None:
                param = ir.VoidType()
            else:
                param = self.symbols[node.child[1].value][2]

            self.scope = node.child[1].value
            tipo_return = None
            if tipo == ir.IntType(32):

                tipo_return = ir.IntType(32)
            if tipo == ir.FloatType():
                tipo_return = ir.FloatType()
            tipo_param = ()
            if param != "void":
                for i in param:
                    if i == "inteiro":
                        tipo_param = ir.IntType(32) + tipo_param
                    if i == "flutuante":
                        tipo_param = ir.FloatType() + tipo_param

            #fnReturntipo = return_tipo
            tipo_func = ir.FunctionType(tipo_return, tipo_param)
            func = ir.Function(self.module, tipo_func, name=node.child[1].value)

            entryBlock = func.append_basic_block('entry')
            exitBasicBlock = func.append_basic_block('exit')

            self.builder = ir.IRBuilder(entryBlock)
            self.symbols[node.child[1].value] = ["funcao", node.child[1].value, [], tipo, 0, self.scope]
            self.cabecalho(node.child[1])

    def cabecalho(self, node):
        list_par = self.lista_parametros(node.child[0])

        self.symbols[node.value][2] = list_par
        self.corpo(node.child[1])

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
        if node.child[0].type == "parametro":
            return self.parametro(node.child[0])
        else:
            self.symbols[self.scope + "-" + node.value] = ["variavel", node.value, False, True,
                                                           node.child[0].type, self.scope]
            return self.tipo(node.child[0])

    def corpo(self, node):
        if len(node.child) == 1:
            return self.vazio(node.child[0])

        else:
            self.corpo(node.child[0])
            self.acao(node.child[1])

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

    #?????????????????
    def atribuicao(self, node):
        try:
            n_var = self.scope + "-" + node.child[0].value
            var_code = self.symbols[n_var][6]
        except:
            n_var = "global-" + node.child[0].value
            var_code = self.symbols[n_var][6]

        self.expressao(node.child[1])

        self.symbols[n_var][2] = True
        self.symbols[n_var][3] = True

        var = None
        no = node.child[1].child[0].child[0].child[0].child[0].child[0].child[0]
        if no == "var":
            try:
                nome_var = self.symbols[
                    self.scope + "-" + node.child[1].child[0].child[0].child[0].child[0].child[0].child[0].value]
                assembly = self.symbols[nome_var][6]
            except:
                nome_var = self.symbols[
                    "global-" + node.child[1].child[0].child[0].child[0].child[0].child[0].child[0].value]
                assembly = self.symbols[nome_var][6]
            self.builder.store(self.builder.load(assembly), self.symbols[n_var][6])

        elif no == "numero":
            valor = node.child[1].child[0].child[0].child[0].child[0].child[0].child[0].value

            if '.' not in valor:
                self.builder.store(ir.Constant(ir.IntType(32), int(valor)), self.symbols[n_var][6])
            else:
                self.builder.store(ir.Constant(ir.FloatType(), float(valor)), self.symbols[n_var][6])
        #self.builder.store(no, self.symbols[n_var][6])

    def leia(self, node):
        if self.scope + "-" + node.value not in self.symbols.keys():
            if "global" + "-" + node.value not in self.symbols.keys():
                print("ERRO: " + node.value + " nao foi declarada")

    # def escreva(self, node):

    def retorna(self, node):
        res = self.expressao(node.child[0])
        return res

    def expressao(self, node):
        if node.child[0].type == "expressao_simples":
            return self.expressao_simples(node.child[0])
        else:
            return self.atribuicao(node.child[0])

    def expressao_simples(self, node):
        if len(node.child) == 1:
            return self.expressao_aditiva(node.child[0])
        else:
            self.expressao_simples(node.child[0])
            self.operador_relacional(node.child[1])
            self.expressao_aditiva(node.child[2])
            return "logico"

    def expressao_aditiva(self, node):
        if len(node.child) == 1:
            return self.expressao_multiplicativa(node.child[0])
        else:
            tipo1 = self.expressao_aditiva(node.child[0])
            self.operador_soma(node.child[1])
            tipo2 = self.expressao_multiplicativa(node.child[2])

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
        return None

    def operador_soma(self, node):
        return None

    def operador_multiplicacao(self, node):
        return None

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

        return self.symbols[node.value][3]

    #def lista_argumentos(self, node):

    def vazio(self, node):
        return "void"

def print_trees(symbols):
    for k, v in symbols.items():
        print(repr(k)+repr(v))

if __name__ == '__main__':
    codigo = open('C:/Users/Mateu/Desktop/UTFPR-BCC/Compiladores/geracao-codigo-testes/gencode-001.tpp')
    #modulo = ir.Module('module_tpp')
    gen = GenCode(codigo.read())
    print(gen.module)
    print_trees(gen.symbols)

    '''
    import sys
    codigo = open(sys.argv[1])
    f = Semantica(codigo.read())
    print_tree(f.tree)
    print_symbols(f.symbols)
    '''