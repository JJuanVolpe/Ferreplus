document.addEventListener('DOMContentLoaded', (event) => {
    // Obtener todos los elementos de mensaje
    const messages = document.querySelectorAll('.message');
    
    // Recorrer cada mensaje y configurarlo para desaparecer después de 3 segundos
    messages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = '0'; // Establece opacidad a 0 para desvanecer
            message.style.transition = 'opacity 1s ease-out'; // Aplica transición a la opacidad
            setTimeout(() => {
                message.style.display = 'none'; // Elimina el mensaje del flujo del documento
            }, 1000); // Espera a que la transición termine (1s)
        }, 5000); // Espera 5 segundos antes de empezar a desvanecer
    });
});