from flet import Page, Text, SnackBar, Colors, ThemeMode, Icons, Column, Row, TextField, ElevatedButton, KeyboardType, FontWeight, MainAxisAlignment, IconButton, AlertDialog, Container, Divider, Dropdown, dropdown, TextStyle, margin, padding, border_radius, ElevatedButton, ButtonStyle, RoundedRectangleBorder, TextButton,Icon
import datetime as dt
import re, phonenumbers , os
from pages import ferramentas, home

#obter pasta global
pasta_global = ferramentas.pasta_global()

def validar_nome(nome):
    return re.fullmatch(r"[A-Za-zÀ-ÿ\s]{2,}", nome.strip()) is not None 

def validar_email(email):
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email.strip()) is not None

def validar_e_formatar_telefone(numero):
    try:
        numero = numero.strip().replace(" ", "").replace("-", "")
        if not numero.startswith("+"):
            numero = "+55" + numero
        parsed = phonenumbers.parse(numero, None)
        if not phonenumbers.is_valid_number(parsed):
            return None
        # Formato nacional bonito
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    except Exception:
        return None

def login_page_1(page):
    page.bgcolor = Colors.LIGHT_BLUE

    def confirmar (e):
        def abrir_termos():
            page.launch_url("https://sites.google.com/view/cubepy/nossos-apps/glicapp/termos-de-uso-e-política-de-privacidade-glicapp")
            page.update()
        def cancelar(e):
            dialog.open = False
            page.update()
        def login_process(e):
            nome = nome_fill.value.strip()
            telefone = tel_fill.value.strip()
            email = email_fill.value.strip()
            cancelar(e)
            if not all([nome, telefone, email]):
                page.add(SnackBar(Text("Preencha todos os campos obrigatórios!"), open=True, bgcolor=Colors.RED))
            else:
                telefone_formatado = validar_e_formatar_telefone(telefone)
                if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]{2,}", nome) or not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) or telefone_formatado is None:
                    page.add(SnackBar(Text("Preencha todos os dados corretamente!"), open=True, bgcolor=Colors.RED))
                else:
                    with open(os.path.join(pasta_global, "nome.txt"), "w") as f:
                        f.write(nome)
                    with open(os.path.join(pasta_global, "telefone.txt"), "w") as f:
                        f.write(telefone_formatado)  # <- Aqui usamos o número formatado!
                    with open(os.path.join(pasta_global, "email.txt"), "w") as f:
                        f.write(email)
                    with open(os.path.join(pasta_global, "dia_nascimento.txt"), "w") as f:
                        f.write(dia_n.value)
                    with open(os.path.join(pasta_global, "mes_nascimento.txt"), "w") as f:
                        f.write(mes_n.value)
                    with open(os.path.join(pasta_global, "ano_nascimento.txt"), "w") as f:
                        f.write(ano_n.value)

                    home.inicial(page)
                    page.add(SnackBar(Text("Bem-vindo(a) ao Glicapp!"), open=True, bgcolor=Colors.GREEN))
        # Configuração do pop-up
        
        dialog = AlertDialog(bgcolor=Colors.with_opacity(0.0,Colors.WHITE),barrier_color=Colors.with_opacity(0.0,Colors.WHITE),
            content=Container(
                            blur=(15,15),
                            bgcolor=Colors.WHITE.with_opacity(0.2, Colors.WHITE70),
                            margin=margin.only(top=4,left=4,right=4,bottom=4),
                            border_radius=border_radius.all(20),
                            expand=True,
                            height=370,
                            width=400,
                            padding=padding.all(6),
                            content=Column(
                                alignment=MainAxisAlignment.START,
                                controls=[
                                    Row(alignment=MainAxisAlignment.SPACE_BETWEEN,controls=[
                                        Icon(name=Icons.DEVICES_OTHER_ROUNDED),
                                        Text("Continuar",size=17,weight=FontWeight.BOLD),
                                        IconButton(icon=Icons.INFO),
                                    ]),
                                    Divider(height=1),
                                    Text('\n',size=3),
                                    
                                    Text('Ao continuar, você concorda com as política de uso e privacidade do Glicapp.',size=15,weight=FontWeight.BOLD),
                                    Column(alignment=MainAxisAlignment.CENTER,expand=True,controls=[
                                        Row(alignment=MainAxisAlignment.CENTER,expand=True,controls=[ElevatedButton(style=ButtonStyle(shape=RoundedRectangleBorder(radius=15)),text='Política de uso e privacidade',icon=Icons.LOCK_ROUNDED,height = 100,on_click= lambda _:abrir_termos())]),
                                        ]),
                                    
                                    Divider(height=1),
                                    
                                    Row(alignment=MainAxisAlignment.END,controls=[
                                        TextButton("Cancelar",on_click=cancelar),
                                        TextButton("Continuar",on_click=login_process),
                                    ])
                                    ])),
        
        )
        page.open(dialog)
        page.update()
    header = Container(
        margin=margin.only(top=15,left=10),
        content=Container(
            padding=0,border_radius=border_radius.all(20),
            content=Row(alignment=MainAxisAlignment.START,
                controls=[
                    Text(value="Bem vindo(a) ao Glicapp!",color=Colors.WHITE,size=23,weight=FontWeight.BOLD),
                ],
            ),
            height=50,
        ),
    )
    #entrada da página
    dia_n = Dropdown(
        width=105,label='Dia',label_style=TextStyle(size=13),
        options=[
            dropdown.Option(i) for i in range(1,32)
        ],
    )
    mes_n = Dropdown(
        width=105,label='Mês',label_style=TextStyle(size=13),
        options=[
            dropdown.Option(i) for i in range(1, 13)
        ],
    )
    ano_atual = dt.datetime.now().year
    ano_n = Dropdown(
        width=105,
        label='Ano',
        label_style=TextStyle(size=13),
        options=[dropdown.Option(str(ano)) for ano in range(ano_atual, ano_atual - 151, -1)]
    )
    #organização das entradas
    data_fill = Row(spacing=10,alignment=MainAxisAlignment.SPACE_BETWEEN,controls=[dia_n,mes_n,ano_n])

    #outras entradas
    nome_fill = TextField(label='Seu nome')
    tel_fill = TextField(label='Telefone',hint_text="(00) 00000-0000",keyboard_type=KeyboardType.PHONE)
    email_fill = TextField(label='E-mail',hint_text='seuemail@email.com',keyboard_type=KeyboardType.EMAIL)
    #outros elementos
    aviso = TextField(border_color=Colors.TRANSPARENT,expand=True,multiline=True,read_only=True,value='Aviso Importante!\nO uso deste aplicativo sem recomendação médica ou sem os dados essenciais (RIC, FSI e META glicêmica) para contagem de carboidratos pode resultar em cálculos incorretos.\nConsulte sempre um profissional de saúde antes de utilizar o app.\n Os dados inseridos no aplicativo serão armazenados localmente e poderão ser utilizados para relatórios personalizados destinados ao acompanhamento profissional.'
                    )
    
    #botões
    prosseguir_btn = ElevatedButton(icon=Icons.ARROW_CIRCLE_RIGHT,text='Continuar',width=300,on_click=confirmar)
    linebtn = Row(alignment=MainAxisAlignment.CENTER,controls=[prosseguir_btn])
    
    #construção da página
    page.add(header,Text('\n',size=5))
    page.add(ferramentas.container(page=page,controles=[
        Text('  Seus dados serão salvos localmente.',size=15,weight=FontWeight.BOLD),
        nome_fill,
        email_fill,
        tel_fill,
        Text('  Data de nascimento.',size=15,weight=FontWeight.BOLD),
        data_fill,
        aviso, 
        linebtn       
    ]))

