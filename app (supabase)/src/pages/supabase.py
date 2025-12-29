import os
import json
import requests
from pages import ferramentas   

# ======================================================
# CONFIGURAÇÕES DE ARQUIVO
# ======================================================

BASE_DIR = ferramentas.pasta_global()

URL_FILE = os.path.join(BASE_DIR, "URL_FILE.txt")
KEY_FILE = os.path.join(BASE_DIR, "TOKEN_FILE.txt")

# ======================================================
# FUNÇÕES DE CREDENCIAIS
# ======================================================

def _ler_arquivo(caminho):
    try:
        with open(caminho, "r") as f:
            return f.read().strip()
    except:
        return None


def obter_credenciais():
    url = 'https://ellyuhvkzfwgkyvhktis.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsbHl1aHZremZ3Z2t5dmhrdGlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYzMzU5NTYsImV4cCI6MjA4MTkxMTk1Nn0.xTcZbx3fDs_tx_uRVG33yIkzAYLdz_sjTZM87vb5QGE'

    if not url or not key:
        return None, None

    return url, key


def _headers(api_key):
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

# ======================================================
# TESTE DE CONEXÃO (CREDENCIAIS)
# ======================================================

def testar_conexao(url,key,tabela_teste="login"):
    """
    Verifica se as credenciais são válidas tentando ler a tabela informada.
    Retorna:
        - lista de dados (pode ser vazia) se OK
        - None se erro
    """
    try:
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{tabela_teste}?limit=1"
        r = requests.get(endpoint, headers=_headers(key), timeout=10)

        if r.status_code == 200:
            return r.json()


    except:
        return None

# ======================================================
# LEITURA DE TABELA
# ======================================================

def ler_tabela(nome_tabela, filtros=None):
    try:
        url, key = obter_credenciais()
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{nome_tabela}"

        params = filtros if filtros else {}

        r = requests.get(
            endpoint,
            headers=_headers(key),
            params=params,
            timeout=10
        )

        if r.status_code == 200:
            return r.json()

    except:
        return None

# ======================================================
# INSERIR LINHA
# ======================================================

def inserir_linha(nome_tabela, dados: dict):
    try:
        url, key = obter_credenciais()
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{nome_tabela}"

        r = requests.post(
            endpoint,
            headers=_headers(key),
            data=json.dumps(dados),
            timeout=10
        )

        if r.status_code in (200, 201):
            return True

        return None

    except:
        return None

# ======================================================
# ATUALIZAR LINHA
# ======================================================

def atualizar_linha(nome_tabela, filtros: dict, novos_dados: dict):
    """
    filtros: {"id": "eq.1"} ou {"email": "eq.teste@gmail.com"}
    """
    try:
        url, key = obter_credenciais()
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{nome_tabela}"

        r = requests.patch(
            endpoint,
            headers=_headers(key),
            params=filtros,
            data=json.dumps(novos_dados),
            timeout=10
        )

        if r.status_code in (200, 204):
            return True

        return None

    except:
        return None

# ======================================================
# EXCLUIR LINHA
# ======================================================

def excluir_linha(nome_tabela, filtros: dict):
    try:
        url, key = obter_credenciais()
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{nome_tabela}"

        r = requests.delete(
            endpoint,
            headers=_headers(key),
            params=filtros,
            timeout=10
        )

        if r.status_code in (200, 204):
            return True

        return None

    except:
        return None
