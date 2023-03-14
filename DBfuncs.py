import sqlite3
from tkinter import messagebox
from sqlalchemy import Column, Integer, String, create_engine, and_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

engine = create_engine('sqlite:///pintura.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class DBForm_173(Base):
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
       conteudoTudo  = [row for row in session.query(DBForm_173).filter(DBForm_173.pendencia == pend).all()]
       return conteudoTudo
   
    def conteudoEspecifico(coluna, id_form173):
        conteudoEspecifico = [row[0] for row in session.query(getattr(DBForm_173, coluna)).filter(DBForm_173.Id_form_173 == id_form173).all()]
        return conteudoEspecifico

class DBForm_40(Base):
    __tablename__= 'form_40'
    
    Id_form_40 = Column(Integer, primary_key=True)
    mescla = Column(String)
    data_prep = Column(String)
    temperatura = Column(Integer)
    umidade = Column(Integer)
    cod_mp = Column(String)
    lotemp = Column(String)
    shelf_life = Column(String)
    ini_agitador = Column(String)
    ter_agitador = Column(String)
    ini_diluentes = Column(String)
    ter_diluentes = Column(String)
    ini_inducao = Column(String)
    term_inducao = Column(String)
    viscosimetro = Column(String)
    viscosidade = Column(Integer)
    proporcao = Column(String)
    ini_adequacao = Column(String)
    term_adequacao = Column(String)
    pot_life = Column(String)
    responsavel = Column(String)
    Id_form173 = Column(Integer)
    print = Column(Integer)
    excessao = Column(Integer)
    
    def __repr__(self):
        return f"""
                id: {self.Id_form_40}  -  Mescla: {self.mescla}, Data Preparação: {self.data_prep}, Temperatura: {self.temperatura}, 
                Umidade: {self.umidade}, CEMB: {self.cod_mp}, Lote: {self.lotemp}, Validade: {self.shelf_life}, Início Agitador: {self.ini_agitador}, 
                Término Agitador: {self.ter_agitador}, Início Diluentes: {self.ini_diluentes}, Término Diluentes: {self.ter_diluentes}, 
                Início Indução: {self.ini_inducao}, Término Indução: {self.term_inducao}, Viscosímetro: {self.viscosimetro}, Viscosidade: {self.viscosidade},
                Proporção: {self.proporcao}, Início Adequação: {self.ini_adequacao}, Término Adequação: {self.term_adequacao}, Pot Life: {self.pot_life}, 
                Responsável: {self.responsavel}, Id_form173: {self.Id_form173}, Imprimiu?: {self.print}, Excessão?: {self.excessao}
                """
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [operador.as_dict for operador in session.query(cls).all()]
        return conteudo
    
    def consultaEspecifica(user):
        conteudo  = [i.as_dict for i in session.query(getattr(DBForm_40, user)).all()]
        return conteudo
    
    def obter_ultima_linha():
        ultima_linha = session.query(DBForm_40).order_by(DBForm_40.Id_form_40.desc()).first()
        return ultima_linha

class Operadores(Base):
    __tablename__= 'operadores'
    
    codigo = Column(Integer, primary_key=True)
    nome = Column(String)
    usuario = Column(String)
    senha = Column(String)
    priority = Column(String)    
    
    def __repr__(self):
        return f"Código: {self.codigo}, Nome: {self.nome}, Usuário: {self.usuario}, Prioridade: {self.priority}"
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [operador.as_dict for operador in session.query(cls).all()]
        return conteudo
    
    def consultaEspecifica(cls, user):
        conteudo  = [operador.as_dict for operador in session.query(cls).filter(Operadores.usuario == user).all()]
        return conteudo
    
    
# print(Operadores.consultaEspecifica(Operadores,'levymc'))
# print(Operadores.consulta())
# print(DBForm_40.consulta())
   
class Relacao_Tintas(Base):
    __tablename__ = 'relacao_tintas'
    
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
    
    def consultaViscosimetro(cemb):
        tintas  = [row[0].replace('Copo', '') for row in session.query(Relacao_Tintas.viscosimetro).filter(Relacao_Tintas.cemb == cemb).all()]
        # session.query(Relacao_Tintas).filter(Relacao_Tintas.cemb == cemb).all()
        return tintas
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [tinta.as_dict for tinta in session.query(cls).all()]
        return conteudo
    
    def consultaViscosidade(cls, cemb, valor_selecionado):
        # conteudo  = [viscosidade.as_dict for viscosidade in session.query(cls).filter(Relacao_Tintas.cemb == cemb AND ).all()]
        visc_max_min = session.query(Relacao_Tintas.viscosidade_min, Relacao_Tintas.viscosidade_max)\
                      .filter(and_(Relacao_Tintas.cemb == cemb,
                                    Relacao_Tintas.viscosimetro.like(f'%{valor_selecionado}%')))\
                      .first()
        return visc_max_min
    
# print(Relacao_Tintas.consultaViscosidade(Relacao_Tintas, 1452923, 'Iso'))
        
    
# for i in Relacao_Tintas.consulta():
#     print(i['viscosidade_min'], i['viscosidade_max'])

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
    # print("AQUIII", ocs)
    for i in ocs:
        try:
            cursor.execute(f"INSERT INTO ocs (oc, quantidade,track_form173) VALUES (?,?,?)",
                           (i['oc'], i['qnt'], id_form173))
        except Exception as e:messagebox.showerror(message=f"Erro: {e} - {type(e)}")
    banco.commit()
    cursor.close()
    banco.close()

# print(conteudoForm173_pendente())