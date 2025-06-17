console.log('delete_column.js carregado');

document.addEventListener('DOMContentLoaded', () => {
    // Use só uma constante para o modal
    const modal = document.getElementById('deleteColumnModal');
    const closeModalBtn = document.getElementById('cancelDeleteColumn')
    const confirmBtn = document.getElementById('confirmDeleteColumn');
    const cancelBtn = document.getElementById('cancelDeleteColumnBtn');
    let selectedColumnId = null;

    function closeModal() {
        selectedColumnId = null;
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('hidden', '');
    }

    function getCookie(name) {
        const cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
        return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
    }

    function deleteColumn() {
        const columnId = window.selectedColumnId;
        if (!columnId) return;

        const url = window.deleteColumnUrlTemplate.replace('/0/', `/${columnId}/`);

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
                const column = document.querySelector(`.column-card[data-column-id="${columnId}"]`);
                if (column) column.remove();
            } else {
                alert(data.error || 'Erro ao excluir coluna.');
            }
            closeModal();
        })
        .catch(() => {
            alert('Erro ao excluir coluna.');
            closeModal();
        });
    }

    // Eventos
    document.querySelectorAll('.delete-column-btn').forEach(button => {
        button.addEventListener('click', () => openDeleteModal(button.dataset.columnId));
    });

    closeModalBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    confirmBtn.addEventListener('click', deleteColumn);


    // Fecha modal com ESC
    window.addEventListener('keydown', e => {
        if (e.key === 'Escape' && !modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Fecha modal clicando fora
    window.addEventListener('click', e => {
        if (e.target === modal) {
            closeModal();
        }
    });
});
