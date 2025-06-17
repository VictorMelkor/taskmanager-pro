console.log('add_column.js carregado');

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
                closeModal();
                window.location.reload(); // recarrega a página para atualizar a coluna criada
            } else {
                alert(data.error || 'Erro ao adicionar a coluna.');
            }
        } catch (error) {
            alert('Erro de conexão: ' + error.message);
        } finally {
            addColumnForm.querySelector('button[type="submit"]').disabled = false;
        }
    });

    // Inicializa edição dos nomes existentes
    document.querySelectorAll('.column-name').forEach(span => {
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
    });

    // Delegação de evento para botões de deletar colunas
    boardColumns.addEventListener('click', (e) => {
        const deleteBtn = e.target.closest('.delete-column-btn');
        if (!deleteBtn) return;

        const column = deleteBtn.closest('.column-card');
        if (!column) return;

        const columnId = column.dataset.columnId; 
        openDeleteModal(columnId);
    });
});
