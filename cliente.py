# cliente.py
#
# Módulo de clientes
# Lê, grava, cadastra, lista, atualiza e deleta clientes.
# Possui testes automáticos (Casos 1–21).

import os
from validacao import validaCPF, validaEmail, SUCESSO, ERRO

CLIENTE_NAO_ENCONTRADO = 2
CPF_JA_CADASTRADO = 5

# Caminho global que será alterado pelos testes
ARQ_CLIENTES = "clientes.txt"

# Lista em memória
lista_clientes = []

#CARREGAR
def carregar_clientes():
    global lista_clientes, ARQ_CLIENTES

    lista_clientes = []

    try:
        f = open(ARQ_CLIENTES, "r")
    except:
        return ERRO

    for linha in f:
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(";")
        if len(partes) != 3:
            continue
        nome, cpf, email = partes
        lista_clientes.append({"nome": nome, "cpf": cpf, "email": email})

    f.close()
    return SUCESSO


# SALVAR
def salvar_clientes():
    global ARQ_CLIENTES, lista_clientes

    try:
        f = open(ARQ_CLIENTES, "w")
    except:
        return ERRO

    for c in lista_clientes:
        f.write(f"{c['nome']};{c['cpf']};{c['email']}\n")

    f.close()
    return SUCESSO


# BUSCAR
def buscar_cliente_por_cpf(cpf):
    for i in range(len(lista_clientes)):
        if lista_clientes[i]["cpf"] == cpf:
            return i
    return -1


# CADASTRAR
def cadastrar_cliente(nome, cpf, email):
    global lista_clientes

    nome = nome.strip()
    cpf = cpf.strip()
    email = email.strip()

    if not nome or not cpf or not email:
        return ERRO

    if validaCPF(cpf) != SUCESSO:
        return ERRO

    if validaEmail(email) != SUCESSO:
        return ERRO

    if buscar_cliente_por_cpf(cpf) != -1:
        return CPF_JA_CADASTRADO

    lista_clientes.append({"nome": nome, "cpf": cpf, "email": email})
    return SUCESSO


# LISTAR
def listar_clientes():
    if not lista_clientes:
        print("Nenhum cliente cadastrado.")
        return ERRO

    for i in range(len(lista_clientes)):
        c = lista_clientes[i]
        print(f"[{i}] Nome: {c['nome']} | CPF: {c['cpf']} | Email: {c['email']}")

    return SUCESSO


# ATUALIZAR
def atualizar_cliente(indice, nome=None, email=None):
    if indice < 0 or indice >= len(lista_clientes):
        return CLIENTE_NAO_ENCONTRADO

    cliente = lista_clientes[indice]
    alterou = False

    if nome is not None:
        nome = nome.strip()
        if nome:
            cliente["nome"] = nome
            alterou = True

    if email is not None:
        email = email.strip()
        if email:
            if validaEmail(email) != SUCESSO:
                return ERRO
            cliente["email"] = email
            alterou = True

    if not alterou:
        return ERRO

    return SUCESSO


# DELETAR
def deletar_cliente(indice):
    if indice < 0 or indice >= len(lista_clientes):
        return CLIENTE_NAO_ENCONTRADO

    del lista_clientes[indice]
    return SUCESSO


# TESTES AUTOMATIZADOS (Casos 1–21)
def testa_carregar_clientes():
    global ARQ_CLIENTES, lista_clientes

    salva = ARQ_CLIENTES

    # Caso 1 — arquivo válido
    ARQ_CLIENTES = "clientes_ok.txt"
    with open(ARQ_CLIENTES, "w") as f:
        f.write("Maria;12345678909;maria@example.com\n")

    assert carregar_clientes() == SUCESSO
    assert len(lista_clientes) == 1

    # Caso 2 — arquivo inexistente
    ARQ_CLIENTES = "clientes_inexistente.txt"
    if os.path.isfile(ARQ_CLIENTES):
        os.remove(ARQ_CLIENTES)

    assert carregar_clientes() == ERRO
    assert len(lista_clientes) == 0

    # Caso 3 — arquivo vazio
    ARQ_CLIENTES = "clientes_vazio.txt"
    with open(ARQ_CLIENTES, "w") as f:
        f.write("")

    assert carregar_clientes() == SUCESSO
    assert len(lista_clientes) == 0

    ARQ_CLIENTES = salva


def testa_salvar_clientes():
    global ARQ_CLIENTES, lista_clientes

    salva = ARQ_CLIENTES
    salva_lista = lista_clientes.copy()

    # Caso 4 — lista não vazia
    lista_clientes = [
        {"nome": "Maria", "cpf": "12345678909", "email": "maria@example.com"}
    ]
    ARQ_CLIENTES = "clientes_salvar_ok.txt"
    assert salvar_clientes() == SUCESSO
    assert os.path.isfile(ARQ_CLIENTES)

    # Caso 5 — erro ao salvar (usar diretório)
    if not os.path.isdir("bloqueado"):
        os.mkdir("bloqueado")
    ARQ_CLIENTES = "bloqueado"
    assert salvar_clientes() == ERRO

    # Caso 6 — lista vazia
    lista_clientes = []
    ARQ_CLIENTES = "clientes_vazio_salvo.txt"
    assert salvar_clientes() == SUCESSO
    assert os.path.getsize(ARQ_CLIENTES) == 0

    ARQ_CLIENTES = salva
    lista_clientes = salva_lista.copy()


def testa_cadastrar_cliente():
    global lista_clientes

    lista_clientes = []

    # Caso 7 — CPF novo
    assert cadastrar_cliente("Maria", "123.456.789-09", "maria@example.com") == SUCESSO
    assert len(lista_clientes) == 1

    # Caso 8 — CPF repetido
    assert cadastrar_cliente("Outra", "123.456.789-09", "outra@example.com") == CPF_JA_CADASTRADO

    # Caso 9 — campos vazios
    assert cadastrar_cliente("", "11122233344", "x@x.com") == ERRO
    assert cadastrar_cliente("Fulano", "", "x@x.com") == ERRO
    assert cadastrar_cliente("Fulano", "11122233344", "") == ERRO

    # Caso 10 — CPF inválido
    assert cadastrar_cliente("Joao", "111.111.111-11", "joao@example.com") == ERRO


def testa_listar_clientes():
    global lista_clientes

    # Caso 11 — lista com clientes
    lista_clientes = [
        {"nome": "Maria", "cpf": "123", "email": "maria@example.com"}
    ]
    assert listar_clientes() == SUCESSO

    # Caso 12 — lista vazia
    lista_clientes = []
    assert listar_clientes() == ERRO


def testa_buscar_cliente_por_cpf():
    global lista_clientes

    lista_clientes = [
        {"nome": "Maria", "cpf": "123", "email": "maria@example.com"}
    ]

    # Caso 13 — existe
    assert buscar_cliente_por_cpf("123") == 0

    # Caso 14 — não existe
    assert buscar_cliente_por_cpf("000") == -1


def testa_atualizar_cliente():
    global lista_clientes

    lista_clientes = [
        {"nome": "Maria", "cpf": "123", "email": "maria@example.com"}
    ]

    # Caso 15 — atualizar nome e email
    assert atualizar_cliente(0, nome="Nova", email="n@example.com") == SUCESSO
    assert lista_clientes[0]["nome"] == "Nova"

    # Caso 16 — índice inválido
    assert atualizar_cliente(9, nome="X") == CLIENTE_NAO_ENCONTRADO

    # Caso 17 — nenhum dado novo
    assert atualizar_cliente(0) == ERRO

    # Caso 18 — atualização parcial
    assert atualizar_cliente(0, nome="Maria") == SUCESSO
    assert lista_clientes[0]["nome"] == "Maria"


def testa_deletar_cliente():
    global lista_clientes

    # Caso 19 — remover OK
    lista_clientes = [
        {"nome": "Maria", "cpf": "123", "email": "maria@example.com"}
    ]
    assert deletar_cliente(0) == SUCESSO

    # Caso 21 — lista vazia
    assert deletar_cliente(0) == CLIENTE_NAO_ENCONTRADO

    # Caso 20 — índice inválido
    lista_clientes = [
        {"nome": "Joao", "cpf": "987", "email": "joao@example.com"}
    ]
    assert deletar_cliente(-1) == CLIENTE_NAO_ENCONTRADO
    assert deletar_cliente(5) == CLIENTE_NAO_ENCONTRADO


def testa_funcoes_cliente():
    testa_carregar_clientes()
    testa_salvar_clientes()
    testa_cadastrar_cliente()
    testa_listar_clientes()
    testa_buscar_cliente_por_cpf()
    testa_atualizar_cliente()
    testa_deletar_cliente()
    print("TODOS OS TESTES CLIENTE (1–21) PASSARAM!")
