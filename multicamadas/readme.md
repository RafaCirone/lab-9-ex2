# Sistema Bancário - Multicamadas (Python)

Evolução do Exercício 1 (MVC). Agora a aplicação permite **Criar Conta**, **Consultar**, **Depositar**, **Sacar** e **ver o Histórico** de transações, organizada em uma **Arquitetura Multicamadas**.

## Estrutura

```
multicamadas/
├── apresentacao/view.py    # Camada de Apresentação: interface Tkinter (entrada e exibição)
├── controle/controller.py  # Camada de Controle: liga a View ao serviço, sem regras do banco
├── negocio/servico.py      # Camada de Negócios: BancoService, aplica TODAS as regras do banco
├── dados/repositorio.py    # Camada de Dados: BancoDados (lista em memória)
├── modelo/modelo.py        # Entidades: Cliente, Conta, Transacao
└── main.py                 # Ponto de entrada (monta as camadas)
```

Fluxo: `View -> Controller -> BancoService (Negócios) -> BancoDados (Dados)`. Cada camada só conversa com a camada logo abaixo.

## Novidades na Conta

- `depositar(valor)` e `sacar(valor)`: alteram o saldo e registram uma `Transacao`.
- `saldo`: propriedade somente leitura (não dá para fazer `conta.saldo = 1000`).
- `historico`: propriedade somente leitura que devolve uma cópia da lista de transações (abertura, depósitos e saques, com data/hora e saldo após a operação).

## Regras do banco (Camada de Negócios)

- Nome e CPF obrigatórios; CPF com 11 dígitos; uma conta por CPF.
- Saldo inicial não pode ser negativo.
- Depósito e saque precisam de valor maior que zero.
- Saque não pode ser maior que o saldo (sem cheque especial).

Quando uma regra é violada, o serviço lança `RegraNegocioError`, e o Controller manda a View exibir a mensagem.

## Como executar

Requer Python 3.8+ (Tkinter já vem com o Python). Execute de dentro da pasta `multicamadas`:

```bash
python main.py
```

No Linux, se o Tkinter não estiver instalado: `sudo apt install python3-tk`

## Como usar

1. Preencha Nome, CPF e Saldo Inicial e clique em **Criar Conta**.
2. Em **Operações**, informe o nº da conta (ou CPF) e um valor, e clique em **Depositar** ou **Sacar**.
3. Clique em **Histórico** para ver todas as transações da conta.
