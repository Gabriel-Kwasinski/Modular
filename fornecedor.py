# IMPORTS
from datetime import datetime
import produto


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
lst_fornecedores = []   # lst_fornecedores = [
                        #     [0] = {
                        #         "nome"     : <str>,
                        #         "cnpj"     : <str>,
                        #         "telefone" : <str>,
                        #         "email"    : <str>,
                        #         "endereco" : <str>
                        #     }
                        #     [1] = ...
                        # ]


produtos_por_fornecedor = []   # produtos_por_fornecedor = [
                               #     [0] = {
                               #         "fornecedor" : <str>,
                               #         "produtos"   : [
                               #             [0] = <str>
                               #             [1] = ...
                               #         ]
                               #     }, 
                               #     [1] = ...
                               # ]


#Funcoes
def carregar_fornecedores():
    with open(arq_fornecedores_path, 'r') as arq:
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

    return 0

def salvar_fornecedores():
    with open(arq_fornecedores_path, 'w') as arq:
        for fornecedor in lst_fornecedores:
            nome  = fornecedor["nome"]
            cnpj  = fornecedor["cnpj"]
            tel   = fornecedor["telefone"]
            email = fornecedor["email"]
            end   = fornecedor["endereco"]

            arq.write(f"{nome},{cnpj},{tel},{email},{end}\n")

    return 0

def cadastrar_fornecedor(nome, cnpj, telefone, email, endereco):
    dict_fornecedor = {
        "nome"     : nome,
        "cnpj"     : cnpj,
        "telefone" : telefone,
        "email"    : email,
        "endereco" : endereco
    }

    lst_fornecedores.append(dict_fornecedor)

def listar_fornecedores():
    for fornecedor in lst_fornecedores:
        nome  = fornecedor["nome"]
        cnpj  = fornecedor["cnpj"]
        tel   = fornecedor["telefone"]
        email = fornecedor["email"]
        end   = fornecedor["endereco"]

        print(f"{nome}, {cnpj}, {tel}, {email}, {end}")

def excluir_fornecedor(cnpj):
    for fornecedor in lst_fornecedores:
        if fornecedor['cnpj'] == cnpj:
            lst_fornecedores.remove(fornecedor)
            return 0
    
    return 9

def associar_produto_fornecedor(indice_produto, indice_fornecedor):
    for prod in produto.lst_produtos:
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
    for dict in produtos_por_fornecedor:
        if dict["fornecedor"] == cnpj:
            print(f"Fornecedor: {cnpj} - ", obtem_nome_fornecedor(cnpj))
            for i in dict["produtos"]:
                print(obtem_nome_produto(i))
    
    return 0

def buscar_fornecedores_do_produto(indice_produto):
    forn = []
    for dict in produtos_por_fornecedor:
        for prod in dict["produtos"]:
            if prod == indice_produto:
                forn.append(dict["fornecedor"])

    if len(forn) == 0:
        return 3, None
    
    return 0, forn

def contatar_fornecedor(indice_fornecedor, motivo, produtos_necessarios):
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
        
        return 0

def gerar_relatorio_fornecedores():

    with open("relatorio_fornecedores", 'w') as arq:
        arq.write("RELATORIO DE FORNECEDORES-PRODUTOS: \n")
        arq.write("Fornecedor     |     Produtos \n")
        for dict in produtos_por_fornecedor:
            arq.write(dict["fornecedor"] + " - " + obtem_nome_fornecedor(dict["fornecedor"]))
            arq.write("   ")
            for prod in dict["produtos"]:
                arq.write(prod + " - " + obtem_nome_produto(prod) + "\n")
            
            arq.write("\n")
        
        return 0

def obtem_nome_produto(codigo):
    for dict in produto.lst_produtos:
        if dict["codigo"] == codigo:
            return dict["nome"]
    return None

def obtem_nome_fornecedor(cnpj):
    for dict in lst_fornecedores:
        if dict["cnpj"] == cnpj:
            return dict["nome"]
    return None
