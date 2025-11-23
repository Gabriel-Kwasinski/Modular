# cliente.py
#
# Módulo de clientes.
# Responsável por carregar, salvar, cadastrar, listar, atualizar,
# deletar e buscar clientes pelo CPF.
#
# Os dados são mantidos em memória em uma lista de dicionários:
#   lista_clientes = [
#       {
#           "nome"  : <str>,
#           "cpf"   : <str>,
#           "email" : <str>
#       },
#       ...
#   ]
#
# A persistência é feita em um arquivo texto (ARQ_CLIENTES), um cliente por linha,
# com o formato:
#       nome;cpf;email
#
# Códigos de retorno (status):
#   SUCESSO               = 0  (importado de validacao)
#   ERRO                  = 1  (importado de validacao)
#   CLIENTE_NAO_ENCONTRADO = 2
#   CPF_JA_CADASTRADO      = 5
#
# CONSTANTES GLOBAIS:
#   ARQ_CLIENTES (str) – caminho do arquivo de clientes (pode ser alterado nos testes).
#
# ESTRUTURA GLOBAL:
#   lista_clientes (list[dict]) – lista de clientes em memória.
#
# FUNÇÕES PRINCIPAIS (ACESSO):
#
# carregar_clientes()
#       Lê o arquivo ARQ_CLIENTES e carrega todos os clientes para lista_clientes.
#       Formato esperado de cada linha: "nome;cpf;email\n".
#       Linhas vazias ou com número de campos diferente de 3 são ignoradas.
#       Parâmetros:
#           nenhum.
#       Efeitos colaterais:
#           - sobrescreve a lista global lista_clientes.
#       Retorno:
#           SUCESSO (0) – se o arquivo foi aberto e processado (mesmo que vazio).
#           ERRO    (1) – se o arquivo não puder ser aberto (ex.: não existe / permissão negada).
#
# salvar_clientes()
#       Grava o conteúdo de lista_clientes no arquivo ARQ_CLIENTES.
#       Cada cliente é gravado em uma linha no formato "nome;cpf;email".
#       Parâmetros:
#           nenhum.
#       Efeitos colaterais:
#           - sobrescreve o arquivo ARQ_CLIENTES.
#       Retorno:
#           SUCESSO (0) – se conseguiu abrir e escrever o arquivo.
#           ERRO    (1) – se não conseguiu abrir/gravar o arquivo.
#
# buscar_cliente_por_cpf(cpf)
#       Procura um cliente pelo CPF dentro de lista_clientes.
#       Parâmetros:
#           cpf (str) – CPF a buscar (string exatamente igual à armazenada).
#       Retorno:
#           (int) índice do cliente na lista_clientes, se encontrado.
#           -1   – se não houver cliente com esse CPF.
#
# cadastrar_cliente(nome, cpf, email)
#       Cadastra um novo cliente na lista em memória.
#       Regras:
#           - remove espaços extras nas extremidades dos campos
#           - não permite campos vazios
#           - valida CPF usando validacao.validaCPF
#           - valida email usando validacao.validaEmail
#           - não permite CPF repetido (usa buscar_cliente_por_cpf)
#       Parâmetros:
#           nome  (str) – nome do cliente.
#           cpf   (str) – CPF em qualquer formato (com ou sem pontuação).
#           email (str) – email do cliente.
#       Efeitos colaterais:
#           - insere um novo dicionário em lista_clientes caso o cadastro seja aceito.
#       Retorno:
#           SUCESSO            (0) – se o cliente foi cadastrado com sucesso.
#           CPF_JA_CADASTRADO  (5) – se o CPF já existe em lista_clientes.
#           ERRO               (1) – se algum campo é vazio ou inválido (CPF/email).
#
# listar_clientes()
#       Imprime todos os clientes cadastrados na tela, com índice, nome, CPF e email.
#       Parâmetros:
#           nenhum.
#       Efeitos colaterais:
#           - escreve na saída padrão (print).
#       Retorno:
#           SUCESSO (0) – se houver pelo menos um cliente e a listagem foi exibida.
#           ERRO    (1) – se lista_clientes estiver vazia.
#
# atualizar_cliente(indice, nome=None, email=None)
#       Atualiza os dados de um cliente já cadastrado, identificado pelo índice.
#       É possível atualizar apenas o nome, apenas o email ou ambos.
#       Regras:
#           - índice deve ser válido (0 <= indice < len(lista_clientes))
#           - nome novo, se fornecido, não pode ser vazio
#           - email novo, se fornecido, deve ser válido (validacao.validaEmail)
#           - se nenhum campo for alterado, a operação é considerada erro
#       Parâmetros:
#           indice (int) – posição do cliente em lista_clientes.
#           nome   (str | None) – novo nome (opcional).
#           email  (str | None) – novo email (opcional).
#       Efeitos colaterais:
#           - modifica o dicionário do cliente em lista_clientes, se os dados forem válidos.
#       Retorno:
#           SUCESSO               (0) – se ao menos um campo foi atualizado.
#           CLIENTE_NAO_ENCONTRADO (2) – se o índice for inválido.
#           ERRO                  (1) – se os parâmetros não resultarem em nenhuma alteração
#                                      válida (ex.: todos None ou email inválido).
#
# deletar_cliente(indice)
#       Remove um cliente de lista_clientes, identificado pelo índice.
#       Parâmetros:
#           indice (int) – posição do cliente em lista_clientes.
#       Efeitos colaterais:
#           - remove a entrada correspondente da lista global lista_clientes.
#       Retorno:
#           SUCESSO               (0) – se o cliente foi removido.
#           CLIENTE_NAO_ENCONTRADO (2) – se o índice é inválido (negativo ou >= len(lista_clientes)).

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
