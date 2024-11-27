import sys
import os
import pytest
from unittest.mock import patch

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.livro import cadastrar_livro, buscar_livros, atualizar_livro, remover_livro

def test_cadastrar_livro():
    """Teste de cadastro de livro"""
    user_inputs = [
        "Python Básico",   # título
        "Maria Silva",     # autor
        "Editora Técnica", # editora
        "2022",            # ano_publicacao
        "10"               # qtd_copias
    ]
    with patch('builtins.input', side_effect=user_inputs):
        cadastrar_livro()
    # Simulating buscar_livros input
    search_inputs = [
        "titulo",         # campo
        "Python Básico"   # valor
    ]
    with patch('builtins.input', side_effect=search_inputs):
        buscar_livros()

def test_buscar_livros():
    """Teste de busca de livros"""
    user_inputs = [
        "Java Avançado",   # título
        "João Souza",      # autor
        "Editora Tech",    # editora
        "2021",            # ano_publicacao
        "5"                # qtd_copias
    ]
    with patch('builtins.input', side_effect=user_inputs):
        cadastrar_livro()
    # Simulating buscar_livros input
    search_inputs = [
        "titulo",         # campo
        "Java Avançado"   # valor
    ]
    with patch('builtins.input', side_effect=search_inputs):
        buscar_livros()

def test_atualizar_livro():
    """Teste de atualização de livro"""
    user_inputs = [
        "Banco de Dados",  # título
        "Carlos Oliveira", # autor
        "Editora Data",    # editora
        "2020",            # ano_publicacao
        "3"                # qtd_copias
    ]
    with patch('builtins.input', side_effect=user_inputs):
        cadastrar_livro()
    # Simulating atualizar_livro input
    update_inputs = [
        "1",               # pk_id_livro
        "Banco de Dados Avançado",  # novo_titulo
        "",                # novo_autor
        "",                # nova_editora
        "",                # novo_ano
        ""                 # nova_qtd
    ]
    with patch('builtins.input', side_effect=update_inputs):
        atualizar_livro()

def test_remover_livro():
    """Teste de remoção de livro"""
    user_inputs = [
        "Redes de Computadores", # título
        "Pedro Santos",         # autor
        "Editora Network",      # editora
        "2019",                 # ano_publicacao
        "2"                     # qtd_copias
    ]
    with patch('builtins.input', side_effect=user_inputs):
        cadastrar_livro()
    # Simulating remover_livro input
    remove_inputs = [
        "1"  # pk_id_livro
    ]
    with patch('builtins.input', side_effect=remove_inputs):
        remover_livro()
