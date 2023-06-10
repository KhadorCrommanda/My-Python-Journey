from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "url of your mongodb atlas"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Usuario logado com sucesso. Conexão efetuada com o banco de dados MongoDB.")
except Exception as e:
    print(e)
    
    
db = client['your cluster name']
#db.create_collection('Bank') uncomment if you dont have runned this code before
colection = db['Bank']

mauro = {
    
    'Nome': "Mauro",
    'Cpf': 4125154646,
    'Endereço': "Algum outro lugar",
    'BankAccounts': {
        '1':{
            'Agencia': '0001',
            'Tipo': 'Corrente',
            'Saldo': 500.00,
            'Saques realizados': 1,
            'Transações': []
        }
    }
}
joe_goes = {
    
    'Nome': "Joe Goes",
    'Cpf': 98765432101,
    'Endereço': 'idk'
}

#result = colection.insert_many([mauro, joe_goes]) uncomment if you dont have iniciate this code before

cpf_pesquisa = 98765432101

criterio = {"Cpf": cpf_pesquisa}

documento = colection.find_one(criterio)

if documento:
    nome = documento['Nome']
    print(f'Usuario encontrado! Nome: {nome}')
else:
    print("Usuário não encontrado.")
