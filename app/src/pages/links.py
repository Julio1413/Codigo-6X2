import flet as ft
from pages import ferramentas, home, supabase
import asyncio

def links_page(page):
    page.clean()
    page.scroll = 'None'
    links = supabase.ler_tabela('links')
    links.reverse()
    
    desativar_excluir = True
    for pessoa in supabase.ler_tabela('adm'):
        if pessoa['nome'].lower() == ferramentas.ler_arquivo('NOME.txt').lower():
            desativar_excluir = False

    coluna_main = ft.Column(controls=[], expand=True, scroll="AUTO")
    
    for link in links:
        titulo = link.get('titulo', 'Sem título')
        url = link.get('link', '#')
        autor = link.get('autor', 'Desconhecido')
        data = link.get('registrado_em', 'Data desconhecida')
        desc = link.get('descrição', '')

        async def copiar_link(url):        
            await ft.Clipboard().set(url)
            page.show_dialog(ft.SnackBar(ft.Text(f"Link copiado para a área de transferência:\n{url}"), bgcolor=ft.Colors.GREEN))


        async def abrir_link(url):
            url_launcher = ft.UrlLauncher()
            await url_launcher.launch_url(url)
            
        def excluir_link(link_id):
            supabase.excluir_linha("links",{"id": f"eq.{link_id}"})
            links_page(page)
            page.update()
            
        loop = asyncio.get_event_loop()
        coluna_main.controls.append(
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.3,ft.Colors.BLACK_26),
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
                        ft.Divider(),
                        ft.Text(f"Link: {url}", size=12, color=ft.Colors.BLUE),
                        ft.Text(f"Adicionado por: {autor} em {data}", size=12),
                        ft.Text(f"Descrição:\n {desc}", size=12),
                        ft.Divider(),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            scroll='None',
                            spacing=7,
                            controls=[
                                ft.ElevatedButton(
                                    expand=True,
                                    bgcolor=ft.Colors.WHITE_12,
                                    on_click=lambda _, u=url: asyncio.run_coroutine_threadsafe(abrir_link(u), loop),
                                    data=url,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(url, color=ft.Colors.BLUE)
                                        ],
                                    ),
                                ),
                                ft.IconButton(bgcolor=ft.Colors.WHITE_12,icon_color=ft.Colors.BLUE,width=35,height=35,icon_size=17,icon=ft.Icons.COPY, tooltip="Copiar url", on_click=lambda _, u=url: asyncio.run_coroutine_threadsafe(copiar_link(u), loop)),
                            ]
                        ),
                    ]
                ),
            )
        )
    
    def adicionar_link():
        descricao = ft.TextField('',width=page.width,label='Descrição',expand=True,border_color=ft.Colors.TRANSPARENT,multiline=True)
        titulo = ft.TextField('',width=page.width,label='Título')
        link = ft.TextField('',width=page.width,label='Link (URL)')
        def adicionar():
            if descricao.value and titulo.value and link.value:
                from datetime import datetime
                agora = datetime.now()
                data_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
                supabase.inserir_linha('links',{
                    'titulo': titulo.value,
                    'link': link.value,
                    'descrição': descricao.value,
                    'autor': ferramentas.ler_arquivo('NOME.txt').strip(),
                    'registrado_em': data_formatada
                })
                links_page(page)
                page.update()
                
                
        page.show_dialog(ferramentas.dialog(
            page=page,
            titulo="Adicionar link",
            icone_d=ft.Icons.ADD_LINK_ROUNDED,
            icone_e=ft.Icons.INFO,
            funcao_btn=lambda _: adicionar(),
            texto_btn="Adicionar",
            conteudo=[
                titulo,
                link,
                descricao,
            ]
        ))
        page.update()
    #action button
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda _:adicionar_link(),
        tooltip="Adicionar novo link",
        bgcolor=ft.Colors.LIGHT_BLUE,
    )

    #header da página
    page.add(ferramentas.header(
        titulo="Links utilitários",
        icone=ft.Icons.LINK,
        page=page,
        destino=home.inicial
    ))
    #container principal
    page.add(ferramentas.container(
        controles=[
            ft.Text("Links utilitários",size=15,weight=ft.FontWeight.BOLD),
            coluna_main,
    
            ],
        page=page,
    ))
    
    page.update()