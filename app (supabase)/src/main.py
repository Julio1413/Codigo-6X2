import flet as ft
import os
from pages import ferramentas,home,login_page,supabase
import shutil

pasta_global = ferramentas.pasta_global()

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
    arquivos = ['INFO.txt', 'URL_FILE.txt', 'TOKEN_FILE.txt']
    page.add(ft.Text(f'\n'))


    # Verifica se o diretório global existe, se não, cria o diretório
    if not os.path.exists(pasta_global):
        os.makedirs(pasta_global)

    # Verifica se o arquivo de cor da página existe, se não existir, cria com
    arquivo_cor = os.path.join(pasta_global, "page_bgcolor.txt")
    page.padding = 5
    if os.path.exists(arquivo_cor):
        with open(arquivo_cor, "r") as file:
            cor_pagina = file.read().strip()
            page.bgcolor = getattr(ft.Colors, cor_pagina, ft.Colors.LIGHT_BLUE)  # Se a cor for inválida, usa preto como fallback
    else:
        cor_pagina = "LIGHT_BLUE"  # Apenas o nome da cor, sem "Colors."
        page.bgcolor = getattr(ft.Colors, cor_pagina, ft.Colors.BLACK)
        with open(arquivo_cor, "w") as file:
            file.write(cor_pagina)  # Salva só o nome da cor
    # Ver   i   ca se todos os arquivos existem no diretório especificado
    todos_existem = all(os.path.exists(os.path.join(pasta_global, arquivo)) for arquivo in arquivos)

    if not todos_existem:        
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_global, arquivo)
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
        login_page.login_page_1(page)
    else:
        # Leitura correta do INFO.txt
        with open(os.path.join(pasta_global, 'INFO.txt'), 'r') as f:
            linhas = f.read().splitlines()
        nome = linhas[0]
        matricula = linhas[1]
        id = linhas[2]  # string UUID

        with open(os.path.join(pasta_global, 'TOKEN_FILE.txt'), 'r') as f:
            token = f.read().splitlines()[0]
        with open(os.path.join(pasta_global, 'URL_FILE.txt'), 'r') as f:
            url = f.read()

        usuario = supabase.ler_tabela(
            "login",
            filtros={"id": f"eq.{id}"}
        )

        if (
            supabase.testar_conexao(url, token)
            and usuario
            and usuario[0]["matricula"] == matricula
            and usuario[0]["nome"] == nome
        ):
            bem_vindo(page)
        else:
            for arquivo in arquivos:
                caminho_arquivo = os.path.join(pasta_global, arquivo)
                if os.path.exists(caminho_arquivo):
                    os.remove(caminho_arquivo)
            login_page.login_page_1(page)
        
ft.app(target=main,assets_dir='assets')
