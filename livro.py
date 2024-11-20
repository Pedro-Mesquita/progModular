class Livro:

    def __init__(self, pk_id_livro, titulo, autor, editora, ano_publicacao, qtd_copias):
        self.pk_id_livro = pk_id_livro
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano_publicacao = ano_publicacao
        self.qtd_copias = qtd_copias

    def atualizar_informacoes(self, titulo=None, autor=None, editora=None, ano_publicacao=None, qtd_copias=None):

        if titulo is not None:
            self.titulo = titulo
        if autor is not None:
            self.autor = autor
        if editora is not None:
            self.editora = editora
        if ano_publicacao is not None:
            self.ano_publicacao = ano_publicacao
        if qtd_copias is not None:
            self.qtd_copias = qtd_copias

    def __str__(self):
        return (f"ID: {self.pk_id_livro}, Título: {self.titulo}, Autor: {self.autor}, "
                f"Editora: {self.editora}, Ano: {self.ano_publicacao}, Exemplares: {self.qtd_copias}")


class Biblioteca:

    def __init__(self):
        self.catalogo = {}

    def cadastrar_livro(self, pk_id_livro, titulo, autor, editora, ano_publicacao, qtd_copias):

        if pk_id_livro in self.catalogo:
            raise ValueError("Já existe um livro cadastrado com esse ID.")
        novo_livro = Livro(pk_id_livro, titulo, autor, editora, ano_publicacao, qtd_copias)
        self.catalogo[pk_id_livro] = novo_livro

    def consultar_livros(self, criterio, valor):

        resultado = [livro for livro in self.catalogo.values() if getattr(livro, criterio, None) == valor]
        return resultado

    def listar_quantidade(self, pk_id_livro):

        livro = self.catalogo.get(pk_id_livro)
        if not livro:
            raise ValueError("Livro não encontrado.")
        return livro.qtd_copias

    def atualizar_livro(self, pk_id_livro, **kwargs):

        livro = self.catalogo.get(pk_id_livro)
        if not livro:
            raise ValueError("Livro não encontrado.")
        livro.atualizar_informacoes(**kwargs)

    def remover_livro(self, pk_id_livro):

        if pk_id_livro not in self.catalogo:
            raise ValueError("Livro não encontrado.")
        del self.catalogo[pk_id_livro]

    def listar_livros(self):

        return [str(livro) for livro in self.catalogo.values()]

    def __str__(self):
        return "\n".join(str(livro) for livro in self.catalogo.values())
