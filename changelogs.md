# 📝 Changelog – TaskManager Pro

Todas as mudanças importantes neste projeto serão documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [Em Desenvolvimento]

### Adicionado
- Autenticação customizada com login por username ou email (CustomUser)
- Integração com django-allauth para login padrão (Google/Facebook a implementar)
- Modelo `Board` com criação, edição, exclusão e slug único incremental
- Modelo `Column` com ordenação e vínculo a Board
- Modelo `Task` com título, descrição, status, vínculo a coluna, sprint e usuário criador
- Modelo `BoardMember` com níveis de permissão: owner, moderator, editor, viewer
- Modelo `BoardInvite` para convites via token UUID com expiração e status
- Views CRUD usando CBVs com verificação de permissão e uso de mensagens de feedback
- Sistema de convite por token com validação, pendência e aceitação (parcial)
- Criação automática de colunas padrão ao criar um board 
- Exibição de tarefas em cards ordenados dentro das colunas
- Modal para detalhes da tarefa 
- Permissões de membros para adicionar/remover usuários no board
- Navegação dinâmica no template base com controle de login
- Uso de CSRF para segurança em formulários
- Organização das pastas templates por app (`userauth/`, `boards/`, `pages/`, `includes/`)
- Estrutura de pastas `static/` para CSS, JS e imagens

### Modificado
- Views protegidas com login obrigatório
- Ajustes no backend de autenticação para mensagens claras e sem bugs
- Reset das migrações para corrigir inconsistências estruturais

---

## 🔜 Próximas Versões

- Implementar sistema de 2FA (dupla autenticação)
- Ordenação explícita das tarefas dentro das colunas
- Checklist de tarefas com itens ordenados e completáveis
- Upload e gerenciamento de anexos em tarefas
- Sistema de comentários em tarefas com criação, edição e remoção
- Troca de permissões e remoção de membros via frontend
- Bloqueio e desbloqueio do quadro (“fechar quadro”)
- Pesquisa e filtro dinâmico de tarefas e colunas
- Interface drag-and-drop para mover colunas e tarefas
- Notificações dinâmicas e em tempo real
- Integração completa com login social Google e Facebook
- Validação e tratamento avançado de dados sensíveis para segurança

