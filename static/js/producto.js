function eliminarProducto(productId) {
        if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
            fetch(`/producto/${productId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al eliminar el producto');
                }
                // No necesitas response.url en este caso
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                // Manejar errores si es necesario
            });
        }
}