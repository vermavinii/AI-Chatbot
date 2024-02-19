
import React,{ Component } from 'react';
import './App.css';
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {},
      isChatOpen: false,
      message: '',
      sentMessages: [],
      buttonMessages: {
        Admissions: 'Admission',
        Courses: 'Courses',
        Scholarships: 'Scholarships',
        Events: 'Events'
      }
    };
  }

  toggleChat = () => {
    this.setState(prevState => ({
      isChatOpen: !prevState.isChatOpen,
      message: !prevState.isChatOpen ? '' : prevState.message,
      sentMessages: !prevState.isChatOpen ? [] : prevState.sentMessages
    }));
  }
  
  
  handleButtonClick = (message) => {
    this.setState(prevState => ({
      sentMessages: [...prevState.sentMessages, message]
    }), () => {
      this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    });
  }

  handleInputChange = (event) => {
    this.setState({ message: event.target.value });
  }

  handleKeyDown = (event) => {
    if (event.key === 'Enter' && this.state.message.trim()) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  sendMessage = () => {
    if (this.state.message.trim() !== '') {
      const newMessage = this.state.message;
      const updatedMessages = [...this.state.sentMessages, newMessage];
  
      this.setState({
        sentMessages: updatedMessages,
        message: ''
      }, () => {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
      });
    }
  }
  
  clearChatWindow = () => {
    console.log('Clearing chat window');
    this.setState({
      isChatOpen: false,
      message: '',
      sentMessages: []
    });
  }
  

  render() {
    return (
      <div className="app">
        {!this.state.isChatOpen && (
          <div className="chat-ball" onClick={this.toggleChat}>
          </div>
        )}
        {this.state.isChatOpen && (
          <div className="chat-window">
            <div className="header">
            <button className="close-btn" onClick={this.clearChatWindow}> X </button>
              <span className="chat-title">BV CHATBOT</span>
              <img src={require('./image.jpg')} alt="User" className="user-avatar" />
           </div>
           <div className="blur-background">
             <img src={require('./images.png')} alt="Background" className="blur-image" />
           </div>
           <div className="message-container" ref={(ref) => {this.messageContainer = ref; }}>
            {this.state.sentMessages.map((message, index) => (
              <div key={index} className="message">{message}</div>
            ))}
          </div>
          {/* <div className="messages" ref={this.messageContainer}>
              {this.state.sentMessages.map((message, index) => (
                <div key={index} className="message">{message}</div>
              ))}
            </div> */}
            <div className="buttons-container">
             {Object.values(this.state.buttonMessages).map((buttonMessage, index) => (
              <div key={index} className="button-box" onClick={() => this.handleButtonClick(buttonMessage)}>{buttonMessage}</div>
            ))}
            </div>
            <div className="input-box">
            <input
            type="text"
            placeholder="Type your message..."
            value={this.state.message}
            onChange={(e) => this.setState({ message: e.target.value })}
            onKeyDown={this.handleKeyDown} 
            />
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default App;
