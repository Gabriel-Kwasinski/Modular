# IMPORTS
from datetime import datetime
import produto
import estoque

# FUNÇÕES (conforme especificação):
# carregar_compras()
# salvar_compras()
# criar_carrinho()
# adicionar_item_carrinho(indice_produto, quantidade)
# remover_item_carrinho(indice_produto)
# exibir_carrinho()
# finalizar_compra(cpf_cliente=None)
# listar_compras(cpf_cliente=None)
# cancelar_carrinho()
#
# Convenção de retorno:
# 0 = SUCESSO
# 1 = ERRO
# 3 = PRODUTO_NAO_ENCONTRADO
# 4 = ESTOQUE_INSUFICIENTE
# 7 = CARRINHO_VAZIO

# LISTAS GLOBAIS
# historico_compras: lista de dicionários
# {
#     "data_hora"  : str,
#     "cpf_cliente": str ou None,
#     "itens"      : [ { "codigo": str, "quantidade": int }, ... ],
#     "valor_total": float
# }
historico_compras = []

# carrinho_atual: lista de dicionários
# [ { "codigo": str, "quantidade": int }, ... ]
carrinho_atual = []

# caminho do arquivo de compras
arq_compras_path = "compras.txt"


def carregar_compras():
    """Carrega histórico de compras do arquivo para a memória.

    Formato de cada linha:
    data_hora,cpf_cliente,valor_total,codigo1,quant1,codigo2,quant2,...
    """
    global historico_compras
    historico_compras = []

    try:
        arq = open(arq_compras_path, "r")
    except:
        return 1

    for lin in arq:
        lin = lin.strip()
        if lin == "":
            continue

        partes = lin.split(",")
        if len(partes) < 3:
            continue

        data_hora = partes[0]
        cpf_cliente = partes[1]
        if cpf_cliente == "-":
            cpf_cliente = None

        try:
            valor_total = float(partes[2])
        except:
            valor_total = 0.0

        itens = []
        i = 3
        while i + 1 < len(partes):
            codigo = partes[i]
            try:
                quantidade = int(partes[i + 1])
            except:
                quantidade = 0

            dict_item = {
                "codigo": codigo,
                "quantidade": quantidade
            }
            itens.append(dict_item)
            i = i + 2

        dict_compra = {
            "data_hora": data_hora,
            "cpf_cliente": cpf_cliente,
            "itens": itens,
            "valor_total": valor_total
        }

        historico_compras.append(dict_compra)

    arq.close()
    return 0


def salvar_compras():
    """Salva histórico de compras da memória para o arquivo."""
    try:
        arq = open(arq_compras_path, "w")
    except:
        return 1

    for compra in historico_compras:
        data_hora = compra["data_hora"]
        cpf_cliente = compra["cpf_cliente"]
        if cpf_cliente is None:
            cpf_cliente = "-"

        valor_total = compra["valor_total"]

        linha = f"{data_hora},{cpf_cliente},{valor_total}"

        for item in compra["itens"]:
            codigo = item["codigo"]
            quantidade = item["quantidade"]
            linha = linha + f",{codigo},{quantidade}"

        linha = linha + "\n"
        arq.write(linha)

    arq.close()
    return 0


def criar_carrinho():
    """Inicializa um novo carrinho vazio."""
    global carrinho_atual
    carrinho_atual = []
    return 0


def _obter_produto_por_codigo(codigo):
    for prod in produto.lst_produtos:
        if prod["codigo"] == codigo:
            return prod
    return None


def _obter_quantidade_em_estoque(codigo):
    for item in estoque.lst_estoque:
        if item["codigo"] == codigo:
            return item["quantidade"]
    return 0


def _buscar_item_carrinho(indice_produto):
    for item in carrinho_atual:
        if item["codigo"] == indice_produto:
            return item
    return None


def adicionar_item_carrinho(indice_produto, quantidade):
    """Adiciona um produto ao carrinho, verificando estoque."""
    if quantidade <= 0:
        return 1

    prod = _obter_produto_por_codigo(indice_produto)
    if prod is None:
        return 3  # produto_nao_encontrado

    estoque_disponivel = _obter_quantidade_em_estoque(indice_produto)

    item_carrinho = _buscar_item_carrinho(indice_produto)
    quantidade_atual = 0
    if item_carrinho is not None:
        quantidade_atual = item_carrinho["quantidade"]

    if quantidade_atual + quantidade > estoque_disponivel:
        return 4  # estoque_insuficiente

    if item_carrinho is None:
        novo_item = {
            "codigo": indice_produto,
            "quantidade": quantidade
        }
        carrinho_atual.append(novo_item)
    else:
        item_carrinho["quantidade"] = item_carrinho["quantidade"] + quantidade

    return 0


def remover_item_carrinho(indice_produto):
    """Remove produto do carrinho atual."""
    item = _buscar_item_carrinho(indice_produto)
    if item is None:
        return 3  # produto_nao_encontrado

    carrinho_atual.remove(item)
    return 0


def exibir_carrinho():
    """Exibe conteúdo do carrinho atual."""
    if len(carrinho_atual) == 0:
        print("Carrinho vazio.")
        return 7  # carrinho_vazio

    total = 0.0

    print("CARRINHO ATUAL:")
    print("CODIGO | NOME | QTD | PRECO_UNIT | SUBTOTAL")

    for item in carrinho_atual:
        codigo = item["codigo"]
        quantidade = item["quantidade"]

        prod = _obter_produto_por_codigo(codigo)
        if prod is None:
            nome = "(desconhecido)"
            preco = 0.0
        else:
            nome = prod["nome"]
            preco = float(prod["preco_venda"])

        subtotal = preco * quantidade
        total = total + subtotal

        print(f"{codigo} | {nome} | {quantidade} | {preco} | {subtotal}")

    print(f"TOTAL: {total}")
    return 0


def finalizar_compra(cpf_cliente=None):
    """Finaliza compra, gera registro, baixa estoque e salva arquivo."""
    if len(carrinho_atual) == 0:
        return 7  # carrinho_vazio

    # baixa estoque e calcula total
    valor_total = 0.0
    for item in carrinho_atual:
        codigo = item["codigo"]
        quantidade = item["quantidade"]

        status_saida = estoque.saida_estoque(codigo, quantidade)
        if status_saida != 0 and status_saida != 8:
            # 8 = estoque_baixo, mas venda foi feita
            return 1

        prod = _obter_produto_por_codigo(codigo)
        if prod is None:
            preco = 0.0
        else:
            preco = float(prod["preco_venda"])

        valor_total = valor_total + (preco * quantidade)

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # copia itens do carrinho
    itens_compra = []
    for item in carrinho_atual:
        dict_item = {
            "codigo": item["codigo"],
            "quantidade": item["quantidade"]
        }
        itens_compra.append(dict_item)

    dict_compra = {
        "data_hora": data_hora,
        "cpf_cliente": cpf_cliente,
        "itens": itens_compra,
        "valor_total": valor_total
    }

    historico_compras.append(dict_compra)

    status_salvar = salvar_compras()
    if status_salvar != 0:
        return 1

    # esvazia carrinho
    criar_carrinho()

    return 0


def listar_compras(cpf_cliente=None):
    """Lista o histórico de compras.

    Se cpf_cliente for informado, mostra apenas as compras desse cliente.
    """
    encontrou = False

    for compra in historico_compras:
        if cpf_cliente is not None and compra["cpf_cliente"] != cpf_cliente:
            continue

        encontrou = True

        print("----------------------------------")
        print(f"Data/Hora: {compra['data_hora']}")
        print(f"CPF Cliente: {compra['cpf_cliente']}")
        print("Itens:")

        for item in compra["itens"]:
            codigo = item["codigo"]
            quantidade = item["quantidade"]

            prod = _obter_produto_por_codigo(codigo)
            if prod is None:
                nome = "(desconhecido)"
            else:
                nome = prod["nome"]

            print(f"  - {codigo} - {nome}: {quantidade}")

        print(f"Valor total: {compra['valor_total']}")

    if not encontrou:
        print("Nenhuma compra registrada.")
        return 1

    return 0


def cancelar_carrinho():
    """Esvazia o carrinho atual."""
    global carrinho_atual
    carrinho_atual = []
    return 0
