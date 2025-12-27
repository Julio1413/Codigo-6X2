import flet as ft
import datetime as dt
import os
from pages import ferramentas, home,supabase
import json

def login_sucesso(page):
    page.clean()
    page.controls.clear()
    page.update()
    home.inicial(page)
#obter pasta global
pasta_global = ferramentas.pasta_global()
def login_page_2(page):
    def validacao (nome,matricula):
        if not nome or not matricula:
            snack = ft.SnackBar(content=ft.Text('Por favor, preencha todos os campos.'),bgcolor=ft.Colors.RED,open=True)
            page.open(snack)
            page.update()
        else:
            dados_login = supabase.ler_tabela('login')
            print(json.dumps(dados_login,indent=4))
            for usuario in range (len(dados_login)):
                if dados_login[usuario]['nome'].split()[0].lower() == nome.lower() and str(dados_login[usuario]['matricula']) == str(matricula):
                    with open (os.path.join(pasta_global,'INFO.txt'),'w') as f:
                        f.write(f"{nome}\n{matricula}\n{usuario}")
                    snack = ft.SnackBar(content=ft.Text('Login - 2 realizado com sucesso!'),bgcolor=ft.Colors.GREEN,open=True)
                    page.open(snack)
                    home.inicial(page)
                    page.update()
                    break
            else:
                snack = ft.SnackBar(content=ft.Text('Matrícula ou nome inválido.'),bgcolor=ft.Colors.RED,open=True)
                page.open(snack)
                page.update()
                return
    page.clean()
    page.update()
    page.add(
        ft.Column(controls=[ft.Container(height=90,
        content=ft.Container(alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=ferramentas.padding(), right=ferramentas.padding(),bottom=10),
            blur=(10,10),
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.LOGIN_ROUNDED, color=ft.Colors.WHITE,size=30),
                    ft.Text(
                        value='Login - 2',
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(name=ft.Icons.CALENDAR_MONTH_ROUNDED, color=ft.Colors.WHITE,size=30),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            height=50,
            margin=ft.margin.all(-10),
        ),
    ),
    ft.Text(f'\n',size=10)]))
    nome = ft.TextField(label='Primeiro nome:',hint_text='Biroska')
    matricula = ft.TextField(label='Número de matrícula: 200008360000')
    page.add(
        ferramentas.container(page=page,controles=[
            nome,
            matricula,
            ft.Text('\n',expand=True),
            ft.Container(height=page.height*0.37),
            ft.ElevatedButton(text='Proseguir',width=page.width,icon=ft.Icons.LOGIN_ROUNDED,on_click=lambda e: validacao(nome.value,matricula.value)),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
                ft.Text('404 Studios - 2025',text_align=ft.TextAlign.CENTER,size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                    ]),
                ft.Text('\n',size=1)
        ]))
    page.update()

def login_page_1(page):
    page.clean()
    page.update()
    page.bgcolor = ft.Colors.LIGHT_BLUE
    if os.path.exists(os.path.join(pasta_global, "bright_mode.txt")):
        with open(os.path.join(pasta_global, "bright_mode.txt"), "r") as file:
            bright_mode = file.read().strip()
    else:
        with open(os.path.join(pasta_global, "bright_mode.txt"), "w") as file:
            file.write("0")
        bright_mode = "0"

    if bright_mode == "0":
        page.theme_mode = ft.ThemeMode.SYSTEM
    
    elif bright_mode == "1":
        page.theme_mode = ft.ThemeMode.DARK
    elif bright_mode == "2":
        page.theme_mode = ft.ThemeMode.LIGHT
    #botões
    token= ft.TextField(label='Token de acesso', password=True)
    link = ft.TextField(label='Link do repoitório')
    def salvar_teste():
        if supabase.testar_conexao(link.value,token.value):
            
            snack = ft.SnackBar(content=ft.Text('Login - 1 realizado com sucesso!'),bgcolor=ft.Colors.GREEN,open=True)
            page.open(snack)
            
            with open(os.path.join(pasta_global,'TOKEN_FILE.txt'),'w') as f:
                f.write(token.value)
            with open(os.path.join(pasta_global,'URL_FILE.txt'),'w') as f:
                f.write(link.value)
                
            login_page_2(page)
            page.update()
            
        else:
            snack = ft.SnackBar(content=ft.Text(f'Erro ao realizar login! Verifique suas credenciais.'),bgcolor=ft.Colors.RED,open=True)
            page.open(snack)
            page.update()
      
    
    
    #construção da página
    page.add(
        ft.Column(controls=[ft.Container(height=90,
        content=ft.Container(alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=ferramentas.padding(), right=ferramentas.padding(),bottom=10),
            blur=(10,10),
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.LOGIN_ROUNDED, color=ft.Colors.WHITE,size=30),
                    ft.Text(
                        value='Login - 1',
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(name=ft.Icons.CALENDAR_MONTH_ROUNDED, color=ft.Colors.WHITE,size=30),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            height=50,
            margin=ft.margin.all(-10),
        ),
    ),
    ft.Text(f'\n',size=10)
                               ])

    )
    page.add(ferramentas.container(page=page,controles=[
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Text('  Seus dados serão salvos localmente.',size=15,weight=ft.FontWeight.BOLD),
                link,
                token,
                ft.Text('\n',expand=True),
                ft.Container(height=page.height*0.37),
                ft.ElevatedButton(text='Proseguir',width=page.width,icon=ft.Icons.LOGIN_ROUNDED,on_click=lambda e: salvar_teste()),
               
                ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
                ft.Text('404 Studios - 2025',text_align=ft.TextAlign.CENTER,size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                    ]),
                ft.Text('\n',size=1)
            ]
        )
    ]))

