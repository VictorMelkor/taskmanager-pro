# 📝 Changelog – TaskManager Pro

Todas as mudanças importantes neste projeto serão documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [Em Desenvolvimento]

### Adicionado
- Modelo `BoardInvite` com UUID e expiração para convites
- View `AddBoardMemberView` com verificação de owner
- Views para criar/visualizar convites por token
- Criação automática de colunas padrão no board (em progresso)
- Estrutura de permissões com `BoardMember` (owner, moderator, editor, viewer)

### Modificado
- Templates organizados com `base.html` e includes
- Views protegidas com login obrigatório
- Navegação dinâmica no template base (autenticado/não autenticado)

### Corrigido
- Backend de autenticação ajustado para mensagens claras e sem bugs
- Reset das migrações para corrigir inconsistências estruturais

---

## [0.1.0] – 2025-05-01

### Adicionado
- Estrutura inicial do projeto Django
- Apps: `userauth`, `tasks`
- Autenticação customizada com login e cadastro
- Modelos: `Board`, `Column`, `Task`, `BoardMember`
- Templates para login, signup e home

---

## 🔜 Próximas Versões

Planejadas para o MVP:

- Aceitar convite via token
- Cancelamento e expiração automática dos convites
- Modal para exibir tarefa
- Ordenação de tarefas nos cards
- Integração com Google e Facebook via django-allauth
- Sistema de notificações e permissões via AJAX
