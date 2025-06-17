console.log('edit_task.js carregado');

document.addEventListener('DOMContentLoaded', () => {
    const editTaskModal = document.getElementById('editTaskModal');
    const editTaskForm = document.getElementById('editTaskForm');
    const closeEditTaskModalBtn = document.getElementById('closeEditTaskModal');

    // Campos do form
    const inputTaskId = document.getElementById('editTaskId');
    const inputTaskName = document.getElementById('editTaskName');
    const inputTaskDescription = document.getElementById('editTaskDescription');
    const selectTaskStatus = document.getElementById('editTaskStatus');

    // Abrir modal
    function openModal() {
        editTaskModal.classList.add('active');
        editTaskModal.setAttribute('aria-hidden', 'false');
        editTaskModal.focus();
    }

    // Fechar modal
    function closeModal() {
        editTaskModal.classList.remove('active');
        editTaskModal.setAttribute('aria-hidden', 'true');
        editTaskForm.reset();
        delete editTaskForm.dataset.columnId;
    }

    // Fechar modal ao clicar no botão fechar
    closeEditTaskModalBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal();
    });

    // Fechar modal ao clicar fora do conteúdo
    editTaskModal.addEventListener('click', (e) => {
        if (e.target === editTaskModal) closeModal();
    });

    // Fechar modal com tecla Esc
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && editTaskModal.classList.contains('active')) {
            closeModal();
        }
    });

    // Abrir modal com dados da tarefa ao clicar na task-card
    document.querySelectorAll('.task-card').forEach(taskCard => {
        taskCard.addEventListener('click', () => {
            const taskId = taskCard.getAttribute('data-task-id');
            const taskName = taskCard.querySelector('.task-name').textContent.trim();
            const taskDescription = taskCard.getAttribute('data-task-description') || '';
            const taskStatus = taskCard.getAttribute('data-task-status') || 'todo';

            const columnElement = taskCard.closest('.column-card');
            if (!columnElement) {
                alert('Erro: coluna da tarefa não identificada.');
                return;
            }
            const columnId = columnElement.getAttribute('data-column-id');

            inputTaskId.value = taskId;
            inputTaskName.value = taskName;
            inputTaskDescription.value = taskDescription;
            selectTaskStatus.value = taskStatus;

            editTaskForm.dataset.columnId = columnId;

            openModal();
        });
    });

    // Envio do formulário via AJAX
    editTaskForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const taskId = inputTaskId.value;
        const columnId = editTaskForm.dataset.columnId;
        if (!columnId) {
            alert('Erro: coluna não especificada para a edição.');
            return;
        }

        const url = `/dashboard/${window.username}/${window.slug}/columns/${columnId}/edit-task/${taskId}/`;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            name: inputTaskName.value.trim(),
            description: inputTaskDescription.value.trim(),
            status: selectTaskStatus.value
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(resp => {
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            return resp.json();
        })
        .then(json => {
            if (json.success) {
                const taskCard = document.querySelector(`.task-card[data-task-id="${json.id}"]`);
                if (taskCard) {
                    taskCard.querySelector('.task-name').textContent = json.name;
                    taskCard.setAttribute('data-task-description', json.description || '');
                    taskCard.setAttribute('data-task-status', json.status || 'todo');

                    // Atualizar a cor da bolinha de status
                    const statusIcon = taskCard.querySelector('.status-dot');
                    if (statusIcon) {
                        statusIcon.classList.remove('todo', 'doing', 'done');
                        statusIcon.classList.add(json.status);
                    }
                }
                closeModal();
            } else {
                alert('Erro: ' + (json.errors ? JSON.stringify(json.errors) : 'Falha ao salvar'));
            }
        })
        .catch(err => {
            alert('Erro na requisição: ' + err.message);
        });
    });
});
