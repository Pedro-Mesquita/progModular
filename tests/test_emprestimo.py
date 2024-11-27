import sys
import os
import pytest
from datetime import datetime
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import mock_open, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
from modules.emprestimo import (
    criaEmprestimo,
    emprestimos,
    excluiEmprestimo,
    acabaEmprestimo,
    salvaEmprestimos,
    listaEmprestimos,
    carrega_emprestimos
)

caminho_arquivo = "data/emprestimos.txt"

@pytest.fixture
def setup_emprestimos():
    emprestimos.clear()  
    yield
    emprestimos.clear()  

    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
    if os.path.exists("data"):
        os.rmdir("data")

def test_cria_emprestimo(setup_emprestimos):
    pk_id_emprestimo = 1
    data_emprestimo = "2024-11-25"
    data_devolucao_real = None
    data_devolucao_prevista = "2024-12-25"
    fk_id_livro = 101
    fk_id_usuario = 202

    criaEmprestimo(pk_id_emprestimo, data_emprestimo, data_devolucao_real, data_devolucao_prevista, fk_id_livro, fk_id_usuario)

    expected_emprestimo = {
        "pk_id_emprestimo": pk_id_emprestimo,
        "data_emprestimo": data_emprestimo,
        "data_devolucao_real": data_devolucao_real,
        "data_devolucao_prevista": data_devolucao_prevista,
        "fk_id_livro": fk_id_livro,
        "fk_id_usuario": fk_id_usuario
    }

    assert pk_id_emprestimo in emprestimos
    assert emprestimos[pk_id_emprestimo] == expected_emprestimo

def test_exclui_emprestimo(setup_emprestimos):
    pk_id_emprestimo = 1
    data_emprestimo = "2024-11-25"
    data_devolucao_real = None
    data_devolucao_prevista = "2024-12-25"
    fk_id_livro = 101
    fk_id_usuario = 202

    criaEmprestimo(pk_id_emprestimo, data_emprestimo, data_devolucao_real, data_devolucao_prevista, fk_id_livro, fk_id_usuario)
    assert pk_id_emprestimo in emprestimos
    excluiEmprestimo(pk_id_emprestimo)
    assert pk_id_emprestimo not in emprestimos

def test_exclui_emprestimo_nonexistent_id(setup_emprestimos):
    assert not emprestimos
    pk_id_emprestimo = 999
    excluiEmprestimo(pk_id_emprestimo)
    assert not emprestimos

def test_acaba_emprestimo(setup_emprestimos):
    pk_id_emprestimo = 1
    data_emprestimo = "2024-11-25"
    data_devolucao_real = None
    data_devolucao_prevista = "2024-12-25"
    fk_id_livro = 101
    fk_id_usuario = 202

    criaEmprestimo(pk_id_emprestimo, data_emprestimo, data_devolucao_real, data_devolucao_prevista, fk_id_livro, fk_id_usuario)
    assert emprestimos[pk_id_emprestimo]["data_devolucao_real"] is None
    acabaEmprestimo(pk_id_emprestimo)
    current_date = datetime.now().strftime("%Y-%m-%d")
    assert emprestimos[pk_id_emprestimo]["data_devolucao_real"] == current_date

def test_acaba_emprestimo_nonexistent_id(setup_emprestimos):
    assert not emprestimos
    pk_id_emprestimo = 999
    acabaEmprestimo(pk_id_emprestimo)
    assert not emprestimos

def test_salva_emprestimos_txt(setup_emprestimos):
    assert not os.path.exists(caminho_arquivo), f"File already exists: {caminho_arquivo}"

    emprestimos_data = [
        {
            "pk_id_emprestimo": 1,
            "data_emprestimo": "2024-11-25",
            "data_devolucao_real": None,
            "data_devolucao_prevista": "2024-12-25",
            "fk_id_livro": 101,
            "fk_id_usuario": 202,
        },
        {
            "pk_id_emprestimo": 2,
            "data_emprestimo": "2024-11-26",
            "data_devolucao_real": "2024-12-01",
            "data_devolucao_prevista": "2024-12-30",
            "fk_id_livro": 102,
            "fk_id_usuario": 203,
        },
    ]

    os.makedirs(os.path.join(root_path, "data"), exist_ok=True)

    for emprestimo in emprestimos_data:
        criaEmprestimo(
            emprestimo["pk_id_emprestimo"],
            emprestimo["data_emprestimo"],
            emprestimo["data_devolucao_real"],
            emprestimo["data_devolucao_prevista"],
            emprestimo["fk_id_livro"],
            emprestimo["fk_id_usuario"],
        )
    salvaEmprestimos()

    assert os.path.exists(os.path.join(root_path, "data", "emprestimos.txt")), f"File not found: {os.path.join(root_path, 'data', 'emprestimos.txt')}"
    with open(os.path.join(root_path, "data", "emprestimos.txt"), "r") as arquivo:
        lines = arquivo.readlines()
    assert len(lines) == len(emprestimos_data), f"Expected {len(emprestimos_data)} lines, but found {len(lines)}"
    for i, emprestimo in enumerate(emprestimos_data):
        expected_line = (
            f"{emprestimo['pk_id_emprestimo']},{emprestimo['data_emprestimo']},"
            f"{emprestimo['data_devolucao_real']},{emprestimo['data_devolucao_prevista']},"
            f"{emprestimo['fk_id_livro']},{emprestimo['fk_id_usuario']}\n"
        )
        assert lines[i] == expected_line, f"Mismatch at line {i+1}: {lines[i]} != {expected_line}"


def test_listaEmprestimos(setup_emprestimos):
    criaEmprestimo(1, "2024-11-25", None, "2024-12-25", 101, 202)
    criaEmprestimo(2, "2024-11-26", "2024-12-01", "2024-12-30", 102, 203)
    
    expected_output = (
        "ID: 1\n"
        "Data Emprestimo: 2024-11-25\n"
        "Data Devolucao Real: None\n"
        "Data Devolucao Prevista: 2024-12-25\n"
        "ID Livro: 101\n"
        "ID Usuario: 202\n"
        "----------\n"
        "ID: 2\n"
        "Data Emprestimo: 2024-11-26\n"
        "Data Devolucao Real: 2024-12-01\n"
        "Data Devolucao Prevista: 2024-12-30\n"
        "ID Livro: 102\n"
        "ID Usuario: 203\n"
        "----------\n"
    )

    f = StringIO()
    with redirect_stdout(f):
        listaEmprestimos()
    output = f.getvalue()
    assert output == expected_output


def test_carrega_emprestimos_with_mocked_file():
    mock_file_content = '1,2024-11-25,None,2024-12-25,101,202\n2,2024-11-26,2024-12-01,2024-12-30,102,203\n'
    
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        result = carrega_emprestimos() 
    
    expected_emprestimos = {
        1: {
            "pk_id_emprestimo": 1,
            "data_emprestimo": "2024-11-25",
            "data_devolucao_real": None,
            "data_devolucao_prevista": "2024-12-25",
            "fk_id_livro": 101,
            "fk_id_usuario": 202
        },
        2: {
            "pk_id_emprestimo": 2,
            "data_emprestimo": "2024-11-26",
            "data_devolucao_real": "2024-12-01",
            "data_devolucao_prevista": "2024-12-30",
            "fk_id_livro": 102,
            "fk_id_usuario": 203
        }
    }
    assert result == expected_emprestimos, f"Expected {expected_emprestimos}, but got {result}"
