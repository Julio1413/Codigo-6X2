import flet as ft
from pages import home, ferramentas


def horario(page):
    page.clean()
    page.add(ferramentas.header(titulo="Horários de aula", icone=ft.Icons.CALENDAR_TODAY_ROUNDED,page=page))
    page.add(ferramentas.container(page=page, controles=[
        ft.Column(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.ExpansionTile(
                title=ft.Text("Segunda-feira", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("7:00 - 12:10"),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=True,
                controls=[
                    ft.Row([ft.Text('7:10 - 8:40 Matemática', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('8:40 - 10:20 - Inglês', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('10:30 - 12:10 - Biologia', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                ],
            ),
        ft.ExpansionTile(
                title=ft.Text("Terça-feira", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("7:00 - 12:10"),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=True,
                controls=[
                    ft.Row([ft.Text('7:10 - 8:40 - IMMH 1', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('8:40 - 10:20 - ALP', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('10:30 - 12:10 - Informática Básica', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                ],
            ),
        ft.ExpansionTile(
                title=ft.Text("Quarta-feira", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("7:00 - 16:30"),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=True,
                controls=[
                    ft.Row([ft.Text('7:10 - 8:40 - Artes', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('8:40 - 10:20 - Informática Básica', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('13:00 - 14:40 - Matemática', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('14:50 - 16:30 - ALP', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                ],
            ),
        ft.ExpansionTile(
                title=ft.Text("Quinta-feira", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("7:00 - 12:10"),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=True,
                controls=[
                    ft.Row([ft.Text('7:10 - 8:40 - Química', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('8:40 - 10:20 - Física', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('10:30 - 12:10 - Português', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                ],
            ),
        ft.ExpansionTile(
                title=ft.Text("Sexta-feira", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("7:00 - 16:30"),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=True,
                controls=[
                    ft.Row([ft.Text('7:10 - 8:40 - Português', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('8:40 - 10:20 - Geografia', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('10:30 - 12:10 - História', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('14:50 - 15:40 - Filosofia', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Row([ft.Text('15:40 - 16:30 - Sociologia', weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.START),
                ],
            ),
            ]
        )
    ]))
    page.update()