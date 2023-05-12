from sqlalchemy import Column, Integer, String, create_engine, and_, func, update, exists, select  
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy import exc

engine = create_engine(r'sqlite:///static/db/db.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


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
    def update_form_173(cls, id_form_173, formulario=None, solicitante=None, data_solicitacao=None, cemb=None, quantidade=None, unidade=None, pendencia=None, pintor=None, print=None):
        session = Session()
        form_173 = session.query(cls).filter_by(id=id_form_173).first()
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

            Session.commit()
            return True
        else:
            return False


dados1 = {'numeroForm': 2323131231232,
            'solicitante': '2',
            'codPintor': 1,
            'cemb': 1,
            'quantidade': 1,
            'unidade': '1',
            'data': '1',
            'status': 1}

# print(DBForm_173.insert(dados1))

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
        with Session.begin() as session:
            consultaEspeficifica = [row.as_dict for row in session.query(cls).filter(getattr(cls, coluna) == arg).all()]
            return consultaEspeficifica
    
    @staticmethod
    def removeOC(id_ocs):
        # Removendo a OC
        Session.query(OCs).filter_by(Id_ocs=id_ocs).delete()
        
        # Atualizando o sqlite_sequence
        query = update(SQlite_Sequence).where(SQlite_Sequence.name == 'ocs').values(name=OCs.ultimoId())
        Session.execute(query)
        
        Session.commit()
        
    @staticmethod
    def ultimoId():
        # Crie uma consulta para encontrar o último ID
        consulta = select(OCs.Id_ocs).order_by(OCs.Id_ocs.desc()).limit(1)

        # Execute a consulta e obtenha o resultado
        resultado = Session.execute(consulta).fetchone()

        # Se o resultado for None, a tabela está vazia
        if resultado is None:
            ultimo_id = 0
        else:
            ultimo_id = resultado[0]
        return ultimo_id

    
    def insertOC(id_form173, ocs):
        with Session.begin() as session:
            print(1)
            for i in ocs:
                print(2)
                try:
                    nova_oc = OCs(oc=i['oc'], quantidade=i['qnt_solicitada'], track_form173=id_form173)
                    print(3)
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
        tintas  = [row[0].replace('Copo', '') for row in Session.query(Relacao_Tintas.viscosimetro).filter(Relacao_Tintas.cemb == cemb).all()]
        # Session.query(Relacao_Tintas).filter(Relacao_Tintas.cemb == cemb).all()
        return tintas
    
    @hybrid_property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def consulta(cls):
        conteudo  = [tinta.as_dict for tinta in Session.query(cls).all()]
        return conteudo
    
    def consultaViscosidade(cls, cemb, valor_selecionado):
        # conteudo  = [viscosidade.as_dict for viscosidade in Session.query(cls).filter(Relacao_Tintas.cemb == cemb AND ).all()]
        visc_max_min = Session.query(Relacao_Tintas.viscosidade_min, Relacao_Tintas.viscosidade_max)\
                      .filter(and_(Relacao_Tintas.cemb == cemb,
                                    Relacao_Tintas.viscosimetro.like(f'%{valor_selecionado}%')))\
                      .first()
        return visc_max_min
    
    def conferenciaMescla(cembMescla): 
        result = Session.query(exists().where(Relacao_Tintas.cemb == cembMescla)).scalar()
        return result
