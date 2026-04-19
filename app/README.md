<h1 align="center">MeiaDouze (6X2 App)</h1>

<p align="center">
  O aplicativo oficial para gerenciamento estudantil, calendários, tarefas, avisos e utilitários. Construído com <b>Python</b> e <b>Flet</b>, desenvolvido para ser multiplataforma.
</p>

## 📋 Sobre o Projeto

O **6X2 App (MeiaDouze)** é uma aplicação voltada para organizar e auxiliar os alunos nas demandas diárias. Ele utiliza a tecnologia do framework **Flet** para entregar uma interface bonita, responsiva e multiplataforma (Windows, Linux, macOS, Android), aliada ao **Supabase** no backend para sincronização e armazenamento em tempo real de eventos, avisos e logins de usuários.

## ✨ Funcionalidades Principais

* 📅 **Calendário Interativo:** Visualize o mês, marque dias com eventos (trabalhos, provas) e acesse detalhes do dia.
* 🕒 **Horários de Aula:** Tenha acesso fácil aos quadros de horários de cada dia da semana.
* 🔔 **Avisos:** Fique por dentro dos principais comunicados e recados e informações de versão.
* 📋 **Exibição em Lista:** Liste todos os eventos/tarefas futuras de maneira organizada.
* 🔗 **Links Utilitários:** Atalhos para os principais sites e recursos úteis para os alunos.
* 🧮 **Calculadora Intregada:** Faça cálculos rápidos sem precisar sair do app.
* 📝 **Bloco de Notas:** Um local simples e rápido para guardar pequenas anotações.
* ⚙️ **Funções de Administrador:** Controle e logs voltados aos administradores da aplicação.
* 🌗 **Suporte a Temas:** Alternância entre modos claro, escuro e padronização pelo sistema.

## 🛠️ Tecnologias Utilizadas

- **[Python 3.9+](https://www.python.org/)** – Linguagem base.
- **[Flet](https://flet.dev/)** (v0.80.2) – Framework de Interface Gráfica, utilizado para criar toda a UI de modo fluído e reativo (baseado no Flutter).
- **[Supabase](https://supabase.io/)** – Backend as a Service utilizado como banco de dados (PostgreSQL) e autenticação.
- **[Requests](https://pypi.org/project/requests/)** – Requisições HTTP, comunicações externas.

## 🚀 Como Executar Localmente

### 1. Requisitos
Você precisa ter o **Python >= 3.9** instalado na sua máquina, além do gerenciador de pacotes da sua preferência (`pip`, `poetry`, ou `uv`).

### 2. Clonando o Repositório
```bash
git clone https://github.com/seu-usuario/Codigo-6X2.git
cd Codigo-6X2/app
```

### 3. Instalando as Dependências
Utilizando o `uv` instalado, ou instalando via requirements extras:
```bash
# Via Poetry Local
poetry install

# Ou caso utilize o Flet/Pip diretamente
pip install flet==0.80.2 requests==2.32.5
```

### 4. Executando o App
Para ver a aplicação rodando como um aplicativo desktop/mobile (via flet app):
```bash
flet run src/
```

Para rodar em modo Android (usado no ambiente de dev):
```bash
flet run --android src/
```

*(Obs: Configurações do Supabase para conexão com banco de dados devem estar devidamente configuradas/arquivadas nos caminhos esperados da aplicação)*.

## 📂 Estrutura de Diretórios Básica

```
Codigo-6X2/
└── app/
    ├── src/
    │   ├── main.py              # Ponto de entrada (Entrypoint)
    │   └── pages/               # Páginas e views da aplicação (home, config, notas, etc.)
    ├── pyproject.toml           # Dependências e Metadados
    └── README.md                # Este documento
```

## 👨‍💻 Autores e Licença
**Equipe:** Error 404 / Cubepy  
**Copyright:** © 2025 by Cubepy  

Sinta-se à vontade para relatar bugs nas *issues* caso encontre alguma anomalia na aplicação.
