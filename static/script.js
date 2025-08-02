const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");

// Function to add message to chat
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerText = text;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Function to send message to API
async function sendMessage() {
  const text = userInput.value.trim();
  if (text === "") return;

  addMessage(text, "user");
  userInput.value = "";

  const typingMsg = document.createElement("div");
  typingMsg.classList.add("message", "bot", "typing");
  typingMsg.innerText = "Lovi is typing... 💭";
  chatWindow.appendChild(typingMsg);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    console.log("📦 API response:", data);
    typingMsg.remove();

    if (data.status === "success") {
      addMessage(data.reply, "bot");
    } else if (data.status === "error") {
      addMessage(data.reply || "Lovi is quiet today 💔", "bot");
    } else {
      addMessage("Lovi didn’t understand that 😳", "bot");
    }

  } catch (error) {
    typingMsg.remove();
    console.error("❌ Fetch Error:", error);
    addMessage("Lovi is offline right now 😢", "bot");
  }
}

// Send on Enter key
userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});
