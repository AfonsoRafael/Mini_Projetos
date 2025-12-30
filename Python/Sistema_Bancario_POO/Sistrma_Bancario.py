from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._agencia = "0001"
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def numero(self):
        return self._numero

    @property
    def saldo(self):
        return self._saldo

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\nOperacao falhou, valor invalido")
            return False

        if valor > self.saldo:
            print("\nOperacao falhou, saldo insuficiente")
            return False

        self._saldo -= valor
        print("\nSaque realizado com sucesso")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\nOperacao falhou, valor invalido")
            return False

        self._saldo += valor
        print("\nDeposito realizado com sucesso")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite=500, limite_saques=3):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = sum(
            1 for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        )

        if valor > self.limite:
            print("\nOperacao falhou, valor do saque excede o limite")
            return False

        if numero_saques >= self.limite_saques:
            print("\nOperacao falhou, numero maximo de saques excedido")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
Agencia:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
=======================================
            BANCO PYTHON
=======================================
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[4]\tNova Conta
[5]\tListar Contas
[6]\tNovo Usuario
[0]\tSair
=> """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente nao possui conta")
        return None
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return

    valor = float(input("Informe o valor do deposito: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Nao foram realizadas movimentacoes.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("=========================================")


def criar_conta(numero_contas, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_contas)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("Conta criada com sucesso")


def listar_contas(contas):
    for conta in contas:
        print("=" * 30)
        print(textwrap.dedent(str(conta)))


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente numeros): ")

    if filtrar_cliente(cpf, clientes):
        print("Ja existe cliente com esse CPF")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco: ")

    clientes.append(
        PessoaFisica(nome, data_nascimento, cpf, endereco)
    )

    print("Cliente criado com sucesso")


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "5":
            listar_contas(contas)
        elif opcao == "6":
            criar_cliente(clientes)
        elif opcao == "0":
            break
        else:
            print("Operacao invalida")


main()
