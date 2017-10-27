
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftIGUALMAIOREQMAIORMENOREQMENORleftPLUSMINUSleftVEZESDIVIDEPLUS MINUS VEZES DIVIDE IGUAL VIRGULA DOISPONTOS LCOLCH RCOLCH NEGACAO LPAREN RPAREN MAIOR MENOR MENOREQ MAIOREQ ATRIBUICAO ELOGICO DIF PR SB ID NUM_FLUTUANTE COMENTARIO NUM_CIENTIFICA NUM_INTEIRO COMENTARIO_INCOMPLETO ATE SE SENAO ENTAO FIM REPITA FLUTUANTE RETORNA LEIA ESCREVA INTEIRO\n        programa : lista_declaracoes\n        \n        lista_declaracoes : lista_declaracoes declaracao\n                            | declaracao\n        \n        declaracao : declaracao_variaveis\n                     | inicializacao_variaveis\n                     | declaracao_funcao\n        \n        declaracao_variaveis : tipo DOISPONTOS lista_variaveis\n        \n        inicializacao_variaveis : atribuicao\n        \n        lista_variaveis : lista_variaveis VIRGULA var\n                          | var\n        \n        var : ID\n              | ID indice\n        \n        indice : indice LCOLCH expressao RCOLCH\n                 | LCOLCH expressao RCOLCH\n        \n        tipo : INTEIRO\n               | FLUTUANTE\n        \n        declaracao_funcao : tipo cabecalho\n                            | cabecalho\n        \n        cabecalho : ID LPAREN lista_parametros RPAREN corpo FIM\n        \n        lista_parametros : lista_parametros VIRGULA parametro\n                           | parametro\n                           | vazio\n        \n        parametro : tipo DOISPONTOS ID\n        \n        parametro :  parametro LCOLCH RCOLCH\n        \n        corpo : corpo acao\n                | vazio\n        \n        acao : expressao\n               | declaracao_variaveis\n               | se\n               | repita\n               | leia\n               | escreva\n               | retorna\n               | error\n        \n        se : SE expressao ENTAO corpo FIM\n             | SE expressao ENTAO corpo SENAO corpo FIM\n        \n        repita : REPITA corpo ATE expressao\n        \n        atribuicao : var ATRIBUICAO expressao\n        \n        leia : LEIA LPAREN ID RPAREN\n        \n        escreva : ESCREVA LPAREN expressao RPAREN\n        \n        retorna : RETORNA LPAREN expressao RPAREN\n        \n        expressao : expressao_simples\n                    | atribuicao\n        \n        expressao_simples : expressao_aditiva\n                            | expressao_simples operador_relacional expressao_aditiva\n        \n        expressao_aditiva : expressao_multiplicativa\n                            | expressao_aditiva operador_soma expressao_multiplicativa\n        \n        expressao_multiplicativa : expressao_unaria\n                                   | expressao_multiplicativa operador_multiplicacao expressao_unaria\n        \n        expressao_unaria : fator\n                           | operador_soma fator\n        \n        operador_relacional : MENOR\n                              | MAIOR\n                              | IGUAL\n                              | DIF\n                              | MENOREQ\n                              | MAIOREQ\n        \n        operador_soma : PLUS\n                        | MINUS\n        \n        operador_multiplicacao : VEZES\n                                 | DIVIDE\n        \n        fator : RPAREN expressao LPAREN\n                | var\n                | chamada_funcao\n                | numero\n        \n        numero : NUM_INTEIRO\n                 | NUM_FLUTUANTE\n                 | NUM_CIENTIFICA\n        \n        chamada_funcao : ID LPAREN lista_argumentos RPAREN\n        \n        lista_argumentos : lista_argumentos VIRGULA expressao\n                           | expressao\n                           | vazio\n        \n        vazio :\n        '
    
_lr_action_items = {'INTEIRO':([0,2,3,4,5,6,8,9,14,16,19,20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,66,70,71,72,73,74,78,79,80,84,85,87,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[10,10,-3,-4,-5,-6,-8,-18,-2,-17,10,-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,10,-14,-9,-45,-47,-49,-62,10,-26,-13,-69,-19,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,10,-73,10,-37,-39,-40,-41,-35,-73,10,-36,]),'FLUTUANTE':([0,2,3,4,5,6,8,9,14,16,19,20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,66,70,71,72,73,74,78,79,80,84,85,87,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[11,11,-3,-4,-5,-6,-8,-18,-2,-17,11,-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,11,-14,-9,-45,-47,-49,-62,11,-26,-13,-69,-19,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,11,-73,11,-37,-39,-40,-41,-35,-73,11,-36,]),'ID':([0,2,3,4,5,6,7,8,9,10,11,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,47,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,68,70,71,72,73,74,78,79,80,84,85,86,87,88,89,90,91,92,93,94,95,96,98,99,105,106,107,108,109,110,114,115,116,117,118,119,120,121,122,],[13,13,-3,-4,-5,-6,17,-8,-18,-15,-16,-2,24,-17,32,-12,32,-7,-10,-11,-63,-38,-42,-43,-44,-46,32,-11,-48,-50,32,-64,-65,-58,-59,-66,-67,-68,32,24,32,-52,-53,-54,-55,-56,-57,32,32,-60,-61,-51,-63,32,-73,83,-14,-9,-45,-47,-49,-62,32,-26,-13,-69,32,-19,-25,-27,-28,-29,-30,-31,-32,-33,-34,32,-73,32,111,32,32,-73,32,32,-37,-39,-40,-41,-35,-73,32,-36,]),'$end':([1,2,3,4,5,6,8,9,14,16,20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,70,71,72,73,74,78,84,85,87,],[0,-1,-3,-4,-5,-6,-8,-18,-2,-17,-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-9,-45,-47,-49,-62,-13,-69,-19,]),'DOISPONTOS':([7,10,11,46,97,],[15,-15,-16,68,15,]),'ATRIBUICAO':([12,13,20,25,32,70,84,],[18,-11,-12,18,-11,-14,-13,]),'LPAREN':([13,17,20,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,64,70,72,73,74,78,84,85,100,101,102,],[19,19,-12,-63,-38,-42,-43,-44,-46,63,-48,-50,-64,-65,-66,-67,-68,-51,-63,78,-14,-45,-47,-49,-62,-13,-69,106,107,108,]),'LCOLCH':([13,20,24,32,44,70,81,82,83,84,],[21,47,21,21,67,-14,67,-24,-23,-13,]),'RPAREN':([18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,88,89,90,91,92,93,94,95,96,98,99,103,105,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,],[35,-73,-12,35,-7,-10,-11,-63,-38,-42,-43,-44,-46,35,-11,-48,-50,35,-64,-65,-58,-59,-66,-67,-68,65,-21,-22,35,35,-52,-53,-54,-55,-56,-57,35,35,-60,-61,-51,-63,35,-73,-14,-9,-45,-47,-49,85,-71,-72,-62,35,-26,-20,-24,-23,-13,-69,35,-25,-27,-28,-29,-30,-31,-32,-33,-34,35,-73,-70,35,35,35,-73,35,116,117,118,35,-37,-39,-40,-41,-35,-73,35,-36,]),'PLUS':([18,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,47,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,70,71,72,73,74,78,79,80,84,85,86,88,89,90,91,92,93,94,95,96,98,99,105,107,108,109,110,114,115,116,117,118,119,120,121,122,],[38,-12,38,-7,-10,-11,-63,-38,-42,-43,38,-46,-11,-48,-50,38,-64,-65,-58,-59,-66,-67,-68,38,38,-52,-53,-54,-55,-56,-57,38,38,-60,-61,-51,-63,38,-73,-14,-9,38,-47,-49,-62,38,-26,-13,-69,38,-25,-27,-28,-29,-30,-31,-32,-33,-34,38,-73,38,38,38,-73,38,38,-37,-39,-40,-41,-35,-73,38,-36,]),'MINUS':([18,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,47,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,70,71,72,73,74,78,79,80,84,85,86,88,89,90,91,92,93,94,95,96,98,99,105,107,108,109,110,114,115,116,117,118,119,120,121,122,],[39,-12,39,-7,-10,-11,-63,-38,-42,-43,39,-46,-11,-48,-50,39,-64,-65,-58,-59,-66,-67,-68,39,39,-52,-53,-54,-55,-56,-57,39,39,-60,-61,-51,-63,39,-73,-14,-9,39,-47,-49,-62,39,-26,-13,-69,39,-25,-27,-28,-29,-30,-31,-32,-33,-34,39,-73,39,39,39,-73,39,39,-37,-39,-40,-41,-35,-73,39,-36,]),'NUM_INTEIRO':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,47,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,70,71,72,73,74,78,79,80,84,85,86,88,89,90,91,92,93,94,95,96,98,99,105,107,108,109,110,114,115,116,117,118,119,120,121,122,],[40,-12,40,-7,-10,-11,-63,-38,-42,-43,-44,-46,40,-11,-48,-50,40,-64,-65,-58,-59,-66,-67,-68,40,40,-52,-53,-54,-55,-56,-57,40,40,-60,-61,-51,-63,40,-73,-14,-9,-45,-47,-49,-62,40,-26,-13,-69,40,-25,-27,-28,-29,-30,-31,-32,-33,-34,40,-73,40,40,40,-73,40,40,-37,-39,-40,-41,-35,-73,40,-36,]),'NUM_FLUTUANTE':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,47,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,70,71,72,73,74,78,79,80,84,85,86,88,89,90,91,92,93,94,95,96,98,99,105,107,108,109,110,114,115,116,117,118,119,120,121,122,],[41,-12,41,-7,-10,-11,-63,-38,-42,-43,-44,-46,41,-11,-48,-50,41,-64,-65,-58,-59,-66,-67,-68,41,41,-52,-53,-54,-55,-56,-57,41,41,-60,-61,-51,-63,41,-73,-14,-9,-45,-47,-49,-62,41,-26,-13,-69,41,-25,-27,-28,-29,-30,-31,-32,-33,-34,41,-73,41,41,41,-73,41,41,-37,-39,-40,-41,-35,-73,41,-36,]),'NUM_CIENTIFICA':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,47,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,70,71,72,73,74,78,79,80,84,85,86,88,89,90,91,92,93,94,95,96,98,99,105,107,108,109,110,114,115,116,117,118,119,120,121,122,],[42,-12,42,-7,-10,-11,-63,-38,-42,-43,-44,-46,42,-11,-48,-50,42,-64,-65,-58,-59,-66,-67,-68,42,42,-52,-53,-54,-55,-56,-57,42,42,-60,-61,-51,-63,42,-73,-14,-9,-45,-47,-49,-62,42,-26,-13,-69,42,-25,-27,-28,-29,-30,-31,-32,-33,-34,42,-73,42,42,42,-73,42,42,-37,-39,-40,-41,-35,-73,42,-36,]),'VIRGULA':([19,20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,43,44,45,61,62,63,70,71,72,73,74,75,76,77,78,81,82,83,84,85,103,],[-73,-12,49,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,66,-21,-22,-51,-63,-73,-14,-9,-45,-47,-49,86,-71,-72,-62,-20,-24,-23,-13,-69,-70,]),'FIM':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,87,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,119,-37,-39,-40,-41,-35,-73,122,-36,]),'error':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,96,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,96,-73,96,-37,-39,-40,-41,-35,-73,96,-36,]),'SE':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,98,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,98,-73,98,-37,-39,-40,-41,-35,-73,98,-36,]),'REPITA':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,99,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,99,-73,99,-37,-39,-40,-41,-35,-73,99,-36,]),'LEIA':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,100,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,100,-73,100,-37,-39,-40,-41,-35,-73,100,-36,]),'ESCREVA':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,101,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,101,-73,101,-37,-39,-40,-41,-35,-73,101,-36,]),'RETORNA':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,65,70,71,72,73,74,78,79,80,84,85,88,89,90,91,92,93,94,95,96,99,105,109,114,115,116,117,118,119,120,121,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-73,-14,-9,-45,-47,-49,-62,102,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,102,-73,102,-37,-39,-40,-41,-35,-73,102,-36,]),'ATE':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,70,71,72,73,74,78,80,84,85,88,89,90,91,92,93,94,95,96,99,105,115,116,117,118,119,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-9,-45,-47,-49,-62,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,110,-37,-39,-40,-41,-35,-36,]),'SENAO':([20,22,23,24,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,70,71,72,73,74,78,80,84,85,88,89,90,91,92,93,94,95,96,109,114,115,116,117,118,119,122,],[-12,-7,-10,-11,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-9,-45,-47,-49,-62,-26,-13,-69,-25,-27,-28,-29,-30,-31,-32,-33,-34,-73,120,-37,-39,-40,-41,-35,-36,]),'VEZES':([20,25,30,32,33,34,36,37,40,41,42,61,62,70,73,74,78,84,85,],[-12,-63,59,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,59,-49,-62,-13,-69,]),'DIVIDE':([20,25,30,32,33,34,36,37,40,41,42,61,62,70,73,74,78,84,85,],[-12,-63,60,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,60,-49,-62,-13,-69,]),'MENOR':([20,25,27,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,],[-12,-63,51,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,]),'MAIOR':([20,25,27,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,],[-12,-63,52,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,]),'IGUAL':([20,25,27,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,],[-12,-63,53,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,]),'DIF':([20,25,27,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,],[-12,-63,54,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,]),'MENOREQ':([20,25,27,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,],[-12,-63,55,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,]),'MAIOREQ':([20,25,27,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,],[-12,-63,56,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,]),'RCOLCH':([20,25,26,27,28,29,30,32,33,34,36,37,40,41,42,48,61,62,67,69,70,72,73,74,78,84,85,],[-12,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,70,-51,-63,82,84,-14,-45,-47,-49,-62,-13,-69,]),'ENTAO':([20,25,26,27,28,29,30,32,33,34,36,37,40,41,42,61,62,70,72,73,74,78,84,85,104,],[-12,-63,-38,-42,-43,-44,-46,-11,-48,-50,-64,-65,-66,-67,-68,-51,-63,-14,-45,-47,-49,-62,-13,-69,109,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'lista_declaracoes':([0,],[2,]),'declaracao':([0,2,],[3,14,]),'declaracao_variaveis':([0,2,79,105,114,121,],[4,4,90,90,90,90,]),'inicializacao_variaveis':([0,2,],[5,5,]),'declaracao_funcao':([0,2,],[6,6,]),'tipo':([0,2,19,66,79,105,114,121,],[7,7,46,46,97,97,97,97,]),'atribuicao':([0,2,18,21,35,47,63,79,86,98,105,107,108,110,114,121,],[8,8,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'cabecalho':([0,2,7,],[9,9,16,]),'var':([0,2,15,18,21,31,35,47,49,50,57,58,63,79,86,98,105,107,108,110,114,121,],[12,12,23,25,25,62,25,25,71,62,62,62,25,25,25,25,25,25,25,25,25,25,]),'indice':([13,24,32,],[20,20,20,]),'lista_variaveis':([15,],[22,]),'expressao':([18,21,35,47,63,79,86,98,105,107,108,110,114,121,],[26,48,64,69,76,89,103,104,89,112,113,115,89,89,]),'expressao_simples':([18,21,35,47,63,79,86,98,105,107,108,110,114,121,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'expressao_aditiva':([18,21,35,47,50,63,79,86,98,105,107,108,110,114,121,],[29,29,29,29,72,29,29,29,29,29,29,29,29,29,29,]),'expressao_multiplicativa':([18,21,35,47,50,57,63,79,86,98,105,107,108,110,114,121,],[30,30,30,30,30,73,30,30,30,30,30,30,30,30,30,30,]),'operador_soma':([18,21,29,35,47,50,57,58,63,72,79,86,98,105,107,108,110,114,121,],[31,31,57,31,31,31,31,31,31,57,31,31,31,31,31,31,31,31,31,]),'expressao_unaria':([18,21,35,47,50,57,58,63,79,86,98,105,107,108,110,114,121,],[33,33,33,33,33,33,74,33,33,33,33,33,33,33,33,33,33,]),'fator':([18,21,31,35,47,50,57,58,63,79,86,98,105,107,108,110,114,121,],[34,34,61,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'chamada_funcao':([18,21,31,35,47,50,57,58,63,79,86,98,105,107,108,110,114,121,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'numero':([18,21,31,35,47,50,57,58,63,79,86,98,105,107,108,110,114,121,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'lista_parametros':([19,],[43,]),'parametro':([19,66,],[44,81,]),'vazio':([19,63,65,99,109,120,],[45,77,80,80,80,80,]),'operador_relacional':([27,],[50,]),'operador_multiplicacao':([30,73,],[58,58,]),'lista_argumentos':([63,],[75,]),'corpo':([65,99,109,120,],[79,105,114,121,]),'acao':([79,105,114,121,],[88,88,88,88,]),'se':([79,105,114,121,],[91,91,91,91,]),'repita':([79,105,114,121,],[92,92,92,92,]),'leia':([79,105,114,121,],[93,93,93,93,]),'escreva':([79,105,114,121,],[94,94,94,94,]),'retorna':([79,105,114,121,],[95,95,95,95,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> lista_declaracoes','programa',1,'p_programa','AnaliseSintatica.py',30),
  ('lista_declaracoes -> lista_declaracoes declaracao','lista_declaracoes',2,'p_lista_declaracoes','AnaliseSintatica.py',36),
  ('lista_declaracoes -> declaracao','lista_declaracoes',1,'p_lista_declaracoes','AnaliseSintatica.py',37),
  ('declaracao -> declaracao_variaveis','declaracao',1,'p_declaracao','AnaliseSintatica.py',46),
  ('declaracao -> inicializacao_variaveis','declaracao',1,'p_declaracao','AnaliseSintatica.py',47),
  ('declaracao -> declaracao_funcao','declaracao',1,'p_declaracao','AnaliseSintatica.py',48),
  ('declaracao_variaveis -> tipo DOISPONTOS lista_variaveis','declaracao_variaveis',3,'p_declaracao_variaveis','AnaliseSintatica.py',54),
  ('inicializacao_variaveis -> atribuicao','inicializacao_variaveis',1,'p_inicializacao_variaveis','AnaliseSintatica.py',60),
  ('lista_variaveis -> lista_variaveis VIRGULA var','lista_variaveis',3,'p_lista_variaveis','AnaliseSintatica.py',66),
  ('lista_variaveis -> var','lista_variaveis',1,'p_lista_variaveis','AnaliseSintatica.py',67),
  ('var -> ID','var',1,'p_var','AnaliseSintatica.py',76),
  ('var -> ID indice','var',2,'p_var','AnaliseSintatica.py',77),
  ('indice -> indice LCOLCH expressao RCOLCH','indice',4,'p_indice','AnaliseSintatica.py',86),
  ('indice -> LCOLCH expressao RCOLCH','indice',3,'p_indice','AnaliseSintatica.py',87),
  ('tipo -> INTEIRO','tipo',1,'p_tipo','AnaliseSintatica.py',96),
  ('tipo -> FLUTUANTE','tipo',1,'p_tipo','AnaliseSintatica.py',97),
  ('declaracao_funcao -> tipo cabecalho','declaracao_funcao',2,'p_declaracao_funcao','AnaliseSintatica.py',103),
  ('declaracao_funcao -> cabecalho','declaracao_funcao',1,'p_declaracao_funcao','AnaliseSintatica.py',104),
  ('cabecalho -> ID LPAREN lista_parametros RPAREN corpo FIM','cabecalho',6,'p_cabecalho','AnaliseSintatica.py',113),
  ('lista_parametros -> lista_parametros VIRGULA parametro','lista_parametros',3,'p_lista_parametros','AnaliseSintatica.py',119),
  ('lista_parametros -> parametro','lista_parametros',1,'p_lista_parametros','AnaliseSintatica.py',120),
  ('lista_parametros -> vazio','lista_parametros',1,'p_lista_parametros','AnaliseSintatica.py',121),
  ('parametro -> tipo DOISPONTOS ID','parametro',3,'p_parametro','AnaliseSintatica.py',130),
  ('parametro -> parametro LCOLCH RCOLCH','parametro',3,'p_parametro2','AnaliseSintatica.py',136),
  ('corpo -> corpo acao','corpo',2,'p_corpo','AnaliseSintatica.py',142),
  ('corpo -> vazio','corpo',1,'p_corpo','AnaliseSintatica.py',143),
  ('acao -> expressao','acao',1,'p_acao','AnaliseSintatica.py',152),
  ('acao -> declaracao_variaveis','acao',1,'p_acao','AnaliseSintatica.py',153),
  ('acao -> se','acao',1,'p_acao','AnaliseSintatica.py',154),
  ('acao -> repita','acao',1,'p_acao','AnaliseSintatica.py',155),
  ('acao -> leia','acao',1,'p_acao','AnaliseSintatica.py',156),
  ('acao -> escreva','acao',1,'p_acao','AnaliseSintatica.py',157),
  ('acao -> retorna','acao',1,'p_acao','AnaliseSintatica.py',158),
  ('acao -> error','acao',1,'p_acao','AnaliseSintatica.py',159),
  ('se -> SE expressao ENTAO corpo FIM','se',5,'p_se','AnaliseSintatica.py',165),
  ('se -> SE expressao ENTAO corpo SENAO corpo FIM','se',7,'p_se','AnaliseSintatica.py',166),
  ('repita -> REPITA corpo ATE expressao','repita',4,'p_repita','AnaliseSintatica.py',175),
  ('atribuicao -> var ATRIBUICAO expressao','atribuicao',3,'p_atribuicao','AnaliseSintatica.py',181),
  ('leia -> LEIA LPAREN ID RPAREN','leia',4,'p_leia','AnaliseSintatica.py',187),
  ('escreva -> ESCREVA LPAREN expressao RPAREN','escreva',4,'p_escreva','AnaliseSintatica.py',193),
  ('retorna -> RETORNA LPAREN expressao RPAREN','retorna',4,'p_retorna','AnaliseSintatica.py',199),
  ('expressao -> expressao_simples','expressao',1,'p_expressao','AnaliseSintatica.py',205),
  ('expressao -> atribuicao','expressao',1,'p_expressao','AnaliseSintatica.py',206),
  ('expressao_simples -> expressao_aditiva','expressao_simples',1,'p_expressao_simples','AnaliseSintatica.py',212),
  ('expressao_simples -> expressao_simples operador_relacional expressao_aditiva','expressao_simples',3,'p_expressao_simples','AnaliseSintatica.py',213),
  ('expressao_aditiva -> expressao_multiplicativa','expressao_aditiva',1,'p_expressao_aditiva','AnaliseSintatica.py',222),
  ('expressao_aditiva -> expressao_aditiva operador_soma expressao_multiplicativa','expressao_aditiva',3,'p_expressao_aditiva','AnaliseSintatica.py',223),
  ('expressao_multiplicativa -> expressao_unaria','expressao_multiplicativa',1,'p_expressao_multiplicativa','AnaliseSintatica.py',232),
  ('expressao_multiplicativa -> expressao_multiplicativa operador_multiplicacao expressao_unaria','expressao_multiplicativa',3,'p_expressao_multiplicativa','AnaliseSintatica.py',233),
  ('expressao_unaria -> fator','expressao_unaria',1,'p_expressao_unaria','AnaliseSintatica.py',242),
  ('expressao_unaria -> operador_soma fator','expressao_unaria',2,'p_expressao_unaria','AnaliseSintatica.py',243),
  ('operador_relacional -> MENOR','operador_relacional',1,'p_operador_relacional','AnaliseSintatica.py',252),
  ('operador_relacional -> MAIOR','operador_relacional',1,'p_operador_relacional','AnaliseSintatica.py',253),
  ('operador_relacional -> IGUAL','operador_relacional',1,'p_operador_relacional','AnaliseSintatica.py',254),
  ('operador_relacional -> DIF','operador_relacional',1,'p_operador_relacional','AnaliseSintatica.py',255),
  ('operador_relacional -> MENOREQ','operador_relacional',1,'p_operador_relacional','AnaliseSintatica.py',256),
  ('operador_relacional -> MAIOREQ','operador_relacional',1,'p_operador_relacional','AnaliseSintatica.py',257),
  ('operador_soma -> PLUS','operador_soma',1,'p_operador_soma','AnaliseSintatica.py',263),
  ('operador_soma -> MINUS','operador_soma',1,'p_operador_soma','AnaliseSintatica.py',264),
  ('operador_multiplicacao -> VEZES','operador_multiplicacao',1,'p_operador_multiplicacao','AnaliseSintatica.py',270),
  ('operador_multiplicacao -> DIVIDE','operador_multiplicacao',1,'p_operador_multiplicacao','AnaliseSintatica.py',271),
  ('fator -> RPAREN expressao LPAREN','fator',3,'p_fator','AnaliseSintatica.py',277),
  ('fator -> var','fator',1,'p_fator','AnaliseSintatica.py',278),
  ('fator -> chamada_funcao','fator',1,'p_fator','AnaliseSintatica.py',279),
  ('fator -> numero','fator',1,'p_fator','AnaliseSintatica.py',280),
  ('numero -> NUM_INTEIRO','numero',1,'p_numero','AnaliseSintatica.py',289),
  ('numero -> NUM_FLUTUANTE','numero',1,'p_numero','AnaliseSintatica.py',290),
  ('numero -> NUM_CIENTIFICA','numero',1,'p_numero','AnaliseSintatica.py',291),
  ('chamada_funcao -> ID LPAREN lista_argumentos RPAREN','chamada_funcao',4,'p_chamada_funcao','AnaliseSintatica.py',297),
  ('lista_argumentos -> lista_argumentos VIRGULA expressao','lista_argumentos',3,'p_lista_argumentos','AnaliseSintatica.py',303),
  ('lista_argumentos -> expressao','lista_argumentos',1,'p_lista_argumentos','AnaliseSintatica.py',304),
  ('lista_argumentos -> vazio','lista_argumentos',1,'p_lista_argumentos','AnaliseSintatica.py',305),
  ('vazio -> <empty>','vazio',0,'p_vazio','AnaliseSintatica.py',314),
]
