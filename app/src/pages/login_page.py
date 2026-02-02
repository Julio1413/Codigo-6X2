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
def normalizar(texto):
    if texto is None:
        return ""
    return str(texto).strip().lower()

def login_page_2(page):
    arquivo_cor = "page_bgcolor.txt"
    if ferramentas.arquivo_existe(arquivo_cor):
        cor_pagina = ferramentas.ler_arquivo(arquivo_cor).strip()
        page.bgcolor = getattr(ft.Colors, cor_pagina, ft.Colors.LIGHT_BLUE)  # Se a cor for inválida, usa preto como fallback
    else:
        cor_pagina = "LIGHT_BLUE"  # Apenas o nome da cor, sem "Colors."
        page.bgcolor = getattr(ft.Colors, cor_pagina, ft.Colors.BLACK)
        ferramentas.criar_arquivo(nome=arquivo_cor,conteudo=cor_pagina) 
    page.update()# Salva só o nome da cor
    def salvar_info(nome, matricula, id):
        ferramentas.criar_arquivo("NOME.txt", nome)
        ferramentas.criar_arquivo("MATRICULA.txt", matricula)
        ferramentas.criar_arquivo("ID.txt", str(id))
      

    def validacao(nome, matricula):
        if not nome or not matricula:
            snack = ft.SnackBar(content=ft.Text('Por favor, preencha todos os campos.'), bgcolor=ft.Colors.RED, open=True)
            page.open(snack)
            page.update()
            return
        print(supabase.testar_conexao(*supabase.obter_credenciais()))
        nome_input = normalizar(nome)
        mat_input = normalizar(matricula)
        dados_login = supabase.ler_tabela('login')
        encontrado = False
        for usuario in range(len(dados_login)):
            nome_db = normalizar(dados_login[usuario].get('nome'))
            mat_db = normalizar(dados_login[usuario].get('matricula'))
            if nome_db.startswith(nome_input) and mat_db == mat_input:
                salvar_info(nome_input, mat_input, usuario)
                print("salvar_info() EXECUTADA")
                page.update()
                supabase.inserir_log(f'Login realizado por {nome_input}')
                home.inicial(page)
                encontrado = True
                break
        if not encontrado:
            snack = ft.SnackBar(content=ft.Text('Matrícula ou nome inválido.'), bgcolor=ft.Colors.RED, open=True)
            page.show_dialog(snack)
            page.update()

    page.clean()
    page.update()
    page.add(
        ft.Column(controls=[ft.Container(height=90,
        content=ft.Container(alignment=ft.Alignment.BOTTOM_CENTER,
            padding=ft.padding.only(left=ferramentas.padding(), right=ferramentas.padding(), bottom=10),
            blur=(10, 10),
            content=ft.Row(
                controls=[
                    ft.Icon(icon=ft.Icons.LOGIN_ROUNDED, color=ft.Colors.WHITE, size=30),
                    ft.Text(
                        value='Login',
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(icon=ft.Icons.CALENDAR_MONTH_ROUNDED, color=ft.Colors.WHITE, size=30),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            height=50,
            margin=ft.margin.all(-10),
        ),
    ),
    ft.Text(f'\n', size=10)]))
    nome = ft.TextField(label='Nome completo (sem acentução ou ç):', hint_text='Cleiton Silva Souza',width=page.width)
    matricula = ft.TextField(label='Número de matrícula: 200008360000',width=page.width)
    page.add(
        ferramentas.container(page=page, controles=[
            nome,
            matricula,
            ft.Text('\n', expand=True),
            ft.Container(height=page.height * 0.37),
            ft.ElevatedButton(content=ft.Text('Proseguir'), width=page.width, icon=ft.Icons.LOGIN_ROUNDED, on_click=lambda e: validacao(nome.value, matricula.value)),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                ft.Text('404 Studios - 2025', text_align=ft.TextAlign.CENTER, size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY),
            ]),
            ft.Text('\n', size=1)
        ]))
    page.update()

def login_page_1(page):
    page.clean()
    page.update()
    page.bgcolor = ft.Colors.LIGHT_BLUE
    if ferramentas.arquivo_existe('bright_mode.txt'):
        bright_mode = ferramentas.ler_arquivo("bright_mode.txt").strip()
    else:
        ferramentas.criar_arquivo("bright_mode.txt","0")
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
            ferramentas.criar_arquivo(nome='TOKEN_FILE.txt',conteudo=token.value)
            ferramentas.criar_arquivo(nome='URL_FILE.txt',conteudo=link.value)
                
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
                        value='Login',
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

