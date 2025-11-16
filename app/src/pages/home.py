import os
import flet as ft
from pages import configs, ferramentas
import platform
import json
from datetime import datetime
import calendar
# Funções do calendário
sistema = platform.system()

if sistema == "Windows":
    pasta_global = r'C:\CubePy\6X2'
    os.makedirs(pasta_global, exist_ok=True)
elif "ANDROID_BOOTLOGO" in os.environ or (sistema == "Linux" and "arm" in platform.uname().machine):
    pasta_global = os.getenv("FLET_APP_STORAGE_DATA")  # Pasta de dados do app no Android
elif sistema == "Linux":
    pasta_global = os.path.expanduser("~/Cubepy/6X2")  # Diretório oculto no home do usuário
    os.makedirs(pasta_global, exist_ok=True)
else:
    pasta_global = r'C:\CubePy\6X2'  # Valor padrão caso o sistema não seja identificado
    os.makedirs(pasta_global, exist_ok=True)
    
if sistema == "Windows":
    repo_global = r'C:\CubePy\6X2\repo'
    os.makedirs(repo_global, exist_ok=True)
elif "ANDROID_BOOTLOGO" in os.environ or (sistema == "Linux" and "arm" in platform.uname().machine):
    repo_global = os.getenv("FLET_APP_STORAGE_DATA/repo")  # Pasta de dados do app no Android
elif sistema == "Linux":
    repo_global = os.path.expanduser("~/Cubepy/6X2/repo")  # Diretório oculto no home do usuário
    os.makedirs(repo_global, exist_ok=True)
else:
    repo_global = r'C:\CubePy\6X2\repo'  # Valor padrão caso o sistema não seja identificado
    os.makedirs(repo_global, exist_ok=True)
    
with open (os.path.join(pasta_global, "INFO.txt"), "r") as f:
    infos = f.readlines()
    
ARQUIVO = os.path.join(repo_global,"eventos.json")
AUTOR_GLOBAL = infos[0].replace('\n','')
print(AUTOR_GLOBAL)

def carregar_eventos():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w") as f:
            json.dump({"eventos": []}, f, indent=4)

    with open(ARQUIVO, "r") as f:
        return json.load(f)


def salvar_eventos(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)


def adicionar_evento(data, materia, titulo, autor, conteudo):
    dados = carregar_eventos()
    registrado = datetime.now().strftime("%d/%m/%Y %H:%M")

    dados["eventos"].append({
        "data": data,
        "materia": materia,
        "titulo": titulo,
        "autor": autor,
        "conteudo": conteudo,
        "registrado_em": registrado
    })

    salvar_eventos(dados)


def listar_eventos(data):
    dados = carregar_eventos()
    return [ev for ev in dados["eventos"] if ev["data"] == data]


def excluir_evento(evento):
    dados = carregar_eventos()
    dados["eventos"].remove(evento)
    salvar_eventos(dados)


def inicial (page):
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
    page.add(ferramentas.header(titulo="6X2_App", icone=ft.Icons.HOME_ROUNDED, page=page, destino=configs.configs,icone_btn=ft.Icons.SETTINGS_ROUNDED))
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
        dados = carregar_eventos()
        dias = set()

        for ev in dados["eventos"]:
            y, m, d = map(int, ev["data"].split("-"))
            if y == ano and m == mes:
                dias.add(d)

        return dias

    # -----------------------------
    # VISUALIZAR CONTEÚDO COMPLETO
    # -----------------------------
    def abrir_dialogo_detalhes(evento):

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{evento['titulo']}"),
            content=ft.Column([
                ft.Text(f"Matéria: {evento['materia']}"),
                ft.Text(f"Autor: {evento['autor']}"),
                ft.Text(f"Registrado em: {evento['registrado_em']}"),
                ft.Divider(),
                ft.Text(evento["conteudo"], size=14),
            ], tight=True),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(dlg))
            ]
        )
        dlg = ferramentas.dialog(
            
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

            for ev in listar_eventos(data_str):

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
                            ft.Text(f"{ev['titulo']} ({ev['materia']})",
                                   weight="bold", size=14),
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
        campo_materia = ft.Dropdown(label="Matéria",
                                    options=[ft.dropdown.Option(m) for m in materias])
        campo_conteudo = ft.TextField(label="Conteúdo", multiline=True, width=300)

        def abrir_add_evento(e):
            dlg2 = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Adicionar evento em {dia}/{mes}/{ano}"),
                content=ft.Column([
                    campo_titulo,
                    campo_materia,
                    campo_conteudo
                ], tight=True),
                actions=[
                    ft.TextButton("Salvar", on_click=lambda e: salvar_evento(dlg2)),
                    ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(dlg2))
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
                autor=AUTOR_GLOBAL,
                conteudo=campo_conteudo.value
            )

            atualizar_lista()
            gerar_calendario(ano, mes)
            fechar_dialog(dlg2)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Eventos de {dia}/{mes}/{ano}"),
            content=ft.Column([
                ft.Text("Eventos cadastrados:", weight="bold"),
                lista_eventos,
                ft.Divider(),
                ft.TextButton("Adicionar novo evento", icon=ft.Icons.ADD, on_click=abrir_add_evento)
            ], tight=True),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(dlg))
            ]
        )

        page.open(dlg)
        page.update()

    # -----------------------------
    # DESENHAR CALENDÁRIO
    # -----------------------------
    def gerar_calendario(ano, mes):
        calendario_container.controls.clear()

        titulo = ft.Text(f"{calendar.month_name[mes]} - {ano}",
                         size=22, weight=ft.FontWeight.BOLD)

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
                            bgcolor="#FFD27F" if tem_evento else None,
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
    page.add(ft.Container(
        width=page.width,
        bgcolor=container_color,
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(20),
        alignment=ft.alignment.center,
        content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
                                ft.ElevatedButton("← Mês anterior", on_click=mes_anterior),
                                ft.ElevatedButton("Próximo mês →", on_click=proximo_mes)
                        ]),
                            calendario_container
            ]
        )
            ]
        )
    ))
   

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
        
    ]
    page.update()
