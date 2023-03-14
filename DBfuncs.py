import sqlite3
from tkinter import messagebox
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///pintura.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Form_173(Base):
    __tablename__='form_173'
    
    Id_form_173 = Column(Integer, primary_key=True)
    formulario = Column(Integer)
    solicitante = Column(String)
    data_solicitacao = Column(String)
    cemb = Column(String)
    quantidade = Column(Integer)
    unidade = Column(String)
    pendencia = Column(Integer)
    pintor = Column(Integer)
    
    def __repr__(self):
        return f"""id: {self.Id_form_173} -  Formulário: {self.formulario}, Solicitante: {self.solicitante}, Data: {self.data_solicitacao},
        CEMB: {self.cemb}, Quantidade: {self.quantidade}, Unidade: {self.unidade}, Pintor: {self.pintor}    
    """
    
    def insert(dados):
        pass
    
    def conteudoTudo(pend):
       conteudoTudo  = [row for row in session.query(Form_173).filter(Form_173.pendencia == pend).all()]
       return conteudoTudo
   
    def conteudoEspecifico(coluna, id_form173):
        conteudoEspecifico = [row[0] for row in session.query(getattr(Form_173, coluna)).filter(Form_173.Id_form_173 == id_form173).all()]
        return conteudoEspecifico
   
class Relacao_Tintas(Base):
    __tablename__='relacao_tintas'
    
    cemb = Column(Integer, primary_key=True)
    descricao = Column(String)
    norma = Column(String)
    norma_embraer = Column(String)
    pressao_especificada = Column(String)
    flash_off = Column(String)
    temperatura_secagem = Column(String)
    viscosidade_min = Column(Integer)
    viscosidade_max = Column(Integer)
    viscosimetro = Column(String)
    bico = Column(String)
    pot_life = Column(String)
    
    def __repr__(self):
        return f"CEMB: {self.cemb}  -  Viscosidade: {self.viscosidade_min}s ~ {self.viscosidade_max}s  - Copo: {self.viscosimetro.replace('Copo', '')}"
    
    def consulta(cemb):
        tintas  = [row[0] for row in session.query(Relacao_Tintas.viscosimetro).filter(Relacao_Tintas.cemb == cemb).all()]
        # session.query(Relacao_Tintas).filter(Relacao_Tintas.cemb == cemb).all()
        return tintas
    

# for i in Form_173.conteudoEspecifico('cemb', 2):
#     print(i)

# for i in Relacao_Tintas.consulta(91721):
#     print("_________________________________________________________\n")
#     print(i)

def conteudoForm173_pendente(db):
    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    conteudo = cursor.execute(f"SELECT * FROM form_173 WHERE pendencia=1").fetchall()
    cursor.close()
    banco.close()
    return conteudo

def insertOC(id_form173, ocs, db):
    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    print("AQUIII", ocs)
    for i in ocs:
        try:
            cursor.execute(f"INSERT INTO ocs (oc, quantidade,track_form173) VALUES (?,?,?)",
                           (i['oc'], i['qnt'], id_form173))
        except Exception as e:messagebox.showerror(message=f"Erro: {e} - {type(e)}")
    banco.commit()
    cursor.close()
    banco.close()

# print(conteudoForm173_pendente())