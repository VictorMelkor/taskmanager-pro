    document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('create-board-modal');
    const openBtn = document.getElementById('open-create-board-modal');
    const closeBtn = document.getElementById('close-create-board-modal');
    const form = document.getElementById('create-board-form');
    const errorDiv = document.getElementById('create-board-error');

    if (!modal || !openBtn || !closeBtn || !form || !errorDiv) {
        console.error('Elemento não encontrado. Verifique os IDs no HTML.');
        return;
    }

    openBtn.addEventListener('click', () => {
        modal.classList.add('active');
        openBtn.setAttribute('aria-expanded', 'true');
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        openBtn.setAttribute('aria-expanded', 'false');
        errorDiv.textContent = '';
        form.reset();
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
        closeBtn.click();
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorDiv.textContent = '';

        const formData = new FormData(form);
        const csrfToken = formData.get('csrfmiddlewaretoken');

        if (!csrfToken) {
        errorDiv.textContent = 'Token CSRF não encontrado.';
        return;
        }

        try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        if (response.status === 400) {
            const data = await response.json();
            errorDiv.textContent = data.error || 'Erro no formulário.';
            return;
        }

        if (!response.ok) {
            errorDiv.textContent = 'Erro ao criar quadro. Tente novamente.';
            return;
        }

        const data = await response.json();

        if (data.success && data.url) {
            window.location.href = data.url;
        } else {
            errorDiv.textContent = data.error || 'Erro inesperado.';
        }
        } catch (error) {
        console.error(error);
        errorDiv.textContent = 'Erro de rede. Tente novamente.';
        }
    });
    });
