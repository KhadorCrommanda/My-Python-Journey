#################################################################
#Sistema bancario feito por KhadorCrommanda.
#O script criará dois arquivos o primeiro chamado 'operacoes.txt' 
#serve para armazenar todos os movimentos financeiros.
#e 'dados_bancarios.json' que serve para armazenar 
#################################################################
import json

limite = 500.00
limite_saques = 3

def carregar_dados():
    try:
        with open('dados_bancarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open('dados_bancarios.json', 'w') as f:
           json.dump({'saldo' : 0.00, 'saques_efetuados' : 0}, f)
           return {'saldo' : 0.00, 'saques_efetuados' : 0}

def extrato():
    try:
        with open('operacoes.txt', 'r') as f:
            conteudo = f.read()
            print("-------- Extrato --------\n")
            print(conteudo)
    except FileNotFoundError:
        print("Nenhuma operação encontrada.")
        with open('operacoes.txt', 'w') as f:
            f.write("")
        return 

def deposito(dados_bancarios):
    saldo = dados_bancarios["saldo"]
    while True:
        try:
            opcao = float(input("Qual o valor do depósito? "))
            if opcao > 0.0:
                saldo += opcao
                dados_bancarios['saldo'] = saldo
                
                with open('dados_bancarios.json', 'w') as f:
                    json.dump(dados_bancarios, f)

                with open('operacoes.txt', 'a') as f:
                    historico = f"Deposito de R$ {opcao}\n"
                    f.write(historico)
                print(f"Depósito de R$ {opcao} realizado com sucesso!")
                return
            else:
                print("O valor a ser depositado deve ser maior que zero. Tente novamente...")
        except ValueError:
            print("Por favor, insira apenas números.")

def saque(dados_bancarios):
    saldo = dados_bancarios["saldo"]
    numero_saques = dados_bancarios["saques_efetuados"]
    while True:
        try:
            opcao = float(input("Qual o valor a ser sacado? "))
            if opcao <= 0.0:
                print("O valor a ser sacado deve ser maior que zero. Tente novamente...")
            elif opcao > saldo:
                print("Saldo insuficiente. Tente novamente...")
            elif numero_saques >= limite_saques:
                print(f"Limite máximo de saques diários atingido ({limite_saques}). Tente novamente amanhã...")
                break
            elif opcao > limite:
                print(f"Valor do saque excedido. A quantia máxima para saques é de R$ {limite}. Tente novamente...")
            else:
                saldo -= opcao
                numero_saques += 1
                   
                with open('dados_bancarios.json', 'w') as f:
                    dados_bancarios['saldo'] = saldo
                    dados_bancarios['saques_efetuados'] = numero_saques
                    json.dump(dados_bancarios, f)
                
                with open('operacoes.txt', 'a') as f:
                    historico = f"Saque de R$ {opcao}\n"
                    f.write(historico)
                print(f"Saque de R$ {opcao} realizado com sucesso!")
                return
        except ValueError:
            print("Por favor, insira apenas números.")

def entrada():
    dados_bancarios = carregar_dados()
    menu = """
    Bem-vindo ao menu do Sistema Bancário CROMMANDA'S LTDA
    Escreva [D] para depositar um valor
    [S] para sacar
    [E] para exibir seu extrato.
    [Q] para sair.
    """
    while True:
        opção = input(menu)
        if(opção == 'S'):
            print("Iniciando, espere um momento...")
            saque(dados_bancarios)
            return
        elif(opção == 'D'):
            print("Iniciando protocolo de deposito...")
            deposito(dados_bancarios)
            return
        elif(opção == 'E'):
            print("Espere um momento...")
            extrato()
            return
        elif(opção == 'Q'):
            print("Compreensivel, tenha um bom dia!")
            break
        else:
            print("Opção invalida. Por favor selecione novamente a operação desejada.")
entrada()