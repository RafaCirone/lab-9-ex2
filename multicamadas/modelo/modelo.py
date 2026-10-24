from datetime import datetime


class Cliente:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"


class Transacao:
    """Registro imutável de uma operação feita na conta."""

    DEPOSITO = "Depósito"
    SAQUE = "Saque"
    ABERTURA = "Abertura"

    def __init__(self, tipo: str, valor: float, saldo_apos: float):
        self._tipo = tipo
        self._valor = valor
        self._saldo_apos = saldo_apos
        self._data = datetime.now()

    @property
    def tipo(self):
        return self._tipo

    @property
    def valor(self):
        return self._valor

    @property
    def saldo_apos(self):
        return self._saldo_apos

    @property
    def data(self):
        return self._data


class Conta:
    _proximo_numero = 1001  # gerador simples de números de conta

    def __init__(self, cliente: Cliente, saldo_inicial: float = 0.0):
        self.numero = Conta._proximo_numero
        Conta._proximo_numero += 1
        self.cliente = cliente
        self._saldo = saldo_inicial
        self._historico = [Transacao(Transacao.ABERTURA, saldo_inicial, saldo_inicial)]

    @property
    def saldo(self) -> float:
        """Somente leitura: o saldo só muda por Depositar/Sacar."""
        return self._saldo

    @property
    def historico(self):
        """Somente leitura: devolve uma cópia da lista de transações."""
        return list(self._historico)

    def depositar(self, valor: float):
        self._saldo += valor
        self._historico.append(Transacao(Transacao.DEPOSITO, valor, self._saldo))

    def sacar(self, valor: float):
        self._saldo -= valor
        self._historico.append(Transacao(Transacao.SAQUE, valor, self._saldo))

    def __str__(self):
        return f"Conta {self.numero} - {self.cliente.nome}"
