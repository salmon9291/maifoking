document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message');
    const fileInput = document.getElementById('file');

    const fetchMessages = () => {
        fetch('/get_messages')
            .then(response => response.json())
            .then(messages => {
                chatBox.innerHTML = '';
                messages.forEach(message => {
                    const messageElement = document.createElement('p');
                    if (message.is_file) {
                        messageElement.innerHTML = `<strong>${message.username}:</strong> <a href="/uploads/${message.content}" target="_blank">${message.content}</a>`;
                    } else {
                        messageElement.innerHTML = `<strong>${message.username}:</strong> ${message.content}`;
                    }
                    messageElement.classList.add('message');
                    chatBox.appendChild(messageElement);
                });
                chatBox.scrollTop = chatBox.scrollHeight;
            });
    };

    chatForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(chatForm);
        fetch('/send_message', {
            method: 'POST',
            body: formData,
        }).then(() => {
            messageInput.value = '';
            fileInput.value = '';
            fetchMessages();
        });
    });

    setInterval(fetchMessages, 1000);
    fetchMessages();
});