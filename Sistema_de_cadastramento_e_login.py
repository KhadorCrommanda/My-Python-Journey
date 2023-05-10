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
        with open('usuarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# E essa função, pelo armazenamento das informações de login no arquivo JSON
def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f)

## Sistema principal
Usuarios = carregar_usuarios() # Esse código anexa as informações do JSON na variável DICT "Usuarios"

# Essa é a função que abriga todo o código responsável pelo login.
def login():
    nome = input("Olá, informe seu nome de usuário: ")
    if(nome in Usuarios.keys()):
        senha = int(input(f"Bem-vindo de volta, {nome}! Informe sua senha: "))
        # Se o nome que o usuário escrever for uma das chaves do dicionário 'Usuarios',
        # será solicitada a senha (ou seja, o valor da chave).
        if(senha == Usuarios[nome]["Senha"]):
            print(f"Acesso permitido para o usuário '{nome}'.")
            # Após o usuário escrever seu nome de usuário e sua senha, será exibida uma mensagem de finalização.
        else:
            print("Senha incorreta, tente novamente.")
            login() # Se o usuário digitar uma senha incorreta, será solicitada novamente.
    else:
        Usuarios[nome] = {"User": nome, "Senha": 1234} # Caso o nome de usuário não exista, é criado um novo usuário com senha padrão 1234.
        print(f"Seu nome de usuário '{nome}' foi registrado com sucesso! Use a senha padrão '1234' para fazer o login.")
        salvar_usuarios(Usuarios)
        login()

def cadastrar_usuario():
    nome = input("Informe um nome de usuário: ")
    if(nome in Usuarios.keys()):
        print("Este nome de usuário já existe, tente outro.")
        cadastrar_usuario() # Caso o nome de usuário já exista, é solicitado que o usuário informe outro nome.
    else:
        try:
            senha = int(input("Informe uma senha: "))
        except:
            print("Ops, erro 0x1. Provavelmente sua senha contém letras (somente números são permitidos).")
            cadastrar_usuario() # Caso a senha contenha letras em vez de números, é solicitado que o usuário informe outra senha.
        else:
            Usuarios[nome] = {"User": nome, "Senha": senha} # Se o nome de usuário escolhido e a senha informada forem válidos, o novo usuário é cadastrado.
            print(f"Usuário '{nome}' cadastrado com sucesso!")
            salvar_usuarios(Usuarios)

# Programa principal
opcao = input("Digite '1' para fazer login ou '2' para cadastrar um novo usuário: ")
if(opcao == "1"):
    login()
elif(opcao == "2"):
    cadastrar_usuario()
else:
    print("Opção invalida")