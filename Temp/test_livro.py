import os
import livro

ARQUIVO_TESTE = "test_livros.txt"

def setup_module(module):
    """
    Configuração inicial antes de todos os testes.
    """
    livro.ARQUIVO = ARQUIVO_TESTE
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)
    livro.inicializar_arquivo()

def teardown_module(module):
    """
    Limpeza após todos os testes.
    """
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)

def test_inicializar_arquivo():
    """
    Testa se o arquivo é criado corretamente.
    """
    assert os.path.exists(ARQUIVO_TESTE)
    with open(ARQUIVO_TESTE, 'r') as arquivo:
        conteudo = arquivo.read()
    assert conteudo.strip() == "id,titulo,autor,editora,ano_publicacao,qtd_copias"

def test_cadastrar_livro():
    """
    Testa o cadastro de um livro.
    """
    livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
    with open(ARQUIVO_TESTE, 'r') as arquivo:
        linhas = arquivo.readlines()
    assert len(linhas) == 2  # Cabeçalho + 1 livro
    assert "1,Livro A,Autor A,Editora A,2023,10\n" in linhas

def test_listar_livros():
    """
    Testa a listagem de livros.
    """
    livro.cadastrar_livro(2, "Livro B", "Autor B", "Editora B", 2022, 5)
    livros = livro.listar_livros()
    assert len(livros) == 2
    assert "1,Livro A,Autor A,Editora A,2023,10\n" in livros
    assert "2,Livro B,Autor B,Editora B,2022,5\n" in livros

def test_buscar_livro():
    """
    Testa a busca de um livro por um campo específico.
    """
    resultado = livro.buscar_livro("titulo", "Livro A")
    assert len(resultado) == 1
    assert "1,Livro A,Autor A,Editora A,2023,10\n" in resultado

def test_atualizar_livro():
    """
    Testa a atualização de dados de um livro.
    """
    livro.atualizar_livro(1, titulo="Livro A Atualizado", qtd_copias=15)
    livros = livro.listar_livros()
    assert "1,Livro A Atualizado,Autor A,Editora A,2023,15\n" in livros

def test_remover_livro():
    """
    Testa a remoção de um livro.
    """
    livro.remover_livro(1)
    livros = livro.listar_livros()
    assert len(livros) == 1
    assert "2,Livro B,Autor B,Editora B,2022,5\n" in livros

def test_quantidade_livro():
    """
    Testa a consulta da quantidade de cópias de um livro.
    """
    quantidade = livro.quantidade_livro(2)
    assert quantidade == 5
    quantidade_inexistente = livro.quantidade_livro(99)
    assert quantidade_inexistente == 0
