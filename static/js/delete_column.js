document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = getCookie('csrftoken');

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Abrir dropdown de opções da coluna (botão ...)
    document.querySelectorAll('.column-options-btn').forEach(button => {
        button.addEventListener('click', e => {
            e.stopPropagation();
            const dropdown = button.nextElementSibling;
            dropdown.classList.toggle('show');
            closeAllDropdowns(button);
        });
    });

    // Fecha dropdown se clicar fora
    window.addEventListener('click', () => {
        closeAllDropdowns();
    });

    function closeAllDropdowns(except = null) {
        document.querySelectorAll('.column-options-dropdown.show').forEach(dropdown => {
            if (!except || except.nextElementSibling !== dropdown) {
                dropdown.classList.remove('show');
            }
        });
    }

    // Abrir modal de confirmação de exclusão
    const deleteModal = document.getElementById('deleteColumnModal');
    const confirmDeleteBtn = deleteModal.querySelector('.confirm-delete');
    const cancelDeleteBtn = deleteModal.querySelector('.cancel-delete');
    let columnIdToDelete = null;
    let urlDelete = null;

    // Botão excluir no dropdown
    document.querySelectorAll('.delete-column-btn').forEach(button => {
        button.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();

            columnIdToDelete = button.dataset.columnId;
            urlDelete = button.dataset.deleteUrl;

            deleteModal.style.display = 'block';
        });
    });

    // Cancelar exclusão
    cancelDeleteBtn.addEventListener('click', () => {
        deleteModal.style.display = 'none';
        columnIdToDelete = null;
        urlDelete = null;
    });

    // Confirmar exclusão
    confirmDeleteBtn.addEventListener('click', async () => {
        if (!columnIdToDelete || !urlDelete) return;

        try {
            const response = await fetch(urlDelete, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Remove coluna do DOM (correção da classe)
                const colElem = document.querySelector(`.column-card[data-column-id="${columnIdToDelete}"]`);
                if (colElem) colElem.remove();

                deleteModal.style.display = 'none';
                columnIdToDelete = null;
                urlDelete = null;
            } else {
                alert(data.error || 'Erro ao excluir coluna');
            }
        } catch (error) {
            alert('Erro na conexão');
        }
    });

    // Fechar modal clicando fora
    window.addEventListener('click', e => {
        if (e.target === deleteModal) {
            deleteModal.style.display = 'none';
            columnIdToDelete = null;
            urlDelete = null;
        }
    });
});
