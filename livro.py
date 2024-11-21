import os

ARQUIVO = "livros.txt"

def inicializar_arquivo():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w') as arquivo:
            arquivo.write("id,titulo,autor,editora,ano_publicacao,qtd_copias\n")

def cadastrar_livro(pk_id_livro, titulo, autor, editora, ano_publicacao, qtd_copias):
    with open(ARQUIVO, 'a') as arquivo:
        arquivo.write(f"{pk_id_livro},{titulo},{autor},{editora},{ano_publicacao},{qtd_copias}\n")

def listar_livros():
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    return livros[1:]

def buscar_livro(campo, valor):
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    return [livro for livro in livros if valor in livro.split(',')[['id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'qtd_copias'].index(campo)]]

def atualizar_livro(pk_id_livro, **novos_dados):
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    header = livros[0]
    atualizados = []
    for livro in livros[1:]:
        dados = livro.strip().split(',')
        if dados[0] == str(pk_id_livro):
            for chave, valor in novos_dados.items():
                if valor is not None:
                    indice = ['id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'qtd_copias'].index(chave)
                    dados[indice] = str(valor)
            atualizados.append(','.join(dados) + '\n')
        else:
            atualizados.append(livro)
    with open(ARQUIVO, 'w') as arquivo:
        arquivo.writelines([header] + atualizados)

def remover_livro(pk_id_livro):
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    header = livros[0]
    restantes = [livro for livro in livros[1:] if livro.split(',')[0] != str(pk_id_livro)]
    with open(ARQUIVO, 'w') as arquivo:
        arquivo.writelines([header] + restantes)

def quantidade_livro(pk_id_livro):
    with open(ARQUIVO, 'r') as arquivo:
        livros = arquivo.readlines()
    for livro in livros[1:]:
        dados = livro.strip().split(',')
        if dados[0] == str(pk_id_livro):
            return int(dados[5])
    return 0
