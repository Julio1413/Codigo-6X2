import flet as ft
import os
from pages import ferramentas,home,login_page,supabase

#paginas de boas vindas
def bem_vindo(page):
    home.inicial(page)
    snack = ft.SnackBar(content=ft.Text('Bem vindo(a) ao 6X2_App!'),bgcolor=ft.Colors.GREEN,open=True)
    page.open(snack)
    page.update()

def main (page= ft.Page):
    page.title = "6X2 O app da 612"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window.maximizable = True
    page.window.resizable = True
    page.scroll = 'none'
    arquivos = ['NOME.txt','ID.txt','MATRICULA.txt']
    page.add(ft.Text(f'\n'))
    
    
    # Verifica se o arquivo de cor da página existe, se não existir, cria com
    arquivo_cor = "page_bgcolor.txt"
    page.padding = 5
    if ferramentas.arquivo_existe(arquivo_cor):
        cor_pagina = ferramentas.ler_arquivo(arquivo_cor).strip()
        page.bgcolor = getattr(ft.Colors, cor_pagina, ft.Colors.LIGHT_BLUE)  # Se a cor for inválida, usa preto como fallback
    else:
        cor_pagina = "LIGHT_BLUE"  # Apenas o nome da cor, sem "Colors."
        page.bgcolor = getattr(ft.Colors, cor_pagina, ft.Colors.BLACK)
        ferramentas.criar_arquivo(nome=arquivo_cor,conteudo=cor_pagina) # Salva só o nome da cor
    # Ver   i   ca se todos os arquivos existem no diretório especificado
    todos_existem = all(ferramentas.arquivo_existe(nome=arquivo) for arquivo in arquivos)

    if not todos_existem:        
        for arquivo in arquivos:
            if ferramentas.arquivo_existe(arquivo):
                ferramentas.excluir_arquivo(arquivo)
        login_page.login_page_2(page)
    else:

        bem_vindo(page)
        
        
ft.app(target=main,assets_dir='assets')
