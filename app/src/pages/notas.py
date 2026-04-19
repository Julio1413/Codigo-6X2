import flet as ft
import os,shutil
from pages import ferramentas, home
from datetime import datetime

def notas(page):
    #gerenciaento de pagina
    page.clean()
    page.scroll = 'None'
    page.add(ferramentas.header(titulo="Notas",page=page,icone=ft.Icons.EDIT_NOTE_ROUNDED))
    
    #exibindo arquivos    
    pasta_principal = os.path.join(ferramentas.PASTA,"notas")
    if os.path.exists(pasta_principal):
        arquivos = os.listdir(pasta_principal)
    else:
        arquivos = []
        os.makedirs(pasta_principal, exist_ok=True)
    
    #funcoes das notas
    def nova_nota():
        def salvar(conteudo, arquivo):
            # Se o título estiver vazio, previne o erro de permissão (IsADirectoryError: É um diretório)
            if not arquivo or not arquivo.strip():
                page.show_dialog(ft.SnackBar(ft.Text("A nota precisa de um título!"), bgcolor=ft.Colors.RED))
                page.update()
                return

            with open(os.path.join(pasta_principal, arquivo), "w") as f:
                f.write(conteudo)
                
            notas(page)
            page.show_dialog(ft.SnackBar(ft.Text("Nota salva com sucesso!"), bgcolor=ft.Colors.GREEN))
            page.update()
            
        nova_nota_titulo = ft.TextField(
                    keyboard_type=ft.KeyboardType.TEXT,
                    value='',
                    width=page.width,
                    label="Título da nota",
                )
        nova_nota_conteudo = ft.TextField(
                    keyboard_type=ft.KeyboardType.TEXT,
                    value='',
                    width=page.width,
                    height=400,
                    border_color=ft.Colors.TRANSPARENT,
                    multiline=True,
                    expand=True,
                    label="Conteúdo da nota",
                )
       
        page.clean()
        page.floating_action_button = ft.FloatingActionButton(bgcolor=page.bgcolor,icon=ft.Icons.SAVE_ROUNDED,on_click=lambda _: salvar(nova_nota_conteudo.value, nova_nota_titulo.value))
        page.add(ferramentas.header(page=page,titulo="Notas",icone=ft.Icons.EDIT_NOTE_ROUNDED,destino=lambda _: notas(page)))
        page.add(
            ferramentas.container(
                page=page,
                controles=[
                    nova_nota_titulo,
                    nova_nota_conteudo
                ]
            )
        )
    
    def excluir(arquivo):
        def permanentemente():
            os.remove(os.path.join(pasta_principal, arquivo))
            page.show_dialog(ft.SnackBar(ft.Text("Nota removida com sucesso!"), bgcolor=ft.Colors.GREEN))
            page.update()
            ferramentas.fechar_dialog(page, dlg)
            notas(page)
        dlg = ferramentas.dialog(
            page=page,
            titulo="Excluir nota",
            icone_d=ft.Icons.DELETE_ROUNDED,
            icone_e=ft.Icons.INFO,
            funcao_btn=lambda _: permanentemente(),
            texto_btn="Excluir",
            conteudo=[
                ft.Text("Tem certeza que deseja excluir essa nota permanentemente? Esta ação não pode ser desfeita."),
            ]
        )
        page.show_dialog(dlg)

    def editar(arquivo):
        def salvar(conteudo, arquivo):
            ferramentas.criar_arquivo(f"notas/{arquivo}", conteudo)
            with open(os.path.join(pasta_principal, arquivo), "w") as f:
                f.write(conteudo)
            
            notas(page)
            page.show_dialog(ft.SnackBar(ft.Text("Nota salva com sucesso!"), bgcolor=ft.Colors.GREEN))
            page.update()
        conteudo = ferramentas.ler_arquivo(f"notas/{arquivo}")
        nota = ft.TextField(
                    keyboard_type=ft.KeyboardType.TEXT,
                    value=conteudo,
                    width=page.width,
                    height=400,
                    border_color=ft.Colors.TRANSPARENT,
                    multiline=True,
                    expand=True,
                    label="Conteúdo da nota",
                )
        
        page.clean()
        page.floating_action_button = ft.FloatingActionButton(bgcolor=page.bgcolor,icon=ft.Icons.SAVE_ROUNDED,on_click=lambda _: salvar(nota.value, arquivo))
        page.add(ferramentas.header(page=page,titulo=arquivo,icone=ft.Icons.EDIT_NOTE_ROUNDED,destino=lambda _: notas(page)))
        page.add(ferramentas.container(page=page,controles=[nota]))
        page.update()

        
        
    #coluna principal    
    coluna_main = ft.Column(controls=[], expand=True, scroll="AUTO")
    for arquivo in arquivos:
        coluna_main.controls.append(
            ft.Container(
                on_click=lambda _, arq=arquivo: editar(arq),
                height=65,
                width=page.width,
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLACK_12),
                border_radius=ft.border_radius.all(27),
                padding=ft.padding.all(13),
                content=ft.Row(
                    width=page.width,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(arquivo, size=16, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.Text(
                                    datetime.fromtimestamp(
                                        os.stat(os.path.join(pasta_principal, arquivo)).st_mtime
                                    ).strftime("%Y-%m-%d %H:%M"),
                                    size=12
                                ),
                                ft.IconButton(
                                    bgcolor=ft.Colors.WHITE_12,
                                    icon=ft.Icons.DELETE_ROUNDED,
                                    icon_color=ft.Colors.RED,
                                    width=35,
                                    height=35,
                                    icon_size=17,
                                    tooltip="Remover nota",
                                    on_click=lambda _, arq=arquivo: excluir(arq)
                                ),
                            ]
                        )
                    ],
                ),
            )
        )
        
        
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda _: nova_nota(),
        tooltip="Adicionar nova nota",
        bgcolor=page.bgcolor,
    )
    page.add(ferramentas.container(
        page=page,
        controles=
            ft.Column(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text("Minhas Notas", weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    coluna_main
                ]
            )
        )
    )
    