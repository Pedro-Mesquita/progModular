# tests/test_multas.py
import sys
import os
import pytest
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.multa import (
    gerar_multa,
    visualizar_multa,
    pagar_multa,
    visualizar_multa
)

from modules.emprestimo import criaEmprestimo
from modules.usuarios import cadastrar_usuario,buscar_usuario
from modules.livro import cadastrar_livro,buscar_livros

def setup_module(module):
    """Preparação inicial para testes de multas"""
    # Limpa multas existentes
    while True:
        multas = visualizar_multa()  # Assumindo que há uma função listar_multas() no módulo
        if not multas:
            break

    # Cadastra usuário de teste
    cadastrar_usuario(
        nome="Usuário Multa", 
        email="usuario.multa@exemplo.com", 
        telefone="(11) 99999-9999", 
        endereco="Rua de Multa, 123"
    )
    
    # Cadastra livro de teste
    cadastrar_livro(
        titulo="Livro Multa", 
        autor="Autor Multa", 
        ano=2023, 
        editora="Editora Multa", 
        isbn="9876543210"
    )

def test_gerar_multa():
    """Teste de geração de multa"""
    # Cria um empréstimo primeiro
    data_atual = datetime.now().strftime("%Y-%m-%d")
    data_devolucao = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
    
    usuarios = buscar_usuario(nome="Usuário Multa")
    livros = buscar_livros(titulo="Livro Multa")
    
    criaEmprestimo(
        pk_id_emprestimo=2001, 
        data_emprestimo=data_atual, 
        data_devolucao_real="None", 
        data_devolucao_prevista=data_devolucao, 
        fk_id_livro=livros[0]['id'], 
        fk_id_usuario=usuarios['id']
    )
    
    # Gera uma multa
    resultado = gerar_multa(
        pk_id_multa=5001, 
        valor=50.0, 
        data=data_atual, 
        fk_id_emprestimo=2001, 
        tipo="atraso", 
        data_geracao=data_atual, 
        status="aberto"
    )
    
    assert resultado is True, "Falha ao gerar multa"
    
    # Verifica se a multa foi gerada
    multas = visualizar_multa()
    assert len(multas) > 0, "Multa não foi adicionada à lista"
    assert multas[0]['id'] == 5001, "ID da multa não corresponde"

def test_visualizar_multa():
    """Teste de visualização de multa"""
    # Gera uma nova multa
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    resultado = gerar_multa(
        pk_id_multa=5002, 
        valor=75.0, 
        data=data_atual, 
        fk_id_emprestimo=2001, 
        tipo="dano", 
        data_geracao=data_atual, 
        status="aberto"
    )
    
    # Visualiza a multa
    multa = visualizar_multa(5002)
    
    assert multa is not None, "Multa não encontrada"
    assert multa['valor'] == 75.0, "Valor da multa não corresponde"
    assert multa['tipo'] == "dano", "Tipo da multa não corresponde"

def test_pagar_multa():
    """Teste de pagamento de multa"""
    # Gera uma multa para pagar
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    resultado = gerar_multa(
        pk_id_multa=5003, 
        valor=100.0, 
        data=data_atual, 
        fk_id_emprestimo=2001, 
        tipo="avaria", 
        data_geracao=data_atual, 
        status="aberto"
    )
    
    # Paga a multa
    resultado_pagamento = pagar_multa(5003)
    
    assert resultado_pagamento is True, "Falha ao pagar multa"
    
    # Verifica o status da multa
    multa = visualizar_multa(5003)
    assert multa['status'] == "pago", "Status da multa não foi atualizado"