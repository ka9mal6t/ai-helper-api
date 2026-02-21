"use strict";

marked.setOptions({
    breaks: true,
    gfm: true
});

const chat = document.getElementById("chat");
const input = document.getElementById("question");

input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function addMessage(text, className) {
    const div = document.createElement("div");
    div.className = "message " + className;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

async function sendMessage(chatId) {

    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    const assistantMessage = addMessage("", "assistant");

    const response = await fetch("/ai/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question,
            chat_id: chatId
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let buffer = "";
    let fullText = "";

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const events = buffer.split("\n\n");
        buffer = events.pop();

        for (let event of events) {
            if (event.startsWith("data: ")) {
                const text = event.slice(6);

                // \n
                fullText += text;

                assistantMessage.textContent = fullText;
            }
        }
    }

    assistantMessage.innerHTML =
        DOMPurify.sanitize(marked.parse(fullText));
}