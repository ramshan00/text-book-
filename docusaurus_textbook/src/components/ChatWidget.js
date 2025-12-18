import React, { useState } from "react";
import axios from "axios";
import "./chat.css";

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([
    { role: "bot", content: "AI_TERMINAL_ONLINE: Diagnostics active. How can I assist with your robotics inquiry?" },
  ]);
  const [loading, setLoading] = useState(false);

  const backendUrl = "http://localhost:8000";

  const handleSend = async () => {
    if (!query.trim()) return;

    const newMessages = [...messages, { role: "user", content: query }];
    setMessages(newMessages);
    setQuery("");
    setLoading(true);

    try {
      const response = await axios.post(`${backendUrl}/ask`, { query });
      setMessages([...newMessages, { role: "bot", content: response.data.answer }]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { role: "bot", content: "ERROR_404: CONNECTION_LOST. Is the neural link (backend) active?" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {isOpen ? (
        <div className="chat-box">
          <div className="chat-header">
            <h3>ROBOTIC_AI_HUD:// v1.0.4</h3>
            <button
              onClick={() => setIsOpen(false)}
              style={{ background: 'transparent', border: 'none', color: 'var(--ifm-color-primary)', cursor: 'pointer', fontSize: '20px', fontWeight: 'bold' }}
            >
              [X]
            </button>
          </div>
          <div className="chat-body">
            {messages.map((msg, index) => (
              <div key={index} className={`bubble ${msg.role}`}>
                {msg.content}
              </div>
            ))}
            {loading && <div className="bubble bot">CALCULATING_TRAJECTORY...</div>}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="ENTER_QUERY_INPUT..."
            />
            <button onClick={handleSend} disabled={loading}>
              {loading ? "..." : "SEND"}
            </button>
          </div>
        </div>
      ) : (
        <button className="chat-button" onClick={() => setIsOpen(true)}>
          AI
        </button>
      )}
    </div>
  );
};

export default ChatWidget;
