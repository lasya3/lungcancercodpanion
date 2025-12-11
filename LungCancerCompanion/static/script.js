const API_URL = 'http://localhost:5000/api';

let isLoading = false;

// Format time for messages
function formatTime() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const displayHours = hours % 12 || 12;
    const displayMinutes = minutes.toString().padStart(2, '0');
    return `${displayHours}:${displayMinutes} ${ampm}`;
}

// Add message to chat
function addMessage(content, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Parse content for line breaks and lists
    const formattedContent = formatMessageContent(content);
    messageContent.innerHTML = formattedContent;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = isUser ? formatTime() : 'Just now';
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Hide suggested questions after first user message
    if (isUser) {
        const suggestedQuestions = document.getElementById('suggestedQuestions');
        if (suggestedQuestions.style.display !== 'none') {
            suggestedQuestions.style.display = 'none';
        }
    }
}

// Format message content with proper line breaks
function formatMessageContent(text) {
    // Convert markdown-style lists and line breaks to HTML
    let formatted = text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert numbered and bullet lists
    const lines = formatted.split('<br>');
    let inList = false;
    let listContent = '';
    let result = [];
    
    for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.match(/^[-*•]\s/) || trimmed.match(/^\d+\.\s/)) {
            if (!inList) {
                inList = true;
                listContent = '<ul>';
            }
            const listItem = trimmed.replace(/^[-*•]\s/, '').replace(/^\d+\.\s/, '');
            listContent += `<li>${listItem}</li>`;
        } else {
            if (inList) {
                listContent += '</ul>';
                result.push(listContent);
                listContent = '';
                inList = false;
            }
            if (trimmed) {
                result.push(`<p>${trimmed}</p>`);
            } else {
                result.push('<br>');
            }
        }
    }
    
    if (inList) {
        listContent += '</ul>';
        result.push(listContent);
    }
    
    return result.length > 0 ? result.join('') : `<p>${text}</p>`;
}

// Show loading indicator
function showLoading() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = 'loadingMessage';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = '<div class="loading"></div>';
    
    loadingDiv.appendChild(messageContent);
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hide loading indicator
function hideLoading() {
    const loadingMessage = document.getElementById('loadingMessage');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Send message to API
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    // Clear input
    input.value = '';
    
    // Add user message
    addMessage(message, true);
    
    // Show loading
    isLoading = true;
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.status === 'success') {
            addMessage(data.response, false);
        } else {
            addMessage('I apologize, but I encountered an error. Please try again or rephrase your question.', false);
        }
    } catch (error) {
        hideLoading();
        addMessage('I apologize, but I\'m having trouble connecting right now. Please check your connection and try again.', false);
        console.error('Error:', error);
    } finally {
        isLoading = false;
    }
}

// Handle key press in input
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Handle topic button clicks
function handleTopicClick(topic) {
    document.getElementById('userInput').value = topic;
    sendMessage();
}

// Handle suggested question clicks
function handleQuestionClick(question) {
    document.getElementById('userInput').value = question;
    sendMessage();
}

// Make functions globally accessible (must be after function definitions)
window.sendMessage = sendMessage;
window.handleTopicClick = handleTopicClick;
window.handleQuestionClick = handleQuestionClick;
window.handleKeyPress = handleKeyPress;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('LumoCare chat initialized');
    // Check API health
    fetch(`${API_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('API connected:', data);
        })
        .catch(error => {
            console.error('API connection error:', error);
            console.log('Make sure Flask server is running on http://localhost:5000');
        });
});

