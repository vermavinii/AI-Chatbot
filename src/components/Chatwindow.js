import React, { useState, useRef, useEffect} from 'react';
import './Chatwindow.css';

const ChatWindow = ({ onClose }) => {
  const [message, setMessage] = useState('');
  const [sentMessages, setSentMessages] = useState([]);
  const [buttonMessages] = useState({
    Admissions: 'Admissions',
    Courses: 'Courses',
    Scholarships: 'Scholarships',
    Events: 'Events'
  });
  
  const messageContainerRef = useRef(null);

  const buttonUrls = {
    Admissions: 'http://www.banasthali.org/banasthali/wcms/en/home/admissions/index.html',
    Courses: 'http://www.banasthali.org/banasthali/admissions/course.html',
    Scholarships: 'http://www.banasthali.org/banasthali/wcms/en/home/financial-assistance/scholarshps/index.html',
    Events: 'http://www.banasthali.org/banasthali/wcms/en/home/lower-menu/news-event-n-announcements/index.html'
  };

  const handleButtonClick = (message) => {
    const url = buttonUrls[message];
    if (url) {
      window.open(url, '_blank');
    }
  };

  const handleInputChange = (event) => {
    setMessage(event.target.value);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && message.trim()) {
      event.preventDefault();
      if (message.trim() !== '') {
        sendMessage();
      }
    }
  };

  useEffect(() => {
    messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
  }, [sentMessages]);
  

  const sendMessage = async () => {
    if (message.trim() !== '') {
      const newMessage = message;
      const updatedMessages = [...sentMessages, newMessage];
      setSentMessages(updatedMessages);
      setMessage('');
      messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;

      try {
        const response = await fetch('http://127.0.1:5000/ask',{
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        });
        const responseData = await response.json();
        const updatedMessages = [...sentMessages, newMessage, responseData.answer];
        setSentMessages(updatedMessages);
        setMessage('');
        console.log(responseData.answer);

        messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  

  return(
    <div className="chat-window">
      <div className="header">
        <button className="close-btn" onClick={onClose}> X </button>
        <span className="chat-title1">वनस्थली विद्यापीठ</span>
        <span className="chat-title2">Banasthali Vidyapith</span>
        
        <img src={require('./image.jpg')} alt="User" className="user-avatar" />
      </div>
      <span className="chat-title3"> Welcome to Vidyapith</span>
      <div className="blur-background">
        <img src={require('./images.png')} alt="Background" className="blur-image" />
      </div>
      <div className="message-container" ref={messageContainerRef}>
        {sentMessages.map((message, index) => (
          <div key={index} className={index % 2 === 0 ? "user-message" : "chatbot-message"}>
            {message}
          </div>
        ))}
      </div>
      {/* <div className="message-container" ref={messageContainerRef}>
      {sentMessages.map((message, index) => (
        <div key={index} className={index % 2 === 0 ? "chatbot-message" : "user-message"}>
          <div className="message-content">
            <div className="message-text">{message}</div>
          </div>
        </div>
      ))}
    </div> */}
    {/* <div className="avatar">
        <img src={require('./images.png')} alt="Background" className="bot-image" />
      </div> */}
      <div className="buttons-container">
        {Object.values(buttonMessages).map((buttonMessage, index) => (
          <button key={index} className="button-box" onClick={() => handleButtonClick(buttonMessage)}>
            {buttonMessage}
          </button>
        ))}
      </div>
      <div className="input-box">
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
        />
      </div>
    </div>
  );
};

export default ChatWindow;
