# validacao.py
#
# Módulo responsável por validar CPF, CNPJ e email.
# Ele não acessa arquivos nem estruturas de dados globais do sistema:
# recebe uma string, verifica se está em formato válido e devolve:
#   SUCESSO (0) se for válido
#   ERRO    (1) se for inválido

SUCESSO = 0
ERRO = 1


def _so_digitos(s):
    """
    Função auxiliar: recebe uma string qualquer e devolve
    apenas os caracteres numéricos (0–9), na mesma ordem.

    Exemplo:
        _so_digitos("123.456-78A") -> "12345678"
    """
    resultado = ""
    for ch in s:
        if ch in "0123456789":
            resultado += ch
    return resultado


def validaCPF(cpf):
    """
    Verifica se um CPF é válido.

    Regras (compatíveis com o relatório):
    - aceita CPF com ou sem pontuação (usa só os dígitos)
    - precisa ter exatamente 11 dígitos
    - rejeita CPFs com todos os dígitos iguais (ex: 11111111111)
    - verifica os dois dígitos verificadores pelo algoritmo oficial

    Retorno:
        SUCESSO (0) se o CPF for válido
        ERRO    (1) caso contrário
    """
    cpf = _so_digitos(cpf)

    # Tamanho incorreto
    if len(cpf) != 11:
        return ERRO

    # Todos os dígitos iguais -> inválido
    if cpf == cpf[0] * 11:
        return ERRO

    # Cálculo do 1º dígito verificador
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1
    dv1 = (soma * 10) % 11
    if dv1 == 10:
        dv1 = 0

    # Cálculo do 2º dígito verificador
    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1
    dv2 = (soma * 10) % 11
    if dv2 == 10:
        dv2 = 0

    # Compara com os dígitos fornecidos
    if dv1 != int(cpf[9]) or dv2 != int(cpf[10]):
        return ERRO

    return SUCESSO


def validaEmail(email):
    """
    Verifica se um email tem formato básico válido.

    Regras (compatíveis com os casos do relatório):
    - remove espaços no início e no fim
    - precisa conter um '@'
    - precisa ter algo antes do '@' (parte local)
    - precisa ter algo depois do '@' (domínio)
    - o domínio precisa ter pelo menos um ponto

    Exemplos de erros:
        "usuariodominio.com"   -> sem '@'
        "usuario@"             -> sem domínio
        "@dominio.com"         -> sem parte local
        "usuario@dominio"      -> sem extensão
        "" ou "   "            -> vazio

    Retorno:
        SUCESSO (0) se for válido
        ERRO    (1) caso contrário
    """
    email = email.strip()

    # Precisa ter '@'
    if "@" not in email:
        return ERRO

    parte_local, _, dominio = email.partition("@")

    # Falta parte antes ou depois do '@'
    if not parte_local or not dominio:
        return ERRO

    # Domínio precisa ter um ponto (ex: dominio.com, empresa.com.br)
    if "." not in dominio:
        return ERRO

    return SUCESSO


def validaCNPJ(cnpj):
    """
    Verifica se um CNPJ é válido.

    Regras:
    - aceita CNPJ com ou sem pontuação (usa só os dígitos)
    - precisa ter exatamente 14 dígitos
    - rejeita CNPJs com todos os dígitos iguais
    - verifica os dois dígitos verificadores com o algoritmo oficial

    Retorno:
        SUCESSO (0) se o CNPJ for válido
        ERRO    (1) caso contrário
    """
    cnpj = _so_digitos(cnpj)

    # Tamanho incorreto
    if len(cnpj) != 14:
        return ERRO

    # Todos os dígitos iguais -> inválido
    if cnpj == cnpj[0] * 14:
        return ERRO

    # Pesos para o 1º dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for i in range(12):
        soma += int(cnpj[i]) * pesos1[i]
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto

    # Pesos para o 2º dígito verificador (começa com 6 e depois pesos1)
    pesos2 = [6] + pesos1
    soma = 0
    for i in range(13):
        soma += int(cnpj[i]) * pesos2[i]
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto

    # Compara com os dígitos fornecidos
    if dv1 != int(cnpj[12]) or dv2 != int(cnpj[13]):
        return ERRO

    return SUCESSO
