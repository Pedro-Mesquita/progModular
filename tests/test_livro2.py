import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import os

from livro import (
    inicializar_arquivo,
    carregar_dados,
    cadastrar_livro,
    listar_livros,
    buscar_livros,
    atualizar_livro,
    remover_livro,
    verificar_quantidade,
    salvar_dados,
    livros_db,
    ARQUIVO,
    gerar_id_unico,
    validar_ano,
    validar_quantidade,
)


def setup_module():
    """
    Configuração inicial antes de todos os testes.
    """
    livros_db.clear()


def test_inicializar_arquivo_novo():
    """
    Testa a inicialização de um novo arquivo vazio.
    """
    with patch("os.path.exists", return_value=False), patch("builtins.open", new_callable=mock_open) as mock_file:
        inicializar_arquivo()
        mock_file.assert_called_once_with(ARQUIVO, 'w')
        mock_file().write.assert_called_once_with("id,titulo,autor,editora,ano_publicacao,qtd_copias\n")


def test_carregar_dados_arquivo_vazio():
    """
    Testa o carregamento de dados quando o arquivo está vazio.
    """
    with patch("builtins.open", new_callable=mock_open, read_data="id,titulo,autor,editora,ano_publicacao,qtd_copias,data_cadastro\n"):
        carregar_dados()
        assert len(livros_db) == 0


def test_carregar_dados_com_conteudo():
    """
    Testa o carregamento de dados com conteúdo.
    """
    data = "id,titulo,autor,editora,ano_publicacao,qtd_copias,data_cadastro\n1001,Livro 1,Autor 1,Editora 1,2022,10,2024-11-26 15:00:00\n"
    with patch("builtins.open", new_callable=mock_open, read_data=data):
        carregar_dados()
        assert len(livros_db) == 1
        assert livros_db[0]['titulo'] == "Livro 1"


def test_cadastrar_livro():
    """
    Testa o cadastro de um livro.
    """
    with patch("builtins.input", side_effect=["Livro Teste", "Autor Teste", "Editora Teste", "2023", "5"]):
        cadastrar_livro()
        assert len(livros_db) == 1
        assert livros_db[0]['titulo'] == "Livro Teste"


def test_cadastrar_livro_titulo_vazio():
    """
    Testa o cadastro de um livro com título vazio.
    """
    with patch("builtins.input", return_value=""):
        try:
            cadastrar_livro()
        except ValueError:
            assert True
        else:
            assert False


def test_validar_ano():
    """
    Testa a validação de um ano válido e inválido.
    """
    assert validar_ano(2023) == 2023
    try:
        validar_ano(1500)
    except ValueError:
        assert True
    else:
        assert False


def test_validar_quantidade():
    """
    Testa a validação de uma quantidade válida e inválida.
    """
    assert validar_quantidade(10) == 10
    try:
        validar_quantidade(-1)
    except ValueError:
        assert True
    else:
        assert False


def test_buscar_livros():
    """
    Testa a busca de livros.
    """
    livros_db.append({
        "pk_id_livro": 1001,
        "titulo": "Livro Teste",
        "autor": "Autor Teste",
        "editora": "Editora Teste",
        "ano_publicacao": 2023,
        "qtd_copias": 5,
        "data_cadastro": "2024-11-26 15:00:00",
    })

    with patch("builtins.input", side_effect=["titulo", "Livro Teste"]), patch("builtins.print") as mock_print:
        buscar_livros()
        assert any("Livro Teste" in args[0] for args in mock_print.call_args_list)


def test_atualizar_livro():
    """
    Testa a atualização de um livro.
    """
    livros_db.append({
        "pk_id_livro": 1001,
        "titulo": "Livro Teste",
        "autor": "Autor Teste",
        "editora": "Editora Teste",
        "ano_publicacao": 2022,
        "qtd_copias": 10,
        "data_cadastro": "2024-11-26 15:00:00",
    })

    with patch("builtins.input", side_effect=["1001", "Novo Título", "Novo Autor", "Nova Editora", "2023", "5"]):
        atualizar_livro()
        assert livros_db[0]['titulo'] == "Novo Título"
        assert livros_db[0]['autor'] == "Novo Autor"


def test_remover_livro():
    """
    Testa a remoção de um livro.
    """
    livros_db.append({
        "pk_id_livro": 1001,
        "titulo": "Livro Teste",
        "autor": "Autor Teste",
        "editora": "Editora Teste",
        "ano_publicacao": 2022,
        "qtd_copias": 10,
        "data_cadastro": "2024-11-26 15:00:00",
    })

    with patch("builtins.input", return_value="1001"):
        remover_livro()
        assert len(livros_db) == 0


def test_salvar_dados():
    """
    Testa o salvamento dos dados no arquivo.
    """
    livros_db.append({
        "pk_id_livro": 1001,
        "titulo": "Livro Teste",
        "autor": "Autor Teste",
        "editora": "Editora Teste",
        "ano_publicacao": 2022,
        "qtd_copias": 10,
        "data_cadastro": "2024-11-26 15:00:00",
    })

    with patch("builtins.open", new_callable=mock_open) as mock_file:
        salvar_dados()
        mock_file.assert_called_once_with(ARQUIVO, 'w', encoding='utf-8')
        mock_file().write.assert_any_call("id,titulo,autor,editora,ano_publicacao,qtd_copias,data_cadastro\n")


if __name__ == "__main__":
    setup_module()  # Inicializa a configuração
    unittest.main()
