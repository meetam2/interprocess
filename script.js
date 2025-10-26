const PORT = "8766";

const status = document.getElementById("status");
const response = document.getElementById("response");
const ws = new WebSocket("ws://localhost:" + PORT);

ws.onopen = () => {
response.textContent = "Connected ✅";
status.textContent = "Connected ✅";
};

ws.onclose = () => {
status.textContent = "Connection closed ❌";
};

ws.onmessage = (event) => {
response.textContent = event.data;
};

document.getElementById("pingBtn").onclick = () => {
ws.send("ping");
response.textContent = "Sent: ping";
};