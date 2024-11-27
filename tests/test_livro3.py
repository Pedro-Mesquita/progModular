import unittest
import os
import livro

class TestLivro(unittest.TestCase):

    def setUp(self):
        """
        Configuração inicial do teste. Limpa ou cria o arquivo de teste.
        """
        livro.ARQUIVO = "test_livros.txt"
        if os.path.exists(livro.ARQUIVO):
            os.remove(livro.ARQUIVO)
        livro.inicializar_arquivo()

    def tearDown(self):
        """
        Limpa o arquivo de teste após cada execução.
        """
        if os.path.exists(livro.ARQUIVO):
            os.remove(livro.ARQUIVO)

    def test_inicializar_arquivo(self):
        """
        Testa se o arquivo é criado corretamente.
        """
        self.assertTrue(os.path.exists(livro.ARQUIVO))
        with open(livro.ARQUIVO, 'r') as arquivo:
            conteudo = arquivo.read()
        self.assertEqual(conteudo.strip(), "id,titulo,autor,editora,ano_publicacao,qtd_copias")

    def test_cadastrar_livro(self):
        """
        Testa o cadastro de um livro.
        """
        livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
        with open(livro.ARQUIVO, 'r') as arquivo:
            linhas = arquivo.readlines()
        self.assertEqual(len(linhas), 2)  # Cabeçalho + 1 livro
        self.assertIn("1,Livro A,Autor A,Editora A,2023,10\n", linhas)

    def test_listar_livros(self):
        """
        Testa a listagem de livros.
        """
        livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
        livro.cadastrar_livro(2, "Livro B", "Autor B", "Editora B", 2022, 5)
        livros = livro.listar_livros()
        self.assertEqual(len(livros), 2)
        self.assertIn("1,Livro A,Autor A,Editora A,2023,10\n", livros)
        self.assertIn("2,Livro B,Autor B,Editora B,2022,5\n", livros)

    def test_buscar_livro(self):
        """
        Testa a busca de um livro por um campo específico.
        """
        livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
        livro.cadastrar_livro(2, "Livro B", "Autor B", "Editora B", 2022, 5)
        resultado = livro.buscar_livro("titulo", "Livro A")
        self.assertEqual(len(resultado), 1)
        self.assertIn("1,Livro A,Autor A,Editora A,2023,10\n", resultado)

    def test_atualizar_livro(self):
        """
        Testa a atualização de dados de um livro.
        """
        livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
        livro.atualizar_livro(1, titulo="Livro A Atualizado", qtd_copias=15)
        livros = livro.listar_livros()
        self.assertIn("1,Livro A Atualizado,Autor A,Editora A,2023,15\n", livros)

    def test_remover_livro(self):
        """
        Testa a remoção de um livro.
        """
        livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
        livro.cadastrar_livro(2, "Livro B", "Autor B", "Editora B", 2022, 5)
        livro.remover_livro(1)
        livros = livro.listar_livros()
        self.assertEqual(len(livros), 1)
        self.assertIn("2,Livro B,Autor B,Editora B,2022,5\n", livros)

    def test_quantidade_livro(self):
        """
        Testa a consulta da quantidade de cópias de um livro.
        """
        livro.cadastrar_livro(1, "Livro A", "Autor A", "Editora A", 2023, 10)
        quantidade = livro.quantidade_livro(1)
        self.assertEqual(quantidade, 10)
        quantidade_inexistente = livro.quantidade_livro(99)
        self.assertEqual(quantidade_inexistente, 0)


if __name__ == '__main__':
    unittest.main()
