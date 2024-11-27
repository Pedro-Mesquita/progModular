import pytest
import emprestimos
from datetime import datetime
import os


@pytest.fixture
def setup_arquivo_emprestimos(tmp_path, monkeypatch):
    """Cria um arquivo temporário para testes e redefine o caminho do arquivo."""
    caminho = tmp_path / "emprestimos_test.txt"
    monkeypatch.setattr(emprestimos, "caminho_arquivo", caminho)
    emprestimos.emprestimos = {}
    return caminho


def test_cria_emprestimo(setup_arquivo_emprestimos):
    emprestimos.cria_emprestimo(1, "2024-11-27", None, "2024-12-10", 101, 202)
    assert len(emprestimos.lista_emprestimos()) == 1
    assert emprestimos.emprestimos[1]["fk_id_livro"] == 101


def test_cria_emprestimo_duplicado(setup_arquivo_emprestimos):
    emprestimos.cria_emprestimo(1, "2024-11-27", None, "2024-12-10", 101, 202)
    with pytest.raises(ValueError):
        emprestimos.cria_emprestimo(1, "2024-11-28", None, "2024-12-11", 102, 203)


def test_exclui_emprestimo(setup_arquivo_emprestimos):
    emprestimos.cria_emprestimo(1, "2024-11-27", None, "2024-12-10", 101, 202)
    emprestimos.exclui_emprestimo(1)
    assert len(emprestimos.lista_emprestimos()) == 0


def test_exclui_emprestimo_inexistente(setup_arquivo_emprestimos):
    with pytest.raises(ValueError):
        emprestimos.exclui_emprestimo(999)


def test_acaba_emprestimo(setup_arquivo_emprestimos):
    emprestimos.cria_emprestimo(1, "2024-11-27", None, "2024-12-10", 101, 202)
    emprestimos.acaba_emprestimo(1)
    assert emprestimos.emprestimos[1]["data_devolucao_real"] == datetime.now().strftime("%Y-%m-%d")


def test_acaba_emprestimo_inexistente(setup_arquivo_emprestimos):
    with pytest.raises(ValueError):
        emprestimos.acaba_emprestimo(999)


def test_carrega_e_salva_emprestimos(setup_arquivo_emprestimos):
    # Criando empréstimos e salvando no arquivo
    emprestimos.cria_emprestimo(1, "2024-11-27", None, "2024-12-10", 101, 202)
    emprestimos.cria_emprestimo(2, "2024-11-28", None, "2024-12-11", 102, 203)
    emprestimos.salva_emprestimos()

    # Recarregando do arquivo para verificar persistência
    emprestimos.emprestimos = {}
    emprestimos.carrega_emprestimos()
    assert len(emprestimos.lista_emprestimos()) == 2
    assert emprestimos.emprestimos[1]["fk_id_usuario"] == 202
    assert emprestimos.emprestimos[2]["fk_id_usuario"] == 203
