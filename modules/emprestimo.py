import os
from datetime import datetime

caminho_arquivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'emprestimos.txt')
delimitador = ","
emprestimos = {}  


def carrega_emprestimos():
    global emprestimos
    emprestimos = {}
    
    # Debug: Checking if the file exists
    print(f"Checking if the file {caminho_arquivo} exists: {os.path.exists(caminho_arquivo)}")
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(delimitador)
                
                # Debug: Print each line after splitting
                print(f"Processed line: {partes}")
                
                emprestimo = {
                    "pk_id_emprestimo": int(partes[0]),
                    "data_emprestimo": partes[1],
                    "data_devolucao_real": partes[2] if partes[2] != "None" else None,
                    "data_devolucao_prevista": partes[3],
                    "fk_id_livro": int(partes[4]),
                    "fk_id_usuario": int(partes[5])
                }
                
                # Debug: Print the emprestimo object before adding
                print(f"Adding emprestimo: {emprestimo}")
                
                emprestimos[emprestimo["pk_id_emprestimo"]] = emprestimo
    
    # Debug: Print the final state of emprestimos after loading
    print(f"Global emprestimos updated: {emprestimos}")
    
    return emprestimos



def listaEmprestimos():
    for emprestimo in emprestimos.values():
        print(f"ID: {emprestimo['pk_id_emprestimo']}")
        print(f"Data Emprestimo: {emprestimo['data_emprestimo']}")
        print(f"Data Devolucao Real: {emprestimo['data_devolucao_real']}")
        print(f"Data Devolucao Prevista: {emprestimo['data_devolucao_prevista']}")
        print(f"ID Livro: {emprestimo['fk_id_livro']}")
        print(f"ID Usuario: {emprestimo['fk_id_usuario']}")
        print("-" * 10)


def criaEmprestimo(pk_id_emprestimo, data_emprestimo, data_devolucao_real, data_devolucao_prevista, fk_id_livro, fk_id_usuario):
    global emprestimos
    novo_emprestimo = {
        "pk_id_emprestimo": pk_id_emprestimo,
        "data_emprestimo": data_emprestimo,
        "data_devolucao_real": data_devolucao_real,
        "data_devolucao_prevista": data_devolucao_prevista,
        "fk_id_livro": fk_id_livro,
        "fk_id_usuario": fk_id_usuario
    }
    emprestimos[pk_id_emprestimo] = novo_emprestimo

def excluiEmprestimo(pk_id_emprestimo):
    global emprestimos
    if pk_id_emprestimo in emprestimos:
        del emprestimos[pk_id_emprestimo]


def acabaEmprestimo(pk_id_emprestimo):
    global emprestimos
    if pk_id_emprestimo in emprestimos:
        emprestimos[pk_id_emprestimo]["data_devolucao_real"] = datetime.now().strftime("%Y-%m-%d")



def salvaEmprestimos():
    with open(caminho_arquivo, "w") as arquivo:
        for emprestimo in emprestimos.values():
            linha = f"{emprestimo['pk_id_emprestimo']},{emprestimo['data_emprestimo']},{emprestimo['data_devolucao_real']},{emprestimo['data_devolucao_prevista']},{emprestimo['fk_id_livro']},{emprestimo['fk_id_usuario']}\n"
            arquivo.write(linha)
