from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(Integer)
    home_address = Column(String)

    bank_accounts = relationship('Account', back_populates='user')


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_type = Column(String)
    account_num = Column(Integer)
    bank_agency = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='bank_accounts')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
with Session() as session:
    
    cerafiao = User(
        name = 'Cerafiao Silva Pinto',
        cpf = 12345678901,
        home_address = 'Algum lugar'
    )
    mauro = User(
        name='Mauro da Silva Rocha',
        cpf=41251256467,
        home_address='Outro lugar',
        bank_accounts=[Account(
            account_type="Corrente",
            account_num=1,
            bank_agency='0001'
        )]
    )
    session.add_all([cerafiao, mauro])
 
    cerafiao = session.query(User).filter_by(name='Cerafiao Silva Pinto').first()

    if cerafiao is not None:
        print(f"User ID: {cerafiao.id}")
        print(f"Name: {cerafiao.name}")
        print(f"CPF: {cerafiao.cpf}")
        print(f"Home Address: {cerafiao.home_address}")
    else:
        print("Usuário não encontrado.")
