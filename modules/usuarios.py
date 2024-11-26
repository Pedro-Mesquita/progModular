import os
import re
import random

ARQUIVO_USUARIOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'usuarios.txt')


usuarios_db = []


def carregar_usuarios():
    global usuarios_db
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r') as f:
            for linha in f:
                pk_id_usuario, nome, endereco, telefone, email = linha.strip().split(';')
                usuario = {
                    "pk_id_usuario": int(pk_id_usuario),
                    "nome": nome,
                    "endereco": endereco,
                    "telefone": int(telefone),
                    "email": email
                }
                usuarios_db.append(usuario)
            print("Usuários carregados do arquivo:", usuarios_db)


def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, 'w') as f:
        for usuario in usuarios_db:
            linha = f"{usuario['pk_id_usuario']};{usuario['nome']};{usuario['endereco']};{usuario['telefone']};{usuario['email']}\n"
            f.write(linha)
        print("Usuários salvos no arquivo TXT.")

# class Usuario:
#     def __init__(self, pk_id_usuario, nome, endereco, telefone, email):
#         self.pk_id_usuario = pk_id_usuario
#         self.nome = nome
#         self.endereco = endereco
#         self.telefone = telefone
#         self.email = email

#     def to_dict(self):
#         return {
#             "pk_id_usuario": self.pk_id_usuario,
#             "nome": self.nome,
#             "endereco": self.endereco,
#             "telefone": self.telefone,
#             "email": self.email
#         }


# Função para criar um novo usuário como dicionário
def criar_usuario(pk_id_usuario, nome, endereco, telefone, email):
    return {
        "pk_id_usuario": pk_id_usuario,
        "nome": nome,
        "endereco": endereco,
        "telefone": telefone,
        "email": email
    }


def gerar_id_unico():
    while True:
        pk_id_usuario = random.randint(1000, 9999)
        if all(user['pk_id_usuario'] != pk_id_usuario for user in usuarios_db):
            return pk_id_usuario



def listar_usuarios():
    if not usuarios_db:
        print("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios_db:
            print(usuario)

def buscar_usuario():
    termo_busca = input("Digite o termo de busca (nome, endereço, email ou telefone): ").lower()
    usuarios_filtrados = [
        usuario for usuario in usuarios_db
        if termo_busca in usuario['nome'].lower() or
           termo_busca in usuario['endereco'].lower() or
           termo_busca in usuario['email'].lower() or
           termo_busca in str(usuario['telefone'])
    ]

    if usuarios_filtrados:
        for usuario in usuarios_filtrados:
            print(usuario)
    else:
        print("Nenhum usuário encontrado com o termo informado.")

def cadastrar_usuario():
    nome = input("Digite o nome do usuário: ")
    endereco = input("Digite o endereço do usuário: ")
    telefone = input("Digite o telefone do usuário: ")
    email = input("Digite o email do usuário: ")

    

    if not nome or not telefone.isdigit() or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Erro: Parâmetro inválido.")
        return

    pk_id_usuario = gerar_id_unico()
    usuario = criar_usuario(pk_id_usuario, nome, endereco, int(telefone), email)
    # usuarios_db.append(usuario.to_dict())
    usuarios_db.append(usuario)
    print("Usuário cadastrado com sucesso!")

def editar_usuario():
    pk_id_usuario = int(input("Digite o ID do usuário a ser editado: "))
    usuario = next((u for u in usuarios_db if u['pk_id_usuario'] == pk_id_usuario), None)

    if usuario:
        print("Pressione enter para manter o valor atual")
        nome = input(f"Digite o novo nome (atual: {usuario['nome']}): ") or usuario['nome']
        endereco = input(f"Digite o novo endereço (atual: {usuario['endereco']}): ") or usuario['endereco']
        telefone = input(f"Digite o novo telefone (atual: {usuario['telefone']}): ") or usuario['telefone']
        email = input(f"Digite o novo email (atual: {usuario['email']}): ") or usuario['email']

        usuario.update({
            'nome': nome,
            'endereco': endereco,
            'telefone': int(telefone),
            'email': email
        })
        print("Usuário atualizado com sucesso!")
    else:
        print("Usuário não encontrado.")

def excluir_usuario():
    pk_id_usuario = int(input("Digite o ID do usuário a ser excluído: "))
    global usuarios_db
    usuarios_db = [usuario for usuario in usuarios_db if usuario['pk_id_usuario'] != pk_id_usuario]
    print(f"Usuário com ID={pk_id_usuario} excluído.")

def ver_informacoes_usuario():
    pk_id_usuario = int(input("Digite o ID do usuário: "))
    usuario = next((u for u in usuarios_db if u['pk_id_usuario'] == pk_id_usuario), None)

    if usuario:
        print("Informações do usuário:")
        print(f"ID: {usuario['pk_id_usuario']}")
        print(f"Nome: {usuario['nome']}")
        print(f"Endereço: {usuario['endereco']}")
        print(f"Telefone: {usuario['telefone']}")
        print(f"Email: {usuario['email']}")
    else:
        print("Usuário não encontrado.")

def finalizar_sessao():
    salvar_usuarios()
    print("Sessão finalizada e dados salvos.")

# Função de menu principal
def menu_principal():
    carregar_usuarios()
    while True:
        print("\n--- Menu Principal ---\n")
        print("1. Cadastrar um usuário")
        print("2. Excluir um usuário")
        print("3. Buscar um usuário")
        print("4. Exibir a lista de todos os usuários")
        print("5. Ver todas as informações de um usuário")
        print("6. Editar um usuário")
        print("7. Finalizar sessão e salvar dados")
        print("\n")
        opcao = input("Escolha uma opção: ")
        print("\n")

        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            excluir_usuario()
        elif opcao == '3':
            buscar_usuario()
        elif opcao == '4':
            listar_usuarios()
        elif opcao == '5':
            ver_informacoes_usuario()
        elif opcao == '6':
            editar_usuario()
        elif opcao == '7':
            finalizar_sessao()
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
    menu_principal()