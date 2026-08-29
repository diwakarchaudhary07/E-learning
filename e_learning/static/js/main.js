const viewAllButton = document.querySelector('.view-all-btn');
const dropdownContent = document.querySelector('.dropdown-content');

if (viewAllButton && dropdownContent) {
    viewAllButton.addEventListener('click', (event) => {
        event.preventDefault();
        dropdownContent.classList.add('open');
    });
}

const aiChatForm = document.getElementById('aiChatForm');
const aiChatInput = document.getElementById('aiChatInput');
const aiChatMessages = document.querySelector('.ai-chat-messages');
const aiChatToggle = document.querySelector('.ai-chat-toggle');
const aiChatPanel = document.getElementById('aiChatPanel');

if (aiChatPanel && aiChatToggle) {
    aiChatPanel.addEventListener('show.bs.offcanvas', () => {
        aiChatToggle.classList.add('hidden');
    });
    aiChatPanel.addEventListener('hidden.bs.offcanvas', () => {
        aiChatToggle.classList.remove('hidden');
    });
}

if (aiChatForm && aiChatInput && aiChatMessages) {
    const appendMessage = (text, isBot) => {
        const messageEl = document.createElement('div');
        messageEl.className = `ai-chat-message ${isBot ? 'ai-bot-message' : 'ai-user-message'}`;
        messageEl.innerHTML = `<div class="ai-chat-bubble">${text}</div>`;
        aiChatMessages.appendChild(messageEl);
        aiChatMessages.scrollTop = aiChatMessages.scrollHeight;
    };

    if (aiChatPanel) {
        aiChatPanel.addEventListener('show.bs.offcanvas', () => {
            if (!aiChatMessages.dataset.hasWelcome) {
                appendMessage('Hi! I am your AI assistant. Ask me anything about our courses, live classes, or how to navigate the site.', true);
                aiChatMessages.dataset.hasWelcome = 'true';
            }
        });
    }

    aiChatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = aiChatInput.value.trim();
        if (!message) {
            return;
        }

        appendMessage(message, false);
        aiChatInput.value = '';

        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
            const response = await fetch('/ai-chat/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `message=${encodeURIComponent(message)}`
            });

            const data = await response.json();
            appendMessage(data.reply || data.error || 'Sorry, something went wrong.', true);
        } catch (error) {
            appendMessage('Unable to send message. Check your connection.', true);
        }
    });
}
