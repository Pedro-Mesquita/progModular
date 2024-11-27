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
    
def test_editar_usuario():
    """Teste de edição de usuário"""
    cadastrar_usuario(
        nome="Pedro Santos",
        endereco="Travessa Central, 789",
        telefone="31777777777",
        email="pedro.santos@exemplo.com"
    )
    
    # Buscar usuário
    usuarios = buscar_usuario("Pedro Santos")
    
    usuarios[0] = editar_usuario(
            pk_id_usuario=usuarios[0]['pk_id_usuario'],
            nome="Pedro Silva",
            endereco="Travessa Central, 790",
            telefone="31777778888",
            email="pedro.silva@exemplo.com"
        )

    # Validar edição
    usuario_editado = buscar_usuario("Pedro Silva")
    

def test_excluir_usuario():
    """Teste de exclusão de múltiplos usuários"""
    # Cadastra dois usuários com nomes semelhantes para teste
    cadastrar_usuario(
        nome="Ana Oliveira",
        endereco="Praça Principal, 321",
        telefone="41666666666",
        email="ana.oliveira@exemplo.com"
    )
    cadastrar_usuario(
        nome="Ana Carolina Oliveira",
        endereco="Rua Secundária, 123",
        telefone="41777777777",
        email="ana.carolina@exemplo.com"
    )

    # Busca todos os usuários com o nome "Ana"
    usuarios = buscar_usuario("Ana Carolina")
    assert usuarios, "Nenhum usuário encontrado para exclusão"
    
    for usuario in usuarios:
        excluir_usuario(pk_id_usuario=usuario['pk_id_usuario'])

    usuarios_restantes = buscar_usuario("Ana Carolina")
    assert not usuarios_restantes, "Alguns usuários ainda não foram excluídos"

    
def test_lista_usuarios():
    """Teste de listagem de usuários"""
    # Limpa usuários existentes
    while True:
        usuarios = listar_usuarios()
        if not usuarios:
            break
        excluir_usuario(usuarios[0]['id'])
    
    # Cadastra alguns usuários
    cadastrar_usuario(nome="Usuario 1", email="usuario1@exemplo.com", telefone="11678653531", endereco="Endereco 1")
    cadastrar_usuario(nome="Usuario 2", email="usuario2@exemplo.com", telefone="22678653531", endereco="Endereco 2")
    
    # Lista usuários
    usuarios = listar_usuarios()
    
    