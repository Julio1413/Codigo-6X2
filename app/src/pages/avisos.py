import flet as ft
from pages import ferramentas, home, supabase

def avisos(page):
    page.clean()
    page.scroll = 'None'
    links = supabase.ler_tabela('avisos')
    links.reverse()
    
        
    desativar_excluir = True
    for pessoa in supabase.ler_tabela('adm'):
        if pessoa['nome'].lower() == ferramentas.ler_arquivo('NOME.txt').lower():
            desativar_excluir = False

    coluna_main = ft.Column(controls=[], expand=True, scroll="AUTO")
    
    for link in links:
        titulo = link.get('titulo', 'Sem título')
        autor = link.get('autor', 'Desconhecido')
        data = link.get('registrado_em', 'Data desconhecida')
        mensagem = link.get('mensagem', '')

            
        def excluir_link(link_id):
            supabase.excluir_linha("avisos",{"id": f"eq.{link_id}"})
            avisos(page)
            page.update()
            
        coluna_main.controls.append(
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.15,ft.Colors.BLACK_12),
                border_radius=ft.border_radius.all(27),
                padding=ft.padding.all(13),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.IconButton(bgcolor=ft.Colors.WHITE_12,icon=ft.Icons.LINK_ROUNDED, icon_color=ft.Colors.BLUE,width=35,height=35,icon_size=17),
                                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
                                ft.IconButton(disabled=desativar_excluir,width=35,height=35,icon_size=17,bgcolor=ft.Colors.WHITE_12,icon=ft.Icons.DELETE_ROUNDED, icon_color=ft.Colors.RED, tooltip="Remover link (apenas para ADMs!)", on_click=lambda _: excluir_link(link['id']) ),
                            ],
                        ),
                        ft.Divider(color=ferramentas.brightness_text(page)),
                        ft.Text(f"Adicionado por: {autor} em {data}", size=12),
                        ft.Text(f'Aviso: \n{mensagem}', size=14),
                        ft.Divider(color=ferramentas.brightness_text(page)),
                    ]
                ),
            )
        )
    
    def adicionar_link():
        descricao = ft.TextField('',width=page.width,label='Aviso',expand=True,border_color=ft.Colors.TRANSPARENT,multiline=True)
        titulo = ft.TextField('',width=page.width,label='Título')
        def adicionar():
            if descricao.value and titulo.value:
                from datetime import datetime
                agora = datetime.now()
                data_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
                supabase.inserir_linha('avisos',{
                    'registrado_em': data_formatada,
                    'autor': ferramentas.ler_arquivo('NOME.txt').strip(),
                    'mensagem': descricao.value,
                    'titulo': titulo.value,
                })
                avisos(page)
                ferramentas.fechar_dialog(page,dlg)
                page.show_dialog(ft.SnackBar(ft.Text("Aviso adicionado com sucesso!"),bgcolor=ft.Colors.GREEN))
                page.update()
            else:
                page.show_dialog(ft.SnackBar(ft.Text("Preencha todos os campos!"),bgcolor=ft.Colors.RED))
                
        dlg = ferramentas.dialog(
            page=page,
            titulo="Adicionar link",
            icone_d=ft.Icons.ADD_LINK_ROUNDED,
            icone_e=ft.Icons.INFO,
            funcao_btn=lambda _: adicionar(),
            texto_btn="Adicionar",
            conteudo=[
                titulo,
                descricao,
            ]
        )
        page.show_dialog(dlg)
        page.update()
    #action button
    if desativar_excluir == False:
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=lambda _:adicionar_link(),
            tooltip="Adicionar novo link",
            bgcolor=page.bgcolor,
        )

    #header da página
    page.add(ferramentas.header(
        titulo="Avisos",
        icone=ft.Icons.LINK,
        page=page,
        destino=home.inicial
    ))
    #container principal
    page.add(ferramentas.container(
        controles=[
            ft.Text("Avisos",weight=ft.FontWeight.BOLD),
            ft.Divider(),
            coluna_main,
    
            ],
        page=page,
    ))
    
    page.update()