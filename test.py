import tkinter as tk

def formatar_horario(hora):
    hora, minuto = divmod(hora, 60)
    return f"{hora:02d}:{minuto:02d}"

def validar_horario(novo_valor):
    try:
        hora, minuto = map(int, novo_valor.split(':'))
        return hora + minuto/60.0
    except:
        return None

root = tk.Tk()

hora = tk.DoubleVar(value=8.0)

hora_spinbox = tk.Spinbox(root, from_=0.0, to=23.99, increment=0.01, format='%02.0f:%02.0f',
                          textvariable=hora, validate='key', validatecommand=(root.register(validar_horario), '%P'),
                          command=lambda: hora.set(hora_spinbox.get()))

hora_spinbox.config(from_='00:00', to='23:59', increment=5, justify='center', validate='all',
                    validatecommand=(root.register(validar_horario), '%P'),
                    format='%02.0f:%02.0f', command=lambda: hora.set(validar_horario(hora_spinbox.get())))
hora_spinbox.icursor(0)

hora_spinbox.pack()

root.mainloop()
