document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('inviteModal');
    const closeBtn = modal?.querySelector('.modal-close-btn');
    const copyBtn = document.getElementById('copyInviteBtn');
    const inviteInput = document.getElementById('inviteLink');

    if (modal) {
        modal.style.display = 'flex';

        closeBtn?.addEventListener('click', () => {
            modal.style.display = 'none';
        });

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                modal.style.display = 'none';
            }
        });
    }

    if (copyBtn && inviteInput) {
        copyBtn.addEventListener('click', () => {
            // Seleciona o texto do input para facilitar visualmente a cópia
            inviteInput.select();
            inviteInput.setSelectionRange(0, 99999);

            // Copia para a área de transferência usando Clipboard API
            navigator.clipboard.writeText(inviteInput.value)
                .then(() => alert('Link copiado!'))
                .catch(() => alert('Erro ao copiar o link.'));
        });
    }
});
