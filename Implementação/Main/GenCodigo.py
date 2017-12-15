from llvmlite import ir
from Main.AnaliseSintatica import Sintatica
from Main.AnaliseSemantica import Semantica
from pprint import pprint

class GenCode:
    def __init__(self, code):
        self.tree = Sintatica(code).ast
        self.module = ir.Module('program')
        self.symbols = Semantica(code).symbols
        self.scope = "global" #escopo atual
        self.scope_list = ["global"] #salva a lista de escopo
        self.builder = None
        self.func = None
        self.bloco = None #bloco atual
        self.ultimo_tipo = None #quando o parametro nao tiver tipo, pega o anterior
        self.posicao_parametro = 0 #controle de parametro
        self.leia_float = ir.Function(self.module, ir.FunctionType(ir.FloatType(), []), name="leiaFlutuante")
        self.leia_int = ir.Function(self.module, ir.FunctionType(ir.IntType(32), []), name="leiaInteiro")
        self.escreve_float = ir.Function(self.module, ir.FunctionType(ir.IntType(32), [ir.FloatType()]), name="escrevaFlutuante")
        self.escreve_int = ir.Function(self.module, ir.FunctionType(ir.IntType(32), [ir.IntType(32)]), name="escrevaInteiro")
        self.programa(self.tree)

    '''
    encontra a variavel na tabela de simbolos de acordo com o escopo
    trata o problema caso uma variavel foi declarada em um lugar e atribuida ou acessada em outro
    '''
    def find_var(self, name):
        for scope in reversed(self.scope_list):
            for key, value in self.symbols.items():
                if value[0] == "variavel" and value[5] == scope and value[1] == name and len(value) >= 7:
                    return value

        return None

    def find_func(self, name):
        for key, value in self.symbols.items():
            if value[0] == "funcao" and value[1] == name:
                return value

        return None

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
            self.declaracao_funcao(node.child[0])
            self.scope_list.pop()
            self.scope = self.scope_list[-1]

    def declaracao_variaveis(self, node):
        var_type = node.child[0].type
        lista_vars = self.lista_variaveis(node.child[1])

        for varname in lista_vars:
            if self.scope == "global":
                if var_type == "inteiro":
                    var = ir.GlobalVariable(self.module, ir.IntType(32), varname)
                    var.initializer = ir.Constant(ir.IntType(32), 0)
                else:
                    var = ir.GlobalVariable(self.module, ir.FloatType(), varname)
                    var.initializer = ir.Constant(ir.FloatType(), 0)
            else:
                if var_type == "inteiro":
                    var = self.builder.alloca(ir.IntType(32), name=varname)
                else:
                    var = self.builder.alloca(ir.FloatType(), name=varname)
                #num = ir.Constant(ir.FloatType(), 0)
                #self.builder.store(num, var)

            var.linkage = "common"
            var.align = 4
            self.symbols[self.scope + "-" + varname] = ["variavel", varname, False, False, var_type, self.scope, var]

    def inicializacao_variaveis(self, node):
        self.atribuicao(node.child[0])

    def lista_variaveis(self, node):
        list_var = []

        if len(node.child) == 1:
            list_var.append(self.varname(node.child[0]))
        else:
            for item in self.lista_variaveis(node.child[0]):
                list_var.append(item)
            list_var.append(self.varname(node.child[1]))

        return list_var

    def varname(self, node):
        if len(node.child) == 0:
            return node.value

        print("eroooo") # todo
        exit(1)

    # todo
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

    def declaracao_funcao(self, node):
        offset = 0
        if len(node.child) == 1:
            retorno = None
            llvm_retorno = ir.VoidType()
        else:
            offset = 1
            if node.child[0].value == "inteiro":
                retorno = "inteiro"
                llvm_retorno = ir.IntType(32)
            else:
                retorno = "flutuante"
                llvm_retorno = ir.FloatType()

        cabeca = self.cabecalho(retorno, node.child[offset])
        lista_param = cabeca[0]
        llvm_params = []
        corpo_node = cabeca[1]
        func_nome = cabeca[2]

        for param in lista_param:
            tipo = param[0]

            if tipo == "inteiro":
                llvm_params.append(ir.IntType(32))
            else:
                llvm_params.append(ir.FloatType())

        if func_nome == "principal":
            nome_func = "main"
        else:
            nome_func = func_nome
        llvm_func_type = ir.FunctionType(llvm_retorno, llvm_params)
        self.func = ir.Function(self.module, llvm_func_type, name=nome_func)

        scope_nome = func_nome
        self.scope_list.append(scope_nome)
        self.scope = scope_nome

        entry_block = self.func.append_basic_block('entry')

        self.builder = ir.IRBuilder(entry_block)
        self.bloco = entry_block
        self.symbols[func_nome] = ["funcao", func_nome, lista_param, llvm_retorno, 0, scope_nome, self.func]
        self.corpo(corpo_node)

    def cabecalho(self, tipo, node):
        self.posicao_parametro = 0
        lista_par = self.lista_parametros(node.child[0])
        print(node.value)

        return [lista_par, node.child[1], node.value]

    def lista_parametros(self, node):
        if len(node.child) == 1 and node.child[0] is not None:
            return [self.parametro(node.child[0])]
        elif len(node.child) == 2:
            parametros = self.lista_parametros(node.child[0])
            parametros.append(self.parametro(node.child[1]))

            return parametros
        else:
            return []

    def parametro(self, node):
        if len(node.child) == 0:
            tipo = self.ultimo_tipo
        else:
            tipo = node.child[0].value

        self.ultimo_tipo = tipo
        name = node.value
        posicao = self.posicao_parametro
        self.posicao_parametro += 1

        return [tipo, name, posicao]

    def corpo(self, node):
        if len(node.child) == 2:
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

    # todo
    def se(self, node):
        if len(node.child) == 2:
            origem_bloco = self.bloco
            condicao_expr = self.expressao(node.child[0])

            true_bloco = self.func.append_basic_block("SE-VERDADE")
            self.bloco = true_bloco
            self.builder.position_at_end(true_bloco)
            self.corpo(node.child[1])
            outer_true_bloco = self.bloco

            self.bloco = origem_bloco
            self.builder.position_at_end(origem_bloco)
            fim_bloco = self.func.append_basic_block("SE-TERMINO")

            self.builder.cbranch(condicao_expr, true_bloco, fim_bloco)

            self.bloco = outer_true_bloco
            self.builder.position_at_end(outer_true_bloco)

            if not self.bloco.is_terminated:
                self.builder.branch(fim_bloco)

            self.bloco = fim_bloco
            self.builder.position_at_end(fim_bloco)
        else:
            origem_bloco = self.bloco
            condicao_expr = self.expressao(node.child[0])

            true_bloco = self.func.append_basic_block("SE-VERDADE")
            self.bloco = true_bloco
            self.builder.position_at_end(true_bloco)
            self.corpo(node.child[1])
            outer_true_bloco = self.bloco

            false_bloco = self.func.append_basic_block("SE-FALSO")
            self.bloco = false_bloco
            self.builder.position_at_end(false_bloco)
            self.corpo(node.child[1])
            outer_false_bloco = self.bloco

            self.bloco = origem_bloco
            self.builder.position_at_end(origem_bloco)
            fim_bloco = self.func.append_basic_block("SE-TERMINO")

            self.builder.cbranch(condicao_expr, true_bloco, false_bloco)

            self.bloco = outer_true_bloco
            self.builder.position_at_end(outer_true_bloco)

            if not self.bloco.is_terminated:
                self.builder.branch(fim_bloco)

            self.bloco = outer_false_bloco
            self.builder.position_at_end(outer_false_bloco)

            if not self.bloco.is_terminated:
                self.builder.branch(fim_bloco)

            self.bloco = fim_bloco
            self.builder.position_at_end(fim_bloco)

    def repita(self, node):
        origem_bloco = self.bloco

        repita = self.func.append_basic_block("REPITA")
        self.builder.branch(repita)
        self.bloco = repita
        self.builder.position_at_end(repita)
        self.corpo(node.child[0])

        ate_expr = self.expressao(node.child[1])

        self.bloco = origem_bloco
        self.builder.position_at_end(origem_bloco)
        fim_repita = self.func.append_basic_block("FIM-REPITA")

        self.bloco = repita
        self.builder.position_at_end(repita)

        self.builder.cbranch(ate_expr, fim_repita, repita)

        self.bloco = fim_repita
        self.builder.position_at_end(fim_repita)

    def atribuicao(self, node):
        varname = self.varname(node.child[0])
        expr = self.expressao(node.child[1])
        var = self.find_var(varname)

        if var is None:
            return

        llvm_var = var[6]

        var[2] = True
        var[3] = True
        self.builder.store(expr, llvm_var)

    def leia(self, node):
        var = self.find_var(node.value)

        if var[4] == "inteiro":
            llvm_func = self.leia_int
        else:
            llvm_func = self.leia_float

        llvm_var = var[6]
        llvm_value = self.builder.call(llvm_func, [], "")
        self.builder.store(llvm_value, llvm_var)

    def escreva(self, node):
        llvm_value = self.expressao(node.child[0])
        llvm_value_type = llvm_value.type

        if llvm_value_type == ir.IntType(32):
            llvm_func = self.escreve_int
        else:
            llvm_func = self.escreve_float

        self.builder.call(llvm_func, [llvm_value], "")

    def retorna(self, node):
        res = self.expressao(node.child[0])
        self.builder.ret(res)

    def expressao(self, node):
        if node.child[0].type == "expressao_simples":
            return self.expressao_simples(node.child[0])
        else:
            return self.atribuicao(node.child[0])

    def expressao_simples(self, node):
        if len(node.child) == 1:
            return self.expressao_aditiva(node.child[0])
        else:
            left = self.expressao_simples(node.child[0])
            tipo_opr = node.child[1].value
            right = self.expressao_aditiva(node.child[2])

            if tipo_opr == "=":
                tipo_opr = "=="
            if tipo_opr == "&&":
                result = self.builder.and_(left, right, "")
            elif tipo_opr == "||":
                result = self.builder.or_(left, right, "")
            else:
                result = self.builder.icmp_signed(tipo_opr, left, right, "")

            return result

    def expressao_aditiva(self, node):
        if len(node.child) == 1:
            return self.expressao_multiplicativa(node.child[0])
        else:
            left = self.expressao_aditiva(node.child[0])
            tipo_opr = node.child[1].value
            right = self.expressao_multiplicativa(node.child[2])

            if left.type is ir.FloatType() or right.type is ir.FloatType():
                if tipo_opr == "+":
                    return self.builder.fadd(left, right)
                elif tipo_opr == "-":
                    return self.builder.fsub(left, right)
            else:
                if tipo_opr == "+":
                    return self.builder.add(left, right)
                elif tipo_opr == "-":
                    return self.builder.sub(left, right)

    def expressao_multiplicativa(self, node):
        if len(node.child) == 1:
            return self.expressao_unaria(node.child[0])
        else:
            left = self.expressao_multiplicativa(node.child[0])
            tipo_opr = node.child[1].value
            right = self.expressao_unaria(node.child[2])

            if left.type is ir.FloatType() or right.type is ir.FloatType():
                if tipo_opr == "*":
                    return self.builder.fmul(left, right)
            else:
                return self.builder.mul(left, right)

            if tipo_opr == "/":
                return self.builder.fdiv(left, right)

    def expressao_unaria(self, node):
        if len(node.child) == 1:
            return self.fator(node.child[0])
        else:
            tipo_opr = node.child[0].value
            expr = self.fator(node.child[1])

            if tipo_opr == "-" or tipo_opr == "!":
                return self.builder.neg(expr)

            return expr

    def fator(self, node):
        if node.child[0].type == "var":
            return self.var(node.child[0])
        elif node.child[0].type == "chamada_funcao":
            return self.chamada_funcao(node.child[0])
        elif node.child[0].type == "numero":
            return self.numero(node.child[0])
        else:
            return self.expressao(node.child[0])

    def var(self, node):
        varname = node.value
        var = self.find_var(varname)

        if var is None:
            func_nome = self.func.name
            func = self.find_func(func_nome)
            params = func[2]

            for param in params:
                nome = param[1]

                if nome == varname:
                    indice = param[2]
                    return self.func.args[indice]

        return self.builder.load(var[6])

    def numero(self, node):
        plain = node.value

        if "e" in plain or "E" in plain:
            print("cientifico")
            exit(1)
            return None

        if "." in plain:
            return ir.Constant(ir.FloatType(), float(plain))
        else:
            return ir.Constant(ir.IntType(32), int(plain))

    def chamada_funcao(self, node):
        func_name = node.value
        lista_args = self.lista_argumentos(node.child[0])
        func = self.find_func(func_name)
        llvm_func = func[6]

        return self.builder.call(llvm_func, lista_args, "")

    def lista_argumentos(self, node):
        if len(node.child) == 1:
            if node.child[0] is None:
                return []

            return [self.expressao(node.child[0])]
        else:
            args = self.lista_argumentos(node.child[0])
            args.append(self.expressao(node.child[1]))
            return args

def print_trees(symbols):
    for k, v in symbols.items():
        print(repr(k)+repr(v))

if __name__ == '__main__':
    codigo = open('C:/Users/Mateu/Desktop/UTFPR-BCC/Compiladores/geracao-codigo-testes/gencode-003.tpp')
    gen = GenCode(codigo.read())
    print(gen.module)
    print_trees(gen.symbols)

    '''
    import sys
    codigo = open(sys.argv[1])
    gen = GenCode(codigo.read())
    print(gen.module)
    '''