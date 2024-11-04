import os

caminho_arquivo = "emprestimos.txt"
delimitador = ","


def carrega_emprestimos():
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
                    "fk_id_usuario": int(partes[5])
                }
                
                emprestimos[emprestimo["pk_id_emprestimo"]] = emprestimo
    return emprestimos

def listaEmprestimos(emprestimos):
    for emprestimo in emprestimos.values():
        print(f"ID: {emprestimo['pk_id_emprestimo']}")
        print(f"Data Emprestimo: {emprestimo['data_emprestimo']}")
        print(f"Data Devolucao Real: {emprestimo['data_devolucao_real']}")
        print(f"Data Devolucao Prevista: {emprestimo['data_devolucao_prevista']}")
        print(f"ID Livro: {emprestimo['fk_id_livro']}")
        print(f"ID Usuario: {emprestimo['fk_id_usuario']}")
        print("-" * 10)

emprestimos = carrega_emprestimos()
listaEmprestimos(emprestimos)