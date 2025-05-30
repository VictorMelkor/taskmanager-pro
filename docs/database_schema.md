# Modelagem de Dados – TaskManager Pro

## Usuário (CustomUser)
- id (PK)
- full_name
- username (único)
- email (único)
- password (hash)
- is_staff
- is_active
- date_joined
- two_factor_active (bool) — a implementar
- two_factor_info (JSON) — a implementar

## Board (Quadro)
- id (PK)
- name
- description (opcional)
- created_by (FK → Usuario)
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
- due_date (opcional)
- notes (opcional)
- column (FK → Column)
- sprint (FK → Sprint, opcional)
- created_by (FK → Usuario)
- status (aberto, em_progresso, concluído) — a implementar

## Sprint
- id (PK)
- title
- start_date
- end_date
- board (FK → Board)

## BoardMember
- id (PK)
- board (FK → Board)
- user (FK → Usuario)
- permission (choice: owner, editor, viewer, moderator)

## TaskAssignment
- id (PK)
- task (FK → Task)
- user (FK → Usuario)
- role (str)

## Comment (Comentário)
- id (PK)
- task (FK → Task)
- user (FK → Usuario)
- text
- created_at

## Attachment (Anexo)
- id (PK)
- task (FK → Task)
- file_url
- file_name
- uploaded_at

## ChecklistItem
- id (PK)
- task (FK → Task)
- description
- completed (bool)
- order (int) — a implementar

## Notification
- id (PK)
- user (FK → Usuario)
- text
- type
- created_at
- read (bool)

## BoardInvite
- id (PK)
- board (FK → Board)
- invitee (FK → Usuario ou email)
- token (UUID)
- expiration (datetime)
- invited_by (FK → Usuario)
- status (pendente, aceito, expirado)
