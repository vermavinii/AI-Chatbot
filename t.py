from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['data']  # Choose or create a database
collection = db['chats']  # Choose or create a collection

bot = ChatBot('ChatBot')
trainer = ListTrainer(bot)

# Train the chatbot with data
for file in os.listdir('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data'):
    chats = open('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data\\' + file, 'r').readlines()
    chats = [chat.lower() for chat in chats]
    trainer.train(chats)


@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    # Get user's message
    message = str(request.form['messageText'])

    # Get chatbot's response
    bot_response = bot.get_response(message)

    # Insert conversation into MongoDB collection
    conversation_entry = {
        'user_message': message,
        'bot_response': str(bot_response)
    }
    try:
        collection.insert_one(conversation_entry)
    except Exception as e:
        print("Error inserting conversation into MongoDB:", e)

    # Check chatbot's confidence
    if bot_response.confidence > 0.1:
        return jsonify({'status': 'OK', 'answer': str(bot_response)})
    elif message == "bye":
        return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
    else:
        try:
            url = "https://en.wikipedia.org/wiki/" + message
            page = get(url).text
            soup = BeautifulSoup(page, "html.parser")
            p = soup.find_all("p")
            return jsonify({'status': 'OK', 'answer': p[1].text})

        except IndexError as error:
            return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})


if __name__ == "__main__":
    app.run()



