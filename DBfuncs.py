import sqlite3
from tkinter import messagebox
from sqlalchemy import Column, Integer, String, create_engine, and_, func, update
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import local

path =local.Local.local()  #'//NasTecplas/Pintura/DB/pintura.db'
engine = create_engine(r'sqlite:///'+path, echo=False)
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
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def insert(dados):
        pass
    
    @classmethod
    def conteudoTudo(cls,pend):
       conteudoTudo  = [row.as_dict for row in session.query(cls).filter(DBForm_173.pendencia == pend).all()]
       return conteudoTudo
    
    @classmethod
    def conteudoTudoEspecifico(cls, pend, data):
        conteudoTudo  = [row.as_dict for row in session.query(cls).filter(and_(DBForm_173.pendencia == pend, DBForm_173.data_solicitacao == data)).all()]
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
    ini_mistura = Column(String)
    ter_mistura = Column(String)
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
                Término Agitador: {self.ter_agitador}, Início Mistura: {self.ini_mistura}, Término Mistura: {self.ter_mistura}, Início Diluentes: {self.ini_diluentes}, Término Diluentes: {self.ter_diluentes}, 
                Início Indução: {self.ini_inducao}, Término Indução: {self.term_inducao}, Viscosímetro: {self.viscosimetro}, Viscosidade: {self.viscosidade},
                Proporção: {self.proporcao}, Início Adequação: {self.ini_adequacao}, Término Adequação: {self.term_adequacao}, Pot Life: {self.pot_life}, 
                Responsável: {self.responsavel}, Id_form173: {self.Id_form173}, Imprimiu?: {self.print}, Exceção?: {self.excessao}
                """
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [operador.as_dict for operador in session.query(cls).all()]
        return conteudo
    
    def consultaEspecifica(coluna, valor):
        conteudo  = [i.as_dict for i in session.query(DBForm_40).filter(getattr(DBForm_40, coluna) == valor).all()][0]
        return conteudo
    
    def consultaEspecificaDia():
        data_atual = datetime.now().strftime('%d-%m-%Y')
        conteudo  = [i.as_dict for i in session.query(DBForm_40).filter(DBForm_40.data_prep.startswith(data_atual)).all()]
        return conteudo
    
    def obter_ultima_linha():
        ultima_linha = session.query(DBForm_40).order_by(DBForm_40.Id_form_40.desc()).first().as_dict
        return ultima_linha

    def update_print(id_form173):
        with Session() as session:
            query = update(DBForm_40).where(DBForm_40.Id_form173 == id_form173).values(print=0)
            session.execute(query)
            session.commit()


# print(DBForm_40.consultaEspecificaDia())
# print(DBForm_40.consulta())

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


class OCs(Base):
    __tablename__ = 'ocs'
    
    Id_ocs = Column(Integer, primary_key=True)
    oc = Column(Integer)
    quantidade = Column(Integer)
    track_form173 = Column(Integer)
    
    def __repr__(self):
        return f"id: {self.Id_ocs}  -  OC: {self.oc}, Quantidade: {self.quantidade}, Id_form173: {self.track_form173}"
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [oc.as_dict for oc in session.query(cls).all()]
        return conteudo
    
    def consultaEspecifica(arg, coluna):
        consultaEspeficifica = [row.as_dict for row in session.query(OCs).filter(getattr(OCs, coluna) == arg).all()]
        return consultaEspeficifica
    
    def removeOC(id_ocs):
        session.query(OCs).filter_by(Id_ocs=id_ocs).delete()
        session.commit()
        session.close()
    
    def insertOC(id_form173, ocs):
        for i in ocs:
            try:
                nova_oc = OCs(oc=i['oc'], quantidade=i['qnt'], track_form173=id_form173)
                session.add(nova_oc)
            except Exception as e:messagebox.showerror(message=f"Erro: {e} - {type(e)}")
        session.commit()
        session.close()
        messagebox.showinfo("Envio completo", "Informações adicionadas!")


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

