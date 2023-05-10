import sqlite3
from sqlalchemy import Column, Integer, String, create_engine, and_, func, update, exists, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import local
from sqlalchemy import exc

path =local.Local.local()  #'//NasTecplas/Pintura/DB/pintura.db'
engine = create_engine(r'sqlite:///static/db/db.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class SQlite_Sequence(Base):
    __tablename__ = "sqlite_sequence"
    name = Column(String, primary_key=True)
    seq = Column(Integer)


class DBForm_161(Base):
    __tablename__ = 'form_161'
    
    Id_form_161 = Column(Integer, primary_key=True)
    track_form173 = Column(Integer)
    print = Column(Integer)
    
    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        consultaEspeficifica = [row.as_dict for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        return consultaEspeficifica
    
    @classmethod
    def insert(cls, track_form173, print):
        form_161 = cls(track_form173=track_form173, print=print)
        session.add(form_161)
        session.commit()
        return form_161

    
    @staticmethod
    def ultimoId():
        # Crie uma consulta para encontrar o último ID
        consulta = select(DBForm_161.Id_form_161).order_by(DBForm_161.Id_form_161.desc()).limit(1)

        # Execute a consulta e obtenha o resultado
        resultado = session.execute(consulta).fetchone()

        # Se o resultado for None, a tabela está vazia
        if resultado is None:
            ultimo_id = 0
        else:
            ultimo_id = resultado[0]
        return ultimo_id
    

class DBForm_173(Base):
    __tablename__ = 'form173'
    
    id = Column(Integer, primary_key=True)
    numeroForm = Column(Integer)
    solicitante = Column(String)
    codPintor = Column(Integer)
    cemb = Column(Integer)
    quantidade = Column(Integer)
    unidade = Column(String)
    data = Column(String)
    status = Column(Integer)
    
    def to_dict(self):
        return {
            'id': self.id,
            'numeroForm': self.numeroForm,
            'solicitante': self.solicitante,
            'codPintor': self.codPintor,
            'cemb': self.cemb,
            'quantidade': self.quantidade,
            'unidade': self.unidade,
            'data': self.data,
            'status': self.status
        }

    def __repr__(self):
        return str(self.to_dict())
    
    @classmethod
    def insert(cls, dados):
        obj = cls(**dados)
        session.add(obj)
        try:
            session.commit()
        except exc.SQLAlchemyError:
            session.rollback()
            raise
        return obj
    
    @classmethod
    def conteudoTudo(cls,pend):
       conteudoTudo  = [row.to_dict for row in session.query(cls).filter(DBForm_173.pendencia == pend).all()]
       return conteudoTudo
    
    @classmethod
    def conteudoTudoEspecifico(cls, status, data):
        conteudoTudo  = [row.to_dict() for row in session.query(cls).filter(and_(DBForm_173.status == status, DBForm_173.data == data)).all()]
        return conteudoTudo
    
    @classmethod
    def conteudoTudoEspecificoDia(cls):
        data_atual = datetime.now().strftime('%d-%m-%Y')
        conteudoTudo  = [row.to_dict for row in session.query(cls).filter((DBForm_173.data_solicitacao.startswith(data_atual))).all()]
        return conteudoTudo

    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        consultaEspeficifica = [row.to_dict for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        return consultaEspeficifica
    
    @classmethod
    def update_form_173(cls, id_form_173, formulario=None, solicitante=None, data_solicitacao=None, cemb=None, quantidade=None, unidade=None, pendencia=None, pintor=None, print=None):
        form_173 = session.query(cls).filter_by(Id_form_173=id_form_173).first()
        if form_173:
            if formulario is not None:
                form_173.formulario = formulario
            if solicitante is not None:
                form_173.solicitante = solicitante
            if data_solicitacao is not None:
                form_173.data_solicitacao = data_solicitacao
            if cemb is not None:
                form_173.cemb = cemb
            if quantidade is not None:
                form_173.quantidade = quantidade
            if unidade is not None:
                form_173.unidade = unidade
            if pendencia is not None:
                form_173.pendencia = pendencia
            if pintor is not None:
                form_173.pintor = pintor
            if print is not None:
                form_173.print = print

            session.commit()
            return True
        else:
            return False


class DBForm_40(Base):
    __tablename__= 'form_40'
    
    id = Column(Integer, primary_key=True)
    track_form173 = Column(Integer)
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
    
    @classmethod
    def consultaEspecifica(cls, coluna, valor):
        conteudo  = [i.as_dict for i in session.query(cls).filter(getattr(DBForm_40, coluna) == valor).all()]
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
   
    @classmethod
    def consultaEspecificaCodigo(cls, codigo):
        conteudo  = [operador.as_dict for operador in session.query(cls).filter(Operadores.codigo == codigo).all()]
        return conteudo
    
    def conferenciaOperador(codigoOperador): 
        result = session.query(exists().where(Operadores.codigo == codigoOperador)).scalar()
        return result
    
    @classmethod
    def confereUsuario(cls, userInput): 
        result = session.query(cls).filter_by(usuario=userInput).first()
        return result
    

class OCs(Base):
    __tablename__ = 'ocs'
    
    id = Column(Integer, primary_key=True)
    track_form173 = Column(Integer)
    oc = Column(Integer)
    quantidade = Column(Integer)
    
    def __repr__(self):
        return f"id: {self.Id_ocs}  -  OC: {self.oc}, Quantidade: {self.quantidade}, Id_form173: {self.track_form173}"
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [oc.as_dict for oc in session.query(cls).all()]
        return conteudo
    
    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        consultaEspeficifica = [row.as_dict for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        return consultaEspeficifica
    
    @staticmethod
    def removeOC(id_ocs):
        # Removendo a OC
        session.query(OCs).filter_by(Id_ocs=id_ocs).delete()
        
        # Atualizando o sqlite_sequence
        query = update(SQlite_Sequence).where(SQlite_Sequence.name == 'ocs').values(name=OCs.ultimoId())
        session.execute(query)
        
        session.commit()
        
    @staticmethod
    def ultimoId():
        # Crie uma consulta para encontrar o último ID
        consulta = select(OCs.Id_ocs).order_by(OCs.Id_ocs.desc()).limit(1)

        # Execute a consulta e obtenha o resultado
        resultado = session.execute(consulta).fetchone()

        # Se o resultado for None, a tabela está vazia
        if resultado is None:
            ultimo_id = 0
        else:
            ultimo_id = resultado[0]
        return ultimo_id

    
    def insertOC(id_form173, ocs):
        for i in ocs:
            try:
                nova_oc = OCs(oc=i['oc'], quantidade=i['qnt_solicitada'], track_form173=id_form173)
                session.add(nova_oc)
            except Exception as e: print("Erro: {e} - {type(e)}")
        session.commit()
        print("Envio completo", "Informações adicionadas!")
  

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
    
    def conferenciaMescla(cembMescla): 
        result = session.query(exists().where(Relacao_Tintas.cemb == cembMescla)).scalar()
        return result
