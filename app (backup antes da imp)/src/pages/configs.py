import os
import flet as ft
from pages import home, ferramentas,login_page

pasta_global = ferramentas.pasta_global()
def configs(page):
    page.clean()
    #configuração da cor do fundo da página
    def deslogar(_):
        def sair():
            os.remove(os.path.join(pasta_global,'INFO.txt'))
            login_page.login_page_1(page)
            dlg.open = False
            page.update()
            
        dlg = ferramentas.dialog(
            page=page,
            titulo='Sair',
            texto_btn='Sair',
            funcao_btn=lambda _:sair(),
            icone_d=ft.Icons.DELETE_FOREVER_ROUNDED,
            icone_e=ft.Icons.DELETE_FOREVER_ROUNDED,
            conteudo=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text('Tem certeza de que deseja\nsair da sua conta 6X2?',weight=ft.FontWeight.BOLD)]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Icon(name=ft.Icons.DELETE_FOREVER_ROUNDED,color=ft.Colors.RED,size=100)]),
            ]
        )
        page.open(dlg)
        page.update()

    def color_config(_):
        
        #função da mudança das cores
        def cordefundo (_,cor_pagina):  # Apenas o nome da cor, sem "ft.Colors."
            page.bgcolor = getattr(ft.Colors,cor_pagina, ft.Colors.BLACK)
            with open(os.path.join(pasta_global, "page_bgcolor.txt"), "w") as file:
                file.write(cor_pagina)  # Salva só o nome da cor
            dlg.open = False
            page.open(ft.SnackBar(ft.Text(f"A cor de fundo foi alterada com sucesso!"), open=True,bgcolor=ft.Colors.GREEN))
            page.update()
        def botoes_c(titulo,cor,funcao):
            return ft.ElevatedButton(
            on_click=funcao,
            width=20, height=20,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            content=ft.Column(alignment=ft.MainAxisAlignment.CENTER, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                    ft.Icon(name=ft.Icons.CIRCLE, size=50, color=cor),
                    ]),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                    ft.Text(titulo, size=12, text_align=ft.TextAlign.CENTER)
               ]),
              ])
            )
        #canc
        #pop up de configuração
        dlg = ferramentas.dialog(
            titulo='Cor de fundo',
            icone_d=ft.Icons.FORMAT_COLOR_FILL_ROUNDED,
            icone_e=ft.Icons.INFO,
            page=page,
            conteudo=[
                ft.GridView(
                    expand=True,
                    runs_count=7,
                    max_extent=150,
                    child_aspect_ratio=1,
                    spacing=6,
                    run_spacing=6,
                    controls=[
                        botoes_c(titulo='Azul claro',cor=ft.Colors.LIGHT_BLUE,funcao=lambda _:cordefundo(_,'LIGHT_BLUE')),
                        botoes_c(titulo='Rosa',cor=ft.Colors.PINK_400,funcao=lambda _:cordefundo(_,'PINK_400')),
                        botoes_c(titulo='Salmão',cor=ft.Colors.PINK_200,funcao=lambda _:cordefundo(_,'PINK_200')),
                        botoes_c(titulo='Indigo',cor=ft.Colors.INDIGO_800,funcao=lambda _:cordefundo(_,'INDIGO_800')),
                        botoes_c(titulo='Vinho',cor=ft.Colors.PINK_900,funcao=lambda _:cordefundo(_,'PINK_900')),
                        botoes_c(titulo='Vermelho',cor=ft.Colors.RED_ACCENT_700,funcao=lambda _:cordefundo(_,'RED_ACCENT_700')),
                        botoes_c(titulo='Vermelho claro',cor=ft.Colors.RED_200,funcao=lambda _:cordefundo(_,'RED_200')),
                        botoes_c(titulo='Roxo',cor=ft.Colors.PURPLE,funcao=lambda _:cordefundo(_,'PURPLE')),
                        botoes_c(titulo='Ciano',cor=ft.Colors.CYAN,funcao=lambda _:cordefundo(_,'CYAN')),
                        botoes_c(titulo='Verde',cor=ft.Colors.GREEN,funcao=lambda _:cordefundo(_,'GREEN')),
                        botoes_c(titulo='Verde azulado',cor=ft.Colors.TEAL,funcao=lambda _:cordefundo(_,'TEAL')),
                    ]
                )
            ]
        )
        page.open(dlg)
        page.update()
        
    page.add(ferramentas.header(titulo='Configurações',icone=ft.Icons.SETTINGS,page=page))
    
    def definir_tema(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.theme_mode = ft.ThemeMode.SYSTEM
        elif selected_index == 1:
            page.theme_mode = ft.ThemeMode.DARK
            page.brightness = ft.Brightness.DARK
        elif selected_index == 2:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.brightness = ft.Brightness.LIGHT
        with open(os.path.join(pasta_global, "bright_mode.txt"), "w") as file:
            file.write(str(selected_index))
        page.update()

    bright_options = ft.CupertinoSlidingSegmentedButton(
        width=page.width,
        selected_index=0,
        on_change=definir_tema,thumb_color=ft.Colors.BLUE_700,
        padding=ft.padding.symmetric(7, 7),
        controls=[
            ft.Text("Auto"),
            ft.Text("Escuro"),
            ft.Text("Claro"),
        ],
    )
    with open(os.path.join(pasta_global, "bright_mode.txt"), "r") as file:
        bright_options.selected_index = int(file.read())
        
    def abrir_termos():
        page.launch_url("https://sites.google.com/view/cubepy/nossos-apps/glicapp/termos-de-uso-e-pol%C3%ADtica-de-privacidade-glicapp")
        page.update()
    #construção da página
    page.add(ft.Column(expand=True,spacing=10,controls=[
        bright_options,
        ft.Divider(height=0.5),
        ft.ElevatedButton(text='Cor de fundo',icon=ft.Icons.COLOR_LENS_ROUNDED,width=page.width,on_click=color_config),
        ft.Divider(height=0.5),
        
        #termos de uso e privacidade
        ft.Column(alignment=ft.MainAxisAlignment.END,expand=True,controls=[
            ft.ElevatedButton(text='Sair',bgcolor=ft.Colors.RED_600,icon=ft.Icons.COLOR_LENS_ROUNDED,width=page.width,on_click=deslogar),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
            ft.Text('404 Studios - 2025',text_align=ft.TextAlign.CENTER,size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                ]),
            ft.Text('\n',size=1)
        ])
    ]))
    page.update()
