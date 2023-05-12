#######################################################
# Este programa permite que usuários façam login ou se cadastrem
# e armazena suas informações em um arquivo JSON.
# O sistema de armazenamento utiliza dicionários, o dicionário 'Usuarios'
# terá dentro de si outros dicionários, cada um com o nome de um usuário e sua senha.
#######################################################

import json

# A função a seguir é responsável pela leitura das informações do arquivo JSON
def carregar_usuarios():
    try:
        with open('Usuarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# E essa função, pelo armazenamento das informações de login no arquivo JSON
def salvar_usuarios(Usuarios):
    with open('Usuarios.json', 'w') as f:
        json.dump(Usuarios, f)

# Essa é a função que abriga todo o código responsável pelo login.
def login():
    while True:
        nome = input("Olá, informe seu nome de usuário: ")
        if (nome in Usuarios):
            senha = int(input(f"Bem-vindo de volta, {nome}! Informe sua senha: "))
            if (senha == Usuarios[nome]["Senha"]):
                print(f"Acesso permitido para o usuário '{nome}'.")
                return # encerra a função login() com sucesso
            else:
                print("Senha incorreta, tente novamente.")
        else:
            print("Nome de usuário não encontrado.")
            opcao = input("Digite '1' para tentar novamente ou '2' para cadastrar um novo usuário: ")
            if opcao == "2":
                cadastrar_usuario()
            elif opcao != "1":
                print("Opção inválida, encerrando o programa.")
                return # encerra a função login() com falha

def cadastrar_usuario():
    while True:
        nome = input("Informe um nome de usuário: ")
        if(nome in Usuarios.keys()):
            print("Este nome de usuário já existe, tente outro.")
            # Caso o nome de usuário já exista, é solicitado que o usuário informe outro nome.
        else:
            try:
                senha = int(input("Informe uma senha: "))
            except:
                print("Ops, erro 0x1. Provavelmente sua senha contém letras (somente números são permitidos).")
                # Caso a senha contenha letras em vez de números, é solicitado que o usuário informe outra senha.
            else:
                Usuarios[nome] = {"User": nome, "Senha": senha} # Se o nome de usuário escolhido e a senha informada forem válidos, o novo usuário é cadastrado.
                print(f"Usuário '{nome}' cadastrado com sucesso!")
                salvar_usuarios(Usuarios)
                return

def excluir_conta():
    nome = input("Informe seu nome de usuario... ")
    if(nome in Usuarios.keys()):
        senha = int(input("Informe a senha de sua conta... "))
        if(senha == Usuarios[nome]["Senha"]):
            print("Excluindo conta do sistema...\n")
            del Usuarios[nome]            
            print("Conta Excluida com sucesso.")
            salvar_usuarios(Usuarios)
        else:
            print("Senha incorreta, tente novamente.")
            excluir_conta()
    else:
        print("Usuario inexistente.")
        excluir_conta();

# Programa principal
Usuarios = carregar_usuarios() # Esse código anexa as informações do JSON na variável DICT "Usuarios"
opcao = input("Digite '1' para fazer login, '2' para cadastrar um novo usuário ou '3' para excluir sua conta: ")
if(opcao == "1"):
    login()
elif(opcao == "2"):
    cadastrar_usuario()
elif(opcao == "3"):
    excluir_conta()
else:
    print("Opção invalida")
