console.log('column_edit.js carregado');

document.addEventListener('DOMContentLoaded', () => {
    initializeAllColumns();
});

// Inicializa a edição do nome para um span específico
function initializeColumnNameEdit(span) {
    span.addEventListener('click', () => {
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

// Inicializa todos os spans de colunas já no DOM
function initializeAllColumns() {
    document.querySelectorAll('.column-name').forEach(span => {
        initializeColumnNameEdit(span);
    });

    initializeColumnOptionsButtons();
}

// Aqui deve ter a função que inicializa os botões de opções e adicionar tarefa, por exemplo:
function initializeColumnOptionsButtons() {
    // Exemplo simples, adapte conforme seu código real
    document.querySelectorAll('.column-options-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            const dropdown = btn.nextElementSibling;
            if (dropdown) {
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            }
        });
    });

    // Também pode adicionar listeners para botões de excluir, mover, adicionar tarefa etc
}

// Exporta essa função para usar no JS que cria a nova coluna
function initializeNewColumn(columnElement) {
    const nameSpan = columnElement.querySelector('.column-name');
    if (nameSpan) initializeColumnNameEdit(nameSpan);

    initializeColumnOptionsButtons();

    // Inicialize outros botões da coluna (ex: add-task-btn) se necessário
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
