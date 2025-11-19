import os
from git import Repo, GitCommandError
import flet as ft
from pages import home, ferramentas, login_page

# ======================================================
# CONFIGURAÇÕES GLOBAIS
# ======================================================

# Pasta global onde o repositório será salvo
pasta_global = os.path.join(f'{ferramentas.repo_global()}')

def carregamento (funcao,page):
    page.add(
        ft.Column(
            
        )
    )

# ======================================================
# FUNÇÃO: CLONAR
# ======================================================

def clone_repo(token,link):
    GITHUB_TOKEN = "SEU_TOKEN_AQUI"       # <- substitua antes de rodar

    # Link HTTPS do repositório sem credenciais
    REPO_URL_BASE = "https://github.com/usuario/repositorio.git"

    # Montagem automática com token
    if GITHUB_TOKEN:
        REPO_URL = REPO_URL_BASE.replace(
            "https://", f"https://{GITHUB_TOKEN}:x-oauth-basic@"
        )
    else:
        REPO_URL = REPO_URL_BASE
    try:
        if not os.path.exists(pasta_global):
            os.makedirs(pasta_global)

        Repo.clone_from(REPO_URL, pasta_global)
        return True

    except GitCommandError:
        return False
    except Exception:
        return False


# ======================================================
# FUNÇÃO: PULL
# ======================================================

def atualizar_repo():
    try:
        repo = Repo(pasta_global)
        origin = repo.remotes.origin
        origin.pull()
        return True

    except Exception:
        return False


# ======================================================
# FUNÇÃO: COMMIT + PUSH
# ======================================================

def commit_push(mensagem="Atualização automática"):
    try:
        repo = Repo(pasta_global)

        # Adiciona tudo
        repo.git.add("--all")

        # Comita
        repo.index.commit(mensagem)

        # Push
        origin = repo.remotes.origin
        origin.push()

        return True

    except Exception:
        return False
