
// ...existing code...

function showEditUserModal(userId) {
    // Close any existing modals
    const existingModal = document.querySelector('.edit-user-modal');
    if (existingModal) {
        existingModal.remove();
    }

    // Create and show the new modal
    const modal = document.createElement('div');
    modal.classList.add('edit-user-modal');
    modal.setAttribute('data-user-id', userId);
    // ...existing code to populate and show the modal...
}

// ...existing code...
