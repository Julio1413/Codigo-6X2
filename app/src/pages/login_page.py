from flet import Page, Text, SnackBar, Colors, ThemeMode, Icons, Column, Row, TextField, ElevatedButton, KeyboardType, FontWeight, MainAxisAlignment, IconButton, AlertDialog, Container, Divider, Dropdown, dropdown, TextStyle, margin, padding, border_radius, ElevatedButton, ButtonStyle, RoundedRectangleBorder, TextButton,Icon
import datetime as dt
import re, phonenumbers , os
from pages import ferramentas, home

#obter pasta global
pasta_global = ferramentas.pasta_global()
def login_page_2(page):
    page.clean()
    page.update()

def login_page_1(page):
    page.clean()
    page.update()
    page.bgcolor = Colors.LIGHT_BLUE
    #botões

    
    #construção da página
    page.add(
        ft.Column(controls=[ft.Container(height=90,
        content=ft.Container(alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=padding(), right=padding(),bottom=10),
            blur=(10,10),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon_color=ft.Colors.WHITE,
                        icon=icone_btn,
                        on_click=lambda _:destino(page),
                        icon_size=25,
                    ),
                    ft.Text(
                        value=titulo,
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(name=icone, color=ft.Colors.WHITE,size=30),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            height=50,
            margin=ft.margin.all(-10),
        ),
    ),
    ft.Text(f'\n',size=1)
                               ])

    )
    page.add(ferramentas.container(page=page,controles=[
        Text('  Seus dados serão salvos localmente.',size=15,weight=FontWeight.BOLD),
         
     
    ]))

