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
