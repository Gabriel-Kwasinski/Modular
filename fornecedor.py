# IMPORTS
from datetime import datetime
import produto
import validacao
import os


# FUNÇÕES:
# carregar_fornecedores()
#       Carrega fornecedores do arquivo para memória
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# salvar_fornecedores()
#       Salva lista de fornecedores da memória para arquivo
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# cadastrar_fornecedor(nome, cnpj, telefone, email, endereco)
#       Cadastra um novo fornecedor
#       Parametros: nome (str), cnpj (str), telefone (str), email (str), endereco (str)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# listar_fornecedores()
#       Exibe todos os fornecedores na tela
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# excluir_fornecedor(cnpj)
#       Remove fornecedor pelo CNPJ
#       Parametros: cnpj (int)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro, 9=fornecedor não encontrado)
#
# associar_produto_fornecedor(indice_produto, indice_fornecedor)
#       Associa um produto a um fornecedor
#       Parametros: indice_produto (int), indice_fornecedor (int)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro, 3=produto_nao_encontrado, 9= fornecedor_não_encontrado)
#
# listar_produtos_por_fornecedor(cnpj)
#       Lista todos os produtos oferecidos por um fornecedor
#       Parametros: cnpj (str)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# buscar_fornecedores_do_produto(indice_produto)
#       Busca quais fornecedores oferecem um produto específico
#       Parametros: indice_produto (str)
#       Retorno: int - STATUS_CODE (0=sucesso, 3=produto_nao_encontrado)
#
# contatar_fornecedor(indice_fornecedor, motivo, produtos_necessarios)
#       Gera contato/pedido para fornecedor com produtos em falta
#       Parametros: indice_fornecedor (int), motivo (str), produtos_necessarios (list)
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)
#
# gerar_relatorio_fornecedores()
#       Gera relatório completo de fornecedores e seus produtos
#       Parametros: None
#       Retorno: int - STATUS_CODE (0=sucesso, 1=erro)


#Parametros globais
arq_fornecedores_path = "fornecedores.txt"

# lst_fornecedores = [
#     [0] = {
#         "nome"     : <str>,
#         "cnpj"     : <str>,
#         "telefone" : <str>,
#         "email"    : <str>,
#         "endereco" : <str>
#     }
#     [1] = ...
# ]
lst_fornecedores = []

# produtos_por_fornecedor = [
#     [0] = {
#         "fornecedor" : <str>,
#         "produtos"   : [
#             [0] = <str>
#             [1] = ...
#         ]
#     }, 
#     [1] = ...
# ]
produtos_por_fornecedor = []

# lst_produtos = [
#     [0] = {
#         "codigo"      : <str>,
#         "nome"        : <str>,
#         "categoria"   : <str>,
#         "preco_venda" : <float> 
#     },
#     [1] = ...
# ]
empty, lst_produtos = produto.carregar_produtos()

#Funcoes
def carregar_fornecedores():
    global arq_fornecedores_path, lst_fornecedores

    try:
        with open(arq_fornecedores_path, 'r') as arq:
            lst_fornecedores = []
            
            for lin in arq:
                lin_args = lin.split(',')
                dict_fornecedores = {
                    "nome"     : lin_args[0],
                    "cnpj"     : lin_args[1],
                    "telefone" : lin_args[2],
                    "email"    : lin_args[3],
                    "endereco" : lin_args[4]
                }

                if dict_fornecedores['endereco'][-1] == '\n':
                    dict_fornecedores['endereco'] = dict_fornecedores['endereco'][:-1] #removes \n
                
                lst_fornecedores.append(dict_fornecedores)
    except:
        return 1

    return 0, lst_fornecedores.copy()

def salvar_fornecedores():
    global arq_fornecedores_path, lst_fornecedores
    
    if not os.path.isfile(arq_fornecedores_path):
        return 1

    try:
        with open(arq_fornecedores_path, 'w') as arq:
            for fornecedor in lst_fornecedores:
                nome  = fornecedor["nome"]
                cnpj  = fornecedor["cnpj"]
                tel   = fornecedor["telefone"]
                email = fornecedor["email"]
                end   = fornecedor["endereco"]

                arq.write(f"{nome},{cnpj},{tel},{email},{end}\n")
    except:
        return 1
    
    return 0

def cadastrar_fornecedor(nome, cnpj, telefone, email, endereco):
    global lst_fornecedores

    erro = None
    erro = validacao.validaCNPJ(cnpj)
    if erro == 1:
        return 1
    erro = validacao.validaEmail(email)
    if erro == 1:
        return 1

    dict_fornecedor = {
        "nome"     : nome,
        "cnpj"     : cnpj,
        "telefone" : telefone,
        "email"    : email,
        "endereco" : endereco
    }

    lst_fornecedores.append(dict_fornecedor)
    return 0

def listar_fornecedores():
    global lst_fornecedores

    if len(lst_fornecedores) == 0:
        print("Nenhum fornecedor cadastrado")
        return 1

    for fornecedor in lst_fornecedores:
        if len(fornecedor) != 5:
            return 1
        
        nome  = fornecedor["nome"]
        cnpj  = fornecedor["cnpj"]
        tel   = fornecedor["telefone"]
        email = fornecedor["email"]
        end   = fornecedor["endereco"]

        print(f"{nome}, {cnpj}, {tel}, {email}, {end}")
        return 0

def excluir_fornecedor(cnpj):
    global lst_fornecedores

    erro = validacao.validaCNPJ(cnpj)
    if erro == 1:
        return 1

    for fornecedor in lst_fornecedores:
        if fornecedor['cnpj'] == cnpj:
            lst_fornecedores.remove(fornecedor)
            return 0
    
    return 9

def associar_produto_fornecedor(indice_produto, indice_fornecedor):
    global lst_fornecedores, produtos_por_fornecedor, lst_produtos
    
    erro = validacao.validaCNPJ(indice_fornecedor)
    if erro == 1:
        return 1
    
    for prod in lst_produtos:
        if prod["codigo"] == indice_produto:
            break    #produto encontrado
    else:
        return 3     #produto nao encontrado
    
    for forn in lst_fornecedores:
        if forn['cnpj'] == indice_fornecedor:
            break #fornecedor encontrado
    else:
        return 9 #fornecedor nao encontrado
    
    for prod_forn in produtos_por_fornecedor:
        if prod_forn["fornecedor"] == indice_fornecedor: 
            prod_forn["produtos"].append(indice_produto)
            break
    else:
        nova_chave = {
            "fornecedor" : indice_fornecedor,
            "produtos"   : [
                indice_produto
            ]
        }
        produtos_por_fornecedor.append(nova_chave)
    
    return 0

def listar_produtos_por_fornecedor(cnpj):
    global produtos_por_fornecedor

    erro = validacao.validaCNPJ(cnpj)
    if erro == 1:
        return 1

    for dict in produtos_por_fornecedor:
        if dict["fornecedor"] == cnpj:
            print(f"Fornecedor: {cnpj} - ", obtem_nome_fornecedor(cnpj))
            if len(dict["produtos"]) == 0:
                print("Nenhum produto associado")
                return 0
            for i in dict["produtos"]:
                print(obtem_nome_produto(i))
    
    return 0

def buscar_fornecedores_do_produto(indice_produto):
    global produtos_por_fornecedor

    if not isinstance(indice_produto, str):
        return 1
    
    forn = []
    for dict in produtos_por_fornecedor:
        for prod in dict["produtos"]:
            if prod == indice_produto:
                forn.append(dict["fornecedor"])

    if len(forn) == 0:
        return 3, None
    
    return 0, forn

def contatar_fornecedor(indice_fornecedor, motivo, produtos_necessarios):
    if len(produtos_necessarios) == 0:
        return 1
    
    try:
        with open("pedido_reposicao", 'w') as arq:
            arq.write("PEDIDO DE REPOSICAO DE ESTOQUE\n")
            arq.write("Data de Solicitacao: " + datetime.today().strftime('%Y-%m-%d') + "\n")
            arq.write("Fornecedor: " + indice_fornecedor + " : " + str(obtem_nome_fornecedor(indice_fornecedor)) + "\n")
            arq.write("Motivo do pedido:\n")
            arq.write(f"{motivo}\n")
            arq.write("------------------------------\n")
            arq.write("Produtos Solicitados: \n")
            for prod in produtos_necessarios:
                arq.write("    - " + prod + " : " + str(obtem_nome_produto(prod)) + "\n")
    except:
        return 1
    
    return 0

def gerar_relatorio_fornecedores():
    global produtos_por_fornecedor

    try:
        if len(produtos_por_fornecedor) == 0:
            return 1
        with open("relatorio_fornecedores", 'w') as arq:
            arq.write("RELATORIO DE FORNECEDORES-PRODUTOS: \n")
            arq.write("Fornecedor     |     Produtos \n")
            for dict in produtos_por_fornecedor:
                arq.write(dict["fornecedor"] + " - " + obtem_nome_fornecedor(dict["fornecedor"]))
                arq.write("   ")
                for prod in dict["produtos"]:
                    arq.write(prod + " - " + obtem_nome_produto(prod) + "\n")
                
                arq.write("\n")
    except:    
        return 1
    
    return 0

# comeco das funcoes auxiliares
def obtem_nome_produto(codigo):
    global lst_produtos

    for dict in lst_produtos:
        if dict["codigo"] == codigo:
            return dict["nome"]
    return None

def obtem_nome_fornecedor(cnpj):
    global lst_fornecedores

    for dict in lst_fornecedores:
        if dict["cnpj"] == cnpj:
            return dict["nome"]
    return None
# fim das funcoes auxiliares

#TESTES DE FUNÇÕES
def testa_carregar_fornecedores():
    global arq_fornecedores_path, lst_fornecedores

    # Caso 65: Arquivo de fornecedores existe e contém dados válidos → retorno
    # SUCESSO (0).
    assert carregar_fornecedores() == 0, "Erro na funcao <carregar_fornecedores.py>. Caso 65."

    # Caso 66: Arquivo inexistente → retorno ERRO (1) e lista vazia.
    salva_arq_fornecedores_path = arq_fornecedores_path
    if os.path.isfile("arquivo_nao_existe.txt"):
        os.remove("arquivo_nao_existe.txt")
    arq_fornecedores_path = "arquivo_nao_existe.txt"
    
    assert carregar_fornecedores() == 1, "Erro na funcao <carregar_fornecedores.py>. Caso 66."
    arq_fornecedores_path = salva_arq_fornecedores_path

    # Caso 67: Arquivo existe mas está vazio → retorno SUCESSO (0) e lista vazia.
    with open("arquivo_vazio.txt", 'w') as vazio:
        vazio.write('')
    
    arq_fornecedores_path = "arquivo_vazio.txt"
    assert carregar_fornecedores() == 0, "Erro na funcao <carregar_fornecedores.py>. Caso 67"
    assert len(lst_fornecedores) == 0, "Erro na funcao <carregar_fornecedores.py>. Caso 67"
    
    # Restaura arq_fornecedores_path
    arq_fornecedores_path = salva_arq_fornecedores_path

def testa_salvar_fornecedores():
    global arq_fornecedores_path, lst_fornecedores

    # Caso 68: Lista não vazia e arquivo gravável → retorno SUCESSO (0).
    carregar_fornecedores()
    salva_lst_fornecedores = lst_fornecedores.copy()
    lst_fornecedores = [
        {
            "nome"     : "Afrib Alimentos",
            "cnpj"     : "11.734.338/0001-93",
            "telefone" : "(24) 97801-4157",
            "email"    : "patrick.medina@example.com",
            "endereco" : "3917 Cherry St"
        }
    ]

    assert salvar_fornecedores() == 0, "Erro na funcao <testa_salvar_fornecedores.py>. Caso 68."

    lst_fornecedores = salva_lst_fornecedores.copy()
    # Caso 69: Erro ao gravar arquivo (ex: permissão negada) → retorno ERRO (1).
    salva_arq_fornecedores_path = arq_fornecedores_path
    if os.path.isfile("arquivo_nao_existe.txt"):
        os.remove("arquivo_nao_existe.txt")
    arq_fornecedores_path = "arquivo_nao_existe.txt"

    assert salvar_fornecedores() == 1, "Erro na funcao <testa_salvar_fornecedores.py>. Caso 69."

    # Caso 70: Lista vazia → retorno SUCESSO (0) e arquivo limpo ou vazio.
    salva_lst_fornecedores = lst_fornecedores.copy()
    arq_fornecedores_path = "copia_de_fornecedores.txt"
    lst_fornecedores = []
    assert salvar_fornecedores() == 0, "Erro na funcao <testa_salvar_fornecedores.py>. Caso 70."
    assert os.path.getsize(arq_fornecedores_path) == 0, "Erro na funcao <testa_salvar_fornecedores.py>. Caso 70."

    #Restaura arq_fornecedores_path
    arq_fornecedores_path = salva_arq_fornecedores_path
    #Restaura lst_fornecedores
    lst_fornecedores = salva_lst_fornecedores.copy()

def testa_cadastrar_fornecedor():
    # Caso 71: Dados válidos → retorno SUCESSO (0).
    assert cadastrar_fornecedor(
        "Afrib Alimentos",
        "11.734.338/0001-93",
        "(24) 97801-4157",
        "patrick.medina@example.com",
        "3917 Cherry St"
    ) == 0, "Erro na funcao <cadastrar_fornecedor.py>. Dados de cadastro inválidos."

    # Caso 72: CNPJ inválido → retorno ERRO (1).
    assert cadastrar_fornecedor(
        "Afrib Alimentos",
        "0000000000",
        "(24) 97801-4157",
        "patrick.medina@example.com",
        "3917 Cherry St"
    ) == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 72."

    # Caso 73: Campos obrigatórios ausentes (nome, CNPJ) → retorno ERRO (1).
    assert cadastrar_fornecedor(
        "",
        "",
        "(24) 97801-4157",
        "patrick.medina@example.com",
        "3917 Cherry St"
    ) == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 73."

def testa_listar_fornecedores():
    global lst_fornecedores

    # Caso 74: Há fornecedores cadastrados → exibir corretamente e SUCESSO
    # (0).
    carregar_fornecedores()
    assert len(lst_fornecedores) != 0 and listar_fornecedores() == 0, "Erro na funcao <cadastrar_fornecedor.py>. Caso 74."
    # Caso 75: Lista vazia → mensagem “Nenhum fornecedor cadastrado” e ERRO
    # (1).
    salva_lst_fornecedores = lst_fornecedores.copy()
    lst_fornecedores = []
    assert listar_fornecedores() == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 75."

    #restaura lst_fornecedores
    lst_fornecedores = salva_lst_fornecedores.copy()

def testa_associar_produto_fornecedor():
    global lst_fornecedores, lst_produtos

    # Caso 76: Índices válidos → associação feita e SUCESSO (0).
    assert associar_produto_fornecedor(
            lst_produtos[0]["codigo"],
            lst_fornecedores[0]["cnpj"]
        ) == 0, "Erro na funcao <cadastrar_fornecedor.py>. Caso 76."

    # Caso 77: Índice de produto inexistente →
    # PRODUTO_NAO_ENCONTRADO (3).
    assert associar_produto_fornecedor(
            "00000000",
            lst_fornecedores[0]["cnpj"]
        ) == 3, "Erro na funcao <cadastrar_fornecedor.py>. Caso 77."

    # Caso 78: Índices inválidos → ERRO (1)
    assert associar_produto_fornecedor(
            lst_produtos[0]["codigo"],
            "00000000000000"
        ) == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 78."

def testa_listar_produtos_por_fornecedor():
    global lst_fornecedores, produtos_por_fornecedor

    # Caso 79: Fornecedor válido com produtos → lista exibida e SUCESSO (0).
    assert listar_produtos_por_fornecedor(
        lst_fornecedores[0]["cnpj"]
    ) == 0, "Erro na funcao <cadastrar_fornecedor.py>. Caso 79."

    # Caso 80: Fornecedor válido sem produtos → mensagem “Nenhum produto
    # associado” e SUCESSO (0).
    salva_produtos_por_fornecedor_0_produtos = produtos_por_fornecedor[0]["produtos"].copy()

    produtos_por_fornecedor[0]["produtos"] = []
    assert listar_produtos_por_fornecedor(
        lst_fornecedores[0]["cnpj"]
    ) == 0, "Erro na funcao <cadastrar_fornecedor.py>. Caso 80."

    produtos_por_fornecedor[0]["produtos"] = salva_produtos_por_fornecedor_0_produtos.copy()
    
    # Caso 81: Índice de fornecedor inválido → ERRO (1).
    assert listar_produtos_por_fornecedor(
        "00000000000000"
    ) == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 81."

def testa_buscar_fornecedores_do_produto():
    global lst_produtos

    # Caso 82: Produto válido → retorna fornecedores e SUCESSO (0).
    assert buscar_fornecedores_do_produto(lst_produtos[0]["codigo"]), "Erro na funcao <cadastrar_fornecedor.py>. Caso 82."

    # Caso 83: Produto inexistente → PRODUTO_NAO_ENCONTRADO (3).
    assert buscar_fornecedores_do_produto("00000000000000"), "Erro na funcao <cadastrar_fornecedor.py>. Caso 83."

def testa_contatar_fornecedor():
    global lst_fornecedores, lst_produtos

    # Caso 84: Dados válidos → contato gerado e SUCESSO (0).
    prods = [
        lst_produtos[0]["codigo"],
        lst_produtos[1]["codigo"],
        lst_produtos[2]["codigo"],
    ]

    assert contatar_fornecedor(
            lst_fornecedores[0]["cnpj"],
            "Reposicao de estoque",
            prods
    ) == 0, "Erro na funcao <cadastrar_fornecedor.py>. Caso 84."

    # Caso 85: Falha ao enviar contato (arquivo/log não acessível) → ERRO (1).

    # Caso 86: Lista de produtos vazia → ERRO (1).
    assert contatar_fornecedor(
            lst_fornecedores[0]["cnpj"],
            "Reposicao de estoque",
            []
    ) == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 86."

def testa_gerar_relatorio_fornecedores():
    global produtos_por_fornecedor

    # Caso 87: Há fornecedores e produtos → relatório gerado e SUCESSO (0).
    assert gerar_relatorio_fornecedores() == 0, "Erro na funcao <cadastrar_fornecedor.py>. Caso 87."
    
    # Caso 88: Nenhum fornecedor → ERRO (1).
    salva_produtos_por_fornecedor = produtos_por_fornecedor.copy()

    produtos_por_fornecedor = {}
    assert gerar_relatorio_fornecedores() == 1, "Erro na funcao <cadastrar_fornecedor.py>. Caso 88."

    produtos_por_fornecedor = salva_produtos_por_fornecedor.copy()


