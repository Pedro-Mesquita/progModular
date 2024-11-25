import os
import os
from datetime import datetime

caminho_arquivo_multas = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'multas.txt')

delimitador = ","

TIPOS_MULTA = {"avaria", "prazo"}
STATUS_MULTA = {"aberto", "pago"}

def carrega_multas(caminho_arquivo=caminho_arquivo_multas):
    multas = {}
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(delimitador)
                pk_id_multa = int(partes[0])
                
                multa = {
                    "pk_id_multa": pk_id_multa,
                    "valor": float(partes[1]),
                    "data": partes[2],
                    "fk_id_emprestimo": int(partes[3]),
                    "tipo": partes[4],
                    "data_geracao": partes[5],
                    "status": partes[6],
                }
                
                multas[pk_id_multa] = multa
    
    return multas


def valida_tipo(tipo):
    if tipo not in TIPOS_MULTA:
        raise ValueError(f"Tipo inválido. Os valores permitidos são: {TIPOS_MULTA}")

def valida_status(status):
    if status not in STATUS_MULTA:
        raise ValueError(f"Status inválido. Os valores permitidos são: {STATUS_MULTA}")


def gerar_multa(pk_id_multa, valor, data, fk_id_emprestimo, tipo, data_geracao, status, caminho_arquivo=caminho_arquivo_multas):
    valida_tipo(tipo)
    valida_status(status)
    
    multa = f"{pk_id_multa}{delimitador}{valor:.2f}{delimitador}{data}{delimitador}{fk_id_emprestimo}{delimitador}{tipo}{delimitador}{data_geracao}{delimitador}{status}\n"
    
    with open(caminho_arquivo, "a") as arquivo:
        arquivo.write(multa)


def visualizar_multa(pk_id_multa, caminho_arquivo=caminho_arquivo_multas):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(delimitador)
                if int(partes[0]) == pk_id_multa:
                    return {
                        "pk_id_multa": int(partes[0]),
                        "valor": float(partes[1]),
                        "data": partes[2],
                        "fk_id_emprestimo": int(partes[3]),
                        "tipo": partes[4],
                        "data_geracao": partes[5],
                        "status": partes[6]
                    }


def encerrar_multa(pk_id_multa, caminho_arquivo=caminho_arquivo_multas):
    if os.path.exists(caminho_arquivo):
        multas_atualizadas = []
        with open(caminho_arquivo, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(delimitador)
                if int(partes[0]) == pk_id_multa:
                    partes[6] = "pago"  # Update status to 'pago'
                multas_atualizadas.append(delimitador.join(partes))
        
        with open(caminho_arquivo, "w") as arquivo:
            for multa in multas_atualizadas:
                arquivo.write(multa + "\n")

def pagar_multa(pk_id_multa, caminho_arquivo=caminho_arquivo_multas):
    multa = visualizar_multa(pk_id_multa, caminho_arquivo)
    if multa:
        if multa["status"] == "aberto":
            print(f"Multa de ID {pk_id_multa} paga com sucesso!")
            encerrar_multa(pk_id_multa, caminho_arquivo)
        else:
            print(f"A multa de ID {pk_id_multa} já está paga.")
    else:
        print(f"Multa de ID {pk_id_multa} não encontrada.")

