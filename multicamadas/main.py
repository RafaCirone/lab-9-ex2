import tkinter as tk

from dados.repositorio import BancoDados
from negocio.servico import BancoService
from controle.controller import BancoController
from apresentacao.view import BancoView


def main():
    root = tk.Tk()
    banco = BancoDados()             # Camada de Dados
    servico = BancoService(banco)    # Camada de Negócios
    view = BancoView(root)           # Camada de Apresentação
    BancoController(view, servico)   # Camada de Controle
    root.mainloop()


if __name__ == "__main__":
    main()
