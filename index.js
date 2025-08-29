document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("chat-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

function toggleChat() {
    let chatWindow = document.getElementById("chat-window");
    chatWindow.style.display = (chatWindow.style.display === "flex") ? "none" : "flex";
}

function sendMessage() {
    let inputField = document.getElementById("chat-input");
    let chatBody = document.getElementById("chat-body");
    let message = inputField.value.trim();

    if (message === "") return;

    // Add User Message
    let userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.innerText = message;
    chatBody.appendChild(userMessage);

    inputField.value = "";

    // Auto-Reply from Bot
    setTimeout(() => {
        let botMessage = document.createElement("p");
        botMessage.className = "bot-message";
        botMessage.innerText = "I'm still learning! 😊";
        chatBody.appendChild(botMessage);
        
        chatBody.scrollTop = chatBody.scrollHeight;  // Auto-scroll
    }, 1000);

    chatBody.scrollTop = chatBody.scrollHeight;
}
