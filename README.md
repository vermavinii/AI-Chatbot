# AI-Chatbot

Welcome to the AI-Chatbot project! 

The AI-Chatbot is designed to provide intelligent and context-aware responses to user inputs. It leverages machine learning algorithms and natural language processing to understand and respond to user queries.

## Features

- Intelligent and context-aware responses
- User-friendly web interface
- Integration with various data sources
- Voice response functionality

## Pre-requisites

- Pycharm
- Python
- Node.js
- npm (Node Package Manager)
- MongoDB

## Softwares Required:
- IDE: Pycharm or VsCode

#### Frontend:
- React [version-20.12.1]

#### Backend:
- Python [version-3.11]
- MongoDBCompass [version-7.0.5]

## Installation

To get started with the AI-Chatbot, follow these steps:

1. Clone the repository:
   
   ```bash
   git clone https://github.com/vermavinii/AI-Chatbot.git

2. Navigate to the project directory:

   ```bash
   cd AI-Chatbot

3. Install the required libraries:
   
   ```bash
   pip install os pyyaml pymongo flask chatterbot chatterbot.trainers requests BeautifulSoup4 nltk scipy flask_cors sentence-transformers
   
4. Configure data file paths:

   Make sure to change the paths of the data files in the project to your local paths. This can typically be done within the code where data files are loaded.
    
5. Set up MongoDB:

   - Install MongoDB from the official website.  
   - Open MongoDB and create a server.  
   - Change the name and path to your MongoDB server in the configuration file.  
   - Run the MongoDB server to allow conversations to be saved.  

6. This project contains the Python(backend) and the React(frontend) as Frameworks. Follow the steps below to set up and run the project locally.

   - Open the terminal and run the Python development server i.e. app.py
     
   - Open another terminal and launch the Node by the following commands:
     
       ```bash
		   npm run start

 This way you get reponses from the chatbot. Feel free to modify the code as per you need.
