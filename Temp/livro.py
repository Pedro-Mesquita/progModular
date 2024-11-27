import os
import random
from datetime import datetime

# Definição do caminho do arquivo
ARQUIVO = os.path.join(os.path.dirname(__file__), 'livros.txt')

livros_db = []


def inicializar_arquivo():
    global livros_db
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) > 1:  # Se houver mais que o cabeçalho
                for linha in linhas[1:]:
                    dados = linha.strip().split(',')
                    if len(dados) == 7:
                        pk_id_livro, titulo, autor, editora, ano_publicacao, qtd_copias, data = dados
                        livro = {
                            "pk_id_livro": int(pk_id_livro),
                            "titulo": titulo,
                            "autor": autor,
                            "editora": editora,
                            "ano_publicacao": int(ano_publicacao),
                            "qtd_copias": int(qtd_copias),
                            "data_cadastro": data
                        }
                        livros_db.append(livro)
            else:
                print("Arquivo vazio. Será criado ao salvar.")
    else:
        with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
            arquivo.write("id,titulo,autor,editora,ano_publicacao,qtd_copias,data_cadastro\n")


def carregar_dados():
    global livros_db
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
            next(arquivo)
            for linha in arquivo:
                dados = linha.strip().split(',')
                if len(dados) == 7:
                    livro = {
                        "pk_id_livro": int(dados[0]),
                        "titulo": dados[1],
                        "autor": dados[2],
                        "editora": dados[3],
                        "ano_publicacao": int(dados[4]),
                        "qtd_copias": int(dados[5]),
                        "data_cadastro": dados[6]
                    }
                    livros_db.append(livro)
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        exit(1)


def gerar_id_unico():
    while True:
        pk_id_livro = random.randint(1000, 9999)
        if not any(livro['pk_id_livro'] == pk_id_livro for livro in livros_db):
            return pk_id_livro


def validar_ano(ano):
    ano_atual = datetime.now().year
    if not (1000 <= ano <= ano_atual):
        raise ValueError(f"Ano deve estar entre 1000 e {ano_atual}")
    return ano


def validar_quantidade(qtd):
    if qtd < 0:
        raise ValueError("Quantidade não pode ser negativa")
    return qtd


def cadastrar_livro():
    global livros_db
    try:
        titulo = input("Digite o título do livro: ").strip()
        autor = input("Digite o autor do livro: ").strip()
        editora = input("Digite a editora do livro: ").strip()
        ano_publicacao = validar_ano(int(input("Digite o ano de publicação: ")))
        qtd_copias = validar_quantidade(int(input("Digite a quantidade de cópias: ")))
        pk_id_livro = gerar_id_unico()
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        livro = {
            "pk_id_livro": pk_id_livro,
            "titulo": titulo,
            "autor": autor,
            "editora": editora,
            "ano_publicacao": ano_publicacao,
            "qtd_copias": qtd_copias,
            "data_cadastro": data_cadastro
        }
        livros_db.append(livro)
        print("\nLivro cadastrado com sucesso!")

    except Exception as e:
        print(f"\nErro ao cadastrar livro: {e}")


def listar_livros():
    print("\n=== LISTA DE LIVROS ===")
    if not livros_db:
        print("\nNenhum livro cadastrado.")
        return

    for livro in livros_db:
        print(f"\nID: {livro['pk_id_livro']}")
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Editora: {livro['editora']}")
        print(f"Ano: {livro['ano_publicacao']}")
        print(f"Quantidade: {livro['qtd_copias']}")
        print(f"Data de Cadastro: {livro['data_cadastro']}")


def buscar_livros():
    campo = input("Digite o campo de busca (titulo, autor ou editora): ").strip()
    valor = input("Digite o valor para buscar: ").strip()
    livros_encontrados = [
        livro for livro in livros_db if valor.lower() in livro[campo].lower()
    ]

    if livros_encontrados:
        print(f"\nForam encontrados {len(livros_encontrados)} livro(s):")
        for livro in livros_encontrados:
            print(f"\nID: {livro['pk_id_livro']} | Título: {livro['titulo']}")
    else:
        print("\nNenhum livro encontrado.")


def atualizar_livro():
    listar_livros()
    try:
        pk_id_livro = int(input("Digite o ID do livro para atualizar: "))
        livro = next(l for l in livros_db if l['pk_id_livro'] == pk_id_livro)
        novo_titulo = input("Novo título (vazio para manter): ").strip()
        if novo_titulo:
            livro['titulo'] = novo_titulo
        print("\nLivro atualizado!")
    except StopIteration:
        print("Livro não encontrado.")


def salvar_dados():
    try:
        with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
            arquivo.write("id,titulo,autor,editora,ano_publicacao,qtd_copias,data_cadastro\n")
            for livro in livros_db:
                arquivo.write(f"{livro['pk_id_livro']},{livro['titulo']},{livro['autor']},{livro['editora']},"
                              f"{livro['ano_publicacao']},{livro['qtd_copias']},{livro['data_cadastro']}\n")
            print("\nDados salvos!")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


def menu_principal():
    inicializar_arquivo()
    while True:
        print("\n=== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ===")
        print("1. Cadastrar Livro\n2. Listar Livros\n3. Buscar Livros\n4. Atualizar Livro\n5. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_livro()
        elif opcao == '2':
            listar_livros()
        elif opcao == '3':
            buscar_livros()
        elif opcao == '4':
            atualizar_livro()
        elif opcao == '5':
            salvar_dados()
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_principal()
