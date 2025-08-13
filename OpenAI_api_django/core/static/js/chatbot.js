$(document).ready(function () {
    // Toggle chat widget and show welcome message on first open
    $('#chatbot-toggle').on("click", function () {
        $('#chatbot-widget').toggleClass('active');

        // This condition ensures the message appears
        // only when the widget is opened for the first time.
        if ($('#chatbot-widget').is(':visible') && !window.chatGreeted) {
            appendTypingMessage('Hello! How can I help you today?', 'bot');
            window.chatGreeted = true;
        }
    });

    $('#chatbot-close').on("click", function () {
        $('#chatbot-widget').removeClass('active');
    })

    function appendTypingMessage(text, sender, callback) {
        const className = sender === 'user' ? 'message user' : 'message bot';
        const $msg = $('<div>').addClass(className);
        $('#chat-box').append($msg);
        $('#chat-box').animate({ scrollTop: $('#chat-box')[0].scrollHeight }, 300);

        let i = 0;
        const typingSpeed = 20;

        function typeLetter() {
            if (i < text.length) {
                $msg.text($msg.text() + text[i]);
                i++;
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                setTimeout(typeLetter, typingSpeed);
            } else if (callback) {
                callback();
            }
        }
        typeLetter();
    }




    const CHATBOT_API_URL = $('#chat-form').data('api-url');

    $('#chat-form').on('submit', function (e) {
        e.preventDefault()


        let $submitButton = $('#submit-button');
        let message = $('#user-input').val().trim()
        if (!message) return

        $submitButton.prop('disabled', true).text('AI Writing...');

        appendTypingMessage(message, 'user')
        $('#user-input').val('')

        axios
            .post(CHATBOT_API_URL,
                { message: message },
                { headers: { 'X-CSRFToken': '{{ csrf_token }}' } }
            )
            .then(function (response) {
                let botReply = response.data.answer || "Sorry, I couldn't respond."
                appendTypingMessage(botReply, 'bot', function () {
                    $submitButton.prop('disabled', false).text('Send');
                    $userInput.focus();
                });
            })
            .catch(function (error) {
                appendTypingMessage('Error. Try again.', 'bot', function () {
                    $submitButton.prop('disabled', false).text('Send');
                    $userInput.focus();
                });
                console.error(error);
            });
    })
})