import React, { useState } from "react";
import './ball.css'; // Import the CSS file for styling the ball
import ChatWindow from "./Chatwindow";

function Ball() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div>
      {!isChatOpen && (
        <div className="chat-ball" onClick={toggleChat}></div>
      )}
      {isChatOpen && <ChatWindow onClose={() => setIsChatOpen(false)} />}
    </div>
  );
}

export default Ball;
