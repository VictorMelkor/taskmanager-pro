console.log('delete_task.js carregado');

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('deleteTaskModal');
    const confirmBtn = document.getElementById('confirmDeleteTask');
    const cancelBtn = document.getElementById('cancelDeleteTask');
    const closeBtn = document.getElementById('closeDeleteModalBtn');
    const openBtn = document.getElementById('openDeleteTaskModal');

    let selectedTaskId = null;
    let selectedColumnId = null;

    function getCookie(name) {
        const cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
        return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
    }

    function openModal(taskId, columnId) {
        selectedTaskId = taskId;
        selectedColumnId = columnId;
        modal.classList.add('active');
        modal.removeAttribute('hidden');
        modal.setAttribute('aria-hidden', 'false');
    }

    function closeModal() {
        selectedTaskId = null;
        selectedColumnId = null;
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('hidden', '');
    }

    function deleteTask() {
        if (!selectedTaskId || !selectedColumnId) return;

        const url = `/dashboard/${window.username}/${window.slug}/columns/${selectedColumnId}/delete-task/${selectedTaskId}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const task = document.querySelector(`.task-card[data-task-id="${selectedTaskId}"]`);
                if (task) task.remove();
                closeModal();
                document.getElementById('editTaskModal').classList.remove('active'); // Fecha o modal de edição
            } else {
                alert(data.error || 'Erro ao excluir tarefa.');
                closeModal();
            }
        })
        .catch(() => {
            alert('Erro ao excluir tarefa.');
            closeModal();
        });
    }

    // Abre o modal de exclusão (botão dentro do modal de edição)
    openBtn.addEventListener('click', () => {
        const taskId = document.getElementById('editTaskId').value;
        const columnId = window.columnIdsByTask[taskId];
        openModal(taskId, columnId);
    });

    confirmBtn.addEventListener('click', deleteTask);
    cancelBtn.addEventListener('click', closeModal);
    closeBtn.addEventListener('click', closeModal);

    // ESC fecha
    window.addEventListener('keydown', e => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Clicou fora do modal = fecha
    window.addEventListener('click', e => {
        if (e.target === modal) {
            closeModal();
        }
    });
});
