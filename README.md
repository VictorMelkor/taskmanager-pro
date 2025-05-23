# 🚀 TaskManager Pro

**TaskManager Pro** é uma aplicação web moderna para organização de tarefas, inspirada no estilo Trello. Desenvolvida com foco em praticidade, organização e escalabilidade, permite que usuários gerenciem múltiplos quadros (boards), colunas e tarefas com uma interface intuitiva e responsiva.

---

## ✨ Características

- 🔐 Autenticação integrada com Django Allauth
- 🧩 Estrutura modular com múltiplos apps Django
- 🎨 Boards personalizáveis com seleção de cores
- 📌 Tarefas organizadas em colunas (Kanban-like)
- 🗂️ Suporte a múltiplos quadros por usuário

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework:** Django 5.0+
- **Banco de Dados:** SQLite (provisório)
- **Frontend:** HTML5, CSS3 (custom), JavaScript (mínimo)
- **Auth:** django-allauth
- **Template Engine:** Django Templates

---

## 📁 Estrutura Geral
taskmanager-pro/
├── core/ # Configurações e base do projeto
├── userauth/ # Registro e login de usuários
├── pages/ # Páginas públicas e estáticas
├── tasks/ # Lógica dos boards, colunas e tarefas
├── templates/ # Templates HTML globais
├── static/ # Arquivos CSS/JS globais (em breve)
└── manage.py
