from datetime import datetime

class Usuario:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
        self.endereco = endereco

class Conta:
    AGENCIA_PADRAO = "0001"
    numero_conta_sequencial = 1
    
    def __init__(self, usuario):
        self.agencia = Conta.AGENCIA_PADRAO
        self.numero = Conta.numero_conta_sequencial
        Conta.numero_conta_sequencial += 1
        self.usuario = usuario
        self.saldo = 0
        self.depositos = []
        self.saques = []
        self.saques_diarios = 0
        self.transacoes_diarias = 0
        self.LIMITE_TRANSACOES = 10

    def validar_transacao(self):
        if self.transacoes_diarias >= self.LIMITE_TRANSACOES:
            print(f"Limite diário de {self.LIMITE_TRANSACOES} transações atingido.")
            return False
        return True

    def sacar(self, valor):
        if not self.validar_transacao():
            return
        if self.saques_diarios >= 3:
            print("Limite de 3 saques diários atingido.")
            return
        if valor > 500:
            print("O valor do saque não pode exceder R$500,00.")
            return
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return
        if valor <= 0:
            print("O valor do saque deve ser positivo.")
            return
        
        self.saldo -= valor
        self.saques.append(f"Saque de R${valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.saques_diarios += 1
        self.transacoes_diarias += 1
        print(f"Saque de R${valor:.2f} realizado com sucesso. Saldo atual: R${self.saldo:.2f}")

    def depositar(self, valor):
        if not self.validar_transacao():
            return
        if valor <= 0:
            print("O valor do depósito deve ser positivo.")
            return
        
        self.saldo += valor
        self.depositos.append(f"Depósito de R${valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.transacoes_diarias += 1
        print(f"Depósito de R${valor:.2f} realizado com sucesso. Saldo atual: R${self.saldo:.2f}")

    def exibir_extrato(self):
        print("\nExtrato da Conta Bancária:")
        print("Depósitos:")
        print('\n'.join(self.depositos) if self.depositos else "Nenhum depósito realizado.")
        print("\nSaques:")
        print('\n'.join(self.saques) if self.saques else "Nenhum saque realizado.")
        print(f"\nSaldo atual: R${self.saldo:.2f}")

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def cadastrar_usuario(self, nome, cpf, endereco):
        cpf = ''.join(filter(str.isdigit, cpf))
        if any(usuario.cpf == cpf for usuario in self.usuarios):
            print("Usuário já cadastrado com este CPF.")
            return None
        usuario = Usuario(nome, cpf, endereco)
        self.usuarios.append(usuario)
        print(f"Usuário {nome} cadastrado com sucesso.")
        return usuario

    def buscar_usuario_por_cpf(self, cpf):
        return next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)

    def criar_conta(self, cpf):
        usuario = self.buscar_usuario_por_cpf(cpf)
        if not usuario:
            print("Usuário não encontrado.")
            return None
        conta = Conta(usuario)
        self.contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {conta.agencia}, Número: {conta.numero}")
        return conta

    def listar_contas_do_usuario(self, cpf):
        contas_usuario = [conta for conta in self.contas if conta.usuario.cpf == cpf]
        if not contas_usuario:
            print("Nenhuma conta encontrada para este usuário.")
        else:
            print(f"Contas do usuário com CPF {cpf}:")
            for conta in contas_usuario:
                print(f"Agência: {conta.agencia}, Número: {conta.numero}")

    def iniciar_programa(self):
        while True:
            print("\nMenu Principal:")
            print("1. Cadastrar usuário")
            print("2. Criar conta")
            print("3. Listar contas do usuário")
            print("4. Acessar conta")
            print("5. Sair")
            opcao = input("Escolha uma opção (1-5): ")
            
            if opcao == '1':
                nome = input("Digite o nome do usuário: ")
                cpf = input("Digite o CPF do usuário: ")
                endereco = input("Digite o endereço: ")
                self.cadastrar_usuario(nome, cpf, endereco)
            elif opcao == '2':
                cpf = input("Digite o CPF do usuário para criar a conta: ")
                self.criar_conta(cpf)
            elif opcao == '3':
                cpf = input("Digite o CPF do usuário para listar as contas: ")
                self.listar_contas_do_usuario(cpf)
            elif opcao == '4':
                cpf = input("Digite o CPF do usuário para acessar uma conta: ")
                contas_usuario = [conta for conta in self.contas if conta.usuario.cpf == cpf]
                if contas_usuario:
                    conta = contas_usuario[0]
                    while True:
                        print("\nMenu da Conta Bancária:")
                        print("1. Saque")
                        print("2. Depósito")
                        print("3. Extrato")
                        print("4. Voltar")
                        opcao_conta = input("Escolha uma opção (1-4): ")
                        if opcao_conta == '1':
                            valor = float(input("Digite o valor do saque: "))
                            conta.sacar(valor)
                        elif opcao_conta == '2':
                            valor = float(input("Digite o valor do depósito: "))
                            conta.depositar(valor)
                        elif opcao_conta == '3':
                            conta.exibir_extrato()
                        elif opcao_conta == '4':
                            break
                        else:
                            print("Opção inválida.")
                else:
                    print("Nenhuma conta encontrada para este CPF.")
            elif opcao == '5':
                print("Encerrando o programa. Até logo!")
                break
            else:
                print("Opção inválida.")

# Iniciar o sistema bancário
banco = Banco()
banco.iniciar_programa()
