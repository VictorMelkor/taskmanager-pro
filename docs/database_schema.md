# Modelagem de Dados – TaskManager Pro (Atualizado)

## Usuário (CustomUser)
- id (PK)
- full_name
- username (único)
- email (único)
- password (hash)
- is_staff
- is_active
- date_joined
- **two_factor_active (bool) — futuro**
- **two_factor_info (JSON) — futuro**

## Board (Quadro)
- id (PK)
- name
- description (opcional)
- created_by (FK → Usuário)
- slug (único, incremental)
- created_at

## Column (Coluna)
- id (PK)
- name
- board (FK → Board)
- order

## Task (Tarefa)
- id (PK)
- title
- description (opcional)
- created_at
- due_date (opcional) — futuro
- notes (opcional) — futuro
- column (FK → Column)
- **sprint (FK → Sprint) — removido (não implementado)**
- created_by (FK → Usuário)
- **status (aberto, em_progresso, concluído) — futuro**

## Sprint
- **removido — não implementado**

## BoardMember
- id (PK)
- board (FK → Board)
- user (FK → Usuário)
- permission (choice: owner, moderator, editor, viewer)

## TaskAssignment
- **removido — não implementado**

## Comment (Comentário)
- **removido — não implementado**

## Attachment (Anexo)
- **removido — não implementado**

## ChecklistItem
- **removido — não implementado**

## Notification
- **removido — não implementado**

## BoardInvite
- id (PK)
- board (FK → Board)
- invitee (FK → Usuário ou email)
- token (UUID)
- expiration (datetime)
- invited_by (FK → Usuário)
- status (pendente, aceito, expirado)

---

**Resumo:**  
O modelo central já implementado contempla Usuário, Board, Column, Task, BoardMember e BoardInvite. Outros modelos como Sprint, TaskAssignment, Comentários, Anexos, Checklist, Notificações, campos de status e campos extras em Task ainda são futuros ou não implementados.  

Se quiser encerrar o projeto, foque na base atual. Futuras atualizações podem incluir os itens marcados como “futuro” ou removidos.

Quer que eu gere esse markdown formatado?
