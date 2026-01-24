from pages import home, ferramentas
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