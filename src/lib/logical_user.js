// Manejar el formulario de agregar usuario
document.getElementById('add-user-form').addEventListener('submit', async (event) => {
	event.preventDefault();

	// Capturar los datos del formulario
	const nombre = document.getElementById('nombre').value.trim();
	const direccion = document.getElementById('direccion').value.trim();
	const telefono = document.getElementById('telefono').value.trim();

	console.log("Datos para agregar usuario:", { nombre, direccion, telefono });

	try {
			// Enviar los datos al backend
			const response = await fetch('http://127.0.0.1:5000/users', {
					method: 'POST',
					headers: {
							'Content-Type': 'application/json',
					},
					body: JSON.stringify({ nombre, direccion, telefono }),
			});

			if (!response.ok) {
					console.error("Error en la respuesta de la API al agregar usuario:", await response.text());
					throw new Error('Error al agregar el usuario');
			}

			// Notificar al usuario y recargar la página
			alert('Usuario agregado exitosamente');

			//limpiar los campos del formulario
			document.getElementById('nombre').value = '';
			document.getElementById('direccion').value = '';
			document.getElementById('telefono').value = '';
		
			// Ocultar el modal
			const addUserModal = document.getElementById('add-user-modal');
			addUserModal.classList.add('hidden');

			location.reload();
	} catch (error) {
			console.error("Error al agregar usuario:", error);
			alert("No se pudo agregar el usuario. Revisa la consola para más detalles.");
	}
});

// Limpiar los campos del modal de agregar usuario cuando se abre
document.querySelector('[data-modal-toggle="add-user-modal"]').addEventListener('click', () => {
	document.getElementById('nombre').value = '';
	document.getElementById('direccion').value = '';
	document.getElementById('telefono').value = '';
});
// Manejar el formulario de editar usuario
// Llenar modal con los datos del usuario seleccionado
document.querySelectorAll('[data-modal-target="edit-user-modal"]').forEach((button) => {
		button.addEventListener('click', (event) => {
				const userId = button.dataset.userId;
				const userName = button.dataset.userName;
				const userAddress = button.dataset.userAddress;
				const userPhone = button.dataset.userPhone;

				console.log("Abriendo modal de edición para el usuario:", { userId, userName, userAddress, userPhone });

				// Llenar campos del modal
				document.getElementById('id_nombre').value = userName || '';
				document.getElementById('id_direccion').value = userAddress || '';
				document.getElementById('id_telefono').value = userPhone || '';

				// Adjuntar el ID del usuario al modal
				const modal = document.getElementById('edit-user-modal');
				modal.dataset.userId = userId;
		});
});

// Enviar datos actualizados al backend
document.querySelector('#edit-user-modal button[type="submit"]').addEventListener('click', async (event) => {
		event.preventDefault();

		const modal = document.getElementById('edit-user-modal');
		const userId = modal.dataset.userId;
		const nombre = document.getElementById('id_nombre').value;
		const direccion = document.getElementById('id_direccion').value;
		const telefono = document.getElementById('id_telefono').value;

		console.log("Enviando actualización para:", { userId, nombre, direccion, telefono });

		try {
				const response = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
						method: 'PUT',
						headers: {
								'Content-Type': 'application/json',
						},
						body: JSON.stringify({ nombre, direccion, telefono }),
				});

				if (!response.ok) throw new Error("Error al actualizar el usuario");

				alert("Usuario actualizado exitosamente");
				location.reload();
		} catch (error) {
				console.error("Error:", error);
				alert("No se pudo actualizar el usuario");
		}
});
// Manejar la eliminación de usuario
document.querySelectorAll('[data-modal-target="delete-user-modal"]').forEach((button) => {
	button.addEventListener('click', (event) => {
			const userId = button.dataset.userId;
			const userName = button.closest('tr').querySelector('td:nth-child(3)').textContent; // Obtener el nombre del usuario desde la fila

			console.log("Abriendo modal de eliminación para el usuario:", { userId, userName });

			// Adjuntar el ID del usuario al modal
			const modal = document.getElementById('delete-user-modal');
			modal.dataset.userId = userId;

			// Mostrar el nombre del usuario en el mensaje
			const deleteUserNameElement = document.getElementById('delete-user-name');
			deleteUserNameElement.textContent = `Are you sure you want to delete the user, ${userName}?`;
	});
});

// Enviar solicitud de eliminación al backend
document.querySelector('#delete-user-modal .text-white.bg-red-600').addEventListener('click', async (event) => {
	event.preventDefault();

	const modal = document.getElementById('delete-user-modal');
	const userId = modal.dataset.userId;

	console.log("Enviando solicitud de eliminación para el usuario:", userId);

	try {
			const response = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
					method: 'DELETE',
			});

			if (!response.ok) throw new Error("Error al eliminar el usuario");

			alert("Usuario eliminado exitosamente");
			location.reload(); // Recargar la página para reflejar los cambios
	} catch (error) {
			console.error("Error:", error);
			alert("No se pudo eliminar el usuario");
	}
});
