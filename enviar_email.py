import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from ttkbootstrap import Style as BsStyle
import smtplib
from email.mime.text import MIMEText
from PIL import ImageTk, Image 
from email.mime.multipart import MIMEMultipart


class Email():
    def __init__(self, msg, assunto):
        # super().__init__()
        # Configurações do servidor SMTP
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        # Informações do remetente
        self.email_remetente = 'levytecplas@gmail.com'
        self.senha_remetente = 'rcgbcfjidtznpcku'

        # Informações do destinatário
        self.email_destinatario = 'processo5@tecplas.com.br'
        
        self.msg = msg
        self.assunto = assunto
    

    def enviar(self):
        ask = messagebox.askquestion("Envio de Email", "Confiama o Envio?")
        print(ask)
        if ask == 'yes':
            # Cria uma mensagem
            msg = MIMEMultipart()
            msg['From'] = self.email_remetente
            msg['To'] = self.email_destinatario
            msg['Subject'] = self.assunto

            # Adiciona o corpo da mensagem
            corpo_mensagem = self.msg
            msg.attach(MIMEText(corpo_mensagem))

            # Conecta-se ao servidor SMTP
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.starttls()
            smtp.login(self.email_remetente, self.senha_remetente)

            # Envia o e-mail
            smtp.sendmail(self.email_remetente, self.email_destinatario, msg.as_string())

            # Encerra a conexão com o servidor SMTP
            smtp.quit()
            messagebox.showinfo(message="Email Enviado!")


class Interface(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("580x400")
        self.resizable(0,0)
        self.title('TECPLAS - Pintura (main)')
        self.iconbitmap(r'logo.ico')
        self.img = PhotoImage(file="logo.png")
        self.style = BsStyle(theme='flatly')
        self.screen_width = self.winfo_screenheight()
        
        self.style.configure('Titulo.TLabel',
                             font=('Roboto', 16, 'bold'),
                             background='#f0f5ff',
                             foreground='#041536'
                             )
        self.style.configure('Principal.TFrame',
                             background='#f0f5ff',
                             )
        self.style.configure('Escritos.TLabel', 
                             font=('Roboto', 12),
                             background='#f0f5ff',
                             )
        self.style.configure('Entry.TEntry',
                             borderwidth = 0,
                             highlightthickness = 0.5
                             )
        self.style.configure('Atualizar.TButton', 
                            font=('Roboto', 10, 'bold'),
                            background='#f26c46',
                            borderwidth=0)
        self.create_widget()
    
    def create_widget(self):
        self.frame= ttk.Frame(self, style='Principal.TFrame')
        self.frame.pack(fill='both', expand=True)
        
        titulo = ttk.Label(self.frame, text="Formulário de Envio de Email para \no Processo", style='Titulo.TLabel')
        titulo.grid(row=0, column=1, pady=20, sticky='nswe')
        
        self.label_assunto = ttk.Label(self.frame, text="Assunto: ", style='Escritos.TLabel' )
        self.label_assunto.grid(row=1, column=0, padx=(10,0), pady=10, sticky='w')
        self.assunto = ttk.Entry(self.frame, width=70, style='Entry.TEntry')
        self.assunto.grid(row=1, column=1, padx=(0, 5), pady=10, sticky='w')
        
        self.label_msg = ttk.Label(self.frame, text="Mensagem: ", style='Escritos.TLabel')
        self.label_msg.grid(row=2, column=0, padx=10, pady=(10,0), sticky='w')
        self.msg = Text(self.frame, height=10, width=70 )
        self.msg.grid(row=2, column=1, padx=(0,5), pady=10, sticky='w')
        
        def conferindo(msg, assunto):
            if msg == '' or assunto == '':
                messagebox.showinfo(message="Os campos devem ser preenchidos")
            else:
                Email(msg, assunto).enviar()
                
        self.enviar = ttk.Button(self.frame,width=10, text="Enviar", style='Atualizar.TButton', command=lambda:[conferindo(self.msg.get("1.0", "end-1c"), self.assunto.get())])
        self.enviar.grid(row=3, column=1, padx=5, pady=(10,0), sticky='e')
        self.mainloop()

# if __name__ == "__main__":
#     app = Interface()
#     app.mainloop()