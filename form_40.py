from tkinter import *
from tkinter import messagebox, ttk
import hashlib, json, sqlite3, re, login_processo
from datetime import timedelta
from datetime import datetime

def validar_horario(novo_valor):
    """Função de validação para aceitar apenas horários no formato HH:MM"""
    # Verifica se o novo valor contém apenas números e dois pontos
    if re.match(r'^\d\d:\d\d$', novo_valor) is not None:
        # Verifica se as horas e minutos estão dentro dos limites válidos
        horas, minutos = novo_valor.split(':')
        if 0 <= int(horas) <= 23 and 0 <= int(minutos) <= 59:
            return True
    return False

def opcoesViscosimetros(db, id_form173):
        opcoesViscosimetros = []
        try:
            banco = sqlite3.connect(db)
            cursor = banco.cursor()
            cemb_tinta = cursor.execute(f"SELECT cemb FROM form_173 WHERE Id_form_173 = {id_form173}").fetchall()[0][0]
            new_cemb = ''
            for i in cemb_tinta:
                if not i=="E":
                    new_cemb += i
            opcoes = cursor.execute(f"SELECT viscosimetro FROM relacao_tintas WHERE cemb = {int(new_cemb)}").fetchall()
            cursor.close()
            banco.close()
            
            for copo in opcoes:
                copo = copo[0].replace("Copo", "").replace("COPO", "")
                opcoesViscosimetros.append(copo)
            
            return opcoesViscosimetros
        except Exception as ex:
            print("Error: ", ex, type(ex))

def conteudo_form173(db):
        try:
                banco = sqlite3.connect(db)
                cursor = banco.cursor()
        except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
        cursor.execute("SELECT * FROM form_173")
        conteudo = cursor.fetchall()
        tamanho = len(conteudo)
        cursor.close()
        banco.close()
        return conteudo, tamanho

def conteudo_form40(db):
        try:
                banco = sqlite3.connect(db)
                cursor = banco.cursor()
        except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
        cursor.execute("SELECT * FROM form_40")
        conteudo = cursor.fetchall()
        tamanho = len(conteudo)
        cursor.close()
        banco.close()
        return conteudo, tamanho

def ultima_mescla(db):
        try:
                banco = sqlite3.connect(db)
                cursor = banco.cursor()
        except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
        
        if (len(cursor.execute("SELECT mescla FROM form_40").fetchall()) != 0):
                ultima_mescla = cursor.execute("SELECT mescla FROM form_40").fetchall()[-1][0]
        else:
                ultima_mescla = '23-000'
        cursor.close()
        banco.close()
        return ultima_mescla
def somar_mescla(db):
        x = ultima_mescla(db)
        x_sep = x.split('-')
        prox = int(x_sep[1])+1
        if len(str(prox))==4:
                return "23-"+str(prox)
        elif len(str(prox))==3:
                return "23-0"+str(prox)
        elif len(str(prox))==2:
                return "23-00"+str(prox)
        elif len(str(prox))==1:
                return "23-000"+str(prox)
        else: print("O número da mescla está inválido!")

class Form_40(Toplevel):
        def __init__(self, id_form173, user, db):
                self.db = db
                super().__init__()
                try:
                        banco = sqlite3.connect(self.db)
                        cursor = banco.cursor()
                except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
                self.geometry("1280x230")
                self.title('Form_40')
                self.configure(bg='white')
                self.iconbitmap(r'logo.ico')
                self.loadimage_form40 = PhotoImage(file=r"form_40.png")
                self.img_frame = Label(self, image=self.loadimage_form40, background='white')
                self.img_frame.place(x=0,y=0)
                self.agora = datetime.today().strftime('%d-%m-%Y %H:%M')
                self.conteudo_form173,self._ = conteudo_form173(self.db)
                self.user = user
                self.id_form173 = id_form173
                self.resizable(0,0)
                cursor.execute(f"SELECT codigo FROM operadores WHERE usuario='{self.user}'")
                self.cod_ope = cursor.fetchall()[0][0]
                cursor.execute(f"SELECT cemb FROM form_173 WHERE Id_form_173 = {self.id_form173}")
                self.cod_mp = cursor.fetchall()
                ultima_mesc = ultima_mescla(self.db)
                self.mescla_atual = somar_mescla(self.db)
                self.create_wigets() # chama a função que cria os widgets
                cursor.close()
                banco.close()

        def create_wigets(self):
                self.mescla_field = Label(self, text=self.mescla_atual, font="Arial 8 bold", bg='white') 
                self.hoje = datetime.today().strftime('%d-%m-%y')
                self.data_field = Label(self, text=self.hoje, font="Arial 8 bold", bg='white') 
                self.temp_field = Entry(self) 
                self.um_field = Entry(self) 
                self.codmp_field = Label(self, text=self.cod_mp, font="Arial 8 bold", bg='white')
                self.lotemp = Entry(self) 
                self.shelf_field = Entry(self) 
                self.iagi_field = Entry(self) 
                self.imcom_field = Entry(self)
                self.imdil_field = Entry(self)
                self.ii_field = Entry(self)
                self.viscosimetro = ttk.Combobox(self, values=opcoesViscosimetros(self.db, self.id_form173), state="readonly")
                self.visc_field = Entry(self)
                self.prop_field = Entry(self)
                self.iniade_field = Entry(self)
                self.plife_field = Entry(self)
                self.resp = Label(self, text=self.cod_ope, font="Arial 8 bold", bg='white')

                self.mescla_field.place(x=8, y=157, width=70) 
                self.data_field.place(x=90, y=157) 
                self.temp_field.place(x=157, y=157, width=81)
                self.um_field.place(x=247, y=157, width=67)
                self.codmp_field.place(x=327, y=157, width=58)
                self.lotemp.place(x=395, y=157, width=60) 
                self.shelf_field.place(x=468, y=157, width=64)
                self.iagi_field.place(x=542, y=157, width=64)
                self.imcom_field.place(x=616, y=157, width=78)
                self.imdil_field.place(x=705, y=157, width=60)
                self.ii_field.place(x=772, y=157, width=93)
                self.viscosimetro.place(x=879, y=157, width=74)
                
                self.visc_field.place(x=961, y=157, width=36)
                self.prop_field.place(x=1008, y=157, width=69)
                self.iniade_field.place(x=1085, y=157, width=60)
                self.plife_field.place(x=1156, y=157, width=50)
                self.resp.place(x=1223, y=157)

                
                print(opcoesViscosimetros(self.db, self.id_form173))
                
                # Defina a variável que vai armazenar o valor selecionado
                self.valor_selecionado = StringVar()
                self.dados = tuple()
                # Defina uma função para atualizar a variável sempre que o valor da Combobox mudar
                def atualizar_valor(*args):
                        self.valor_selecionado.set(self.viscosimetro.get())
                        # print(self.valor_selecionado.get())
                        self.dados = (self.mescla_atual ,
                                self.agora ,
                                self.temp_field.get() ,
                                self.um_field.get() ,
                                self.cod_mp[0][0] ,
                                self.lotemp.get(),
                                self.shelf_field.get() ,
                                self.iagi_field.get() ,
                                self.imcom_field.get() ,
                                self.imdil_field.get() ,
                                self.ii_field.get() ,
                                self.valor_selecionado.get() ,
                                self.visc_field.get() ,
                                self.prop_field.get() ,
                                self.iniade_field.get() ,
                                self.plife_field.get()
                                )

                # Associe a função à Combobox
                self.viscosimetro.bind("<<ComboboxSelected>>", lambda event: atualizar_valor())
                
                
                
                self.submit = Button(self, text="Enviar Informações", fg="Black", bg="Red", font="Arial 8 bold", command=lambda:[self.insert()])
                self.submit.place(x=1128, y=200)
                
                self.autorizar = Button(self, text="Autorizar", fg='white', bg='blue', font="Arial 7 bold", command=lambda:[login_processo.Login(self.db, self.dados, self.id_form173)])
                self.autorizar.place(x=10, y=205)
                self.autorizarText = Label(self, text="Em caso de excessões, acionar o processo!", font="Arial 8 bold", bg='white', fg="red")
                self.autorizarText.place(x=70, y=205)

        def insert(self):
                if (
                self.mescla_atual == "" and
                self.temp_field.get() == "" and
                self.um_field.get() == "" and
                self.lotemp.get() == "" and
                self.shelf_field.get() == "" and
                self.iagi_field.get() == "" and
                self.imcom_field.get() == "" and
                self.imdil_field.get() == "" and
                self.ii_field.get() == "" and
                self.valor_selecionado.get() == "" and
                self.visc_field.get() == "" and
                self.prop_field.get() == "" and
                self.iniade_field.get() == "" and
                self.plife_field.get() == "" 
                ): 
                        messagebox.showinfo(message="Campos não preenchidos.") 
        
                else: 
                        dados = (self.mescla_atual ,
                        self.agora ,
                        self.temp_field.get() ,
                        self.um_field.get() ,
                        self.cod_mp[0][0] ,
                        self.lotemp.get(),
                        self.shelf_field.get() ,
                        self.iagi_field.get() ,
                        self.imcom_field.get() ,
                        self.imdil_field.get() ,
                        self.ii_field.get() ,
                        self.valor_selecionado.get() ,
                        self.visc_field.get() ,
                        self.prop_field.get() ,
                        self.iniade_field.get() ,
                        self.plife_field.get()
                        )
                        ### Conferindo o formato dos horários
                        pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
                        pattern = re.compile(pattern)
                        try:
                                banco = sqlite3.connect(self.db)
                                cursor = banco.cursor()
                        except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
                        try:
                                visc_max_min = cursor.execute(f"SELECT viscosidade_min,viscosidade_max FROM relacao_tintas WHERE cemb={self.cod_mp[0][0]}").fetchall()[0]
                                # print(self.cod_mp[0][0], visc_max_min[1])
                                # if dados[10]== "" and int(dados[10])>int(visc_max_min[1]) or int(dados[10])<int(visc_max_min[0]):
                                #         messagebox.showinfo(message='O valor da viscosidade está fora da norma')
                                if not self.iagi_field.get() == '' and not pattern.match(self.iagi_field.get()):
                                        messagebox.showinfo(message="O valor de 'Agitação de Tintas' foi digitado de forma errada!")   
                                elif not self.imcom_field.get() == '' and not pattern.match(self.imcom_field.get()):
                                        messagebox.showinfo(message="O valor de 'Mistura dos Componentes' foi digitado de forma errada!")
                                elif not self.imdil_field.get() == '' and not pattern.match(self.imdil_field.get()):
                                        messagebox.showinfo(message="O valor de 'Mistura Diluentes' foi digitado de forma errada!")     
                                elif not self.iniade_field.get() == '' and not pattern.match(self.iniade_field.get()):
                                        messagebox.showinfo(message="O valor de 'Mistura Adequação Viscosidade' foi digitado de forma errada!")
                                elif not self.ii_field.get()=='' and not pattern.match(self.ii_field.get()):
                                        messagebox.showinfo(message="O valor de 'Tempo Indução' foi digitado de forma errada!")
                                else:
                                        x = messagebox.askquestion(title="Double-Check", message="Confirma o Envio dos Dados??")
                                        if x=='yes':
                                                try:                                                                                                       
                                                        cursor.execute("""INSERT INTO form_40 (mescla, data_prep, temperatura, umidade, cod_mp, lotemp, shelf_life, ini_agitador, ini_mistura, ini_diluentes, viscosidade, proporcao, ini_adequacao, ini_inducao, pot_life, responsavel, Id_form173)
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                                        """, (dados[0],dados[1],dados[2],dados[3],dados[4],dados[5],dados[6],dados[7] ,dados[8],dados[9],dados[10],dados[11],dados[12],dados[13],dados[14], self.cod_ope, self.id_form173))
                                                        cursor.execute("INSERT INTO form_161 (track_form173, print) VALUES(?,?)", (self.id_form173, 0))
                                                except Exception as ex: messagebox.showerror(message=ex)
                                                if not dados[13] == '':
                                                        (h,m) = dados[13].split(':')
                                                        term_inducao = timedelta(hours=int(h), minutes=int(m)+30)
                                                        term_inducao = str(term_inducao)[:-3]
                                                        cursor.execute(f"UPDATE form_40 SET term_inducao='{str(term_inducao)}' WHERE mescla='{dados[0]}'")
                                                        banco.commit()
                                                        # except ValueError: 
                                                        #         messagebox.showinfo(message='O horário de "Indução" foi digitado errôneamente')
                                                        #         # cursor.execute(f"DELETE FROM form_40 WHERE mescla='{dados[0]}'")
                                                if not dados[12] == '':
                                                        if not dados[12] == r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$':
                                                                messagebox.showinfo(message='O valor digitado para "Início da Adequação" está no formato errado!')
                                                        else:
                                                                (h,m) = dados[12].split(':')
                                                                term_adequacao = timedelta(hours=int(h), minutes=int(m)+12)
                                                                term_adequacao = str(term_adequacao)[:-3]
                                                                # cursor.execute("INSERT INTO form_40 (term_adequacao) VALUES (?)", str(term_adequcao))
                                                                cursor.execute(f"UPDATE form_40 SET term_adequacao='{str(term_adequacao)}' WHERE mescla='{dados[0]}'")
                                                                banco.commit()
                                                if not dados[9] == '':
                                                        (h,m) = dados[9].split(':')
                                                        ter_diluentes = timedelta(hours=int(h), minutes=int(m)+12)
                                                        ter_diluentes = str(ter_diluentes)[:-3]
                                                        cursor.execute(f"UPDATE form_40 SET ter_diluentes='{str(ter_diluentes)}' WHERE mescla='{dados[0]}'")
                                                        banco.commit()
                                                if not dados[8] == '':
                                                        (h,m) = dados[8].split(':')
                                                        ter_mistura = timedelta(hours=int(h), minutes=int(m)+12)
                                                        ter_mistura = str(ter_mistura)[:-3]
                                                        cursor.execute(f"UPDATE form_40 SET ter_mistura='{str(ter_mistura)}' WHERE mescla='{dados[0]}'")
                                                        banco.commit()
                                                if not dados[7] == '':
                                                        (h,m) = dados[7].split(':')
                                                        ter_agitador = timedelta(hours=int(h), minutes=int(m)+12)
                                                        ter_agitador = str(ter_agitador)[:-3]
                                                        cursor.execute(f"UPDATE form_40 SET ter_agitador='{str(ter_agitador)}' WHERE mescla='{dados[0]}'")
                                                        banco.commit()
                                                self.destroy()
                                                cursor.close()
                                                banco.close()
                        except Exception as ex: 
                                messagebox.showerror(message="Ocorreu um erro!!")
                                print(ex, type(ex)) 
                                        