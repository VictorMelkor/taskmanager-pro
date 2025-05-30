# Arquitetura – TaskManager Pro

## Visão Geral

TaskManager Pro é uma aplicação web fullstack com arquitetura MVC (Model–View–Controller) baseada no Django. O sistema é modularizado em apps com responsabilidades específicas e uso extensivo de CBVs (Class-Based Views), formulários Django e autenticação personalizada.

---

## Camadas e Componentes

### 🧠 Backend (Django)
- **Core**: configurações globais, middlewares, roteamento base
- **userauth**: autenticação, cadastro, login social, permissões
- **tasks**: CRUD de tarefas, colunas, boards e lógica de organização
- **pages**: páginas estáticas e views de navegação
- **models**: modelagem relacional com uso de ForeignKey e UUIDs

### 🎨 Frontend (HTML/CSS/JS)
- Templates Django renderizados server-side (com blocos reutilizáveis)
- CSS customizado via `styles.css`, com estrutura BEM básica
- JavaScript vanilla para modais e ações leves (ex: confirmação, toggle)
- Estrutura planejada para futura migração parcial para AJAX

---

## Fluxo de Acesso

1. **Usuário acessa app:** verifica autenticação
2. **Home:** redireciona para lista de Boards
3. **Board selecionado:** exibe colunas e tarefas via Django Template
4. **Permissões:** controladas pela model `BoardMember`
5. **Ações:** criação/edição/remoção controladas por permissões no backend

---

## Segurança

- CSRF ativo em todos formulários
- Validação de permissões para cada view sensível
- URLs com tokens UUID para convites
- Uso de `get_object_or_404` para evitar acesso indevido
- Planos futuros de rate-limiting e 2FA

---

## Organização de Diretórios
```bash
Taskmanager-pro/
│
├── taskmanagerpro/ # Configurações principais
├── userauth/ # Autenticação e usuários
├── boards/ # Lógica de tarefas, colunas, boards
│
├── templates/
│ ├── base.html
│ ├── includes/ # Navbar, mensagens, etc
│ ├── boards/ # Templates de tarefas e boards
│ ├── userauth/ # Login, signup, etc
│ └── pages/ # Home, dashboard, erro
│
├── static/
│ ├── css/
│ │ └── styles.css
│ ├── js/
│ └── img/
│
├── docs/ # Documentação técnica
│
└── manage.py
```


---

## Dependências Externas

- **django-allauth**: login tradicional e via redes sociais
- **Tailwind CSS (opcional)**: planeja-se adicionar para estilização
- **uuid**: geração de tokens seguros para convites
- **Vanilla JS**: modais e interações leves sem framework JS pesado

---

## Extensões Futuras

- Integração AJAX para interações no board
- Comentários e anexos em tarefas
- Notificações em tempo real com WebSockets
- API pública (Django REST Framework)

