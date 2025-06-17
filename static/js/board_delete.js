console.log('board_delete.js carregado');

document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('open-delete-modal');
    const modal = document.getElementById('delete-modal');
    const cancelBtn = document.getElementById('cancel-delete');

    if (!openBtn || !modal || !cancelBtn) return;

    openBtn.addEventListener('click', function() {
        modal.classList.add('active');
        modal.focus();
    });

    cancelBtn.addEventListener('click', function() {
        modal.classList.remove('active');
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === "Escape" && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    });
});
