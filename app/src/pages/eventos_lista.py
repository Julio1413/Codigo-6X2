import flet as ft
from pages import supabase,ferramentas, home
from datetime import datetime, date
import json


def eventos_lista(page,filtro = ''):
    page.clean()
    page.scroll = "None"
    coluna_main = ft.Column(alignment=ft.MainAxisAlignment.START,scroll="auto",expand=True)
    coluna_main.controls.clear()
    eventos = supabase.ler_tabela("eventos")

    hoje = date.today()

    eventos_futuros = [
    e for e in eventos
    if datetime.strptime(e["data"], "%Y-%m-%d").date() >= hoje
    ]

    eventos = sorted(
        eventos_futuros,
        key=lambda e: datetime.strptime(e["data"], "%Y-%m-%d")
        )


    #loop para adicionar os eventos
    for evento in eventos:
        data = evento['data']
        materia = evento['materia']
        titulo = evento['titulo']
        autor = evento['autor']
        conteudo = evento['conteudo']
        registrado_em = evento['registrado_em']

        if filtro in materia or filtro == '':
            coluna_main.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLACK_12),
                    border_radius=ft.border_radius.all(27),
                    padding=ft.padding.all(13),
                    margin=ft.margin.only(bottom=10),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Icon(icon=ft.Icons.CALENDAR_TODAY_ROUNDED),    
                                    ft.Text(f"{titulo} | {materia}", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Icon(icon=ft.Icons.ACCESS_TIME_FILLED_ROUNDED),
                                    ]
                                ),
                            ft.Divider(color=ferramentas.brightness_text(page)),
                            ft.Text(f"Data: {data}", size=14),
                            ft.Text(f"Registrado por: {autor} em {registrado_em}", size=12),
                            ft.Divider(color=ferramentas.brightness_text(page)),
                            ft.Text(conteudo, size=14),
                        ]
                    )
                )
            )
    if len(coluna_main.controls) == 0:
        coluna_main.controls.append(
            ft.Text("Nenhuma tarefa encontrado para o filtro selecionado.", size=14)
        )
        page.show_dialog(ft.SnackBar(ft.Text('Nenhum evento encontrado para o filtro selecionado.'),bgcolor=ft.Colors.RED))
    else:
        if filtro != '':
            page.show_dialog(ft.SnackBar(ft.Text(f'{len(coluna_main.controls)} tarefas encontradas para {filtro}!'),bgcolor=ft.Colors.GREEN))
    #header da página
    page.add(ferramentas.header(page=page,titulo="Exibição em Lista",icone=ft.Icons.FORMAT_LIST_BULLETED_ROUNDED))
    
    
    dropdown = ft.Dropdown(border_radius=27,label="Filtrar por matéria", options=[ft.dropdown.Option(m) for m in home.materias],expand=True)
    if filtro != '':dropdown.value = filtro
    page.add(ferramentas.container(page=page,controles=[
            ft.Row(
                controls=[
                    dropdown,
                    ft.IconButton(
                        icon=ft.Icons.SEARCH_ROUNDED,
                        on_click=lambda _: eventos_lista(page,filtro=dropdown.value)
                    )
                ]
            ),
            ft.Divider(),
            coluna_main
    ]))