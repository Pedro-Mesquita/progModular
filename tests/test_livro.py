# tests/test_livros.py
import sys
import os
import pytest

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.livro import (
    cadastrar_livro,
    buscar_livros,
    atualizar_livro,
    remover_livro,
    listar_livros
)

def setup_module(module):
    """Limpa a lista de livros antes dos testes"""
    # Remove todos os livros existentes
    while True:
        livros = listar_livros()
        if not livros:
            break
        remover_livro(livros[0]['id'])

def test_cadastrar_livro():
    """Teste de cadastro de livro"""
    resultado = cadastrar_livro(
        titulo="Python Básico", 
        autor="Maria Silva", 
        ano=2022, 
        editora="Editora Técnica", 
        isbn="1234567890"
    )
    
    assert resultado is True, "Falha ao cadastrar livro"
    
    # Verifica se o livro foi cadastrado
    livros = listar_livros()
    assert len(livros) > 0, "Livro não foi adicionado à lista"
    assert livros[0]['titulo'] == "Python Básico", "Título do livro não corresponde"

def test_buscar_livros():
    """Teste de busca de livros"""
    # Cadastra alguns livros para busca
    cadastrar_livro(
        titulo="Java Avançado", 
        autor="João Souza", 
        ano=2021, 
        editora="Editora Tech", 
        isbn="0987654321"
    )
    
    cadastrar_livro(
        titulo="Python Avançado", 
        autor="Maria Silva", 
        ano=2023, 
        editora="Editora Técnica", 
        isbn="5432167890"
    )
    
    # Busca livros por título
    livros_python = buscar_livros(titulo="Python")
    
    assert len(livros_python) == 2, "Número de livros encontrados não corresponde"
    
    # Busca livros por autor
    livros_maria = buscar_livros(autor="Maria Silva")
    
    assert len(livros_maria) == 2, "Número de livros do autor não corresponde"

def test_atualizar_livro():
    """Teste de atualização de livro"""
    # Cadastra um livro para atualizar
    cadastrar_livro(
        titulo="Banco de Dados", 
        autor="Carlos Oliveira", 
        ano=2020, 
        editora="Editora Data", 
        isbn="6543210987"
    )
    
    # Busca o livro cadastrado
    livros = buscar_livros(titulo="Banco de Dados")
    livro = livros[0]
    
    # Atualiza o livro
    resultado = atualizar_livro(
        id_livro=livro['id'], 
        titulo="Banco de Dados Avançado", 
        autor="Carlos Oliveira", 
        ano=2021, 
        editora="Editora Data Plus", 
        isbn="6543210988"
    )
    
    assert resultado is True, "Falha ao atualizar livro"
    
    # Verifica se a atualização foi realizada
    livros_atualizados = buscar_livros(titulo="Banco de Dados Avançado")
    assert len(livros_atualizados) > 0, "Livro atualizado não encontrado"
    assert livros_atualizados[0]['editora'] == "Editora Data Plus", "Editora não foi atualizada corretamente"

def test_remover_livro():
    """Teste de remoção de livro"""
    # Cadastra um livro para remover
    cadastrar_livro(
        titulo="Redes de Computadores", 
        autor="Pedro Santos", 
        ano=2019, 
        editora="Editora Network", 
        isbn="1122334455"
    )
    
    # Busca o livro cadastrado
    livros = buscar_livros(titulo="Redes de Computadores")
    livro = livros[0]
    
    # Remove o livro
    resultado = remover_livro(id_livro=livro['id'])
    
    assert resultado is True, "Falha ao remover livro"
    
    # Verifica se o livro foi removido
    livros_apos_remocao = buscar_livros(titulo="Redes de Computadores")
    assert len(livros_apos_remocao) == 0, "Livro não foi removido"