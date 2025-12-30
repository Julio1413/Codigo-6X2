
import os
import flet as ft
from pages import configs, ferramentas, horarios_aula, supabase
import platform
from datetime import datetime
import calendar

# Funções do calendário
if ferramentas.arquivo_existe("NOME.txt") and ferramentas.arquivo_existe("MATRICULA.txt") and ferramentas.arquivo_existe("ID.txt"):
    nome = ferramentas.ler_arquivo("NOME.txt").strip()
    matricula = ferramentas.ler_arquivo("MATRICULA.txt").strip()
    id_usuario = ferramentas.ler_arquivo("ID.txt").strip()
else:
    nome = "Usuário"
    matricula = "000000"
    id_usuario = "0"



# --- NOVAS FUNÇÕES OBRIGATÓRIAS (APENAS SUPABASE) ---
def listar_eventos(data):
    return supabase.ler_tabela(
        "eventos",
        filtros={"data": f"eq.{data}"}
    ) or []

def adicionar_evento(data, materia, titulo, autor, conteudo):
    registrado = datetime.now().strftime("%d/%m/%Y %H:%M")
    supabase.inserir_linha(
        "eventos",
        {
            "data": data,
            "materia": materia,
            "titulo": titulo,
            "autor": autor,
            "conteudo": conteudo,
            "registrado_em": registrado
        }
    )

def excluir_evento(evento):
    supabase.excluir_linha(
        "eventos",
        filtros={"id": f"eq.{evento['id']}"}
    )


def inicial (page):
    dlg = ft.AlertDialog(
        modal=True,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Container(
            bgcolor=ft.Colors.TRANSPARENT,
            margin=ft.margin.only(top=6,left=7,right=7,bottom=4),
            border_radius=ft.border_radius.all(20),
            expand=True,
            height=150,
            width=300,
            padding=ft.padding.all(6),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(width=50, height=50, color=ft.Colors.BLUE)
                ]
            )
        )
    )
    #page.open(dlg)
    page.update()
    container_color = ferramentas.brightness(page)
    
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month

    calendario_container = ft.Column()
    materias = [
        "Matemática",
        "Português",
        "História",
        "Geografia",
        "Biologia",
        "Física",
        "Química",
        "Inglês",
        "Informática",
        "Artes",
        "Algoritmos",
        "Sociologia",
        "Filosofia",
        "IMMH 1"
        ]
    pasta_global = ferramentas.pasta_global()
    page.clean()
   #page.overlay.clear()
    #page.update()
    if os.path.exists(os.path.join(pasta_global, "bright_mode.txt")):
        with open(os.path.join(pasta_global, "bright_mode.txt"), "r") as file:
            bright_mode = file.read().strip()
    else:
        with open(os.path.join(pasta_global, "bright_mode.txt"), "w") as file:
            file.write("0")
        bright_mode = "0"

    if bright_mode == "0":
        page.theme_mode = ft.ThemeMode.SYSTEM
        if page.platform_brightness == ft.Brightness.LIGHT:
            icon_color = ft.Colors.BLACK
        else:
            icon_color = ft.Colors.WHITE
    elif bright_mode == "1":
        page.theme_mode = ft.ThemeMode.DARK
        icon_color = ft.Colors.WHITE
    elif bright_mode == "2":
        page.theme_mode = ft.ThemeMode.LIGHT
        icon_color = ft.Colors.BLACK

    page.update()
    #Restante do calendário
    def abrir_dialog(dlg):
        page.dialog = dlg
        dlg.open = True
        page.update()

    def fechar_dialog(dlg):
        dlg.open = False
        page.update()

    # -----------------------------
    # MARCAR DIAS COM EVENTO
    # -----------------------------
    def marcar_dias(ano, mes):
        dados = supabase.ler_tabela("eventos") or []
        dias = set()
        for ev in dados:
            y, m, d = map(int, ev["data"].split("-"))
            if y == ano and m == mes:
                dias.add(d)
        return dias

    # -----------------------------
    # VISUALIZAR CONTEÚDO COMPLETO
    # -----------------------------
    def abrir_dialogo_detalhes(evento):

        dlg = ferramentas.dialog(page,
            icone_d=ft.Icons.MENU_BOOK_ROUNDED,
            icone_e=ft.Icons.CALENDAR_TODAY_ROUNDED,
            titulo=f"{evento['titulo']}",
            conteudo=[
                ft.Text(f"Matéria: {evento['materia']}"),
                ft.Text(f"Autor: {evento['autor']}"),
                ft.Text(f"{evento['registrado_em']}"),
                ft.Divider(),
                ft.Text(evento["conteudo"], size=14),
            ]
        )

        page.open(dlg)
        page.update()

    # -----------------------------
    # DIÁLOGO PARA GERENCIAR DIA
    # -----------------------------
    def abrir_dialogo_dia(ano, mes, dia):
        data_str = f"{ano}-{mes:02d}-{dia:02d}"
        lista_eventos = ft.Column(scroll="auto", height=200)

        def atualizar_lista():
            lista_eventos.controls.clear()
            eventos = listar_eventos(data_str)
            for ev in eventos:
                def abrir_conteudo(ev=ev):
                    abrir_dialogo_detalhes(ev)
                def remover(ev=ev):
                    excluir_evento(ev)
                    atualizar_lista()
                    gerar_calendario(ano, mes)
                lista_eventos.controls.append(
                    ft.Container(
                        padding=10,
                        border=ft.border.all(1, "#AAA"),
                        border_radius=10,
                        bgcolor=container_color,
                        content=ft.Column([
                            ft.Text(f"{ev['titulo']} ({ev['materia']})", weight="bold", size=14),
                            ft.Row([
                                ft.TextButton("Ver detalhes", on_click=lambda e, ev=ev: abrir_conteudo(ev)),
                                ft.TextButton("Excluir", on_click=lambda e, ev=ev: remover(ev))
                            ])
                        ])
                    )
                )
            page.update()

        atualizar_lista()

        # --------------- DIALOG PARA ADICIONAR EVENTO ---------------
        campo_titulo = ft.TextField(label="Título", width=250)
        campo_materia = ft.Dropdown(label="Matéria", options=[ft.dropdown.Option(m) for m in materias])
        campo_conteudo = ft.TextField(label="Conteúdo", multiline=True, width=300)

        def abrir_add_evento(e):
            dlg2 = ferramentas.dialog(
                page,
                titulo=f"Adicionar em {dia}/{mes}/{ano}",
                icone_d=ft.Icons.ADD,
                icone_e=ft.Icons.CALENDAR_TODAY_ROUNDED,
                funcao_btn=lambda e: salvar_evento(dlg2),
                texto_btn="Salvar",
                conteudo=[
                    campo_titulo,
                    campo_materia,
                    campo_conteudo
                ]
            )
            page.open(dlg2)
            page.update()

        def salvar_evento(dlg2):
            if not campo_titulo.value or not campo_materia.value or not campo_conteudo.value:
                return
            adicionar_evento(
                data=data_str,
                materia=campo_materia.value,
                titulo=campo_titulo.value,
                autor=nome,
                conteudo=campo_conteudo.value
            )
            atualizar_lista()
            gerar_calendario(ano, mes)
            fechar_dialog(dlg2)
            page.update()

        dlg = ferramentas.dialog(
            page,
            titulo=f"Eventos de {dia}/{mes}/{ano}",
            icone_d=ft.Icons.MENU_BOOK_ROUNDED,
            icone_e=ft.Icons.CALENDAR_TODAY_ROUNDED,
            funcao_btn=abrir_add_evento,
            texto_btn="Adicionar terefa",
            conteudo=[
                ft.Text("Eventos cadastrados:", weight="bold"),
                lista_eventos,
            ]
        )
        page.open(dlg)
        page.update()

    # -----------------------------
    # DESENHAR CALENDÁRIO
    def mes_anterior(e):
        nonlocal mes_atual, ano_atual
        mes_atual -= 1
        if mes_atual < 1:
            mes_atual = 12
            ano_atual -= 1
        gerar_calendario(ano_atual, mes_atual)

    def proximo_mes(e):
        nonlocal mes_atual, ano_atual
        mes_atual += 1
        if mes_atual > 12:
            mes_atual = 1
            ano_atual += 1
        gerar_calendario(ano_atual, mes_atual)
    # -----------------------------
    def gerar_calendario(ano, mes):
        calendario_container.controls.clear()

        titulo = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,on_click=mes_anterior),
            ft.Text(f"{calendar.month_name[mes]} - {ano}", size=22, weight=ft.FontWeight.BOLD),
            ft.IconButton(icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,on_click=proximo_mes)
            ]
        )

        calendario_container.controls.append(titulo)

        cal = calendar.Calendar()
        semanas = cal.monthdayscalendar(ano, mes)

        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        calendario_container.controls.append(
            ft.Row([ft.Text(d, width=40, weight="bold") for d in dias_semana])
        )

        dias_coloridos = marcar_dias(ano, mes)

        for semana in semanas:
            linha = ft.Row()

            for dia in semana:
                if dia == 0:
                    linha.controls.append(
                        ft.Container(width=40, height=40)
                    )
                else:
                    tem_evento = dia in dias_coloridos

                    linha.controls.append(
                        ft.Container(
                            width=40,
                            height=40,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.LIGHT_BLUE_900 if tem_evento else None,
                            border=ft.border.all(1, "#999"),
                            border_radius=5,
                            content=ft.Text(str(dia)),
                            on_click=lambda e, d=dia: abrir_dialogo_dia(ano, mes, d)
                        )
                    )
            calendario_container.controls.append(linha)

        page.update()

    # -----------------------------
    # CONTROLES DE MÊS
    # -----------------------------
   

    gerar_calendario(ano_atual, mes_atual)
    # Costrução da página
    
    def botoes_g(texto,icon,funcao):
        return ft.ElevatedButton(
        on_click=funcao,
        width=250, height=250,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        content=ft.Column(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                ft.Icon(name=icon, size=100, color=icon_color),
                ]),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                ft.Text(texto, size=12, text_align=ft.TextAlign.CENTER)
                ]),
        ])
        )
    
    menu = [
        botoes_g(texto='Calculadora',icon=ft.Icons.CALCULATE_ROUNDED,funcao=lambda _:None),
        botoes_g(texto='Horários de aula',icon=ft.Icons.CALENDAR_TODAY_ROUNDED,funcao=lambda _:horarios_aula.horario(page)),
        botoes_g(texto='Notas',icon=ft.Icons.EDIT_NOTE_ROUNDED,funcao=lambda _:None),
        botoes_g(texto='Links utilitários',icon=ft.Icons.INSERT_LINK_OUTLINED,funcao=lambda _:None),
    ]
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Text(f'\n',size=33),
                            ft.Container(
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            bgcolor=container_color,
                                            padding=ft.padding.all(10),
                                            border_radius=ft.border_radius.all(20),
                                            content=ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    calendario_container
                                                ]
                                            )
                                        )
                                    ]
                                )
                            ),
                            ft.GridView(
                                expand=True,
                                runs_count=2,
                                max_extent=page.width/2,
                                child_aspect_ratio=1,
                                spacing=20,
                                run_spacing=20,
                                controls=menu
                                        ),
                            
                    ]),
                ferramentas.header(titulo="6X2_App", icone=ft.Icons.HOME_ROUNDED, page=page, destino=configs.configs,icone_btn=ft.Icons.SETTINGS_ROUNDED),
                
            ]
        )
    )
    page.update()
