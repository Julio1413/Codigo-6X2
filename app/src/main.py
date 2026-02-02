import flet as ft
from pages import ferramentas, home, login_page
import os, platform

def bem_vindo(page):
    page.clean()
    home.inicial(page)
    page.show_dialog(ft.SnackBar(
        content=ft.Text("Bem vindo(a) ao 6X2_App!"),
        bgcolor=ft.Colors.GREEN,
    ))
    page.update() 


async def main(page: ft.Page):
    page.title = "6X2 O app da 612"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 5

    sistema = platform.system()
    # Windows
    if sistema == "Windows":
        ferramentas.PASTA = r"C:\CubePy\6X2"
        os.makedirs(ferramentas.PASTA, exist_ok=True)
        
    # Android
    elif "ANDROID_BOOTLOGO" in os.environ or (sistema == "Linux" and "arm" in platform.uname().machine):
        storage = ft.StoragePaths()
        ferramentas.PASTA = await storage.get_application_support_directory()

    # macOS
    elif sistema == "Darwin":
        ferramentas.PASTA = os.path.expanduser("~/Library/Application Support/CubePy/6X2")
        os.makedirs(ferramentas.PASTA, exist_ok=True)

    # Linux comum
    elif sistema == "Linux":
        ferramentas.PASTA = os.path.expanduser("~/Cubepy/6X2")
        os.makedirs(ferramentas.PASTA, exist_ok=True)
        
    
    
     
    # Verifica se o arquivo de cor da página existe, se não existir, cria com
    page.padding = 5
    # ---------- DECIDE A PRIMEIRA TELA ----------
    arquivos = ["NOME.txt", "ID.txt", "MATRICULA.txt"]
    todos_existem = all(ferramentas.arquivo_existe(a) for a in arquivos)
    
    # Ver   i   ca se todos os arquivos existem no diretório especificado

    page.clean()

    if todos_existem:
        bem_vindo(page)
    else:
        login_page.login_page_2(page)

    page.update()


ft.app(target=main)
