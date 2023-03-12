import tkinter as tk
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email():
    def __init__(self, msg):
        # super().__init__()
        # Configurações do servidor SMTP
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        # Informações do remetente
        self.email_remetente = 'levytecplas@gmail.com'
        self.senha_remetente = 'rcgbcfjidtznpcku'

        # Informações do destinatário
        self.email_destinatario = 'levymcruz@gmail.com'
        
        self.msg = msg

    def enviar(self):
        # Cria uma mensagem
        msg = MIMEMultipart()
        msg['From'] = self.email_remetente
        msg['To'] = self.email_destinatario
        msg['Subject'] = 'Assunto do e-mail'

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

Email("TESTANDOOOOOOOOOOOO FRED").enviar()