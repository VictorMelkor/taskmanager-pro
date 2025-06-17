console.log('add_column.js carregado');

document.addEventListener('DOMContentLoaded', () => {
    initializeAllColumns();
});

// Inicializa a edição do nome para um span específico
function initializeColumnNameEdit(span) {
    span.addEventListener('click', (e) => {
        e.stopPropagation(); // impede fechamento do dropdown ao clicar para editar

        console.log('clicou no nome da coluna');

        if (span.querySelector('input')) return; // já em edição

        const oldName = span.textContent.trim();
        const input = document.createElement('input');
        input.type = 'text';
        input.value = oldName;
        input.classList.add('column-name-input', 'input-field');

        span.textContent = '';
        span.appendChild(input);
        input.focus();

        const cancelEdit = () => {
            input.removeEventListener('blur', saveEdit);
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
                e.preventDefault();
                cancelEdit();
            }
        });
    });
}

// Inicializa todos os spans de colunas já no DOM
function initializeAllColumns() {
    document.querySelectorAll('.column-name').forEach(span => {
        initializeColumnNameEdit(span);
    });
}

// Exporta para uso externo
function initializeNewColumn(columnElement) {
    const nameSpan = columnElement.querySelector('.column-name');
    if (nameSpan) initializeColumnNameEdit(nameSpan);
}

// Função para pegar CSRF cookie (padrão Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}