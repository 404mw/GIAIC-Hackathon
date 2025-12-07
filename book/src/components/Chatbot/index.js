import React, { useState } from 'react';
import './styles.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isVisible, setIsVisible] = useState(false); // New state for visibility

  const handleSend = async () => {
    if (inputValue.trim()) {
      const newMessages = [...messages, { text: inputValue, sender: 'user' }];
      setMessages(newMessages);
      setInputValue('');
      setIsLoading(true);

      try {
        const response = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: inputValue,
            conversation_history: messages.map(msg => msg.text),
          }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setMessages([...newMessages, { text: data.answer, sender: 'bot' }]);
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        alert('Failed to get response from the chatbot. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="chatbot-widget">
      <button className="chatbot-toggle-button" onClick={() => setIsVisible(!isVisible)}>
        {isVisible ? 'Close Chat' : 'Open Chat'}
      </button>
      {isVisible && (
        <div className="chatbot-container">
          <div className="chatbot-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.sender}`}>
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div className="message bot">
                Loading...
              </div>
            )}
          </div>
          <div className="chatbot-input">
            <input
              type="text"
              placeholder="Ask something..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
