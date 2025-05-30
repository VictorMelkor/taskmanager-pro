# Notas de Desenvolvimento – TaskManager Pro

## Autenticação
- CustomUser implementado com login por username ou email.
- django-allauth configurado para login padrão (Google/Facebook a implementar).

## Permissões e Membros
- BoardMember controla os acessos com quatro níveis: owner, moderator, editor, viewer.
- Apenas owners podem adicionar ou remover membros.

## Convites com Token
- BoardInvite usa UUID e data de expiração.
- Sistema de aceite pendente de finalização (token, status e validação).

## Organização de Templates
- Templates organizados por app:
  - `userauth/`, `tasks/`, `pages/`, `includes/`
- Base HTML com navegação dinâmica via `request.user`.

## Padrões e Boas Práticas
- CBVs usadas para CRUD.
- CSRF habilitado.
- Uso de `messages` para feedback ao usuário.
- Estrutura organizada com pasta `static/` e `templates/` fora das apps.

## Futuros Recursos (pós-MVP)
- Integração AJAX para todas ações no board (adicionar/editar tarefas, membros, colunas).
- Modal para tarefas (detalhe na mesma página).
- Notificações em tempo real.
- Checklist com ordenação.
- Sistema de comentários e arquivos por tarefa.
