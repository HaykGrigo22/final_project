const socket = new WebSocket('ws://localhost:8000/ws/user/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    displayMessage(data.message, 'received');
};

socket.onopen = function() {
    console.log('WebSocket connected');
};

socket.onclose = function() {
    console.log('WebSocket closed');
};

document.getElementById('send-button').onclick = function() {
    const inputField = document.getElementById('input-field');
    const message = inputField.value;
    if (message) {
        displayMessage(message, 'sent');
        socket.send(JSON.stringify({ 'message': message }));
        inputField.value = '';
    }
};

function displayMessage(message, type) {
    const messageList = document.getElementById('message-list');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);
    messageElement.textContent = message;
    messageList.appendChild(messageElement);
    messageList.scrollTop = messageList.scrollHeight; // Auto-scroll
}
