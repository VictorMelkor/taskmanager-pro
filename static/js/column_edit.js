document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = getCookie('csrftoken');

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

    function ajaxEditColumn(columnId, newName, span, input) {
        fetch(`/${span.dataset.username}/${span.dataset.slug}/columns/${columnId}/edit-ajax/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ name: newName })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success) {
                span.textContent = body.name;
            } else {
                alert(body.error || 'Erro ao editar coluna');
            }
            span.style.display = 'inline';
            input.remove();
        })
        .catch(() => {
            alert('Erro na requisição');
            span.style.display = 'inline';
            input.remove();
        });
    }

    document.querySelectorAll('.column-name').forEach(span => {
        span.addEventListener('click', function () {
            const columnId = this.dataset.columnId;
            const username = this.dataset.username;
            const slug = this.dataset.slug;
            const currentName = this.textContent.trim();

            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentName;

            this.style.display = 'none';
            this.parentNode.insertBefore(input, this);
            input.focus();

            input.addEventListener('blur', () => {
                const newName = input.value.trim();
                if (newName && newName !== currentName) {
                    ajaxEditColumn(columnId, newName, span, input);
                } else {
                    span.style.display = 'inline';
                    input.remove();
                }
            });

            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    input.blur();
                } else if (e.key === 'Escape') {
                    span.style.display = 'inline';
                    input.remove();
                }
            });
        });
    });
});
