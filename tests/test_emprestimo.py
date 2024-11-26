# tests/test_emprestimos.py
import sys
import os
import pytest
from datetime import datetime, timedelta
# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.emprestimo import (
    criaEmprestimo,
    listaEmprestimos,
    acabaEmprestimo,
    excluiEmprestimo
)
from modules.usuarios import cadastrar_usuario,buscar_usuario
from modules.livro import cadastrar_livro,buscar_livros
def setup_module(module):
    """Preparação inicial para testes de empréstimos"""
    # Limpa empréstimos existentes
    while True:
        emprestimos = listaEmprestimos()
        if not emprestimos:
            break
        excluiEmprestimo(emprestimos[0]['id'])
    
    # Cadastra usuário de teste
    cadastrar_usuario(
        nome="Usuário Teste", 
        email="usuario.teste@exemplo.com", 
        telefone="(11) 99999-9999", 
        endereco="Rua de Teste, 123"
    )
    
    # Cadastra livro de teste
    cadastrar_livro(
        titulo="Livro Teste", 
        autor="Autor Teste", 
        ano=2023, 
        editora="Editora Teste", 
        isbn="1234567890"
    )
def test_cria_emprestimo():
    """Teste de criação de empréstimo"""
    data_atual = datetime.now().strftime("%Y-%m-%d")
    data_devolucao = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
    
    # Busca o usuário e livro de teste
    usuarios = cadastrar_usuario(
        nome="Usuário Empréstimo", 
        email="usuario.emprestimo@exemplo.com", 
        telefone="(11) 88888-8888", 
        endereco="Rua de Empréstimo, 456"
    )
    
    livros = buscar_livros(titulo="Livro Teste")
    
    resultado = criaEmprestimo(
        pk_id_emprestimo=1001, 
        data_emprestimo=data_atual, 
        data_devolucao_real="None", 
        data_devolucao_prevista=data_devolucao, 
        fk_id_livro=livros[0]['id'], 
        fk_id_usuario=usuarios['id']
    )
    
    assert resultado is True, "Falha ao criar empréstimo"
    
    # Verifica se o empréstimo foi criado
    emprestimos = listaEmprestimos()
    assert len(emprestimos) > 0, "Empréstimo não foi adicionado à lista"
    assert emprestimos[0]['id'] == 1001, "ID do empréstimo não corresponde"

def test_lista_emprestimos():
    """Teste de listagem de empréstimos"""
    # Cria alguns empréstimos
    data_atual = datetime.now().strftime("%Y-%m-%d")
    data_devolucao = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
    
    usuarios = buscar_usuario(nome="Usuário Empréstimo")
    livros = buscar_livros(titulo="Livro Teste")
    
    criaEmprestimo(
        pk_id_emprestimo=1002, 
        data_emprestimo=data_atual, 
        data_devolucao_real="None", 
        data_devolucao_prevista=data_devolucao, 
        fk_id_livro=livros[0]['id'], 
        fk_id_usuario=usuarios['id']
    )
    
    criaEmprestimo(
        pk_id_emprestimo=1003, 
        data_emprestimo=data_atual, 
        data_devolucao_real="None", 
        data_devolucao_prevista=data_devolucao, 
        fk_id_livro=livros[0]['id'], 
        fk_id_usuario=usuarios['id']
    )
    
    # Lista empréstimos
    emprestimos = listaEmprestimos()
    
    assert len(emprestimos) >= 3, "Número de empréstimos não corresponde ao esperado"
def test_acaba_emprestimo():
    """Teste de finalização de empréstimo"""
    # Busca um empréstimo existente
    emprestimos = listaEmprestimos()
    emprestimo = emprestimos[0]
    
    # Finaliza o empréstimo
    resultado = acabaEmprestimo(emprestimo['id'])
    
    assert resultado is True, "Falha ao finalizar empréstimo "
        # Verifica se o empréstimo foi finalizado
    emprestimos_atualizados = listaEmprestimos()
    emprestimo_finalizado = next(
        (e for e in emprestimos_atualizados if e['id'] == emprestimo['id']),
        None
    )
    
    assert emprestimo_finalizado is not None, "Empréstimo não encontrado após finalização"
    assert emprestimo_finalizado['data_devolucao_real'] != "None", "Data de devolução real não foi atualizada"
    assert emprestimo_finalizado['data_devolucao_real'] == datetime.now().strftime("%Y-%m-%d"), "Data de devolução real está incorreta"
    
def test_exclui_emprestimo():
    """Teste de exclusão de empréstimo"""
    # Cria um novo empréstimo para teste de exclusão
    data_atual = datetime.now().strftime("%Y-%m-%d")
    data_devolucao = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
    
    usuarios = buscar_usuario(nome="Usuário Empréstimo")
    livros = buscar_livros(titulo="Livro Teste")
    
    criaEmprestimo(
        pk_id_emprestimo=1004, 
        data_emprestimo=data_atual, 
        data_devolucao_real="None", 
        data_devolucao_prevista=data_devolucao, 
        fk_id_livro=livros[0]['id'], 
        fk_id_usuario=usuarios['id']
    )
    
    # Verifica que o empréstimo foi adicionado
    emprestimos = listaEmprestimos()
    novo_emprestimo = next(
        (e for e in emprestimos if e['id'] == 1004),
        None
    )
    
    assert novo_emprestimo is not None, "Empréstimo de teste para exclusão não encontrado"
    
    # Exclui o empréstimo
    resultado = excluiEmprestimo(novo_emprestimo['id'])
    
    assert resultado is True, "Falha ao excluir empréstimo"
    
    # Verifica se o empréstimo foi removido
    emprestimos_atualizados = listaEmprestimos()
    emprestimo_excluido = next(
        (e for e in emprestimos_atualizados if e['id'] == novo_emprestimo['id']),
        None
    )
    
    assert emprestimo_excluido is None, "Empréstimo não foi excluído corretamente"
