const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const chatContainer = document.getElementById("chat-container");
let isLoading = false;

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

function addMessage(text, sender) {
  const message = document.createElement("div");
  message.className = `chatbot-message ${sender}`;
  message.textContent = text;
  chatContainer.appendChild(message);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text || isLoading) return;

  addMessage(text, "user");
  input.value = "";
  isLoading = true;

  try {
    const res = await fetch("http://localhost:7777/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: text }),
    });

    if (!res.body) throw new Error("No response body");

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let botText = "";

    const botMsg = document.createElement("div");
    botMsg.className = "chatbot-message bot";
    chatContainer.appendChild(botMsg);

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      botText += decoder.decode(value, { stream: true });
      botMsg.textContent = botText;
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  } catch (error) {
    console.error(error);
    addMessage("Something went wrong!", "bot");
  } finally {
    isLoading = false;
  }
}
