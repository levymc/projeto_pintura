from ttkbootstrap import Style as BsStyle
import hashlib, json, sqlite3

class Estilos():
    def __init__(self):
        self.style = BsStyle(theme='flatly')
        
        
        # LABEL
        
        self.style.configure('infoOC.TLabel', 
                            font=('Roboto', 9, 'bold'),
                            )
        
        self.style.configure('TituloMenor.TLabel',
                             font=('Roboto', 12, 'bold'),
                             )
        self.style.configure('Titulo.TLabel',
                             font=('Roboto', 16, 'bold'),
                             background='#f0f5ff',
                             foreground='#041536'
                             )
        
        
        # BUTTON
        
        self.style.configure('Atualizar.TButton', 
                            font=('Roboto', 10, 'bold'),
                            background='#f26c46',
                            borderwidth=0)
        
        self.style.map('Mescla.TButton', background=[('active', '#3e3e3e')], 
          foreground=[('active', 'white')]) ## O .map serve para configuração de estilos de estado (pressionado, ativo, ....)
        self.style.configure('Mescla.TButton', background='#384a6e',  #.configure serve para configurações de estilo no geral
                highlightbackground='#4CAF50', 
                highlightcolor='#4CAF50', 
                highlightthickness=1,
                padding=3,
                font=('Helvetica', 12, 'bold'),
                foreground='white',
                borderwidth=5,
                relief='ridge',)
        
        self.style.map('Add.TButton', 
                       background=[('active', '#c44c2b'), ('pressed', 'white')],
                       )
        self.style.configure('Add.TButton', 
                            font=('Roboto', 10, 'bold'),
                            background='#f26c46',
                            highlightbackground='#4CAF50', 
                            highlightcolor='#4CAF50',
                            borderwidth=0.1,
                            highlightthickness=0.5)
        
        self.style.map('Att.TButton', 
                       background=[('active', '#3e3e3e'), ('pressed', 'white')],
                       )
        self.style.configure('Att.TButton', 
                            font=('Roboto', 8, 'bold'),
                            background='#384a6e',
                            borderwidth=0.1,
                            highlightthickness=0.5)
        
        self.style.map('Enviar.TButton', background=[('active', '#a35c33')], 
          foreground=[('active', 'white')],
          bordercolor=[('active', '#384a6e')]) ## O .map serve para configuração de estilos de estado (pressionado, ativo, ....)
        self.style.configure('Enviar.TButton', background='#f75c02',  #.configure serve para configurações de estilo no geral
                font=('Roboto', 9, 'bold'),
                foreground='white',
                borderwidth=0.3,
                relief='solid',
                border_radius=10,
                bordercolor='#cbd8f2')   
        
        self.style.map('Custom.TButton', background=[('active', '#3e3e3e')], 
          foreground=[('active', 'white')]) ## O .map serve para configuração de estilos de estado (pressionado, ativo, ....)
        self.style.configure('Custom.TButton', background='#384a6e',  #.configure serve para configurações de estilo no geral
                highlightbackground='#4CAF50', 
                highlightcolor='#4CAF50', 
                highlightthickness=1,
                font=('Helvetica', 12, 'bold'),
                foreground='white',
                borderwidth=5,
                relief='ridge',)
        
        self.style.configure('Processo.TButton',
                             padding=2,
                             font=('Roboto', 7),
                             foreground='red',
                             background='white',
                             border=0.5,
                             )
        
        self.style.map('FinalizarForm40.TButton',
                       background=[('active', '#750701')],
                       foreground=[('active', '#f7dedc')])
        
        self.style.configure('FinalizarForm40.TButton',
                             font=('Roboto', 8, 'bold'),
                             foreground='#750701',
                             background='#f7dedc'
                             )
        
        self.style.map('Enviar2.TButton', background=[('active', '#a35c33')], 
          foreground=[('active', 'white')],
          bordercolor=[('active', '#384a6e')]) ## O .map serve para configuração de estilos de estado (pressionado, ativo, ....)
        self.style.configure('Enviar2.TButton', background='#f75c02',  #.configure serve para configurações de estilo no geral
                font=('Roboto', 8, 'bold'),
                foreground='white',
                borderwidth=0.3,
                relief='solid',
                border_radius=10,
                bordercolor='#cbd8f2')   
        
        self.style.map('Limpar.TButton',
                    background=[('active', '#b3c9f5')], 
                    foreground=[('active', 'white')]
                    )  
        self.style.configure('Limpar.TButton',
                            background='#cbd8f2',
                            foreground='black',
                            borderwidth=0.1,
                            font=('Roboto', 7, 'bold'),
                             )
        
        self.style.map('Deletar.TButton', 
                        background=[('active', '#f2bfbf')], 
                        foreground=[('active', '#380101')]
                        )  
        self.style.configure('Deletar.TButton',
                            background='#a61919',
                            foreground='#f2bfbf',
                            borderwidth=0.3,
                            font=('Roboto', 7, 'bold'),
                             )
        
        self.style.configure('Escritos.TLabel', 
                             font=('Roboto', 12),
                             background='#f0f5ff',
                             )
        
        
        ## ENTRY
        
        self.style.configure('Form40.TEntry',
                             font=('Roboto', 6),
                             padding=0
                             )
        
        self.style.configure('Entry.TEntry',
                             borderwidth = 0,
                             highlightthickness = 0.5
                             )
        
        
        ## FRAME
        
        self.style.configure('TFrame', background='#960222')
        
        self.style.configure('FundoOC.TFrame', 
                             background='#203C75'
                             )
        
        self.style.configure('Principal.TFrame',
                             background='#f0f5ff',
                             )    
        
        self.style.configure('Frame1.TFrame', 
                            background='#041536'
                            )
        
        self.style.configure('TFrame', 
                            background='#f0f5ff'
                            )
        
        self.style.configure('FrameOC.TFrame', borderwidth=5,
                            highlightbackground='black',
                            bordercolor='#f26c46',
                            background='white',
                            relief='solid',
                             )
        
        self.retorno()
        
    def retorno(self):
        return self.style
