import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the root directory to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.multa import gerar_multa, visualizar_multa, pagar_multa
from modules.usuarios import cadastrar_usuario, buscar_usuario
from modules.livro import cadastrar_livro, buscar_livros

def setup_module(module):
    global usuarios_db, livros_db
    usuarios_db = []
    livros_db = []

    cadastrar_usuario("Usuário Multa", "Rua de Multa, 123", "11999999999", "usuario.multa@exemplo.com")

    livro_inputs = [
        "Livro Multa", "Autor Multa", "Editora Multa", "2023", "5"
    ]
    with patch('builtins.input', side_effect=livro_inputs):
        cadastrar_livro()
def test_gerar_multa_simple():
    """Simplified test for generating a multa"""
    # Create mock data for the necessary input
    mock_emprestimo = {
        'pk_id_emprestimo': 2001,
        'data_emprestimo': '2024-11-10',
        'data_devolucao_real': None,
        'data_devolucao_prevista': '2024-11-25',
        'fk_id_livro': 6341,
        'fk_id_usuario': 3977,
    }
    
    # Mock a simple function to simulate the creation of the multa
    data_atual = '2024-11-27'
    gerar_multa(
        pk_id_multa=5001,
        valor=50.0,
        data=data_atual,
        fk_id_emprestimo=mock_emprestimo['pk_id_emprestimo'],
        tipo="prazo",  # Use a valid value from TIPOS_MULTA
        data_geracao=data_atual,
        status="aberto"
    )
    
    # Verify the multa was created correctly
    multa = visualizar_multa(5001)
    assert multa is not None, "Multa não encontrada"
    assert multa['pk_id_multa'] == 5001, "ID da multa não corresponde"
    assert multa['valor'] == 50.0, "Valor da multa não corresponde"
    assert multa['status'] == "aberto", "Status da multa não corresponde"


def test_visualizar_multa():
    """Test visualizing a multa"""
    data_atual = datetime.now().strftime("%Y-%m-%d")
    pk_id_emprestimo = 2001  # Example loan ID

    gerar_multa(
        pk_id_multa=5002,
        valor=75.0,
        data=data_atual,
        fk_id_emprestimo=pk_id_emprestimo,
        tipo="avaria",
        data_geracao=data_atual,
        status="aberto"
    )

    multa = visualizar_multa(5002)
    assert multa is not None, "Multa não encontrada"
    assert multa['valor'] == 75.0, "Valor da multa não corresponde"
    assert multa['tipo'] == "avaria", "Tipo da multa não corresponde"

def test_pagar_multa():
    """Test paying a multa"""
    data_atual = datetime.now().strftime("%Y-%m-%d")
    pk_id_emprestimo = 2001  # Example loan ID

    gerar_multa(
        pk_id_multa=5003,
        valor=100.0,
        data=data_atual,
        fk_id_emprestimo=pk_id_emprestimo,
        tipo="prazo",
        data_geracao=data_atual,
        status="aberto"
    )

    pagar_multa(5003)

    multa = visualizar_multa(5003)
    assert multa['status'] == "pago", "Status da multa não foi atualizado"

if __name__ == "__main__":
    pytest.main()
