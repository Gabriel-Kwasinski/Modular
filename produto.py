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
                    #         "codigo"      : "10001-2",
                    #         "nome"        : "arroz",
                    #         "categoria"   : "nao-pereciveis",
                    #         "preco_venda" : 8.5 
                    #     },
                    #     [1] = ...
                    # ]


#Funcoes
def carregar_produtos():
    global lst_produtos
    lst_produtos.clear()
    
    if not arq_produtos_path or arq_produtos_path == "produtos.txt":
        if not os.path.exists("produtos.txt"):
            return 1, []
    
    arq_caminho = os.path.dirname(arq_produtos_path)
    if arq_caminho and not os.path.exists(arq_caminho):
        return 1, []

    if not os.path.exists(arq_produtos_path):
        return 1, []

    try:
        with open(arq_produtos_path, 'r') as arq_prod:
            for linha in arq_prod:
                linha = linha.strip()
                if linha:
                    dados = linha.split(',')
                    if len(dados) == 4:
                        dict_produtos = {
                            "codigo": dados[0].strip(),
                            "nome": dados[1].strip(),
                            "categoria": dados[2].strip(),
                            "preco_venda": float(dados[3].strip())
                        }
                        lst_produtos.append(dict_produtos)
        return 0, lst_produtos.copy()
    except Exception as e:
        return 1, []

def salvar_produtos():
    arq_caminho = os.path.dirname(arq_produtos_path)
    if arq_caminho and not os.path.exists(arq_caminho):
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
        return 1

    if not codigo or not nome:
        return 1

    preco_venda = float(preco_venda)
    if preco_venda <= 0:
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
        return 3

# Teste carregar_produtos()
def testa_carregar_produtos():
    global arq_produtos_path, lst_produtos

    #Caso 22: Arquivo de produtos existe e contém dados válidos
    resultado, lista = carregar_produtos()
    assert resultado == 0, "Erro na funcao <carregar_produtos>. Caso 22."
    assert len(lista) > 0, "Erro na funcao <carregar_produtos>. Caso 22: lista vazia."

    #Caso 23: Arquivo inexistente
    salva_arq_produtos_path = arq_produtos_path
    arq_produtos_path = "arquivo_nao_existe.txt"
    
    assert carregar_produtos()[0] == 1, "Erro na funcao <carregar_produtos>. Caso 23."
    arq_produtos_path = salva_arq_produtos_path

    #Caso 24: Arquivo existe mas está vazio
    with open("arquivo_vazio.txt", 'w') as vazio:
        vazio.write('')
    
    arq_produtos_path = "arquivo_vazio.txt"
    resultado, lista = carregar_produtos()
    assert resultado == 0, "Erro na funcao <carregar_produtos>. Caso 24"
    assert len(lista) == 0, "Erro na funcao <carregar_produtos>. Caso 24"
    
    arq_produtos_path = salva_arq_produtos_path
    
# Teste salvar_produtos()
def testa_salvar_produtos():
    global arq_produtos_path, lst_produtos

    #Caso 25: Lista não vazia e arquivo gravável
    carregar_produtos()
    salva_lst_produtos = lst_produtos.copy()
    lst_produtos = [
        {
            "codigo": "99999-9",
            "nome": "Produto Teste", 
            "categoria": "teste",
            "preco_venda": 10.50
        }
    ]

    assert salvar_produtos() == 0, "Erro na funcao <salvar_produtos>. Caso 25."

    lst_produtos = salva_lst_produtos.copy()
    salvar_produtos()

    #Caso 26: Erro ao gravar arquivo (caminho inválido)
    salva_arq_produtos_path = arq_produtos_path
    arq_produtos_path = "/caminho/invalido/produtos.txt"

    assert salvar_produtos() == 1, "Erro na funcao <salvar_produtos>. Caso 26."

    #Caso 27: Lista vazia e arquivo limpo ou vazio
    salva_lst_produtos = lst_produtos.copy()
    arq_produtos_path = "copia_de_produtos.txt"
    lst_produtos = []
    assert salvar_produtos() == 0, "Erro na funcao <salvar_produtos>. Caso 27."
    assert os.path.getsize(arq_produtos_path) == 0, "Erro na funcao <salvar_produtos>. Caso 27."

    if os.path.exists("copia_de_produtos.txt"):
        os.remove("copia_de_produtos.txt")


    arq_produtos_path = salva_arq_produtos_path

    lst_produtos = salva_lst_produtos.copy()

# Teste cadastrar_produto()
def testa_cadastrar_produto():
    global lst_produtos

    #Caso 28: Dados válidos
    salva_lst_produtos = lst_produtos.copy()
    lst_produtos = []
    
    assert cadastrar_produto("20001-5", "Novo Produto", "bebidas", 25.99) == 0, "Erro na funcao <cadastrar_produto>. Caso 28."
    assert len(lst_produtos) == 1, "Erro na funcao <cadastrar_produto>. Caso 28: produto não adicionado."

    #Caso 29: Código já cadastrado
    assert cadastrar_produto("20001-5", "Outro Produto", "limpeza", 15.50) == 6, "Erro na funcao <cadastrar_produto>. Caso 29."

    #Caso 30: Preço inválido (negativo)
    assert cadastrar_produto("20003-7", "Produto Preço Negativo", "bebidas", -5.0) == 1, "Erro na funcao <cadastrar_produto>. Caso 30."

    #Caso 30: Preço inválido (string)
    assert cadastrar_produto("20004-8", "Produto Preço String", "bebidas", "dez") == 1, "Erro na funcao <cadastrar_produto>. Caso 30."

    #Caso 30: Preço zero
    assert cadastrar_produto("20005-9", "Produto Preço Zero", "bebidas", 0) == 1, "Erro na funcao <cadastrar_produto>. Caso 30."

    #Caso 31: Campos obrigatórios ausentes (código, nome)
    assert cadastrar_produto("", "Produto Sem Código", "bebidas", 10.0) == 1, "Erro na funcao <cadastrar_produto>. Caso 31."
    assert cadastrar_produto("20002-6", "", "bebidas", 10.0) == 1, "Erro na funcao <cadastrar_produto>. Caso 31."

    lst_produtos = salva_lst_produtos.copy()

# Teste listar_produtos()
def testa_listar_produtos():
    global lst_produtos

    #Caso 32: Há produtos cadastrados
    carregar_produtos()
    if len(lst_produtos) > 0:
        assert listar_produtos() == 0, "Erro na funcao <listar_produtos>. Caso 32."
    
    #Caso 33: Lista vazia
    salva_lst_produtos = lst_produtos.copy()
    lst_produtos = []
    assert listar_produtos() == 1, "Erro na funcao <listar_produtos>. Caso 33."

    lst_produtos = salva_lst_produtos.copy()

# Teste buscar_produto_por_codigo()
def testa_buscar_produto_por_codigo():
    global lst_produtos

    #Caso 34: Código existente → retorna índice correto
    carregar_produtos()
    if len(lst_produtos) > 0:
        codigo_teste = lst_produtos[0]["codigo"]
        assert buscar_produto_por_codigo(codigo_teste) == 0, "Erro na funcao <buscar_produto_por_codigo>. Caso 34."

    #Caso 35: Código inexistente
    assert buscar_produto_por_codigo("00000-0") == -1, "Erro na funcao <buscar_produto_por_codigo>. Caso 35."

    #Caso 36: Código vazio
    assert buscar_produto_por_codigo("") == -1, "Erro na funcao <buscar_produto_por_codigo>. Caso 36."

# Teste burcar_produto_por_indice()
def testa_buscar_produto_por_indice():
    global lst_produtos

    #Caso 37: Índice válido → retorno SUCESSO (0)
    carregar_produtos()
    if len(lst_produtos) > 0:
        assert buscar_produto_por_indice(0) == 0, "Erro na funcao <buscar_produto_por_indice>. Caso 37."

    #Caso 38: Índice negativo → retorno PRODUTO_NAO_ENCONTRADO (3)
    assert buscar_produto_por_indice(-1) == 3, "Erro na funcao <buscar_produto_por_indice>. Caso 38."

    #Caso 39: Índice maior que lista → retorno PRODUTO_NAO_ENCONTRADO (3)
    assert buscar_produto_por_indice(len(lst_produtos) + 10) == 3, "Erro na funcao <buscar_produto_por_indice>. Caso 39."

# Teste atualizar_produto()
def testa_atualizar_produto():
    global lst_produtos

    #Caso 40: Atualização válida
    carregar_produtos()
    if len(lst_produtos) > 0:
        salva_lst_produtos = lst_produtos.copy()
        
        codigo_original = lst_produtos[0]["codigo"]
        
        assert atualizar_produto(0, nome="Novo Nome Produto") == 0, "Erro na funcao <atualizar_produto>. Caso 40."
        assert lst_produtos[0]["nome"] == "Novo Nome Produto", "Erro na funcao <atualizar_produto>. Caso 40."
        assert lst_produtos[0]["codigo"] == codigo_original, "Erro na funcao <atualizar_produto>. Caso 40: código alterado."

    #Caso 41: Atualização múltipla
        assert atualizar_produto(0, nome="Nome Atualizado", categoria="nova-categoria", preco_venda=99.99) == 0, "Erro na funcao <atualizar_produto>. Caso 41."
        assert lst_produtos[0]["nome"] == "Nome Atualizado", "Erro na funcao <atualizar_produto>. Caso 41."
        assert lst_produtos[0]["categoria"] == "nova-categoria", "Erro na funcao <atualizar_produto>. Caso 41."
        assert lst_produtos[0]["preco_venda"] == 99.99, "Erro na funcao <atualizar_produto>. Caso 41."

    #Caso 42: Nenhum campo para atualizar
        assert atualizar_produto(0) == 1, "Erro na funcao <atualizar_produto>. Caso 42."

    #Caso 43: Índice inválido
        assert atualizar_produto(-1, nome="Teste") == 3, "Erro na funcao <atualizar_produto>. Caso 43."

    #Caso 44: Preço inválido (negativo)
        assert atualizar_produto(0, preco_venda=-10.0) == 1, "Erro na funcao <atualizar_produto>. Caso 44."

    #Caso 44: Preço zero
        assert atualizar_produto(0, preco_venda=0) == 1, "Erro na funcao <atualizar_produto>. Caso 44."

        lst_produtos = salva_lst_produtos.copy()

#Teste deletar_produto()
def testa_deletar_produto():
    global lst_produtos

    #Caso 45: Índice válido
    carregar_produtos()
    if len(lst_produtos) > 0:
        salva_lst_produtos = lst_produtos.copy()
        tamanho_original = len(lst_produtos)
        codigo_removido = lst_produtos[0]["codigo"]
        
        assert deletar_produto(0) == 0, "Erro na funcao <deletar_produto>. Caso 45."
        assert len(lst_produtos) == tamanho_original - 1, "Erro na funcao <deletar_produto>. Caso 45."
        
        #Verifica se o produto correto foi removido
        assert buscar_produto_por_codigo(codigo_removido) == -1, "Erro na funcao <deletar_produto>. Caso 45: produto ainda encontrado."

    #Caso 46: Índice inválido → retorno PRODUTO_NAO_ENCONTRADO (3)
        assert deletar_produto(-1) == 3, "Erro na funcao <deletar_produto>. Caso 46."
        assert deletar_produto(len(lst_produtos) + 5) == 3, "Erro na funcao <deletar_produto>. Caso 46."

    #Caso 47: Lista vazia
        salva_lst_produtos_vazia = lst_produtos.copy()
        lst_produtos = []
        assert deletar_produto(0) == 3, "Erro na funcao <deletar_produto>. Caso 47."
        assert deletar_produto(-1) == 3, "Erro na funcao <deletar_produto>. Caso 47."
        lst_produtos = salva_lst_produtos_vazia.copy()

    #Caso 48: Remoção seguida de nova listagem para confirmar ausência do item
        if len(lst_produtos) > 1:
            codigo_para_remover = lst_produtos[1]["codigo"]
            nome_para_remover = lst_produtos[1]["nome"]
            
            assert deletar_produto(1) == 0, "Erro na funcao <deletar_produto>. Caso 48: falha na remoção."
            
            assert buscar_produto_por_codigo(codigo_para_remover) == -1, "Erro na funcao <deletar_produto>. Caso 48: produto ainda encontrado por código."
            
            tamanho_apos_remocao = len(lst_produtos)
            assert tamanho_apos_remocao == tamanho_original - 2, "Erro na funcao <deletar_produto>. Caso 48: tamanho inconsistente da lista."
            
            #Verifica se os produtos restantes mantêm a ordem correta
            for i in range(len(lst_produtos)):
                assert buscar_produto_por_indice(i) == 0, f"Erro na funcao <deletar_produto>. Caso 48: índice {i} inválido após remoção."
            
            print(f"Produto '{nome_para_remover}' (código: {codigo_para_remover}) removido com sucesso e lista mantém consistência")

        lst_produtos = salva_lst_produtos.copy()

def testa_funcoes_produto():
    testa_carregar_produtos()
    print("Testes de carregar produtos passaram\n")
    
    testa_salvar_produtos()
    print("Testes de salvar produtos passaram\n")
    
    testa_cadastrar_produto()
    print("Testes de cadastrar produto passaram\n")
    
    testa_listar_produtos()
    print("Testes de listar produtos passaram\n")
    
    testa_buscar_produto_por_codigo()
    print("Testes de buscar produto por código passaram\n")
    
    testa_buscar_produto_por_indice()
    print("Testes de buscar produto por índice passaram\n")
    
    testa_atualizar_produto()
    print("Testes de atualizar produto passaram\n")
    
    testa_deletar_produto()
    print("Testes de deletar produto passaram")




