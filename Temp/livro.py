import os

ARQUIVO = "livros.txt"


def inicializar_arquivo():
    """
    Inicializa o arquivo de armazenamento de livros se não existir.
    """
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w') as arquivo:
            arquivo.write("id,titulo,autor,editora,ano_publicacao,qtd_copias\n")
        return True
    return False


def cadastrar_livro(pk_id_livro, titulo, autor, editora, ano_publicacao, qtd_copias):
    """
    Cadastra um novo livro no arquivo.
    Retorna True se bem-sucedido.
    """
    try:
        with open(ARQUIVO, 'a') as arquivo:
            arquivo.write(f"{pk_id_livro},{titulo},{autor},{editora},{ano_publicacao},{qtd_copias}\n")
        return True
    except Exception as e:
        print(f"Erro ao cadastrar livro: {e}")
        return False


def listar_livros():
    """
    Lista todos os livros no arquivo.
    Retorna uma lista de strings com os dados dos livros ou lista vazia.
    """
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    return livros[1:]  # Ignorar o cabeçalho


def buscar_livro(campo, valor):
    """
    Busca um livro no arquivo com base no campo e valor fornecidos.
    Retorna uma lista de livros encontrados.
    """
    campos_validos = ['id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'qtd_copias']
    if campo not in campos_validos:
        raise ValueError("Campo de busca inválido")
    indice = campos_validos.index(campo)
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    return [
        livro for livro in livros[1:]  # Ignorar cabeçalho
        if valor.lower() in livro.strip().split(',')[indice].lower()
    ]


def atualizar_livro(pk_id_livro, **novos_dados):
    """
    Atualiza os dados de um livro baseado no ID fornecido.
    Retorna True se a atualização for bem-sucedida, False se o livro não for encontrado.
    """
    if not os.path.exists(ARQUIVO):
        return False

    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()

    header = livros[0]
    atualizados = []
    livro_encontrado = False

    for livro in livros[1:]:
        dados = livro.strip().split(',')
        if dados[0] == str(pk_id_livro):
            for chave, valor in novos_dados.items():
                if valor is not None:
                    indice = ['id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'qtd_copias'].index(chave)
                    dados[indice] = str(valor)
            atualizados.append(','.join(dados) + '\n')
            livro_encontrado = True
        else:
            atualizados.append(livro)

    if livro_encontrado:
        with open(ARQUIVO, 'w') as arquivo:
            arquivo.writelines([header] + atualizados)
        return True
    return False


def remover_livro(pk_id_livro):
    """
    Remove um livro baseado no ID fornecido.
    Retorna True se o livro for removido, False se não for encontrado.
    """
    if not os.path.exists(ARQUIVO):
        return False

    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()

    header = livros[0]
    restantes = [livro for livro in livros[1:] if livro.split(',')[0] != str(pk_id_livro)]

    if len(restantes) < len(livros) - 1:
        with open(ARQUIVO, 'w') as arquivo:
            arquivo.writelines([header] + restantes)
        return True
    return False


def quantidade_livro(pk_id_livro):
    """
    Retorna a quantidade de cópias de um livro baseado no ID fornecido.
    Retorna 0 se o livro não for encontrado.
    """
    if not os.path.exists(ARQUIVO):
        return 0

    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()

    for livro in livros[1:]:
        dados = livro.strip().split(',')
        if dados[0] == str(pk_id_livro):    
            return int(dados[5])
    return 0


if __name__ == "__main__":
    inicializar_arquivo()
    print("Módulo carregado.")
