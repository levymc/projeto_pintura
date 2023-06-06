from sqlalchemy import Column, Integer, String, create_engine, and_, func, update, exists, select  
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy import exc, desc
import datetime

engine = create_engine(r'sqlite:///static/db/db.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class DBForm_40(Base):
    __tablename__= 'form40'
    
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
    ter_inducao = Column(String)
    viscosimetro = Column(String)
    viscosidade = Column(Integer)
    proporcao = Column(String)
    ini_adequacao = Column(String)
    ter_adequacao = Column(String)
    pot_life = Column(String)
    responsavel = Column(String)
    excessao = Column(Integer)
    
    def __repr__(self):
        return f"""
                id: {self.id}  -  Mescla: {self.mescla}, Data Preparação: {self.data_prep}, Temperatura: {self.temperatura}, 
                Umidade: {self.umidade}, CEMB: {self.cod_mp}, Lote: {self.lotemp}, Validade: {self.shelf_life}, Início Agitador: {self.ini_agitador}, 
                Término Agitador: {self.ter_agitador}, Início Mistura: {self.ini_mistura}, Término Mistura: {self.ter_mistura}, Início Diluentes: {self.ini_diluentes}, Término Diluentes: {self.ter_diluentes}, 
                Início Indução: {self.ini_inducao}, Término Indução: {self.ter_inducao}, Viscosímetro: {self.viscosimetro}, Viscosidade: {self.viscosidade},
                Proporção: {self.proporcao}, Início Adequação: {self.ini_adequacao}, Término Adequação: {self.ter_adequacao}, Pot Life: {self.pot_life}, 
                Responsável: {self.responsavel}, Id_form173: {self.track_form173}, Exceção?: {self.excessao}
                """
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
    @classmethod
    def insert(cls, **kwargs):
        form40_instance = cls(**kwargs)

        ini_agitador = datetime.datetime.strptime(kwargs['ini_agitador'], '%H:%M').time()
        ter_agitador = (datetime.datetime.combine(datetime.date.today(), ini_agitador) + datetime.timedelta(minutes=15)).time()
        form40_instance.ter_agitador = ter_agitador.strftime('%H:%M')

        ini_mistura = datetime.datetime.strptime(kwargs['ini_mistura'], '%H:%M').time()
        ter_mistura = (datetime.datetime.combine(datetime.date.today(), ini_mistura) + datetime.timedelta(minutes=15)).time()
        form40_instance.ter_mistura = ter_mistura.strftime('%H:%M')

        ini_diluentes = datetime.datetime.strptime(kwargs['ini_diluentes'], '%H:%M').time()
        ter_diluentes = (datetime.datetime.combine(datetime.date.today(), ini_diluentes) + datetime.timedelta(minutes=15)).time()
        form40_instance.ter_diluentes = ter_diluentes.strftime('%H:%M')

        ini_inducao = datetime.datetime.strptime(kwargs['ini_inducao'], '%H:%M').time()
        ter_inducao = (datetime.datetime.combine(datetime.date.today(), ini_inducao) + datetime.timedelta(minutes=15)).time()
        form40_instance.ter_inducao = ter_inducao.strftime('%H:%M')

        ini_adequacao = datetime.datetime.strptime(kwargs['ini_adequacao'], '%H:%M').time()
        ter_adequacao = (datetime.datetime.combine(datetime.date.today(), ini_adequacao) + datetime.timedelta(minutes=15)).time()
        form40_instance.ter_adequacao = ter_adequacao.strftime('%H:%M')

        session = Session()
        session.add(form40_instance)
        session.commit()
        session.close()
    
    @classmethod
    def consulta(cls):
        conteudo  = [operador.as_dict for operador in Session.query(cls).all()]
        return conteudo
    
    @classmethod
    def consultaEspecifica(cls, coluna, valor):
        conteudo  = [i.as_dict for i in Session.query(cls).filter(getattr(DBForm_40, coluna) == valor).all()]
        return conteudo
    
    def consultaEspecificaDia():
        data_atual = datetime.now().strftime('%d-%m-%Y')
        conteudo  = [i.as_dict for i in Session.query(DBForm_40).filter(DBForm_40.data_prep.startswith(data_atual)).all()]
        return conteudo
    
    def obter_ultima_linha():
        ultima_linha = Session.query(DBForm_40).order_by(DBForm_40.Id_form_40.desc()).first().as_dict
        return ultima_linha

    def update_print(id_form173):
        with Session() as Session:
            query = update(DBForm_40).where(DBForm_40.Id_form173 == id_form173).values(print=0)
            Session.execute(query)
            Session.commit()


class DBForm_173(Base):
    __tablename__ = 'form173'
   
    id = Column(Integer, primary_key=True)
    mescla = Column(Integer)
    numeroForm = Column(Integer)
    solicitante = Column(String)
    codPintor = Column(Integer)
    cemb = Column(Integer)
    quantidade = Column(Integer)
    unidade = Column(String)
    data = Column(String)
    status = Column(Integer)
    mescla = Column(String)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'mescla': self.mescla,
            'numeroForm': self.numeroForm,
            'solicitante': self.solicitante,
            'codPintor': self.codPintor,
            'cemb': self.cemb,
            'quantidade': self.quantidade,
            'unidade': self.unidade,
            'data': self.data,
            'status': self.status,
            'mescla': self.mescla
        }

    def __repr__(self):
        return str(self.to_dict())
    
    @classmethod
    def get_ultima_linha_form173(cls):
        session = Session()
        ultima_linha = session.query(cls).order_by(desc(cls.id)).first()
        if ultima_linha is not None:
            return ultima_linha.to_dict()
        return None
    
    @classmethod
    def insert(cls, dados):
        session = Session()
        obj = cls(**dados)
        session.add(obj)
        try:
            session.commit()
            session.refresh(obj)  # Atualiza o objeto com os valores do banco de dados, incluindo o ID gerado
            return obj.to_dict()  # Retorna um dicionário com os valores do objeto
        except exc.SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    
    @classmethod
    def conteudoTudoEspecifico(cls, status, data):
        session = scoped_session(sessionmaker(bind=engine))
        conteudoTudo = session.query(cls).filter(and_(DBForm_173.status == status, DBForm_173.data == data)).all()
        session.close()
        return [row.to_dict() for row in conteudoTudo]
    
    @classmethod
    def conteudoTudo(cls, pend):
        session = Session()
        conteudoTudo = [row.to_dict() for row in session.query(cls).filter(DBForm_173.pendencia == pend).all()]
        session.close()
        return conteudoTudo
    
    @classmethod
    def conteudoTudoEspecificoDia(cls):
        data_atual = datetime.now().strftime('%d-%m-%Y')
        session = Session()
        conteudoTudo = [row.to_dict() for row in session.query(cls).filter(DBForm_173.data_solicitacao.startswith(data_atual)).all()]
        session.close()
        return conteudoTudo

    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        session = Session()
        consultaEspecifica = [row.to_dict() for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        session.close()
        return consultaEspecifica
    
    @classmethod
    def update_form_173(cls, id_form_173, formulario=None, solicitante=None, data_solicitacao=None, cemb=None, quantidade=None, unidade=None, status=None, pintor=None):
        session = Session()
        form_173 = session.query(cls).filter_by(id=id_form_173).first()
        if form_173:
            if formulario is not None:
                form_173.mescla = formulario
            if solicitante is not None:
                form_173.solicitante = solicitante
            if data_solicitacao is not None:
                form_173.numeroForm = data_solicitacao
            if cemb is not None:
                form_173.cemb = cemb
            if quantidade is not None:
                form_173.quantidade = quantidade
            if unidade is not None:
                form_173.unidade = unidade
            if status is not None:
                form_173.status = status
            if pintor is not None:
                form_173.codPintor = pintor

            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False


class DBForm_161(Base):
    __tablename__ = 'form161'
    
    id = Column(Integer, primary_key=True)
    track_form173 = Column(Integer)
    data = Column(String)
    usuario = Column(String)
    
    def to_dict(self):
        return {
            'id': self.id,
            'track_form173': self.track_form173,
            'data': self.data,
            'usuario': self.usuario
        }
    
    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        consultaEspeficifica = [row.as_dict for row in Session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        return consultaEspeficifica
    
    @classmethod
    def insert(cls, dados):
        session = Session()
        obj = cls(**dados)
        session.add(obj)
        try:
            session.commit()
            session.refresh(obj)  # Atualiza o objeto com os valores do banco de dados, incluindo o ID gerado
            return obj.to_dict()  # Retorna um dicionário com os valores do objeto
        except exc.SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    
    @staticmethod
    def ultimoId():
        # Crie uma consulta para encontrar o último ID
        consulta = select(DBForm_161.Id_form_161).order_by(DBForm_161.Id_form_161.desc()).limit(1)

        # Execute a consulta e obtenha o resultado
        resultado = Session.execute(consulta).fetchone()

        # Se o resultado for None, a tabela está vazia
        if resultado is None:
            ultimo_id = 0
        else:
            ultimo_id = resultado[0]
        return ultimo_id


class Operadores(Base):
    __tablename__ = 'operadores'
    
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
        with Session() as session:
            conteudo = [operador.as_dict for operador in session.query(cls).all()]
            return conteudo
    
    @classmethod
    def consultaEspecifica(cls, user):
        with Session() as session:
            conteudo = [operador.as_dict for operador in session.query(cls).filter(Operadores.usuario == user).all()]
            return conteudo
   
    @classmethod
    def consultaEspecificaCodigo(cls, codigo):
        with Session() as session:
            conteudo = [operador.as_dict for operador in session.query(cls).filter(Operadores.codigo == codigo).all()]
            return conteudo
    
    @classmethod
    def conferenciaOperador(cls, codigoOperador): 
        with Session() as session:
            result = session.query(exists().where(cls.codigo == codigoOperador)).scalar()
            return result
    
    @classmethod
    def confereUsuario(cls, userInput): 
        with Session() as session:
            result = session.query(cls).filter_by(usuario=userInput).first()
            return result

print(Operadores.consultaEspecificaCodigo(18880))

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
        conteudo  = [oc.as_dict for oc in Session.query(cls).all()]
        return conteudo
    
    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        session = Session()
        consultaEspeficifica = [row.as_dict for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        return consultaEspeficifica
    
    @classmethod
    def removeOC(cls, oc_id):
        session = Session()
        oc = session.query(cls).filter_by(id=oc_id).first()
        if oc:
            session.delete(oc)
            session.commit()
            print("OC removido com sucesso!")
        else:
            print("OC não encontrado!")
        
        
    @staticmethod
    def ultimoId():
        consulta = select(OCs.Id_ocs).order_by(OCs.Id_ocs.desc()).limit(1)
        resultado = Session.execute(consulta).fetchone()
        if resultado is None:
            ultimo_id = 0
        else:
            ultimo_id = resultado[0]
        return ultimo_id

    
    def insertOC(id_form173, ocs):
        with Session.begin() as session:
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
    graph = Column(String)
    
    def to_dict(self):
        return {
            'cemb': self.cemb,
            'descricao': self.descricao,
            'norma': self.norma,
            'norma_embraer': self.norma_embraer,
            'pressao_especificada': self.pressao_especificada,
            'flash_off': self.flash_off,
            'temperatura_secagem': self.temperatura_secagem,
            'viscosidade_min': self.viscosidade_min,
            'viscosidade_max': self.viscosidade_max,
            'viscosimetro': self.viscosimetro,
            'bico': self.bico,
            'pot_life': self.pot_life,
            'graph': self.graph
        }


    def __repr__(self):
        return str(self.to_dict())
    
    @classmethod
    def consultaViscosimetro(cls, cemb):
        session = Session()
        tintas = session.query(cls.viscosimetro).filter(cls.cemb == cemb).all()
        tintas = [row[0].replace('Copo', '') for row in tintas]
        return tintas
    
    @classmethod
    def insert(cls, dados):
        session = Session()
        obj = cls(**dados)
        session.add(obj)
        try:
            session.commit()
            session.refresh(obj)  # Atualiza o objeto com os valores do banco de dados, incluindo o ID gerado
            return obj.to_dict()  # Retorna um dicionário com os valores do objeto
        except exc.SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        session = Session()
        conteudo  = [tinta.as_dict for tinta in session.query(cls).all()]
        return conteudo
    
    def consultaViscosidade(cls, cemb, valor_selecionado):
        # conteudo  = [viscosidade.as_dict for viscosidade in Session.query(cls).filter(Relacao_Tintas.cemb == cemb AND ).all()]
        visc_max_min = Session.query(Relacao_Tintas.viscosidade_min, Relacao_Tintas.viscosidade_max)\
                      .filter(and_(Relacao_Tintas.cemb == cemb,
                                    Relacao_Tintas.viscosimetro.like(f'%{valor_selecionado}%')))\
                      .first()
        return visc_max_min
    
    def conferenciaMescla(cembMescla): 
        session = Session()
        result = session.query(exists().where(Relacao_Tintas.cemb == cembMescla)).scalar()
        return result
    
    @classmethod
    def consultaEspecifica(cls, arg, coluna):
        session = Session()
        consultaEspecifica = [row.to_dict() for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
        session.close()
        return consultaEspecifica

# print(Relacao_Tintas.consultaEspecifica(917221, 'cemb'))