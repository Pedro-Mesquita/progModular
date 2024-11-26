# tests/test_usuarios.py
import sys
import os
import pytest

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.usuarios import (
    cadastrar_usuario, 
    buscar_usuario, 
    editar_usuario, 
    excluir_usuario, 
    listar_usuarios,
    carregar_usuarios,
    salvar_usuarios
)

def setup_module(module):
    carregar_usuarios()

def teardown_module(module):
    salvar_usuarios()

def test_cadastrar_usuario():
    usuarios = listar_usuarios()
    
    # Cadastra um novo usuário
    resultado = cadastrar_usuario(
        nome="João da Silva", 
        endereco="Rua Principal, 123",
        telefone="21999999999", 
        email="joao.silva@gmail.com"
    )
    
    # Verifica se o usuário foi cadastrado
    usuarios_atualizados = listar_usuarios()

def test_buscar_usuario():
    """Teste de busca de usuário"""
    # Cadastra um usuário para buscar
    cadastrar_usuario(
        nome="Maria Souza", 
        endereco="Avenida Secundária, 456",
        telefone="21888888888", 
        email="maria.souza@exemplo.com"
    )
    
    # Busca o usuário cadastrado
    usuario = buscar_usuario("Maria Souza")
    
    assert usuario is not None, "Usuário não encontrado"
    assert usuario['nome'] == "Maria Souza", "Nome do usuário não corresponde"

def test_editar_usuario():
    """Teste de edição de usuário"""
    # Cadastra um usuário para editar
    cadastrar_usuario(
        nome="Pedro Santos", 
        endereco="Travessa Central, 789",
        telefone="31777777777", 
        email="pedro.santos@exemplo.com"
    )
    
    # Busca o usuário
    usuario = buscar_usuario("Pedro Santos")
    
    # Edita o usuário
    resultado = editar_usuario(
        id_usuario=usuario['id'], 
        nome="Pedro Silva", 
        endereco="Travessa Central, 790",
        telefone="31777778888", 
        email="pedro.silva@exemplo.com"
        
    )
    
    assert resultado is True, "Falha ao editar usuário"
    
    # Verifica se a edição foi realizada
    usuario_editado = buscar_usuario("Pedro Silva")
    assert usuario_editado is not None, "Usuário editado não encontrado"
    assert usuario_editado['telefone'] == "31777778888", "Telefone não foi atualizado corretamente"

def test_excluir_usuario():
    """Teste de exclusão de usuário"""
    # Cadastra um usuário para excluir
    cadastrar_usuario(
        nome="Ana Oliveira", 
        endereco="Praça Principal, 321",
        telefone="41666666666", 
        email="ana.oliveira@exemplo.com"
    )
    
    # Busca o usuário
    usuario = buscar_usuario("Ana Oliveira")
    
    # Exclui o usuário
    resultado = excluir_usuario(id_usuario=usuario['id'])
    
    assert resultado is True, "Falha ao excluir usuário"
    
    # Verifica se o usuário foi removido
    usuario_excluido = buscar_usuario("Ana Oliveira")
    assert usuario_excluido is None, "Usuário não foi removido"

def test_lista_usuarios():
    """Teste de listagem de usuários"""
    # Limpa usuários existentes
    while True:
        usuarios = listar_usuarios()
        if not usuarios:
            break
        excluir_usuario(usuarios[0]['id'])
    
    # Cadastra alguns usuários
    cadastrar_usuario(nome="Usuario 1", email="usuario1@exemplo.com", telefone="1111", endereco="Endereco 1")
    cadastrar_usuario(nome="Usuario 2", email="usuario2@exemplo.com", telefone="2222", endereco="Endereco 2")
    
    # Lista usuários
    usuarios = listar_usuarios()
    
    assert len(usuarios) == 2, "Número de usuários não corresponde ao esperado"
    assert usuarios[0]['nome'] == "Usuario 1", "Primeiro usuário não corresponde"
    assert usuarios[1]['nome'] == "Usuario 2", "Segundo usuário não corresponde"