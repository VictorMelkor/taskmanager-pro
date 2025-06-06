document.addEventListener('DOMContentLoaded', () => {
    const addColumnBtn = document.getElementById('add-column-btn');
    const addColumnModal = document.getElementById('addColumnModal');
    const cancelAddBtn = document.getElementById('cancelAddColumn');
    const cancelAddSecondary = document.getElementById('cancelAddColumnSecondary');
    const addColumnForm = document.getElementById('addColumnForm');
    const boardColumns = document.querySelector('.board-columns');

    function openModal() {
        addColumnModal.classList.add('active');
        addColumnModal.removeAttribute('hidden');
        addColumnModal.setAttribute('aria-hidden', 'false');
        addColumnForm.name.focus();
    }

    function closeModal() {
        addColumnModal.classList.remove('active');
        addColumnModal.setAttribute('aria-hidden', 'true');
        addColumnModal.setAttribute('hidden', '');
        addColumnForm.reset();
        addColumnBtn.focus();
    }

    addColumnBtn.addEventListener('click', openModal);
    cancelAddBtn.addEventListener('click', closeModal);
    if (cancelAddSecondary) {
        cancelAddSecondary.addEventListener('click', closeModal);
    }

    window.addEventListener('click', (e) => {
        if (e.target === addColumnModal) closeModal();
    });

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && addColumnModal.classList.contains('active')) closeModal();
    });

    // Pegando CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    addColumnForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = addColumnForm.name.value.trim();
        if (!name) {
            alert('O nome da coluna é obrigatório.');
            addColumnForm.name.focus();
            return;
        }

        addColumnForm.querySelector('button[type="submit"]').disabled = true;

        try {
            const response = await fetch(
                `/dashboard/${window.username}/${window.slug}/add-column/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ name }),
                }
            );

            const data = await response.json();

            if (response.ok && data.success) {
                insertNewColumn(data.id, data.name);
                closeModal();
            } else {
                alert(data.error || 'Erro ao adicionar a coluna.');
            }
        } catch (error) {
            alert('Erro de conexão: ' + error.message);
        } finally {
            addColumnForm.querySelector('button[type="submit"]').disabled = false;
        }
    });

    function insertNewColumn(id, name) {
        const section = document.createElement('section');
        section.className = 'column-card';
        section.dataset.columnId = id;

        const header = document.createElement('header');
        header.className = 'column-header';
        header.dataset.columnId = id;

        const span = document.createElement('span');
        span.className = 'column-name';
        span.tabIndex = 0;
        span.setAttribute('role', 'button');
        span.setAttribute('aria-label', 'Editar nome da coluna');
        span.textContent = name;
        header.appendChild(span);

        // Botões de opções, você pode adaptar se quiser, aqui só reproduzi
        const optionsBtn = document.createElement('button');
        optionsBtn.className = 'column-options-btn';
        optionsBtn.setAttribute('aria-label', 'Opções da coluna');
        optionsBtn.innerHTML = '<i class="fas fa-ellipsis-h"></i>';

        const dropdown = document.createElement('div');
        dropdown.className = 'column-options-dropdown';
        dropdown.style.display = 'none';

        const moveBtn = document.createElement('button');
        moveBtn.className = 'move-column-btn';
        moveBtn.disabled = true;
        moveBtn.textContent = 'Mover coluna';

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-column-btn';
        deleteBtn.dataset.columnId = id;
        deleteBtn.dataset.deleteUrl = `/${window.username}/${window.slug}/columns/${id}/delete-ajax/`;
        deleteBtn.textContent = 'Excluir';

        dropdown.appendChild(moveBtn);
        dropdown.appendChild(deleteBtn);
        header.appendChild(optionsBtn);
        header.appendChild(dropdown);

        section.appendChild(header);

        const tasksContainer = document.createElement('div');
        tasksContainer.className = 'tasks-container';
        section.appendChild(tasksContainer);

        // Botão "+ Adicionar tarefa" SEM condicionais JS
        const addTaskBtn = document.createElement('button');
        addTaskBtn.className = 'add-task-btn';
        addTaskBtn.textContent = '+ Adicionar tarefa';
        section.appendChild(addTaskBtn);

        const createColumnSection = document.querySelector('.column-card.create-column');
        if (createColumnSection) {
            boardColumns.insertBefore(section, createColumnSection);
        } else {
            boardColumns.appendChild(section);
        }

        // Inicializa funcionalidades da coluna
        initializeColumnNameEdit(span);
        initializeColumnOptionsButtons();
    }

    function initializeColumnNameEdit(span) {
        span.addEventListener('click', () => {
            if (span.querySelector('input')) return;

            const oldName = span.textContent.trim();
            const input = document.createElement('input');
            input.type = 'text';
            input.value = oldName;
            input.classList.add('column-name-input', 'input-field');

            span.textContent = '';
            span.appendChild(input);
            input.focus();

            const cancelEdit = () => {
                span.textContent = oldName;
            };

            const saveEdit = () => {
                const newName = input.value.trim();
                if (!newName || newName === oldName) {
                    cancelEdit();
                    return;
                }

                const columnId = span.closest('.column-card').dataset.columnId;
                fetch(`/dashboard/${window.username}/${window.slug}/columns/${columnId}/edit-ajax/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ name: newName })
                })
                .then(resp => resp.json())
                .then(data => {
                    if (data.success) {
                        span.textContent = data.name;
                    } else {
                        alert(data.error || 'Erro ao editar coluna');
                        cancelEdit();
                    }
                })
                .catch(() => {
                    alert('Erro na comunicação com o servidor');
                    cancelEdit();
                });
            };

            input.addEventListener('blur', saveEdit);

            input.addEventListener('keydown', e => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    input.blur();
                } else if (e.key === 'Escape') {
                    cancelEdit();
                }
            });
        });
    }

    function initializeColumnOptionsButtons() {
        document.querySelectorAll('.column-options-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const dropdown = btn.nextElementSibling;
                if (dropdown) {
                    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
                }
            });
        });
    }

    // Inicializa colunas existentes
    document.querySelectorAll('.column-name').forEach(span => {
        initializeColumnNameEdit(span);
    });
    initializeColumnOptionsButtons();
});
