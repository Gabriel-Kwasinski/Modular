#IMPORTS:
import os

# FUNCOES:
# def carregar_produtos():
#       Carrega produtos do arquivo para memória.
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# def salvar_produtos():
#       Salva lista de produtos da memória para arquivo
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# def cadastrar_produto(codigo, nome, categoria, preco_venda):
#       Cadastra um novo produto.
#       Parametros: codigo (str), nome (str), categoria (str), preco_venda (float)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro, 6=codigo_ja_cadastrado)
#
# def listar_produtos():
#       Exibe todos os produtos na tela.
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# def buscar_produto_por_codigo(codigo):
#     	Busca produto pelo código e retorna índice na lista
#     	Parametros: codigo (str)
#     	Retorno: int - índice do produto na lista ou -1 se não encontrado
#
# def buscar_produto_por_indice(indice):
#       Verifica se índice é válido na lista de produtos
#       Parametros: indice (int)
#       Retorno: int - STATUS_CODE (0=sucesso, 3=produto_nao_encontrado)
#
# def atualizar_produto(indice, nome=None, categoria=None, preco_venda=None):
#       Atualiza dados do produto pelo índice
#       Parametros: indice (int), campos opcionais
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro, 3=produto_nao_encontrado)
#
# def deletar_produto(indice):
#       Remove produto pelo índice
#       Parametros: indice (int)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro, 3=produto_nao_encontrado)


#Parametros globais
arq_produtos_path = "produtos.txt"
lst_produtos = []   # lst_produtos = [
                    #     [0] = {
                    #         "codigo"      : <str>,
                    #         "nome"        : <str>,
                    #         "categoria"   : <str>,
                    #         "preco_venda" : <float> 
                    #     },
                    #     [1] = ...
                    # ]


#Funcoes
def carregar_produtos():
    arq_caminho = os.path.dirname(arq_produtos_path)
    if arq_caminho and not os.path.exists(arq_caminho):
        print("O caminho para o arquivo nao existe.")
        return 1

    if not os.path.exists(arq_produtos_path):
        print("Arquivo inexistente.")
        return 1

    with open(arq_produtos_path, 'r') as arq_prod:
        for linha in arq_prod:
            dados = linha.split(',')
            dict_produtos = {
                "codigo"       : dados[0],
                "nome"         : dados[1],
                "categoria"    : dados[2],
                "preco_venda"  : float(dados[3].strip())
            }
            lst_produtos.append(dict_produtos)
    return 0, lst_produtos.copy()

def salvar_produtos():
    arq_caminho = os.path.dirname(arq_produtos_path)
    if arq_caminho and not os.path.exists(arq_caminho):
        print("O caminho para o arquivo nao existe.")
        return 1

    try:
        with open(arq_produtos_path, 'w') as arq_prod:
            for el in lst_produtos:
                codigo = el['codigo']
                nome = el['nome']
                categoria = el['categoria']
                preco_venda = el['preco_venda']
          
                arq_prod.write(f"{codigo}, {nome}, {categoria}, {preco_venda}\n") 
    except Exception as e:
        print("Erro ao salvar arquivo:", e)
        return 1  
    return 0

#Inicio da função auxilicar
def eh_float(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False
#Fim da função auxiliar

def cadastrar_produto(codigo, nome, categoria, preco_venda):
    for el in lst_produtos:
        if el['codigo'] == codigo:
            return 6
          
    if not eh_float(preco_venda):
        print("Erro ao converter o preco para float.\n")
        return 1

    if not codigo or not nome:
        print("Codigo e nome sao obrigatorios.\n")
        return 1

    preco_venda = float(preco_venda)
    if preco_venda <= 0:
        print("Preco deve ser positivo.\n")
        return 1

    dict_produto = {
        "codigo"      : codigo,
        "nome"        : nome,
        "categoria"   : categoria,
        "preco_venda" : preco_venda
    }

    lst_produtos.append(dict_produto)  
    return 0

def listar_produtos():
    if not lst_produtos:
        print("Nenhum produto foi cadastrado.\n")
        return 1

    for el in lst_produtos:
        print(f"{el['codigo']}, {el['nome']}, {el['categoria']}, {el['preco_venda']}\n")
    return 0

def buscar_produto_por_codigo(codigo):
    if not codigo:
        return -1

    for i, el in enumerate(lst_produtos):
        if el['codigo'] == codigo:
            return i
    return -1

def buscar_produto_por_indice(indice):
    if 0 <= indice < len(lst_produtos):
        return 0
    else:
        print("Indice nao foi encontrado.\n")
        return 3

def atualizar_produto(indice, nome=None, categoria=None, preco_venda=None):
    if buscar_produto_por_indice(indice) != 0:
        return 3

    if nome is None and categoria is None and preco_venda is None:
        return 1

    if preco_venda is not None:
        if preco_venda <= 0:
            return 1
      
    prod = lst_produtos[indice]
    if nome is not None:
        prod['nome'] = nome
      
    if categoria is not None:
        prod['categoria'] = categoria

    if preco_venda is not None:
        prod['preco_venda'] = preco_venda

    return 0

def deletar_produto(indice):
    if 0 <= indice < len(lst_produtos):
        lst_produtos.pop(indice)
        return 0
    else:
        print("Produto nao encontrado.\n")
        return 3



