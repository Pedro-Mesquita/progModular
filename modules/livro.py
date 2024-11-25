import os
import random
from datetime import datetime

ARQUIVO = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'livros.txt')


livros_db = []

def inicializar_arquivo():
    global livros_db
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) > 1:  
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
                        print(f"Erro na linha: '{linha.strip()}'. Número de campos inválido.")
            else:
                print("Arquivo está vazio, criando novo arquivo.")
    else:
        with open(ARQUIVO, 'w') as arquivo:
            arquivo.write("id,titulo,autor,editora,ano_publicacao,qtd_copias\n")



def carregar_dados():
    global livros_db
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
            next(arquivo)  
            for linha in arquivo:
                try:
                    dados = linha.strip().split(',')
                    if len(dados) >= 7:  
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
                except (ValueError, IndexError) as e:
                    print(f"Erro ao ler linha do arquivo: {linha.strip()}. Erro: {e}")
            
            print(f"Dados carregados com sucesso. Total de livros: {len(livros_db)}")
    
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
    print("\n=== CADASTRO DE LIVRO ===")
    try:
        titulo = input("Digite o título do livro: ").strip()
        if not titulo:
            raise ValueError("Título não pode estar vazio")
        
        autor = input("Digite o autor do livro: ").strip()
        if not autor:
            raise ValueError("Autor não pode estar vazio")
        
        editora = input("Digite a editora do livro: ").strip()
        if not editora:
            raise ValueError("Editora não pode estar vazia")
        
        try:
            ano_publicacao = int(input("Digite o ano de publicação: "))
            ano_publicacao = validar_ano(ano_publicacao)
        except ValueError as e:
            raise ValueError(f"Ano inválido: {e}")
        
        try:
            qtd_copias = int(input("Digite a quantidade de cópias: "))
            qtd_copias = validar_quantidade(qtd_copias)
        except ValueError as e:
            raise ValueError(f"Quantidade inválida: {e}")
        
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
        print(f"\nLivro cadastrado com sucesso! ID: {pk_id_livro}")
        
    except Exception as e:
        print(f"\nErro ao cadastrar livro: {e}")

def listar_livros():
    print("\n=== LISTA DE LIVROS ===")
    if not livros_db:
        print("\nNenhum livro cadastrado no sistema.")
        return [] 
    
    print(f"\nTotal de livros cadastrados: {len(livros_db)}")
    
    for livro in livros_db:
        try:
            print("\n" + "="*50)
            print(f"ID: {livro['pk_id_livro']}")
            print(f"Título: {livro['titulo']}")
            print(f"Autor: {livro['autor']}")
            print(f"Editora: {livro['editora']}")
            print(f"Ano: {livro['ano_publicacao']}")
            print(f"Quantidade: {livro['qtd_copias']}")
            print(f"Data de Cadastro: {livro['data_cadastro']}")
            print("="*50)
        except KeyError as e:
            print(f"Erro ao exibir livro: dados inconsistentes. Erro: {e}")
    
    return livros_db  

def buscar_livros():
    print("\n=== BUSCA DE LIVROS ===")
    campos_validos = ['titulo', 'autor', 'editora']
    
    print("\nCampos disponíveis para busca:")
    for campo in campos_validos:
        print(f"- {campo}")
    
    campo = input("\nDigite o campo de busca: ").lower().strip()
    if campo not in campos_validos:
        print("Campo de busca inválido!")
        return
    
    valor = input("Digite o valor de busca: ").strip()
    if not valor:
        print("Valor de busca não pode estar vazio!")
        return
    
    livros_encontrados = [
        livro for livro in livros_db
        if str(valor).lower() in str(livro[campo]).lower()
    ]
    
    if not livros_encontrados:
        print("\nNenhum livro encontrado com os critérios especificados.")
        return
    
    print(f"\nForam encontrados {len(livros_encontrados)} livro(s):")
    
    for livro in livros_encontrados:
        print("\n" + "="*50)
        print(f"ID: {livro['pk_id_livro']}")
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Editora: {livro['editora']}")
        print(f"Ano: {livro['ano_publicacao']}")
        print(f"Quantidade: {livro['qtd_copias']}")
        print(f"Data de Cadastro: {livro['data_cadastro']}")
        print("="*50)

def atualizar_livro():
    global livros_db
    print("\n=== ATUALIZAÇÃO DE LIVRO ===")
    
    listar_livros()
    if not livros_db:
        return
    
    try:
        pk_id_livro = int(input("\nDigite o ID do livro a ser atualizado (0 para cancelar): "))
        if pk_id_livro == 0:
            print("Operação cancelada!")
            return
        
        livro = next((l for l in livros_db if l['pk_id_livro'] == pk_id_livro), None)
        if not livro:
            print(f"Livro com ID {pk_id_livro} não encontrado!")
            return
        
        print("\nDados atuais do livro:")
        print("="*50)
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Editora: {livro['editora']}")
        print(f"Ano: {livro['ano_publicacao']}")
        print(f"Quantidade: {livro['qtd_copias']}")
        print("="*50)
        
        print("\nDeixe em branco para manter o valor atual")
        
        novo_titulo = input("Novo título: ").strip()
        novo_autor = input("Novo autor: ").strip()
        nova_editora = input("Nova editora: ").strip()
        
        if novo_titulo:
            livro['titulo'] = novo_titulo
        if novo_autor:
            livro['autor'] = novo_autor
        if nova_editora:
            livro['editora'] = nova_editora
        
        try:
            novo_ano = input("Novo ano de publicação (deixe em branco para manter): ")
            if novo_ano:
                livro['ano_publicacao'] = validar_ano(int(novo_ano))
            
            nova_qtd = input("Nova quantidade de cópias (deixe em branco para manter): ")
            if nova_qtd:
                livro['qtd_copias'] = validar_quantidade(int(nova_qtd))
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
        
        livro['data_cadastro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\nLivro atualizado com sucesso!")
    
    except ValueError as e:
        print(f"Erro ao atualizar livro: {e}")

def remover_livro():
    global livros_db
    print("\n=== REMOÇÃO DE LIVRO ===")
    listar_livros()
    
    try:
        pk_id_livro = int(input("\nDigite o ID do livro a ser removido (0 para cancelar): "))
        if pk_id_livro == 0:
            print("Operação cancelada!")
            return
        
        livro = next((l for l in livros_db if l['pk_id_livro'] == pk_id_livro), None)
        if livro:
            livros_db.remove(livro)
            print("\nLivro removido com sucesso!")
        else:
            print("\nLivro não encontrado!")
    except ValueError:
        print("\nID inválido!")


def verificar_quantidade():
    print("\n=== VERIFICAÇÃO DE QUANTIDADE ===")
    
    try:
        pk_id_livro = int(input("Digite o ID do livro: "))
        livro = next((l for l in livros_db if l['pk_id_livro'] == pk_id_livro), None)
        
        if livro:
            print("\nInformações do livro:")
            print("="*50)
            print(f"Título: {livro['titulo']}")
            print(f"Autor: {livro['autor']}")
            print(f"Quantidade disponível: {livro['qtd_copias']}")
            print("="*50)
        else:
            print(f"\nLivro com ID {pk_id_livro} não encontrado!")
            
    except ValueError:
        print("\nErro: ID deve ser um número!")

def salvar_dados():
    try:
        with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
            arquivo.write("id,titulo,autor,editora,ano_publicacao,qtd_copias,data_cadastro\n")
            for livro in livros_db:
                arquivo.write(f"{livro['pk_id_livro']},{livro['titulo']},{livro['autor']},{livro['editora']},"
                               f"{livro['ano_publicacao']},{livro['qtd_copias']},{livro['data_cadastro']}\n")
            print("\nDados salvos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def menu_principal():
    inicializar_arquivo()

    while True:
        print("\n=== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ===")
        print("\n1. Cadastrar livro")
        print("2. Listar livros")
        print("3. Buscar livro")
        print("4. Atualizar livro")
        print("5. Remover livro")
        print("6. Verificar quantidade")
        print("7. Sair")
        print("\nTotal de livros cadastrados:", len(livros_db))

        try:
            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == '1':
                cadastrar_livro()
            elif opcao == '2':
                listar_livros()
            elif opcao == '3':
                buscar_livros()
            elif opcao == '4':
                atualizar_livro()
            elif opcao == '5':
                remover_livro()
            elif opcao == '6':
                verificar_quantidade()
            elif opcao == '7':
                print("\nSalvando dados e encerrando o programa...")
                salvar_dados()
                print("Programa encerrado.")
                break
            else:
                print("\nOpção inválida! Por favor, escolha uma opção válida.")

        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário.")
            salvar_dados() 
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")

if __name__ == "__main__":
    menu_principal()
