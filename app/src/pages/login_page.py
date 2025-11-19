import flet as ft
import datetime as dt
import os
from pages import ferramentas, home

#obter pasta global
pasta_global = ferramentas.pasta_global()
def login_page_2(page):
    page.clean()
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
    def salvar_teste():
        pass
    
    #campos de entrada
    token= ft.TextField(label='Token de acesso', password=True)
    link = ft.TextField(label='Link do repoitório')
    
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
                        value='Login - 1°',
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
                ft.Text('Error 404 - 2025',text_align=ft.TextAlign.CENTER,size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                    ]),
                ft.Text('\n',size=1)
            ]
        )
    ]))

