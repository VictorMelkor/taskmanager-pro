# TaskManager Pro

> Sistema web fullstack para gerenciamento de tarefas e quadros, inspirado no Trello.  
> Desenvolvido com Django (backend Python) e frontend básico em HTML/CSS/JS, com foco em permissões de usuários e colaboração.

---

## 🚀 Sobre o Projeto

TaskManager Pro é um gerenciador de tarefas com criação, edição e exclusão de boards, colunas e tarefas. Implementa níveis granulares de permissão: **owner**, **moderator**, **editor** e **viewer**.  
Autenticação com django-allauth (login padrão e social Google/Facebook). Segurança com validação de permissões no backend e uso de tokens CSRF.

---

> ⚠️ **Status do Projeto:**  
> Este projeto está em desenvolvimento ativo. Funcionalidades serão adicionadas, ajustadas e otimizadas continuamente. Use com cuidado e acompanhe os commits para atualizações.

## 🛠 Tecnologias

- **Backend:** Python 3, Django 4.x  
- **Frontend:** HTML5, CSS3 (Tailwind CSS para estilização básica sem frameworks pesados), JavaScript (Vanilla)  
- **Banco de dados:** SQLite (para desenvolvimento)  
- **Autenticação:** django-allauth (login, registro, social login Google e Facebook)  
- **Controle de versão:** Git  
- **Hospedagem local:** `python manage.py runserver`

---

## ⚙ Funcionalidades Principais

- Cadastro, login e autenticação com níveis de permissão por usuário em cada board  
- Criação, edição e exclusão de boards, colunas e tarefas  
- Interface para edição inline do nome das colunas via AJAX  
- Remoção e saída de membros dos boards, com restrições para owner  
- Geração de links de convite para adicionar membros com expiração e tokens seguros  
- Visualização e interação com as tarefas dentro das colunas  
- Interface responsiva básica para desktops  
- Mensagens e alertas de validação para ações do usuário  
- Uso de CSRF tokens e verificação de permissão no backend para segurança  

---

## 💻 Como Rodar Localmente

1. Clone o repositório  
   ```bash
   git clone https://github.com/victormelkor/taskmanager-pro.git
   cd taskmanager-pro
    ```

2. Crie e ative um ambiente virtual Python (recomendado)
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3. Instale as dependências
    ```bash
    pip install -r requirements.txt
    ```

4. Rode as Migrações
    ```bash
    python manage.py migrate
    ```

5. Crie um superusuário (opcional)
    ```bash
    python manage.py createsuperuser
    ```

6. Execute o servidor local
    ```bash
    python manage.py runserver
    ```

7. Acesse http://127.0.0.1:8000/ no navegador

--- 

## 📚 Documentação

- [Modelagem de Dados](docs/database_schema.md)  
- [Notas de Desenvolvimento](docs/dev_notes.md)  
- [Tarefas e Pendências](TODO.md)

---

### 📁 `docs/architecture.md`

```bash
    # Arquitetura – TaskManager Pro

    ## Visão Geral

    Projeto Django modularizado com foco em colaboração, permissões e segurança. Cada app tem responsabilidade única, usando CBVs, formulários e autenticação customizada.

    ---

    ## Camadas

    - **userauth/** – login, cadastro, permissões, social login  
    - **tasks/** – boards, colunas, tarefas, convites  
    - **templates/** – HTML modular (base + includes + apps)  
    - **static/** – CSS, JS e imagens

    ---

    ## Fluxo

    1. Acesso exige login  
    2. Home → lista de boards  
    3. Ações baseadas nas permissões (`BoardMember`)  
    4. Convites via token UUID com expiração

    ---

    ## Segurança

    - CSRF tokens  
    - Validação de permissões no backend  
    - Tokens UUID para convites  
    - `get_object_or_404` em views críticas
```


## 🤝 Como Contribuir
1. Fork este repositório

2. Crie uma branch com sua feature:
    ```bash
    git checkout -b feature/nome-da-feature
    ```

3. Commit suas mudanças:
    ```bash
    git commit -m 'Descrição da feature'
    ```

4. Push para a branch:
    ```bash
    git push origin feature/nome-da-feature
    ```

5. Abra um Pull Request no GitHub para revisão

---

## 📝 Considerações Finais
Este projeto foi desenvolvido para demonstrar habilidades fullstack em Python/Django e integração frontend-backend, com foco em boas práticas de código, segurança e UX básico. Serve como portfólio para oportunidades na área de desenvolvimento web.


## 📄 Licença

MIT License © Victor Rodrigues

GitHub: [victormelkor](https://github.com/victormelkor)


## Estrutura
```bash    
    Taskmanager-pro/
    │
    ├── taskmanagerpro/ # Configurações principais
    ├── userauth/       # Autenticação e usuários
    ├── boards/         # Lógica de tarefas, colunas, boards
    │
    ├── templates/
    │ ├── base.html
    │ ├── includes/     # Navbar, mensagens, etc
    │ ├── boards/       # Templates de tarefas e boards
    │ ├── userauth/     # Login, signup, etc
    │ └── pages/        # Home, dashboard, erro
    │
    ├── static/
    │ ├── css/
    │ │ └── styles.css
    │ ├── js/
    │ └── img/
    │
    ├── docs/           # Documentação técnica
    │
    └── manage.py
```



## Futuro (Roadmap)
• Completar funcionalidades AJAX para edição dinâmica de tarefas e colunas

• Implementar notificações via WebSocket

• Desenvolver API REST com Django REST Framework para integração futura

• Adicionar suporte a comentários e anexos nas tarefas

• Melhorar frontend com CSS organizado e responsivo

• Automatizar criação de colunas padrão ao criar novo board

• Modal para visualização e edição rápida de tarefas (sem recarregar página)

• Controle refinado de permissões e fluxos de convite

• Refinar testes automatizados e documentação

---

## Contato

GitHub: [victormelkor](https://github.com/victormelkor)

Email: victor.melkor@gmail.com
