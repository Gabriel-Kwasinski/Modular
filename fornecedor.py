# IMPORTS
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
#       int - STATUS_CODE (0=sucesso, 1=erro, 3=produto_nao_encontrado, 9= fornecedor_não_encontrado)


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




