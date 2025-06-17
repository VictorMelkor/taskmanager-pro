---

### 📁 `docs/architecture.md`

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

---



