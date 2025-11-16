from flet import Page, Text, SnackBar, Colors, ThemeMode, KeyboardType, TextField, ElevatedButton, ButtonStyle, RoundedRectangleBorder, Icons, Column, Row, MainAxisAlignment, alignment, border_radius, Container, margin, padding, Divider, GridView, Brightness, CupertinoSlidingSegmentedButton, Icon, TextAlign, FontWeight
import os, phonenumbers, re
from pages import home, ferramentas

def configs(page):
    pasta_global = ferramentas.pasta_global()
    page.clean()
    #configuração da cor do fundo da página

    def color_config(_):
        
        #função da mudança das cores
        def cordefundo (_,cor_pagina):  # Apenas o nome da cor, sem "Colors."
            page.bgcolor = getattr(Colors,cor_pagina, Colors.BLACK)
            with open(os.path.join(pasta_global, "page_bgcolor.txt"), "w") as file:
                file.write(cor_pagina)  # Salva só o nome da cor
            dlg.open = False
            page.open(SnackBar(Text(f"A cor de fundo foi alterada com sucesso!"), open=True,bgcolor=Colors.GREEN))
            page.update()
        def botoes_c(titulo,cor,funcao):
            return ElevatedButton(
            on_click=funcao,
            width=20, height=20,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=20)),
            content=Column(alignment=MainAxisAlignment.CENTER, controls=[
                Row(alignment=MainAxisAlignment.CENTER, controls=[
                    Icon(name=Icons.CIRCLE, size=50, color=cor),
                    ]),
                Row(alignment=MainAxisAlignment.CENTER, controls=[
                    Text(titulo, size=12, text_align=TextAlign.CENTER)
                    ]),
            ])
            )
        #canc
        #pop up de configuração
        dlg = ferramentas.dialog(
            titulo='Cor de fundo',
            icone_d=Icons.FORMAT_COLOR_FILL_ROUNDED,
            icone_e=Icons.INFO,
            page=page,
            conteudo=[
                GridView(
                    expand=True,
                    runs_count=7,
                    max_extent=150,
                    child_aspect_ratio=1,
                    spacing=6,
                    run_spacing=6,
                    controls=[
                        botoes_c(titulo='Azul claro',cor=Colors.LIGHT_BLUE,funcao=lambda _:cordefundo(_,'LIGHT_BLUE')),
                        botoes_c(titulo='Rosa',cor=Colors.PINK_400,funcao=lambda _:cordefundo(_,'PINK_400')),
                        botoes_c(titulo='Salmão',cor=Colors.PINK_200,funcao=lambda _:cordefundo(_,'PINK_200')),
                        botoes_c(titulo='Indigo',cor=Colors.INDIGO_800,funcao=lambda _:cordefundo(_,'INDIGO_800')),
                        botoes_c(titulo='Vinho',cor=Colors.PINK_900,funcao=lambda _:cordefundo(_,'PINK_900')),
                        botoes_c(titulo='Vermelho',cor=Colors.RED_ACCENT_700,funcao=lambda _:cordefundo(_,'RED_ACCENT_700')),
                        botoes_c(titulo='Vermelho claro',cor=Colors.RED_200,funcao=lambda _:cordefundo(_,'RED_200')),
                        botoes_c(titulo='Roxo',cor=Colors.PURPLE,funcao=lambda _:cordefundo(_,'PURPLE')),
                        botoes_c(titulo='Ciano',cor=Colors.CYAN,funcao=lambda _:cordefundo(_,'CYAN')),
                        botoes_c(titulo='Verde',cor=Colors.GREEN,funcao=lambda _:cordefundo(_,'GREEN')),
                        botoes_c(titulo='Verde azulado',cor=Colors.TEAL,funcao=lambda _:cordefundo(_,'TEAL')),
                    ]
                )
            ]
        )
        page.open(dlg)
        page.update()
        
    page.add(ferramentas.header(titulo='Configurações',icone=Icons.SETTINGS,page=page))
    
    def definir_tema(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.theme_mode = ThemeMode.SYSTEM
        elif selected_index == 1:
            page.theme_mode = ThemeMode.DARK
            page.brightness = Brightness.DARK
        elif selected_index == 2:
            page.theme_mode = ThemeMode.LIGHT
            page.brightness = Brightness.LIGHT
        with open(os.path.join(pasta_global, "bright_mode.txt"), "w") as file:
            file.write(str(selected_index))
        page.update()

    bright_options = CupertinoSlidingSegmentedButton(
        width=page.width,
        selected_index=0,
        on_change=definir_tema,thumb_color=Colors.BLUE_700,
        padding=padding.symmetric(7, 7),
        controls=[
            Text("Auto"),
            Text("Escuro"),
            Text("Claro"),
        ],
    )
    with open(os.path.join(pasta_global, "bright_mode.txt"), "r") as file:
        bright_options.selected_index = int(file.read())
        
    def abrir_termos():
        page.launch_url("https://sites.google.com/view/cubepy/nossos-apps/glicapp/termos-de-uso-e-pol%C3%ADtica-de-privacidade-glicapp")
        page.update()
    #construção da página
    page.add(Column(expand=True,spacing=10,controls=[
        bright_options,
        Divider(height=0.5),
        ElevatedButton(text='Cor de fundo',icon=Icons.COLOR_LENS_ROUNDED,width=page.width,on_click=color_config),
        Divider(height=0.5),
        
        #termos de uso e privacidade
        Column(alignment=MainAxisAlignment.END,expand=True,controls=[
            Row(alignment=MainAxisAlignment.CENTER,controls=[
            Text('Error 404 - 2025',text_align=TextAlign.CENTER,size=10,weight=FontWeight.BOLD,color=Colors.GREY),
                ]),
            Text('\n',size=1)
        ])
    ]))
    page.update()
