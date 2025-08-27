$(document).ready(function() {
    const sendBtn = $('#sendBtn');
    const speakBtn = $('#speakBtn');
    const userInput = $('#userInput');
    const chatBox = $('#chatBox');

    // Append a message to chat box
    function appendMessage(message, sender) {
        const messageDiv = $('<div>').addClass('message').addClass(sender).text(message);
        chatBox.append(messageDiv);
        chatBox.scrollTop(chatBox[0].scrollHeight);
    }

    // Send query to FastAPI
    async function sendQuery(query) {
        if (!query) return;

        appendMessage(query, 'user');

        // Add typing indicator
        const typingDiv = $('<div>').addClass('message ai').attr('id', 'typing').text('...');
        chatBox.append(typingDiv);
        chatBox.scrollTop(chatBox[0].scrollHeight);

        try {
            const res = await axios.post("http://127.0.0.1:8000/ask", { query });
            const aiText = res.data.response;

            $('#typing').remove(); // Remove typing placeholder

            // Type out AI message gradually
            let i = 0;
            const speed = 30; // ms per character
            const chunkSize = 15; // characters to speak at once

            const aiDiv = $('<div>').addClass('message ai');
            chatBox.append(aiDiv);

            function typeAndSpeak() {
                if (i < aiText.length) {
                    const nextChunk = aiText.slice(i, i + chunkSize);
                    aiDiv.append(nextChunk);
                    i += chunkSize;

                    // Speak current chunk
                    const utterance = new SpeechSynthesisUtterance(nextChunk);
                    utterance.lang = "en-US";
                    speechSynthesis.speak(utterance);

                    chatBox.scrollTop(chatBox[0].scrollHeight);
                    setTimeout(typeAndSpeak, speed * chunkSize);
                }
            }

            typeAndSpeak();

        } catch (err) {
            console.error("Error:", err);
            $('#typing').remove();
            appendMessage("Error: Could not get response from AI.", 'ai');
        }
    }

    // Send button click
    sendBtn.on('click', () => {
        const query = userInput.val().trim();
        userInput.val('');
        sendQuery(query);
    });

    // Enter key to send
    userInput.on('keypress', function(e) {
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            sendBtn.click();
        }
    });

    // Voice input button
    speakBtn.on('click', () => {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert("Your browser does not support speech recognition.");
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.start();

        recognition.onresult = (event) => {
            const spokenText = event.results[0][0].transcript;
            userInput.val(spokenText);
            sendQuery(spokenText);
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
        };
    });
});
