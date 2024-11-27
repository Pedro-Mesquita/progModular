import os
from datetime import datetime

caminho_arquivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'emprestimos.txt')
delimitador = ","
emprestimos = {}


def carrega_emprestimos():
    """Carrega os empréstimos do arquivo TXT para o dicionário global."""
    global emprestimos
    emprestimos = {}

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(delimitador)
                emprestimo = {
                    "pk_id_emprestimo": int(partes[0]),
                    "data_emprestimo": partes[1],
                    "data_devolucao_real": partes[2] if partes[2] != "None" else None,
                    "data_devolucao_prevista": partes[3],
                    "fk_id_livro": int(partes[4]),
                    "fk_id_usuario": int(partes[5]),
                }
                emprestimos[emprestimo["pk_id_emprestimo"]] = emprestimo
    return emprestimos


def lista_emprestimos():
    for emprestimo in emprestimos.values():
        print(f"ID: {emprestimo['pk_id_emprestimo']}")
        print(f"Data Emprestimo: {emprestimo['data_emprestimo']}")
        print(f"Data Devolucao Real: {emprestimo['data_devolucao_real']}")
        print(f"Data Devolucao Prevista: {emprestimo['data_devolucao_prevista']}")
        print(f"ID Livro: {emprestimo['fk_id_livro']}")
        print(f"ID Usuario: {emprestimo['fk_id_usuario']}")
        print("----------")



def cria_emprestimo(pk_id_emprestimo, data_emprestimo, data_devolucao_real, data_devolucao_prevista, fk_id_livro, fk_id_usuario):
    """Cria um novo empréstimo e o adiciona ao dicionário."""
    if pk_id_emprestimo in emprestimos:
        raise ValueError("Já existe um empréstimo com esse ID.")
    novo_emprestimo = {
        "pk_id_emprestimo": pk_id_emprestimo,
        "data_emprestimo": data_emprestimo,
        "data_devolucao_real": data_devolucao_real,
        "data_devolucao_prevista": data_devolucao_prevista,
        "fk_id_livro": fk_id_livro,
        "fk_id_usuario": fk_id_usuario,
    }
    emprestimos[pk_id_emprestimo] = novo_emprestimo


def exclui_emprestimo(pk_id_emprestimo):
    """Remove um empréstimo do dicionário."""
    if pk_id_emprestimo in emprestimos:
        del emprestimos[pk_id_emprestimo]
    else:
        raise ValueError("Empréstimo não encontrado.")


def acaba_emprestimo(pk_id_emprestimo):
    """Finaliza um empréstimo ao registrar a data de devolução real."""
    if pk_id_emprestimo in emprestimos:
        emprestimos[pk_id_emprestimo]["data_devolucao_real"] = datetime.now().strftime("%Y-%m-%d")
    else:
        raise ValueError("Empréstimo não encontrado.")


def salva_emprestimos():
    """Persiste os empréstimos do dicionário em memória para o arquivo TXT."""
    with open(caminho_arquivo, "w") as arquivo:
        for emprestimo in emprestimos.values():
            linha = f"{emprestimo['pk_id_emprestimo']},{emprestimo['data_emprestimo']},{emprestimo['data_devolucao_real']},{emprestimo['data_devolucao_prevista']},{emprestimo['fk_id_livro']},{emprestimo['fk_id_usuario']}\n"
            arquivo.write(linha)
