(function() {
    function initChatbot() {
        // ============================================
        // DYNAMIC CLIENT CONFIG
        // Reads from window.CHATBOT_CONFIG with default fallbacks
        // ============================================
        const DEFAULT_CONFIG = {
            clientId: "eastblue_gym",
            botName: "Neural Assistant HUD",
            welcomeMessage: "System Online. How can I help you today?",
            primaryColor: "#F5E642",
            backendUrl: ""
        };

        const CONFIG = Object.assign({}, DEFAULT_CONFIG, window.CHATBOT_CONFIG);

        // Resolve Backend URL dynamically if not explicitly provided
        let resolvedBackendUrl = CONFIG.backendUrl || "";
        if (!resolvedBackendUrl) {
            resolvedBackendUrl = window.location.origin;
        }

        // Inject Stylesheet into host head
        const style = document.createElement('style');
        style.textContent = `
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

            .chatbot-container {
                --chatbot-primary: ${CONFIG.primaryColor || '#4f46e5'};
                --chatbot-bg: rgba(255, 255, 255, 0.95);
                --chatbot-border: rgba(226, 232, 240, 0.8);
                --chatbot-text: #1e293b;
                --chatbot-text-secondary: #64748b;
                --chatbot-font: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                
                position: fixed;
                bottom: 24px;
                right: 24px;
                z-index: 999999;
                font-family: var(--chatbot-font);
            }

            .chatbot-container *,
            .chatbot-container *::before,
            .chatbot-container *::after {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: var(--chatbot-font);
                line-height: 1.5;
                letter-spacing: normal;
                text-transform: none;
                text-shadow: none;
            }

            .chatbot-container button,
            .chatbot-container input {
                border: none;
                outline: none;
                background: none;
                box-shadow: none;
                font-family: var(--chatbot-font);
            }

            .chatbot-bubble {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: var(--chatbot-primary);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15), inset 0 2px 4px rgba(255, 255, 255, 0.2);
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
            }

            .chatbot-bubble:hover {
                transform: scale(1.08) translateY(-2px);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2), inset 0 2px 4px rgba(255, 255, 255, 0.3);
            }

            .chatbot-bubble svg {
                width: 28px;
                height: 28px;
                fill: #ffffff;
                transition: transform 0.3s ease;
            }

            .chatbot-bubble:hover svg {
                transform: rotate(10deg);
            }

            .neural-pulse {
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background: var(--chatbot-primary);
                opacity: 0.4;
                z-index: -1;
                animation: pulse-ring 2s cubic-bezier(0.215, 0.610, 0.355, 1) infinite;
            }

            @keyframes pulse-ring {
                0% { transform: scale(0.95); opacity: 0.5; }
                100% { transform: scale(1.4); opacity: 0; }
            }

            .chatbot-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 380px;
                height: 520px;
                border-radius: 24px;
                background: var(--chatbot-bg);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.4);
                box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                opacity: 0;
                transform: translateY(20px) scale(0.95);
                pointer-events: none;
                transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .chatbot-window.active {
                opacity: 1;
                transform: translateY(0) scale(1);
                pointer-events: auto;
            }

            .chatbot-header {
                padding: 20px 24px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                border-bottom: 1px solid var(--chatbot-border);
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .chatbot-header h3 {
                margin: 0;
                font-size: 16px;
                font-weight: 700;
                color: var(--chatbot-text);
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .chatbot-header h3::before {
                content: '';
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10b981;
                display: inline-block;
                box-shadow: 0 0 8px #10b981;
            }

            .close-chat {
                font-size: 24px;
                font-weight: 400;
                color: var(--chatbot-text-secondary);
                cursor: pointer;
                transition: color 0.2s ease;
                line-height: 1;
            }

            .close-chat:hover {
                color: var(--chatbot-text);
            }

            .chatbot-messages {
                flex: 1;
                padding: 24px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }

            .chatbot-messages::-webkit-scrollbar {
                width: 6px;
            }

            .chatbot-messages::-webkit-scrollbar-thumb {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 3px;
            }

            .message {
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 16px;
                font-size: 14px;
                line-height: 1.5;
                animation: fadeIn 0.25s ease forwards;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(6px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .message.bot {
                align-self: flex-start;
                background: #f1f5f9;
                color: var(--chatbot-text);
                border-bottom-left-radius: 4px;
            }

            .message.user {
                align-self: flex-end;
                background: var(--chatbot-primary);
                color: #ffffff;
                border-bottom-right-radius: 4px;
            }

            .typing {
                display: none;
                align-self: flex-start;
                margin-left: 24px;
                margin-bottom: 16px;
                padding: 8px 16px;
                background: #f1f5f9;
                color: var(--chatbot-text-secondary);
                border-radius: 16px;
                border-bottom-left-radius: 4px;
                font-size: 13px;
                font-style: italic;
            }

            .chatbot-input {
                padding: 16px 20px;
                border-top: 1px solid var(--chatbot-border);
                display: flex;
                align-items: center;
                gap: 12px;
                background: rgba(255, 255, 255, 0.5);
            }

            .chatbot-input input {
                flex: 1;
                font-size: 14px;
                color: var(--chatbot-text);
                padding: 8px 0;
            }

            .chatbot-input input::placeholder {
                color: var(--chatbot-text-secondary);
            }

            .chatbot-input button {
                background: var(--chatbot-primary);
                width: 36px;
                height: 36px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .chatbot-input button:hover {
                transform: scale(1.05);
                opacity: 0.9;
            }

            .chatbot-input button svg {
                width: 16px;
                height: 16px;
                fill: #ffffff;
                transform: translate(1px, 0);
            }

            @media (max-width: 480px) {
                body.chatbot-is-open {
                    overflow: hidden;
                }
                .chatbot-window {
                    width: calc(100vw - 32px);
                    height: calc(100vh - 100px);
                    bottom: 80px;
                }
            }
        `;
        document.head.appendChild(style);

        // Build chatbot UI
        const chatbotContainer = document.createElement('div');
        chatbotContainer.className = 'chatbot-container';

        chatbotContainer.innerHTML = `
            <div class="chatbot-bubble" id="chatbotBubble">
                <div class="neural-pulse"></div>
                <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>
            </div>
            <div class="chatbot-window" id="chatbotWindow">
                <div class="chatbot-header">
                    <h3>${CONFIG.botName}</h3>
                    <span class="close-chat" id="closeChat">&times;</span>
                </div>
                <div class="chatbot-messages" id="chatMessages">
                    <div class="message bot">${CONFIG.welcomeMessage}</div>
                </div>
                <div class="typing" id="typingIndicator">Thinking...</div>
                <form class="chatbot-input" id="chatbotForm">
                    <input type="text" id="chatInput" placeholder="Type your message..." required autocomplete="off">
                    <button type="submit">
                        <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                    </button>
                </form>
            </div>
        `;

        document.body.appendChild(chatbotContainer);

        const bubble = document.getElementById('chatbotBubble');
        const chatWindow = document.getElementById('chatbotWindow');
        const closeBtn = document.getElementById('closeChat');
        const form = document.getElementById('chatbotForm');
        const input = document.getElementById('chatInput');
        const messagesContainer = document.getElementById('chatMessages');
        const typingIndicator = document.getElementById('typingIndicator');

        let chatHistory = [];

        bubble.addEventListener('click', () => {
            chatWindow.classList.toggle('active');
            document.body.classList.toggle('chatbot-is-open', chatWindow.classList.contains('active'));
            if (chatWindow.classList.contains('active')) input.focus();
        });

        closeBtn.addEventListener('click', () => {
            chatWindow.classList.remove('active');
            document.body.classList.remove('chatbot-is-open');
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            input.value = '';
            typingIndicator.style.display = 'block';
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            setTimeout(async () => {
                let reply = "Connection failed. Please try again.";

                try {
                    const API_URL = resolvedBackendUrl;
                    const response = await fetch(`${API_URL}/api/chat`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message,
                            history: chatHistory,
                            client_id: CONFIG.clientId
                        })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        reply = data.response || data.reply || reply;
                    } else {
                        reply = 'Connection interrupted. Try again in a moment.';
                    }
                } catch (err) {
                    console.error("Connection failed:", err);
                    reply = 'Offline. The backend may be waking up - try again in a few seconds.';
                }

                addMessage(reply, 'bot');
                chatHistory.push({ role: 'user', text: message });
                chatHistory.push({ role: 'bot', text: reply });

                typingIndicator.style.display = 'none';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 500);
        });

        function addMessage(text, sender) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            msgDiv.textContent = text;
            messagesContainer.appendChild(msgDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbot);
    } else {
        initChatbot();
    }
})();
