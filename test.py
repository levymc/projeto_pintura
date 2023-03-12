import tkinter as tk
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do servidor SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Informações do remetente
email_remetente = 'levytecplas@gmail.com'
senha_remetente = 'rcgbcfjidtznpcku'

# Informações do destinatário
email_destinatario = 'levymcruz@gmail.com'

# Cria uma mensagem
msg = MIMEMultipart()
msg['From'] = email_remetente
msg['To'] = email_destinatario
msg['Subject'] = 'Assunto do e-mail'

# Adiciona o corpo da mensagem
corpo_mensagem = 'Olá, este é um exemplo de e-mail enviado através de Python!'
msg.attach(MIMEText(corpo_mensagem))

# Conecta-se ao servidor SMTP
smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()
smtp.login(email_remetente, senha_remetente)

# Envia o e-mail
smtp.sendmail(email_remetente, email_destinatario, msg.as_string())

# Encerra a conexão com o servidor SMTP
smtp.quit()

