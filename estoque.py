# IMPORTS
import produto
import fornecedor

# FUNÇÕES (conforme especificação):
# carregar_estoque()
# salvar_estoque()
# adicionar_produto_estoque(indice_produto, quantidade, quantidade_minima=0, quantidade_padrao_compra=0)
# entrada_estoque(indice_produto, quantidade)
# saida_estoque(indice_produto, quantidade)
# consultar_estoque()
# definir_quantidade_minima(indice_produto, quantidade_minima)
# verificar_produtos_abaixo_minimo()
# gerar_pedidos_reposicao()
# contatar_fornecedores_estoque_baixo()
# verificar_disponibilidade_fornecedor(indice_produto)
#
# Convenção de retorno:
# 0 = SUCESSO
# 1 = ERRO
# 3 = PRODUTO_NAO_ENCONTRADO
# 4 = ESTOQUE_INSUFICIENTE
# 8 = ESTOQUE_BAIXO

# LISTA GLOBAL DE ESTOQUE
# Cada item é um dicionário:
# {
#     "codigo"                 : str,
#     "quantidade"             : int,
#     "quantidade_minima"      : int,
#     "quantidade_padrao_compra": int
# }
lst_estoque = []

# CAMINHO DO ARQUIVO
arq_estoque_path = "estoque.txt"


def carregar_estoque():
    """Carrega dados de estoque do arquivo para a memória.

    Formato de cada linha do arquivo:
    codigo,quantidade,quantidade_minima,quantidade_padrao_compra
    """
    global lst_estoque
    lst_estoque = []

    try:
        arq = open(arq_estoque_path, "r")
    except:
        return 1  # erro ao abrir arquivo

    for lin in arq:
        lin = lin.strip()
        if lin == "":
            continue

        partes = lin.split(",")
        if len(partes) < 4:
            continue  # linha inválida, ignora

        codigo = partes[0]

        try:
            quantidade = int(partes[1])
            quantidade_minima = int(partes[2])
            quantidade_padrao = int(partes[3])
        except:
            continue

        dict_item = {
            "codigo": codigo,
            "quantidade": quantidade,
            "quantidade_minima": quantidade_minima,
            "quantidade_padrao_compra": quantidade_padrao
        }
        lst_estoque.append(dict_item)

    arq.close()
    return 0


def salvar_estoque():
    """Salva dados de estoque da memória para o arquivo."""
    try:
        arq = open(arq_estoque_path, "w")
    except:
        return 1

    for item in lst_estoque:
        codigo = item["codigo"]
        quantidade = item["quantidade"]
        quantidade_minima = item["quantidade_minima"]
        quantidade_padrao = item["quantidade_padrao_compra"]

        arq.write(f"{codigo},{quantidade},{quantidade_minima},{quantidade_padrao}\n")

    arq.close()
    return 0


def _buscar_item_estoque(indice_produto):
    """Procura um produto pelo código dentro de lst_estoque."""
    for item in lst_estoque:
        if item["codigo"] == indice_produto:
            return item
    return None


def adicionar_produto_estoque(indice_produto, quantidade, quantidade_minima=0, quantidade_padrao_compra=0):
    """Adiciona um produto ao estoque ou aumenta a quantidade.

    indice_produto: código do produto (string)
    """
    if quantidade < 0:
        return 1

    # verifica se produto existe na lista de produtos
    for prod in produto.lst_produtos:
        if prod["codigo"] == indice_produto:
            break
    else:
        return 3  # produto_nao_encontrado

    item = _buscar_item_estoque(indice_produto)

    if item is None:
        novo_item = {
            "codigo": indice_produto,
            "quantidade": quantidade,
            "quantidade_minima": quantidade_minima,
            "quantidade_padrao_compra": quantidade_padrao_compra
        }
        lst_estoque.append(novo_item)
    else:
        item["quantidade"] = item["quantidade"] + quantidade
        # só muda mínimos se valores positivos forem passados
        if quantidade_minima > 0:
            item["quantidade_minima"] = quantidade_minima
        if quantidade_padrao_compra > 0:
            item["quantidade_padrao_compra"] = quantidade_padrao_compra

    return 0


def entrada_estoque(indice_produto, quantidade):
    """Adiciona quantidade ao estoque existente."""
    if quantidade <= 0:
        return 1

    item = _buscar_item_estoque(indice_produto)
    if item is None:
        return 3  # produto_nao_encontrado

    item["quantidade"] = item["quantidade"] + quantidade
    return 0


def saida_estoque(indice_produto, quantidade):
    """Remove quantidade do estoque (por venda).

    Retornos:
    0 = sucesso
    1 = erro
    3 = produto_nao_encontrado
    4 = estoque_insuficiente
    8 = estoque_baixo (venda realizada, mas abaixo do mínimo)
    """
    if quantidade <= 0:
        return 1

    item = _buscar_item_estoque(indice_produto)
    if item is None:
        return 3  # produto_nao_encontrado

    if item["quantidade"] < quantidade:
        return 4  # estoque_insuficiente

    item["quantidade"] = item["quantidade"] - quantidade

    if item["quantidade"] < item["quantidade_minima"]:
        return 8  # estoque_baixo

    return 0


def consultar_estoque():
    """Exibe relatório completo do estoque."""
    if len(lst_estoque) == 0:
        print("Estoque vazio.")
        return 1

    print("CODIGO | NOME DO PRODUTO | QTD | QTD_MINIMA | QTD_PADRAO_COMPRA")
    for item in lst_estoque:
        codigo = item["codigo"]
        nome = fornecedor.obtem_nome_produto(codigo)
        if nome is None:
            nome = "(desconhecido)"

        quantidade = item["quantidade"]
        quantidade_minima = item["quantidade_minima"]
        quantidade_padrao = item["quantidade_padrao_compra"]

        print(f"{codigo} | {nome} | {quantidade} | {quantidade_minima} | {quantidade_padrao}")

    return 0


def definir_quantidade_minima(indice_produto, quantidade_minima):
    """Define quantidade mínima para um produto."""
    if quantidade_minima < 0:
        return 1

    item = _buscar_item_estoque(indice_produto)
    if item is None:
        return 3

    item["quantidade_minima"] = quantidade_minima
    return 0


def verificar_produtos_abaixo_minimo():
    """Verifica e exibe produtos com estoque abaixo do mínimo."""
    achou = False

    for item in lst_estoque:
        if item["quantidade"] < item["quantidade_minima"]:
            if not achou:
                print("PRODUTOS ABAIXO DO MÍNIMO:")
            achou = True
            codigo = item["codigo"]
            nome = fornecedor.obtem_nome_produto(codigo)
            if nome is None:
                nome = "(desconhecido)"
            print(f"{codigo} - {nome}: quantidade = {item['quantidade']}, mínimo = {item['quantidade_minima']}")

    if not achou:
        print("Nenhum produto abaixo do mínimo.")

    return 0


def gerar_pedidos_reposicao():
    """Gera e exibe pedidos de reposição para produtos abaixo do mínimo."""
    tem_pedido = False

    for item in lst_estoque:
        if item["quantidade"] < item["quantidade_minima"]:
            if not tem_pedido:
                print("PEDIDOS DE REPOSIÇÃO:")
            tem_pedido = True

            codigo = item["codigo"]
            nome = fornecedor.obtem_nome_produto(codigo)
            if nome is None:
                nome = "(desconhecido)"

            qtd_comprar = item["quantidade_padrao_compra"]
            print(f"Produto {codigo} - {nome} | Quantidade sugerida: {qtd_comprar}")

    if not tem_pedido:
        print("Nenhum produto precisa de reposição.")

    return 0


def contatar_fornecedores_estoque_baixo():
    """Identifica produtos abaixo do mínimo e contata fornecedores."""
    for item in lst_estoque:
        if item["quantidade"] < item["quantidade_minima"]:
            codigo = item["codigo"]
            status, lista_fornecedores = fornecedor.buscar_fornecedores_do_produto(codigo)

            if status != 0:
                continue

            if len(lista_fornecedores) == 0:
                continue

            motivo = "Reposição automática de estoque - produto abaixo do mínimo."
            lista_produtos = [codigo]

            for cnpj in lista_fornecedores:
                fornecedor.contatar_fornecedor(cnpj, motivo, lista_produtos)

    return 0


def verificar_disponibilidade_fornecedor(indice_produto):
    """Mostra quais fornecedores podem fornecer um produto."""
    status, lista_fornecedores = fornecedor.buscar_fornecedores_do_produto(indice_produto)

    if status != 0:
        return 3  # produto_nao_encontrado

    if len(lista_fornecedores) == 0:
        print("Nenhum fornecedor cadastrado para este produto.")
        return 0

    print(f"Fornecedores para o produto {indice_produto}:")
    for cnpj in lista_fornecedores:
        nome = fornecedor.obtem_nome_fornecedor(cnpj)
        print(f"- {cnpj} - {nome}")

    return 0


# TESTES AUTOMATIZADOS
def testa_carregar_estoque():
    """Testa a função carregar_estoque()"""
    global lst_estoque, arq_estoque_path
    import os

    salva_path = arq_estoque_path
    salva_estoque = lst_estoque.copy()

    # Caso 85: Arquivo válido com dados
    arq_estoque_path = "estoque_teste.txt"
    with open(arq_estoque_path, "w") as f:
        f.write("10001-2,50,10,20\n")
        f.write("10002-3,30,5,15\n")
    
    assert carregar_estoque() == 0, "Erro em carregar_estoque. Caso 85."
    assert len(lst_estoque) == 2, "Erro em carregar_estoque. Caso 85: quantidade incorreta de itens."
    assert lst_estoque[0]["codigo"] == "10001-2", "Erro em carregar_estoque. Caso 85: código incorreto."

    # Caso 86: Arquivo inexistente
    arq_estoque_path = "estoque_nao_existe.txt"
    if os.path.exists(arq_estoque_path):
        os.remove(arq_estoque_path)
    
    assert carregar_estoque() == 1, "Erro em carregar_estoque. Caso 86."

    # Caso 87: Arquivo vazio
    arq_estoque_path = "estoque_vazio.txt"
    with open(arq_estoque_path, "w") as f:
        f.write("")
    
    assert carregar_estoque() == 0, "Erro em carregar_estoque. Caso 87."
    assert len(lst_estoque) == 0, "Erro em carregar_estoque. Caso 87: deveria estar vazio."

    # Limpeza
    if os.path.exists("estoque_teste.txt"):
        os.remove("estoque_teste.txt")
    if os.path.exists("estoque_vazio.txt"):
        os.remove("estoque_vazio.txt")

    arq_estoque_path = salva_path
    lst_estoque = salva_estoque.copy()


def testa_salvar_estoque():
    """Testa a função salvar_estoque()"""
    global lst_estoque, arq_estoque_path
    import os

    salva_path = arq_estoque_path
    salva_estoque = lst_estoque.copy()

    # Caso 88: Salvar estoque não vazio
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]
    arq_estoque_path = "estoque_salvar_teste.txt"
    
    assert salvar_estoque() == 0, "Erro em salvar_estoque. Caso 88."
    assert os.path.exists(arq_estoque_path), "Erro em salvar_estoque. Caso 88: arquivo não criado."

    # Caso 89: Estoque vazio
    lst_estoque = []
    arq_estoque_path = "estoque_vazio_salvo.txt"
    
    assert salvar_estoque() == 0, "Erro em salvar_estoque. Caso 89."
    assert os.path.getsize(arq_estoque_path) == 0, "Erro em salvar_estoque. Caso 89: arquivo deveria estar vazio."

    # Limpeza
    if os.path.exists("estoque_salvar_teste.txt"):
        os.remove("estoque_salvar_teste.txt")
    if os.path.exists("estoque_vazio_salvo.txt"):
        os.remove("estoque_vazio_salvo.txt")

    arq_estoque_path = salva_path
    lst_estoque = salva_estoque.copy()


def testa_adicionar_produto_estoque():
    """Testa a função adicionar_produto_estoque()"""
    global lst_estoque
    import produto

    salva_estoque = lst_estoque.copy()
    salva_produtos = produto.lst_produtos.copy()

    # Setup
    produto.lst_produtos = [
        {"codigo": "10001-2", "nome": "Produto A", "categoria": "teste", "preco_venda": 10.0}
    ]
    lst_estoque = []

    # Caso 90: Adicionar novo produto
    assert adicionar_produto_estoque("10001-2", 50, 10, 20) == 0, "Erro em adicionar_produto_estoque. Caso 90."
    assert len(lst_estoque) == 1, "Erro em adicionar_produto_estoque. Caso 90: produto não adicionado."
    assert lst_estoque[0]["quantidade"] == 50, "Erro em adicionar_produto_estoque. Caso 90: quantidade incorreta."

    # Caso 91: Produto inexistente
    assert adicionar_produto_estoque("99999-9", 10, 5, 10) == 3, "Erro em adicionar_produto_estoque. Caso 91."

    # Caso 92: Quantidade negativa
    assert adicionar_produto_estoque("10001-2", -5, 10, 20) == 1, "Erro em adicionar_produto_estoque. Caso 92."

    # Caso 93: Adicionar a produto já existente
    assert adicionar_produto_estoque("10001-2", 10, 5, 15) == 0, "Erro em adicionar_produto_estoque. Caso 93."
    assert lst_estoque[0]["quantidade"] == 60, "Erro em adicionar_produto_estoque. Caso 93: quantidade não somada."

    lst_estoque = salva_estoque.copy()
    produto.lst_produtos = salva_produtos.copy()


def testa_entrada_estoque():
    """Testa a função entrada_estoque()"""
    global lst_estoque

    salva_estoque = lst_estoque.copy()

    # Setup
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]

    # Caso 94: Entrada válida
    assert entrada_estoque("10001-2", 20) == 0, "Erro em entrada_estoque. Caso 94."
    assert lst_estoque[0]["quantidade"] == 70, "Erro em entrada_estoque. Caso 94: quantidade não atualizada."

    # Caso 95: Produto inexistente
    assert entrada_estoque("99999-9", 10) == 3, "Erro em entrada_estoque. Caso 95."

    # Caso 96: Quantidade inválida (zero ou negativa)
    assert entrada_estoque("10001-2", 0) == 1, "Erro em entrada_estoque. Caso 96."
    assert entrada_estoque("10001-2", -5) == 1, "Erro em entrada_estoque. Caso 96."

    lst_estoque = salva_estoque.copy()


def testa_saida_estoque():
    """Testa a função saida_estoque()"""
    global lst_estoque

    salva_estoque = lst_estoque.copy()

    # Setup
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]

    # Caso 97: Saída válida
    assert saida_estoque("10001-2", 20) == 0, "Erro em saida_estoque. Caso 97."
    assert lst_estoque[0]["quantidade"] == 30, "Erro em saida_estoque. Caso 97: quantidade não atualizada."

    # Caso 98: Produto inexistente
    assert saida_estoque("99999-9", 10) == 3, "Erro em saida_estoque. Caso 98."

    # Caso 99: Estoque insuficiente
    assert saida_estoque("10001-2", 100) == 4, "Erro em saida_estoque. Caso 99."

    # Caso 100: Saída que deixa abaixo do mínimo
    lst_estoque[0]["quantidade"] = 15
    assert saida_estoque("10001-2", 10) == 8, "Erro em saida_estoque. Caso 100."
    assert lst_estoque[0]["quantidade"] == 5, "Erro em saida_estoque. Caso 100: quantidade incorreta."

    # Caso 101: Quantidade inválida
    assert saida_estoque("10001-2", 0) == 1, "Erro em saida_estoque. Caso 101."
    assert saida_estoque("10001-2", -5) == 1, "Erro em saida_estoque. Caso 101."

    lst_estoque = salva_estoque.copy()


def testa_consultar_estoque():
    """Testa a função consultar_estoque()"""
    global lst_estoque

    salva_estoque = lst_estoque.copy()

    # Caso 102: Estoque com produtos
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]
    assert consultar_estoque() == 0, "Erro em consultar_estoque. Caso 102."

    # Caso 103: Estoque vazio
    lst_estoque = []
    assert consultar_estoque() == 1, "Erro em consultar_estoque. Caso 103."

    lst_estoque = salva_estoque.copy()


def testa_definir_quantidade_minima():
    """Testa a função definir_quantidade_minima()"""
    global lst_estoque

    salva_estoque = lst_estoque.copy()

    # Setup
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]

    # Caso 104: Definir quantidade mínima válida
    assert definir_quantidade_minima("10001-2", 15) == 0, "Erro em definir_quantidade_minima. Caso 104."
    assert lst_estoque[0]["quantidade_minima"] == 15, "Erro em definir_quantidade_minima. Caso 104: não atualizado."

    # Caso 105: Produto inexistente
    assert definir_quantidade_minima("99999-9", 10) == 3, "Erro em definir_quantidade_minima. Caso 105."

    # Caso 106: Quantidade negativa
    assert definir_quantidade_minima("10001-2", -5) == 1, "Erro em definir_quantidade_minima. Caso 106."

    lst_estoque = salva_estoque.copy()


def testa_verificar_produtos_abaixo_minimo():
    """Testa a função verificar_produtos_abaixo_minimo()"""
    global lst_estoque

    salva_estoque = lst_estoque.copy()

    # Caso 107: Produtos abaixo do mínimo
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 5, "quantidade_minima": 10, "quantidade_padrao_compra": 20},
        {"codigo": "10002-3", "quantidade": 30, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]
    assert verificar_produtos_abaixo_minimo() == 0, "Erro em verificar_produtos_abaixo_minimo. Caso 107."

    # Caso 108: Nenhum produto abaixo do mínimo
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]
    assert verificar_produtos_abaixo_minimo() == 0, "Erro em verificar_produtos_abaixo_minimo. Caso 108."

    lst_estoque = salva_estoque.copy()


def testa_gerar_pedidos_reposicao():
    """Testa a função gerar_pedidos_reposicao()"""
    global lst_estoque

    salva_estoque = lst_estoque.copy()

    # Caso 109: Gerar pedidos para produtos abaixo do mínimo
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 5, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]
    assert gerar_pedidos_reposicao() == 0, "Erro em gerar_pedidos_reposicao. Caso 109."

    # Caso 110: Nenhum pedido necessário
    lst_estoque = [
        {"codigo": "10001-2", "quantidade": 50, "quantidade_minima": 10, "quantidade_padrao_compra": 20}
    ]
    assert gerar_pedidos_reposicao() == 0, "Erro em gerar_pedidos_reposicao. Caso 110."

    lst_estoque = salva_estoque.copy()


def testa_funcoes_estoque():
    """Executa todos os testes do módulo estoque"""
    print("Iniciando testes do módulo estoque...")
    
    testa_carregar_estoque()
    print("✓ Testes de carregar_estoque passaram (casos 85-87)")
    
    testa_salvar_estoque()
    print("✓ Testes de salvar_estoque passaram (casos 88-89)")
    
    testa_adicionar_produto_estoque()
    print("✓ Testes de adicionar_produto_estoque passaram (casos 90-93)")
    
    testa_entrada_estoque()
    print("✓ Testes de entrada_estoque passaram (casos 94-96)")
    
    testa_saida_estoque()
    print("✓ Testes de saida_estoque passaram (casos 97-101)")
    
    testa_consultar_estoque()
    print("✓ Testes de consultar_estoque passaram (casos 102-103)")
    
    testa_definir_quantidade_minima()
    print("✓ Testes de definir_quantidade_minima passaram (casos 104-106)")
    
    testa_verificar_produtos_abaixo_minimo()
    print("✓ Testes de verificar_produtos_abaixo_minimo passaram (casos 107-108)")
    
    testa_gerar_pedidos_reposicao()
    print("✓ Testes de gerar_pedidos_reposicao passaram (casos 109-110)")
    
    print("\nTODOS OS TESTES DO MÓDULO ESTOQUE (85-110) PASSARAM!")
