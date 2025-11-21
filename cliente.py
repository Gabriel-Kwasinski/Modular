# cliente.py
#
# Módulo de clientes do sistema de supermercado.
# Guarda os clientes em memória na lista 'lista_clientes'
# e faz a leitura/gravação em um arquivo texto 'clientes.txt'.

from validacao import validaCPF, validaEmail, SUCESSO, ERRO

CLIENTE_NAO_ENCONTRADO = 2
CPF_JA_CADASTRADO = 5

ARQ_CLIENTES = "clientes.txt"
lista_clientes = []   # cada item é {"nome": ..., "cpf": ..., "email": ...}


def carregar_clientes():
    global lista_clientes
    lista_clientes = []

    try:
        f = open("clientes.txt", "r")
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

def salvar_clientes():
    try:
        f = open("clientes.txt", "w")
    except:
        return ERRO

    for c in lista_clientes:
        f.write(f"{c['nome']};{c['cpf']};{c['email']}\n")

    f.close()
    return SUCESSO


def buscar_cliente_por_cpf(cpf):
    """
    Procura um cliente pelo CPF.

    Retorna:
      índice do cliente (0, 1, 2, ...) se achar
      -1 se não encontrar
    """
    for i in range(len(lista_clientes)):
        if lista_clientes[i]["cpf"] == cpf:
            return i
    return -1


def cadastrar_cliente(nome, cpf, email):
    """
    Cadastra um novo cliente.

    Regras:
      - nome, cpf e email não podem ser vazios
      - cpf deve ser válido (validaCPF)
      - email deve ser válido (validaEmail)
      - cpf não pode estar repetido

    Retorna:
      SUCESSO (0) se cadastrar
      CPF_JA_CADASTRADO (5) se CPF já existe
      ERRO (1) para qualquer outro problema
    """
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


def listar_clientes():
    """
    Mostra todos os clientes na tela.

    Retorna:
      SUCESSO (0) se listou pelo menos 1 cliente
      ERRO    (1) se lista estiver vazia
    """
    if not lista_clientes:
        print("Nenhum cliente cadastrado.")
        return ERRO

    for i in range(len(lista_clientes)):
        c = lista_clientes[i]
        print(f"[{i}] Nome: {c['nome']} | CPF: {c['cpf']} | Email: {c['email']}")

    return SUCESSO


def atualizar_cliente(indice, nome=None, email=None):
    """
    Atualiza nome e/ou email de um cliente.

    Regras:
      - índice inválido -> CLIENTE_NAO_ENCONTRADO (2)
      - se não mudar nada (nenhum campo válido) -> ERRO (1)
      - se email novo for inválido -> ERRO (1)
      - se conseguir atualizar -> SUCESSO (0)
    """
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


def deletar_cliente(indice):
    """
    Remove um cliente da lista.

    Retorna:
      SUCESSO (0) se remover
      CLIENTE_NAO_ENCONTRADO (2) se índice for inválido
    """
    if indice < 0 or indice >= len(lista_clientes):
        return CLIENTE_NAO_ENCONTRADO

    del lista_clientes[indice]
    return SUCESSO
