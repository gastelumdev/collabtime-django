// Connect to WebSockets server (EchoConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http' ? 'ws' : 'wss'}://${document.body.dataset.host}/ws/echo/`);

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Display the message in '#welcome'.
    document.querySelector("#welcome").textContent = event.data;
});