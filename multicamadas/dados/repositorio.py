from modelo.modelo import Conta


class BancoDados:
    """Camada de Dados: simula um banco de dados usando uma lista em memória."""

    def __init__(self):
        self._contas = []

    def salvar(self, conta: Conta):
        self._contas.append(conta)

    def listar(self):
        return list(self._contas)

    def buscar_por_numero(self, numero: int):
        for conta in self._contas:
            if conta.numero == numero:
                return conta
        return None

    def buscar_por_cpf(self, cpf: str):
        for conta in self._contas:
            if conta.cliente.cpf == cpf:
                return conta
        return None
