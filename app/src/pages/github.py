import os
import flet as ft
from pages import home, ferramentas
import datetime as dt
import shutil

from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.errors import NotGitRepository

# ======================================================
# CONFIGURAÇÕES GLOBAIS
# ======================================================

pasta_global = ferramentas.pasta_global()
repo_global = os.path.join(f"{ferramentas.repo_global()}")

if os.path.exists(os.path.join(pasta_global, "INFO.txt")):
    with open(os.path.join(pasta_global, "INFO.txt"), "r") as f:
        infos = f.readlines()[0].strip()
else:
    infos = "Desconhecido"



# ======================================================
# FUNÇÃO: CLONAR
# ======================================================
# Caminho do arquivo onde o token será salvo
TOKEN_FILE = os.path.join(pasta_global, "TOKEN.txt")
LINK_FILE = os.path.join(pasta_global, "LINK.txt")

# ======================================================
# FUNÇÃO: SALVAR TOKEN
# ======================================================
def salvar_token(token: str,link:str):
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token.strip())
        with open(LINK_FILE, "w") as f:
            f.write(link.strip())
        return True
    except:
        return False

# ======================================================
# FUNÇÃO: OBTER TOKEN
# ======================================================
def obter_token():
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()
        return None
    except:
        return None

# ======================================================
# FUNÇÃO: CLONAR (salva token automaticamente)
# ======================================================
def clone_repo(token, link):
    try:
        salvar_token(token, link)

        if not os.path.exists(repo_global):
            os.makedirs(repo_global)

        username = "git"
        clean_link = link.replace("https://", "")  # github.com/user/repo
        repo_url = f"https://{username}:{token}@{clean_link}"

        porcelain.clone(repo_url, target=repo_global)
        return True

    except Exception as e:
        print("Erro clone_repo:", e)
        try:
            os.remove(TOKEN_FILE)
            os.remove(LINK_FILE)
        except:
            pass
        try:
            shutil.rmtree(repo_global)
        except:
            pass
        return e


# ======================================================
# FUNÇÃO: PULL
# ======================================================
def atualizar_repo():
    try:
        repo = Repo(repo_global)
        token = obter_token()

        cfg = repo.get_config()
        remote_url = cfg.get((b'remote "origin"',), b'url').decode()

        username = "git"
        clean_link = remote_url.replace("https://", "").split("@")[-1]
        remote_url_fixed = f"https://{username}:{token}@{clean_link}"

        porcelain.pull(repo, remote_url_fixed.encode())
        return True

    except Exception as e:
        print("Erro atualizar_repo:", e)
        return False

# ======================================================
# FUNÇÃO: COMMIT + PUSH (usa token salvo)
# ======================================================
def commit_push(mensagem=None):
    token = obter_token()

    if mensagem is None:
        mensagem = f'Atualização em {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} por {infos}'

    try:
        repo = Repo(repo_global)
        porcelain.add(repo, b".")
        porcelain.commit(repo, mensagem.encode())

        cfg = repo.get_config()

        # Garantir que exista origin
        try:
            remote_url = cfg.get((b'remote "origin"',), b'url').decode()
        except KeyError:
            with open(LINK_FILE, "r") as f:
                link_salvo = f.read().strip()

            username = "git"
            clean_link = link_salvo.replace("https://", "")
            remote_url = f"https://{username}:{token}@{clean_link}"

            cfg.set((b'remote "origin"',), b"url", remote_url.encode())
            cfg.write_to_path()

        # Reforçar token correto sempre
        username = "git"
        clean_link = remote_url.replace("https://", "").split("@")[-1]
        remote_url_fixed = f"https://{username}:{token}@{clean_link}"

        porcelain.push(repo, remote_location=remote_url_fixed.encode())
        return True

    except Exception as e:
        print("Erro commit_push:", e)
        return False

# ======================================================
# FUNÇÃO: LOGS
# ======================================================
def atualizar_logs(mensagem=str, atualizar_repo=None):
    try:
        with open(os.path.join(repo_global, 'LOG.txt'), 'a') as f:
            f.write(f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} por {infos}\n{mensagem}\n\n')

        if atualizar_repo:
            atualizar_repo()

        return True

    except Exception as e:
        print("Erro atualizar_logs:", e)
        return False