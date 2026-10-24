from modelo.modelo import Cliente, Conta
from dados.repositorio import BancoDados


class RegraNegocioError(Exception):
    """Erro lançado quando uma regra do banco é violada."""


class BancoService:
    """Camada de Negócios: único ponto que aplica as regras do banco.

    Regras:
      - Nome e CPF são obrigatórios; CPF deve ter 11 dígitos.
      - Só pode existir uma conta por CPF.
      - Saldo inicial não pode ser negativo.
      - Depósitos e saques devem ter valor maior que zero.
      - Não é permitido sacar mais do que o saldo (sem cheque especial).
    """

    def __init__(self, banco: BancoDados):
        self.banco = banco

    # ---------------- utilitários ----------------
    @staticmethod
    def _normalizar_cpf(cpf: str) -> str:
        return cpf.replace(".", "").replace("-", "").strip()

    @staticmethod
    def _converter_valor(texto, campo: str) -> float:
        try:
            return float(str(texto).replace(",", "."))
        except ValueError:
            raise RegraNegocioError(f"{campo} deve ser um número.")

    # ---------------- casos de uso ----------------
    def criar_conta(self, nome: str, cpf: str, saldo_texto: str) -> Conta:
        if not nome or not cpf or not saldo_texto:
            raise RegraNegocioError("Preencha Nome, CPF e Saldo Inicial.")

        cpf_numeros = self._normalizar_cpf(cpf)
        if not cpf_numeros.isdigit() or len(cpf_numeros) != 11:
            raise RegraNegocioError("CPF inválido. Informe 11 dígitos.")

        if self.banco.buscar_por_cpf(cpf_numeros):
            raise RegraNegocioError("Já existe uma conta cadastrada para este CPF.")

        saldo = self._converter_valor(saldo_texto, "Saldo inicial")
        if saldo < 0:
            raise RegraNegocioError("O saldo inicial não pode ser negativo.")

        conta = Conta(Cliente(nome, cpf_numeros), saldo)
        self.banco.salvar(conta)
        return conta

    def buscar_conta(self, termo: str) -> Conta:
        termo = self._normalizar_cpf(termo or "")
        if not termo:
            raise RegraNegocioError("Informe o número da conta ou o CPF.")

        conta = None
        if termo.isdigit() and len(termo) == 11:
            conta = self.banco.buscar_por_cpf(termo)
        elif termo.isdigit():
            conta = self.banco.buscar_por_numero(int(termo))

        if conta is None:
            raise RegraNegocioError("Conta não encontrada.")
        return conta

    def depositar(self, termo: str, valor_texto: str) -> Conta:
        conta = self.buscar_conta(termo)
        valor = self._converter_valor(valor_texto, "Valor do depósito")
        if valor <= 0:
            raise RegraNegocioError("O valor do depósito deve ser maior que zero.")
        conta.depositar(valor)
        return conta

    def sacar(self, termo: str, valor_texto: str) -> Conta:
        conta = self.buscar_conta(termo)
        valor = self._converter_valor(valor_texto, "Valor do saque")
        if valor <= 0:
            raise RegraNegocioError("O valor do saque deve ser maior que zero.")
        if valor > conta.saldo:
            raise RegraNegocioError("Saldo insuficiente para realizar o saque.")
        conta.sacar(valor)
        return conta

    def historico(self, termo: str):
        conta = self.buscar_conta(termo)
        return conta, conta.historico
