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


# TESTES AUTOMATIZADOS
def testa_carregar_compras():
    """Testa a função carregar_compras()"""
    global historico_compras, arq_compras_path
    import os

    # Salva estado original
    salva_path = arq_compras_path
    salva_historico = historico_compras.copy()

    # Caso 65: Arquivo válido com compras
    arq_compras_path = "compras_teste.txt"
    with open(arq_compras_path, "w") as f:
        f.write("2025-11-23 10:00:00,12345678909,50.00,10001-2,2,10002-3,1\n")
    
    assert carregar_compras() == 0, "Erro em carregar_compras. Caso 65."
    assert len(historico_compras) == 1, "Erro em carregar_compras. Caso 65: historico vazio."
    assert historico_compras[0]["cpf_cliente"] == "12345678909", "Erro em carregar_compras. Caso 65: CPF incorreto."

    # Caso 66: Arquivo inexistente
    arq_compras_path = "compras_nao_existe.txt"
    if os.path.exists(arq_compras_path):
        os.remove(arq_compras_path)
    
    assert carregar_compras() == 1, "Erro em carregar_compras. Caso 66."

    # Caso 67: Arquivo vazio
    arq_compras_path = "compras_vazio.txt"
    with open(arq_compras_path, "w") as f:
        f.write("")
    
    result = carregar_compras()
    assert result == 0, "Erro em carregar_compras. Caso 67."
    assert len(historico_compras) == 0, "Erro em carregar_compras. Caso 67: deveria estar vazio."

    # Limpeza
    if os.path.exists("compras_teste.txt"):
        os.remove("compras_teste.txt")
    if os.path.exists("compras_vazio.txt"):
        os.remove("compras_vazio.txt")

    arq_compras_path = salva_path
    historico_compras = salva_historico.copy()


def testa_salvar_compras():
    """Testa a função salvar_compras()"""
    global historico_compras, arq_compras_path
    import os

    salva_path = arq_compras_path
    salva_historico = historico_compras.copy()

    # Caso 68: Salvar histórico não vazio
    historico_compras = [{
        "data_hora": "2025-11-23 10:00:00",
        "cpf_cliente": "12345678909",
        "itens": [{"codigo": "10001-2", "quantidade": 2}],
        "valor_total": 50.0
    }]
    arq_compras_path = "compras_salvar_teste.txt"
    
    assert salvar_compras() == 0, "Erro em salvar_compras. Caso 68."
    assert os.path.exists(arq_compras_path), "Erro em salvar_compras. Caso 68: arquivo não criado."

    # Caso 69: Histórico vazio
    historico_compras = []
    arq_compras_path = "compras_vazio_salvo.txt"
    
    assert salvar_compras() == 0, "Erro em salvar_compras. Caso 69."
    assert os.path.getsize(arq_compras_path) == 0, "Erro em salvar_compras. Caso 69: arquivo deveria estar vazio."

    # Limpeza
    if os.path.exists("compras_salvar_teste.txt"):
        os.remove("compras_salvar_teste.txt")
    if os.path.exists("compras_vazio_salvo.txt"):
        os.remove("compras_vazio_salvo.txt")

    arq_compras_path = salva_path
    historico_compras = salva_historico.copy()


def testa_criar_carrinho():
    """Testa a função criar_carrinho()"""
    global carrinho_atual

    # Caso 70: Criar carrinho vazio
    carrinho_atual = [{"codigo": "10001-2", "quantidade": 1}]
    assert criar_carrinho() == 0, "Erro em criar_carrinho. Caso 70."
    assert len(carrinho_atual) == 0, "Erro em criar_carrinho. Caso 70: carrinho não foi esvaziado."


def testa_adicionar_item_carrinho():
    """Testa a função adicionar_item_carrinho()"""
    global carrinho_atual
    import produto
    import estoque

    salva_carrinho = carrinho_atual.copy()
    salva_produtos = produto.lst_produtos.copy()
    salva_estoque = estoque.lst_estoque.copy()

    # Setup: produtos e estoque para teste
    produto.lst_produtos = [
        {"codigo": "10001-2", "nome": "Produto A", "categoria": "teste", "preco_venda": 10.0}
    ]
    estoque.lst_estoque = [
        {"codigo": "10001-2", "quantidade": 5, "quantidade_minima": 2, "quantidade_padrao_compra": 10}
    ]
    criar_carrinho()

    # Caso 71: Adicionar produto válido
    assert adicionar_item_carrinho("10001-2", 2) == 0, "Erro em adicionar_item_carrinho. Caso 71."
    assert len(carrinho_atual) == 1, "Erro em adicionar_item_carrinho. Caso 71: item não adicionado."
    assert carrinho_atual[0]["quantidade"] == 2, "Erro em adicionar_item_carrinho. Caso 71: quantidade incorreta."

    # Caso 72: Produto inexistente
    assert adicionar_item_carrinho("99999-9", 1) == 3, "Erro em adicionar_item_carrinho. Caso 72."

    # Caso 73: Estoque insuficiente
    assert adicionar_item_carrinho("10001-2", 10) == 4, "Erro em adicionar_item_carrinho. Caso 73."

    # Caso 74: Quantidade inválida (zero ou negativa)
    assert adicionar_item_carrinho("10001-2", 0) == 1, "Erro em adicionar_item_carrinho. Caso 74."
    assert adicionar_item_carrinho("10001-2", -1) == 1, "Erro em adicionar_item_carrinho. Caso 74."

    # Restaura estado
    carrinho_atual = salva_carrinho.copy()
    produto.lst_produtos = salva_produtos.copy()
    estoque.lst_estoque = salva_estoque.copy()


def testa_remover_item_carrinho():
    """Testa a função remover_item_carrinho()"""
    global carrinho_atual

    salva_carrinho = carrinho_atual.copy()

    # Caso 75: Remover produto existente
    carrinho_atual = [{"codigo": "10001-2", "quantidade": 2}]
    assert remover_item_carrinho("10001-2") == 0, "Erro em remover_item_carrinho. Caso 75."
    assert len(carrinho_atual) == 0, "Erro em remover_item_carrinho. Caso 75: produto não removido."

    # Caso 76: Remover produto inexistente
    carrinho_atual = [{"codigo": "10001-2", "quantidade": 2}]
    assert remover_item_carrinho("99999-9") == 3, "Erro em remover_item_carrinho. Caso 76."

    carrinho_atual = salva_carrinho.copy()


def testa_exibir_carrinho():
    """Testa a função exibir_carrinho()"""
    global carrinho_atual
    import produto

    salva_carrinho = carrinho_atual.copy()
    salva_produtos = produto.lst_produtos.copy()

    produto.lst_produtos = [
        {"codigo": "10001-2", "nome": "Produto A", "categoria": "teste", "preco_venda": 10.0}
    ]

    # Caso 77: Carrinho com itens
    carrinho_atual = [{"codigo": "10001-2", "quantidade": 2}]
    assert exibir_carrinho() == 0, "Erro em exibir_carrinho. Caso 77."

    # Caso 78: Carrinho vazio
    carrinho_atual = []
    assert exibir_carrinho() == 7, "Erro em exibir_carrinho. Caso 78."

    carrinho_atual = salva_carrinho.copy()
    produto.lst_produtos = salva_produtos.copy()


def testa_finalizar_compra():
    """Testa a função finalizar_compra()"""
    global carrinho_atual, historico_compras
    import produto
    import estoque

    salva_carrinho = carrinho_atual.copy()
    salva_historico = historico_compras.copy()
    salva_produtos = produto.lst_produtos.copy()
    salva_estoque = estoque.lst_estoque.copy()

    # Setup
    produto.lst_produtos = [
        {"codigo": "10001-2", "nome": "Produto A", "categoria": "teste", "preco_venda": 10.0}
    ]
    estoque.lst_estoque = [
        {"codigo": "10001-2", "quantidade": 10, "quantidade_minima": 2, "quantidade_padrao_compra": 10}
    ]
    historico_compras = []

    # Caso 79: Finalizar compra com sucesso
    carrinho_atual = [{"codigo": "10001-2", "quantidade": 2}]
    assert finalizar_compra("12345678909") == 0, "Erro em finalizar_compra. Caso 79."
    assert len(historico_compras) == 1, "Erro em finalizar_compra. Caso 79: compra não registrada."
    assert len(carrinho_atual) == 0, "Erro em finalizar_compra. Caso 79: carrinho não esvaziado."

    # Caso 80: Carrinho vazio
    carrinho_atual = []
    assert finalizar_compra() == 7, "Erro em finalizar_compra. Caso 80."

    # Restaura estado
    carrinho_atual = salva_carrinho.copy()
    historico_compras = salva_historico.copy()
    produto.lst_produtos = salva_produtos.copy()
    estoque.lst_estoque = salva_estoque.copy()


def testa_listar_compras():
    """Testa a função listar_compras()"""
    global historico_compras

    salva_historico = historico_compras.copy()

    # Caso 81: Histórico com compras
    historico_compras = [{
        "data_hora": "2025-11-23 10:00:00",
        "cpf_cliente": "12345678909",
        "itens": [{"codigo": "10001-2", "quantidade": 2}],
        "valor_total": 20.0
    }]
    assert listar_compras() == 0, "Erro em listar_compras. Caso 81."

    # Caso 82: Histórico vazio
    historico_compras = []
    assert listar_compras() == 1, "Erro em listar_compras. Caso 82."

    # Caso 83: Filtrar por CPF
    historico_compras = [
        {
            "data_hora": "2025-11-23 10:00:00",
            "cpf_cliente": "12345678909",
            "itens": [{"codigo": "10001-2", "quantidade": 2}],
            "valor_total": 20.0
        },
        {
            "data_hora": "2025-11-23 11:00:00",
            "cpf_cliente": "98765432100",
            "itens": [{"codigo": "10002-3", "quantidade": 1}],
            "valor_total": 15.0
        }
    ]
    assert listar_compras("12345678909") == 0, "Erro em listar_compras. Caso 83."

    historico_compras = salva_historico.copy()


def testa_cancelar_carrinho():
    """Testa a função cancelar_carrinho()"""
    global carrinho_atual

    # Caso 84: Cancelar carrinho com itens
    carrinho_atual = [{"codigo": "10001-2", "quantidade": 2}]
    assert cancelar_carrinho() == 0, "Erro em cancelar_carrinho. Caso 84."
    assert len(carrinho_atual) == 0, "Erro em cancelar_carrinho. Caso 84: carrinho não esvaziado."


def testa_funcoes_compra():
    """Executa todos os testes do módulo compra"""
    print("Iniciando testes do módulo compra...")
    
    testa_carregar_compras()
    print("✓ Testes de carregar_compras passaram (casos 65-67)")
    
    testa_salvar_compras()
    print("✓ Testes de salvar_compras passaram (casos 68-69)")
    
    testa_criar_carrinho()
    print("✓ Testes de criar_carrinho passaram (caso 70)")
    
    testa_adicionar_item_carrinho()
    print("✓ Testes de adicionar_item_carrinho passaram (casos 71-74)")
    
    testa_remover_item_carrinho()
    print("✓ Testes de remover_item_carrinho passaram (casos 75-76)")
    
    testa_exibir_carrinho()
    print("✓ Testes de exibir_carrinho passaram (casos 77-78)")
    
    testa_finalizar_compra()
    print("✓ Testes de finalizar_compra passaram (casos 79-80)")
    
    testa_listar_compras()
    print("✓ Testes de listar_compras passaram (casos 81-83)")
    
    testa_cancelar_carrinho()
    print("✓ Testes de cancelar_carrinho passaram (caso 84)")
    
    print("\nTODOS OS TESTES DO MÓDULO COMPRA (65-84) PASSARAM!")
