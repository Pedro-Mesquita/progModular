import os

caminho_arquivo_multas = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'multas.txt')
delimitador = ","

TIPOS_MULTA = {"avaria", "prazo"}
STATUS_MULTA = {"aberto", "pago"}

multas = []

def valida_tipo(tipo):
    if tipo not in TIPOS_MULTA:
        raise ValueError(f"Tipo inválido. Os valores permitidos são: {TIPOS_MULTA}")

def valida_status(status):
    if status not in STATUS_MULTA:
        raise ValueError(f"Status inválido. Os valores permitidos são: {STATUS_MULTA}")

def carrega_multas(caminho_arquivo=caminho_arquivo_multas):

    global multas
    multas = [] 
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(delimitador)
                multa = {
                    "pk_id_multa": int(partes[0]),
                    "valor": float(partes[1]),
                    "data": partes[2],
                    "fk_id_emprestimo": int(partes[3]),
                    "tipo": partes[4],
                    "data_geracao": partes[5],
                    "status": partes[6],
                }
                multas.append(multa)


def salva_multas(caminho_arquivo=caminho_arquivo_multas):
    with open(caminho_arquivo, "w") as arquivo:
        for multa in multas:
            linha = f"{multa['pk_id_multa']}{delimitador}{multa['valor']:.2f}{delimitador}{multa['data']}{delimitador}{multa['fk_id_emprestimo']}{delimitador}{multa['tipo']}{delimitador}{multa['data_geracao']}{delimitador}{multa['status']}\n"
            arquivo.write(linha)


def gerar_multa(pk_id_multa, valor, data, fk_id_emprestimo, tipo, data_geracao, status):
    valida_tipo(tipo)
    valida_status(status)
    
    multa = {
        "pk_id_multa": pk_id_multa,
        "valor": valor,
        "data": data,
        "fk_id_emprestimo": fk_id_emprestimo,
        "tipo": tipo,
        "data_geracao": data_geracao,
        "status": status,
    }
    multas.append(multa)


def visualizar_multa(pk_id_multa):
    for multa in multas:
        if multa["pk_id_multa"] == pk_id_multa:
            return multa
    return None


def encerrar_multa(pk_id_multa):
    for multa in multas:
        if multa["pk_id_multa"] == pk_id_multa:
            multa["status"] = "pago"
            break


def pagar_multa(pk_id_multa):
    multa = visualizar_multa(pk_id_multa)
    if multa:
        if multa["status"] == "aberto":
            print(f"Multa de ID {pk_id_multa} paga com sucesso!")
            encerrar_multa(pk_id_multa)
        else:
            print(f"A multa de ID {pk_id_multa} já está paga.")
    else:
        print(f"Multa de ID {pk_id_multa} não encontrada.")


