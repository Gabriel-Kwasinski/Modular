#IMPORTANT:
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
                    #         "codigo"      : "10001-2",
                    #         "nome"        : "arroz",
                    #         "categoria"   : "nao-pereciveis",
                    #         "preco_venda" : 8.5 
                    #     },
                    #     [1] = ...
                    # ]


#Funcoes
def carregar_produtos():
    arq_caminho = os.path.dirname(arq_produtos)
    if not os.path.exists(arq_caminho) and arq_caminho:
        printf("O caminho para o arquivo nao existe.")
        return 1

    with open(arq_produtos_path, 'r') as arq_prod:
        for linha in arq_prod:
            dados = linha.split(',')
            dict_produtos = {
                "codigo" = dados[0]
                "nome" = dados[1]
                "categoria" = dados[2]
                "preco_venda" = float(dados[3].strip())
            }
            lst_produtos.append(dict_produtos)
    return 0

def salvar_produtos():
    return 0

def cadastrar_produto(codigo, nome, categoria, preco_venda):
    return 0

def listar_produtos():
    return 0

def buscar_produto_por_codigo(codigo):
    return 0

def buscar_produto_por_indice(indice):
    return 0

def atualizar_produto(indice, nome=None, categoria=None, preco_venda=None):
    return 0

def deletar_produto(indice):

    return 0
