# Arquitetura – TaskManager Pro

## Visão Geral

TaskManager Pro é uma aplicação web fullstack com arquitetura MVC (Model–View–Controller) baseada no Django. O sistema é modularizado em apps com responsabilidades específicas e uso extensivo de CBVs (Class-Based Views), formulários Django e autenticação personalizada.

---

## Camadas e Componentes

### 🧠 Backend (Django)
- **taskmanagerpro**: configurações globais, middlewares, roteamento base  
- **userauth**: autenticação, cadastro, controle de permissões  
- **boards**: CRUD de tarefas, colunas, boards e lógica de organização  
- **pages**: páginas estáticas e views de navegação  
- **models**: modelagem relacional com uso de ForeignKey e UUIDs  

### 🎨 Frontend (HTML/CSS/JS)
- Templates Django renderizados server-side com blocos reutilizáveis  
- CSS customizado em arquivos separados (`styles.css`), seguindo estrutura simples e organizada  
- JavaScript vanilla para modais, confirmação e interações leves (toggle, fetch AJAX)  
- Estrutura preparada para futura migração parcial para AJAX e frontend mais dinâmico  

---

## Fluxo de Acesso

1. Usuário acessa a aplicação, sistema verifica autenticação  
2. Usuário autenticado é redirecionado para lista de Boards  
3. Seleção do Board exibe colunas e tarefas via templates Django  
4. Permissões são controladas via modelo `BoardMember` e validadas no backend  
5. Ações de criação, edição e remoção restritas conforme permissão do usuário  

---

## Segurança

- CSRF habilitado em todos os formulários  
- Validação rigorosa de permissões em todas as views sensíveis  
- URLs protegidas por tokens UUID para convites  
- Uso de `get_object_or_404` para evitar acesso indevido a objetos  
- Planejamento futuro para implementação de 2FA e rate-limiting  

---

## Organização de Diretórios

```bash
Taskmanager-pro/
│
├── taskmanagerpro/      # Configurações principais do projeto
├── userauth/            # Autenticação e gerenciamento de usuários
├── boards/               # Lógica de tarefas, colunas e boards
├── pages/               # Views e templates para páginas estáticas e navegação
│
├── templates/
│   ├── base.html
│   ├── includes/        # Navbar, mensagens, componentes reutilizáveis
│   ├── boards/           # Templates de boards, colunas e tarefas
│   ├── userauth/        # Login, cadastro, etc.
│   └── pages/           # Home, dashboard, página de erro
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   └── img/
│
├── docs/                # Documentação técnica
│
└── manage.py
```

## Dependências Externas
django-allauth: suporte a login tradicional e via redes sociais (em planejamento)

uuid: geração de tokens seguros para convites

Vanilla JS: manipulação de modais e interações leves sem frameworks pesados

Tailwind CSS (opcional): planejado para futuras melhorias no estilo

## Extensões Futuras
Migração para interações AJAX para atualização parcial do board

Implementação de comentários e anexos em tarefas

Sistema de notificações em tempo real via WebSockets

API pública com Django REST Framework

Implementação de 2FA e mecanismos avançados de segurança

Interface drag-and-drop para movimentação de colunas e tarefas

Sistema de checklist em tarefas com itens ordenados e completáveis