window.selectedColumnId = null;


// static/js/column_utils.js
window.openDeleteModal = function(columnId) {
    const modal = document.getElementById('deleteColumnModal');
    const confirmBtn = document.getElementById('confirmDeleteColumn');

    window.selectedColumnId = columnId;
    modal.classList.add('active');
    modal.removeAttribute('hidden');
    modal.setAttribute('aria-hidden', 'false');
    confirmBtn.focus();
};
