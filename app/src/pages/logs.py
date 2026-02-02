from pages import home, ferramentas,supabase
import flet as ft
import asyncio,os

def logs(page):
    page.clean()
    page.scroll = 'None'

    async def carregar_logs():
        storage = ft.StoragePaths()
        pasta = await storage.get_console_log_filename()

        if os.path.exists(os.path.join(pasta)):
            with open(os.path.join(pasta), "r") as f:
                log = f.read()
        else:
            log = "Nenhum log encontrado."
        
        
        def usuarios(tabela,titulo,icone):
            mensagem_add = 'Usuário adicionado por ' if tabela=='login' else 'ADM adicionado por '
            mensagem_rm = 'Usuário removido por ' if tabela=='login' else 'ADM removido por '
            
            #função de adicionar usuário
            def adicionar_usuario(tbl):
                nome = ft.TextField(label='Nome do usuário')
                matricula = ft.TextField(label='Matrícula do usuário')
                def adicionar():
                    if tbl=='login':
                        supabase.inserir_linha(tbl,{"nome": nome.value, "matricula": matricula.value})
                    else:
                        supabase.inserir_linha(tbl,{"nome": nome.value})
                    supabase.inserir_log(f'{mensagem_add}{ferramentas.ler_arquivo("NOME.txt")}: \n{nome.value}')
                    page.update()
                    page.show_dialog(ft.SnackBar(ft.Text(f"Usuário adicionado com sucesso!"),bgcolor=ft.Colors.GREEN))
                    dialogo.open = False
                
                conteudo = ft.Column(alignment=ft.MainAxisAlignment.START,controls=[nome])
                if tbl=='login':conteudo.controls.append(matricula)
                
                dialogo = ferramentas.dialog(
                    page=page,
                    titulo='Adicionar usuário' if tbl=='login' else 'Adicionar ADM',
                    icone_d=ft.Icons.PERSON_ADD_ROUNDED,
                    funcao_btn=lambda _: adicionar(),
                    texto_btn='Adicionar',
                    icone_e=ft.Icons.INFO_OUTLINE_ROUNDED,
                    conteudo=[conteudo]
                )
                page.show_dialog(dialogo)
            #função de apagar usuário
            def apagar_usuario(tbl,link_id):
                supabase.excluir_linha(tbl,{"nome": f"eq.{link_id}"})
                supabase.inserir_log(f'{mensagem_rm}{ferramentas.ler_arquivo("NOME.txt")}: \n{link_id}')
                page.show_dialog(ft.SnackBar(ft.Text(f"Usuário removido com sucesso!"),bgcolor=ft.Colors.GREEN))
                page.update() 
                
            #lista de usuários
            usuarios = supabase.ler_tabela(tabela)
            conteudo = []
            for usuario in usuarios:
                conteudo.append(
                    ft.Container(
                        bgcolor=ferramentas.brightness(page),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.IconButton(icon=ft.Icons.DELETE_ROUNDED,icon_color=ft.Colors.RED,tooltip="Remover usuário",on_click=lambda _, nome=usuario:apagar_usuario(tabela,nome['nome'])),
                                ft.Text(f"{usuario['nome']}", selectable=True),
                            ]
                        )
                    )
                )
            #dialogo principal
            dialog =ferramentas.dialog(
                    page=page,
                    titulo=titulo,
                    icone_d=icone,
                    funcao_btn=lambda _:adicionar_usuario(tabela),
                    texto_btn='Adicionar usuário' if tabela=='login' else 'Adicionar ADM',
                    icone_e=ft.Icons.INFO_OUTLINE_ROUNDED,
                    conteudo=conteudo        
                    )
            page.show_dialog(dialog)
        
        def log_dialog():

            conteudo=[]
            logs = supabase.ler_tabela('logs')
            for log in logs[::-1]:
                conteudo.append(ft.Text(f"Registrado em: {log['registrado_em']}\nPor: {log['autor']}\n {log['mensagem']}", selectable=True))
                conteudo.append(ft.Divider())
                
            dlg = ferramentas.dialog(
                page=page,
                titulo='Logs do servidor',
                icone_d=ft.Icons.BUILD_ROUNDED,
                icone_e=ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED,
                conteudo=conteudo
            )
            page.show_dialog(dlg)
        
        
        
        def botao_sheet(
            icone,titulo,funcao
        ):
            return ft.ElevatedButton(
                on_click=funcao,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Icon(icone, size=20,color=ferramentas.brightness_text(page)),
                        ft.Text(titulo, size=13,color=ferramentas.brightness_text(page)),
                    ]
                )
                )
        
            
        def abrir_sheet():
            sheet = ferramentas.bottom_sheet(
                    page=page,
                    titulo='Opções do administrador',
                    icone_d=ft.Icons.BUILD_ROUNDED,
                    icone_e=ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED,
                    controles=[
                        botao_sheet(icone=ft.Icons.SETTINGS_SYSTEM_DAYDREAM_ROUNDED,titulo='Logs do servidor',funcao=log_dialog),
                        botao_sheet(icone=ft.Icons.PERSON,titulo='Gerenciar usuários',funcao=lambda _:usuarios('login','Gerenciar usuários',ft.Icons.PERSON)),
                        botao_sheet(icone=ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED,titulo='Gerenciar ADMs',funcao=lambda _:usuarios('adm','Gerenciar ADMs',ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED)   ),
                    ]
                )
            page.show_dialog(sheet)
        page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.BUILD_ROUNDED,
        on_click=lambda _:abrir_sheet(),
        tooltip="Outras opções",
        bgcolor=page.bgcolor,
        )
        
        
        
        page.add(ferramentas.header(
            titulo='Logs',
            page=page,
            icone=ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED
        ))

        page.add(ferramentas.container(page=page,
            controles=[ft.Text(log, selectable=True)]
        ))

        page.update()

    page.run_task(carregar_logs)