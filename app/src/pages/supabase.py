import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import threading
from pages import ferramentas   
# ======================================================
# HELPER DE THREADS
# ======================================================

def _run_in_thread(func, callback=None):
    def runner():
        try:
            result = func()
            if callback:
                callback(result)
        except Exception as e:
            print("Erro na thread Supabase:", e)
            if callback:
                callback(None)

    threading.Thread(target=runner, daemon=True).start()

# ======================================================
# CONFIGURAÇÕES DE ARQUIVO
# ======================================================


# URL_FILE = ferramentas.ler_arquivo('URL_FILE.txt')
# KEY_FILE = ferramentas.ler_arquivo('TOKEN_FILE.txt')

# ======================================================
# FUNÇÕES DE CREDENCIAIS
# ======================================================

def _ler_arquivo(caminho):
    try:
        return ferramentas.ler_arquivo(caminho).strip()
    except Exception as e:
        print(f"Erro ao ler arquivo {caminho}: {e}")
        return None


def obter_credenciais():
    url = 'https://ellyuhvkzfwgkyvhktis.supabase.co'
    key = ''

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
        r = requests.get(
            endpoint, 
            headers=_headers(key), 
            timeout=1000,
            verify=False
        )

        if r.status_code == 200:
            return r.json()

    except Exception as e:
        print(f"Erro no testar_conexao: {e}")
        return None

# ======================================================
# LEITURA DE TABELA
# ======================================================

def ler_tabela(nome_tabela, filtros=None):
    print("ler_tabela() chamada")
    def ler_tabela_async(nome_tabela, filtros=None, callback=None):
        _run_in_thread(
            lambda: ler_tabela(nome_tabela, filtros),
            callback
        )
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
            timeout=1000,
            verify=False
        )

        if r.status_code == 200:
            return r.json()

    except Exception as e:
        print("ERRO:", e)
        return None

# ======================================================
# INSERIR LINHA
# ======================================================

def inserir_linha(nome_tabela, dados: dict):
    print("inserir_linha() chamada")
    def inserir_linha_async(nome_tabela, dados: dict, callback=None):
        _run_in_thread(
            lambda: inserir_linha(nome_tabela, dados),
            callback
        )
    try:
        url, key = obter_credenciais()
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{nome_tabela}"

        r = requests.post(
            endpoint,
            headers=_headers(key),
            data=json.dumps(dados),
            timeout=1000,
            verify=False
        )

        if r.status_code in (200, 201):
            return True

        return None

    except Exception as e:
        print("ERRO:", e)
        return None

# ======================================================
# ATUALIZAR LINHA
# ======================================================

def atualizar_linha(nome_tabela, filtros: dict, novos_dados: dict):
    print("atualizar_linha() chamada")
    def atualizar_linha_async(nome_tabela, filtros: dict, novos_dados: dict, callback=None):
        _run_in_thread(
            lambda: atualizar_linha(nome_tabela, filtros, novos_dados),
            callback
        )
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
            timeout=1000,
            verify=False
        )

        if r.status_code in (200, 204):
            return True

        return None

    except Exception as e:
        print("ERRO:", e)
        return None

# ======================================================
# EXCLUIR LINHA
# ======================================================

def excluir_linha(nome_tabela, filtros: dict):
    print("excluir_linha() chamada")
    def excluir_linha_async(nome_tabela, filtros: dict, callback=None):
        _run_in_thread(
            lambda: excluir_linha(nome_tabela, filtros),
            callback
        )
    try:
        url, key = obter_credenciais()
        if not url or not key:
            return None

        endpoint = f"{url}/rest/v1/{nome_tabela}"

        r = requests.delete(
            endpoint,
            headers=_headers(key),
            params=filtros,
            timeout=1000,
            verify=False
        )

        if r.status_code in (200, 204):
            return True

        return None

    except Exception as e:
        print("ERRO:", e)
        return None
def inserir_log(mensagem: str):
    from datetime import datetime
    agora = datetime.now()
    log = {
        "mensagem": mensagem,
        "registrado_em":agora.strftime("%d/%m/%Y %H:%M:%S"),
        "autor": ferramentas.ler_arquivo('NOME.txt')
        }
    inserir_linha('logs',log)
    return log
