from flet import Page, Text, SnackBar, Colors, ThemeMode, app
import os
from pages import ferramentas,home,login_page

pasta_global = ferramentas.pasta_global()

#paginas de boas vindas
def bem_vindo(page):
    home.inicial(page)
    snack = SnackBar(content=Text('Bem vindo(a) ao 6X2_App!'),bgcolor=Colors.GREEN,open=True)
    page.open(snack)
    page.update()

def main (page= Page):
    page.title = "Glicapp"
    page.theme_mode = ThemeMode.SYSTEM
    page.window.maximizable = True
    page.window.resizable = True
    page.scroll = 'none'
    arquivos = ['INFO.txt','LOGIN.txt']
    page.add(Text(f'\n'))


    # Verifica se o arquivo de cor da página existe,sudo se não existir, cria com
    arquivo_cor = os.path.join(pasta_global, "page_bgcolor.txt")
    page.padding = 5
    if os.path.exists(arquivo_cor):
        with open(arquivo_cor, "r") as file:
            cor_pagina = file.read().strip()
            page.bgcolor = getattr(Colors, cor_pagina, Colors.LIGHT_BLUE)  # Se a cor for inválida, usa preto como fallback
    else:
        cor_pagina = "LIGHT_BLUE"  # Apenas o nome da cor, sem "Colors."
        page.bgcolor = getattr(Colors, cor_pagina, Colors.BLACK)
        with open(arquivo_cor, "w") as file:
            file.write(cor_pagina)  # Salva só o nome da cor
    # Verifica se todos os arquivos existem no diretório especificado
    todos_existem = all(os.path.exists(os.path.join(pasta_global, arquivo)) for arquivo in arquivos)

    if not todos_existem:
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_global, arquivo)
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
        login_page.login_page_1(page)
    else:
        bem_vindo(page)

app(target=main,assets_dir='assets')
