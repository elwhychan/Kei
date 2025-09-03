    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('contact-form');
        const message = document.getElementById('contact-message');

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const userMessage = document.getElementById('message').value;

            fetch('/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: name, email: email, message: userMessage })
            })
            .then(response => response.json())
            .then(data => {
                message.textContent = data.message;
                if (data.success) {
                    message.style.color = 'green';
                    form.reset();
                } else {
                    message.style.color = 'red';
                }
            })
            .catch(error => {
                message.textContent = 'Terjadi kesalahan. Silakan coba lagi.';
                message.style.color = 'red';
                console.error('Error:', error);
            });
        });
    });
