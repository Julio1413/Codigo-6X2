import flet as ft
import os
from pages import ferramentas,home,login_page,github
import shutil

pasta_global = ferramentas.pasta_global()
repo_global = ferramentas.repo_global()

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
    arquivos = ['INFO.txt', 'TOKEN.txt', 'LINK.txt']
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
        if os.path.exists(os.path.join(ferramentas.repo_global())):
            shutil.rmtree(os.path.join(ferramentas.repo_global()))
        
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_global, arquivo)
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
        login_page.login_page_1(page)
    else:
        #do usuario
        with open (os.path.join(pasta_global,'INFO.txt'),'r') as f:
            nome = f.readlines()[0].replace('\n','')
        with open (os.path.join(pasta_global,'INFO.txt'),'r') as f:
            matricula = f.readlines()[1].replace('\n','')
        # Validos
        with open(os.path.join(repo_global,'ID.txt'),'r') as f:
            matriculas_validas = [line.strip() for line in f.readlines()]
                
        with open(os.path.join(repo_global,'NOMES.txt'),'r') as f:
            nomes_validos = [line.strip() for line in f.readlines()]
            
            
        if matricula in matriculas_validas and nome in nomes_validos:
            index = matriculas_validas.index(matricula)
            print(index)
            if nomes_validos[index] == nome and matriculas_validas[index] == matricula:
                with open(os.path.join(pasta_global,'INFO.txt'),'w') as f:
                    f.write(f'{nome}\n{matricula}')
                snack = ft.SnackBar(content=ft.Text('Login - 2 realizado com sucesso!'),bgcolor=ft.Colors.GREEN,open=True)
                page.open(snack)
                home.inicial(page)
                page.update()
                return
            
        else:
            snack = ft.SnackBar(content=ft.Text('Matrícula ou nome inválido.'),bgcolor=ft.Colors.RED,open=True)
            page.open(snack)
            os.remove(os.path.join(pasta_global,'INFO.txt'))
            shutil.rmtree(os.path.join(ferramentas.repo_global()))
            login_page.login_page_1(page)
            page.update()
            page.update()

ft.app(target=main,assets_dir='assets')
