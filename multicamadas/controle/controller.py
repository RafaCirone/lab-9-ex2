from negocio.servico import BancoService, RegraNegocioError


class BancoController:
    """Camada de Controle: liga a View à Camada de Negócios.

    Não contém regras do banco: apenas lê dados da View, chama o
    serviço e manda a View exibir o resultado (ou o erro).
    """

    def __init__(self, view, servico: BancoService):
        self.view = view
        self.servico = servico
        self.view.set_controller(self)

    def criar_conta(self):
        try:
            conta = self.servico.criar_conta(
                self.view.ler_nome(), self.view.ler_cpf(), self.view.ler_saldo()
            )
        except RegraNegocioError as erro:
            self.view.exibir_erro(str(erro))
            return
        self.view.exibir_conta(conta)
        self.view.limpar_campos()
        self.view.exibir_mensagem(f"Conta {conta.numero} criada com sucesso!")

    def consultar_conta(self):
        try:
            conta = self.servico.buscar_conta(self.view.ler_busca())
        except RegraNegocioError as erro:
            self.view.exibir_erro(str(erro))
            return
        self.view.exibir_conta(conta)

    def depositar(self):
        try:
            conta = self.servico.depositar(self.view.ler_busca(), self.view.ler_valor())
        except RegraNegocioError as erro:
            self.view.exibir_erro(str(erro))
            return
        self.view.limpar_valor()
        self.view.exibir_conta(conta)
        self.view.exibir_mensagem("Depósito realizado com sucesso!")

    def sacar(self):
        try:
            conta = self.servico.sacar(self.view.ler_busca(), self.view.ler_valor())
        except RegraNegocioError as erro:
            self.view.exibir_erro(str(erro))
            return
        self.view.limpar_valor()
        self.view.exibir_conta(conta)
        self.view.exibir_mensagem("Saque realizado com sucesso!")

    def ver_historico(self):
        try:
            conta, transacoes = self.servico.historico(self.view.ler_busca())
        except RegraNegocioError as erro:
            self.view.exibir_erro(str(erro))
            return
        self.view.exibir_historico(conta, transacoes)
