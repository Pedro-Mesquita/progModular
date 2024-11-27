# Estrutura de diretórios:
# biblioteca/
# ├── teste.py
# ├── conf_testes.py
# ├── data/
# │   ├── usuarios.txt
# │   ├── livros.txt
# │   ├── emprestimos.txt
# │   └── multas.txt
# ├── modules/
# │   ├── usuarios.py
# │   ├── livros.py
# │   ├── emprestimos.py
# │   ├── multas.py
# │   └── utf_converter.py
# ├── tests/
# │   ├── test_usuarios.py
# │   ├── test_livros.py
# │   ├── test_emprestimos.py
# │   └── test_multas.py




# bibliotecas
import os
import random
from datetime import datetime


from modules.multa import *
from modules.usuarios import *
from modules.emprestimo import *
from modules.livro import *
from modules.utf_converter import *


def converter_encoding(arquivo_entrada, arquivo_saida, origem='utf8', destino='utf32'):
    if origem == 'utf8' and destino == 'utf32':
        conv_utf8_to_utf32(arquivo_entrada, arquivo_saida)
    elif origem == 'utf32' and destino == 'utf8':
        conv_utf32_to_utf8(arquivo_entrada, arquivo_saida)
    else:
        raise ValueError("Conversão não suportada")


def backup_sistema():
    arquivos = ['usuarios.txt', 'emprestimos.txt', 'multas.txt', 'livros.txt']
    for arquivo in arquivos:
        input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'progModular/data', arquivo)
        backup_nome = f"backup_{arquivo}.utf32"
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'progModular/data', backup_nome)
        conv_utf8_to_utf32(input_path, output_path)
        print(f"Backup criado: {backup_nome}")

def restaurar_backup():
    arquivos = ['usuarios.txt', 'emprestimos.txt', 'multas.txt', 'livros.txt']
    for arquivo in arquivos:
        backup_nome = f"backup_{arquivo}.utf32"
        input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'progModular/data', backup_nome)
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'progModular/data', arquivo)
        if os.path.exists(input_path):
            conv_utf32_to_utf8(input_path, output_path)
            print(f"Arquivo restaurado: {arquivo}")
        else:
            print(f"Backup não encontrado: {backup_nome}")




# Menus do sistema
def menu_usuarios():
    while True:
        print("\n=== Gestão de Usuários ===")
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Buscar Usuário")
        print("4. Editar Usuário")
        print("5. Excluir Usuário")
        print("6. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            buscar_usuario()
        elif opcao == '4':
            editar_usuario()
        elif opcao == '5':
            excluir_usuario()
        elif opcao == '6':
            break
        else:
            print("Opção inválida!")

def menu_livros():
    while True:
        print("\n=== Gestão de Livros ===")
        print("1. Cadastrar Livro")
        print("2. Listar Livros")
        print("3. Buscar Livro")
        print("4. Atualizar Livro")
        print("5. Remover Livro")
        print("6. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            cadastrar_livro()
            print("Livro cadastrado com sucesso!")
        
        elif opcao == '2':
            listar_livros()

        elif opcao == '3':
            buscar_livros()
        
        elif opcao == '4':
            atualizar_livro()
            print("Livro atualizado com sucesso!")
        
        elif opcao == '5':
            remover_livro()
            print("Livro removido com sucesso!")
        
        elif opcao == '6':
            break
        else:
            print("Opção inválida!")

def menu_emprestimos():
    while True:
        print("\n=== Gestão de Empréstimos ===")
        print("1. Criar Empréstimo")
        print("2. Listar Empréstimos")
        print("3. Finalizar Empréstimo")
        print("4. Excluir Empréstimo")
        print("5. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            try:
                data_atual = datetime.now().strftime("%Y-%m-%d")
                pk_id_emprestimo = random.randint(1000, 9999)
                fk_id_livro = int(input("ID do livro: "))
                fk_id_usuario = int(input("ID do usuário: "))
                data_devolucao = input("Data de devolução prevista (AAAA-MM-DD): ")
                
                if criaEmprestimo(pk_id_emprestimo, data_atual,"None", data_devolucao, fk_id_livro, fk_id_usuario):
                    print("Empréstimo realizado com sucesso!")
            except ValueError:
                print("Erro: Dados inválidos fornecidos")
            
        
        elif opcao == '2':
            listaEmprestimos()
        
        elif opcao == '3':
            pk_id_emprestimo = int(input("ID do empréstimo: "))
            acabaEmprestimo(pk_id_emprestimo)
            print("Empréstimo finalizado!")
        
        elif opcao == '4':
            pk_id_emprestimo = int(input("ID do empréstimo: "))
            excluiEmprestimo(pk_id_emprestimo)
            print("Empréstimo excluído!")
        
        elif opcao == '5':
            break
        else:
            print("Opção inválida!")

def menu_multas():
    while True:
        print("\n=== Gestão de Multas ===")
        print("1. Gerar Multa")
        print("2. Visualizar Multa")
        print("3. Pagar Multa")
        print("4. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            pk_id_multa = random.randint(1000, 9999)
            valor = float(input("Valor da multa: "))
            data = datetime.now().strftime("%Y-%m-%d")
            fk_id_emprestimo = int(input("ID do empréstimo: "))
            tipo = input("Tipo (avaria/prazo): ")
            data_geracao = datetime.now().strftime("%Y-%m-%d")
            status = "aberto"
            
            try:
                gerar_multa(pk_id_multa, valor, data, fk_id_emprestimo, 
                           tipo, data_geracao, status)
                print("Multa gerada com sucesso!")
            except ValueError as e:
                print(f"Erro: {e}")
        
        elif opcao == '2':
            pk_id_multa = int(input("ID da multa: "))
            multa = visualizar_multa(pk_id_multa)
            if multa:
                print("\nDetalhes da multa:")
                for key, value in multa.items():
                    print(f"{key}: {value}")
            else:
                print("Multa não encontrada!")
        
        elif opcao == '3':
            pk_id_multa = int(input("ID da multa: "))
            pagar_multa(pk_id_multa)
        
        elif opcao == '4':
            break
        else:
            print("Opção inválida!")

def menu_principal():
    
    carregar_usuarios()
    inicializar_arquivo()  
    carrega_emprestimos()
    carrega_multas()
    
    while True:
        print("\n=== Sistema de Biblioteca ===")
        print("1. Gestão de Usuários")
        print("2. Gestão de Livros")
        print("3. Gestão de Empréstimos")
        print("4. Gestão de Multas")
        print("5. Criar Backup (UTF-32)")
        print("6. Restaurar Backup")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            menu_usuarios()
        elif opcao == '2':
            menu_livros()
        elif opcao == '3':
            menu_emprestimos()
        elif opcao == '4':
            menu_multas()
        elif opcao == '5':
            backup_sistema()
        elif opcao == '6':
            restaurar_backup()
        elif opcao == '7':
            print("Finalizando sistema...")
            salvar_usuarios()
            salvar_dados() #livros
            salva_emprestimos()
            salva_multas()

            print("Dados salvos. Sistema finalizado.")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
