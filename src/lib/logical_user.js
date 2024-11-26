//Importación de la librería
import Swal from 'sweetalert2';

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
			await Swal.fire({
				title: 'Usuario registrado',
				text: 'Usuario ingresado exitosamente',
				icon: 'success',
				confirmButtonColor: '#3085d6', // Cambiar a azul
			});
			//location.reload();

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
			await Swal.fire({
				title: 'Usuario no registrado',
				text: 'Usuario no se pudo ingresar',
				icon: 'error',	
				confirmButtonColor: '#3085d6', // Cambiar a azul
			});
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

			await Swal.fire({
					title: 'Usuario actualizado',
					text: 'Usuario actualizado exitosamente',
					icon: 'success',
					confirmButtonColor: '#3085d6', // Cambiar a azul
			});

			// Ocultar el modal
			modal.classList.add('hidden');
			location.reload();

	} catch (error) {
			await Swal.fire({
					title: 'Usuario sin actualizar',
					text: 'Usuario no se puede actualizar',
					icon: 'error',
					confirmButtonColor: '#3085d6', // Cambiar a azul
			});

			// Ocultar el modal incluso si ocurre un error
			modal.classList.add('hidden');
			location.reload();
	}
});

// Manejar la eliminación de usuario con SweetAlert2
document.querySelectorAll('[data-modal-target="delete-user-modal"]').forEach((button) => {
	button.addEventListener('click', async () => {
					const userId = button.dataset.userId;
					const userName = button.closest('tr').querySelector('td:nth-child(3)').textContent;

					console.log("Preparando eliminación para el usuario:", { userId, userName });

					const result = await Swal.fire({
									title: `Eliminar Usuario`,
									text: `¿Estás seguro de que quieres eliminar a ${userName}?`,
									icon: 'warning',
									showCancelButton: true,
									confirmButtonColor: '#d33',
									cancelButtonColor: '#3085d6',
									confirmButtonText: 'Sí, eliminar',
									cancelButtonText: 'Cancelar',
					});

					if (result.isConfirmed) {
									try {
													const response = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
																	method: 'DELETE',
													});

													if (!response.ok) throw new Error("Error al eliminar el usuario");

													Swal.fire({
																	title: 'Usuario eliminado',
																	text: `El usuario ${userName} fue eliminado exitosamente`,
																	icon: 'success',
																	confirmButtonColor: '#3085d6', // Cambiar a azul
													}).then(() => location.reload());
									} catch (error) {
													console.error("Error al eliminar usuario:", error);
													Swal.fire({
																	title: 'Error',
																	text: 'No se pudo eliminar el usuario',
																	icon: 'error',
																	confirmButtonColor: '#3085d6', // Cambiar a azul
													});
									}
					}
	});
});

