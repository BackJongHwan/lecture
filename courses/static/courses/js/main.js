// 챗봇 관련 스크립트
function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        const chatMessages = document.getElementById('chatMessages');
        
        // 사용자 메시지 추가
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message';
        userMessageDiv.textContent = message;
        chatMessages.appendChild(userMessageDiv);
        
        // 봇 응답 메시지 추가 (예시)
        setTimeout(() => {
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message bot-message';
            botMessageDiv.textContent = "죄송합니다. 아직 응답을 구현하지 않았습니다.";
            chatMessages.appendChild(botMessageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
        
        input.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Enter 키로 메시지 전송
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('messageInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}); 