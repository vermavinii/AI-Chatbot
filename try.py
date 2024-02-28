from gensim.models import Word2Vec
from gensim import downloader as api
import numpy as np
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['data']  # Choose or create a database
collection = db['chats']  # Choose or create a collection

# bot = ChatBot('ChatBot')
# trainer = ListTrainer(bot)

# Create an empty ListTrainer instance
#
# Create an instance of the ChatBot class
chatbot = ChatBot("MyChatBot")

# Create an instance of the ListTrainer class without passing any additional arguments
trainer = ListTrainer(chatbot)

# Train the chatbot with data
trainer.train(["Hi there!", "Hello!"])



# Train the chatbot with data
for file in os.listdir('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data'):
    chats = open('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data\\' + file, 'r').readlines()
    chats = [chat.lower() for chat in chats]
    trainer.train(chats)


@app.route("/")
def hello():
    return render_template('chat.html')


# Load Word2Vec model
word_vectors = api.load("glove-wiki-gigaword-100")


# Function to calculate semantic similarity between two sentences
def semantic_similarity(sentence1, sentence2):
    tokens1 = sentence1.split()
    tokens2 = sentence2.split()
    vector1 = np.mean([word_vectors[word] for word in tokens1 if word in word_vectors], axis=0)
    vector2 = np.mean([word_vectors[word] for word in tokens2 if word in word_vectors], axis=0)
    if np.all(vector1) and np.all(vector2):
        similarity_score = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        return similarity_score
    else:
        return 0.0  # If any of the vectors is all zeros, return 0 similarity


DEFAULT_THRESHOLD = 0.8


# Modify the ask() function to utilize semantic similarity
@app.route("/ask", methods=['POST'])
# def ask():
#     # Get user's message
#     message = str(request.form['messageText'])
#
#     # Get the threshold from request parameters or use the default value
#     threshold = float(request.form.get('threshold', DEFAULT_THRESHOLD))
#
#     # Get chatbot's response
#     bot_response = bot.get_response(message)
#
#     # Insert conversation into MongoDB collection
#     conversation_entry = {
#         'user_message': message,
#         'bot_response': str(bot_response)
#     }
#     try:
#         collection.insert_one(conversation_entry)
#     except Exception as e:
#         print("Error inserting conversation into MongoDB:", e)
#
#     # Check chatbot's confidence
#     if bot_response.confidence > 0.1:
#         return jsonify({'status': 'OK', 'answer': str(bot_response)})
#     elif message == "bye":
#         return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
#     else:
#         # Find most similar question from training data
#         similar_question = max(trainer.train([]), key=lambda x: semantic_similarity(message, x.text))
#         # Get response corresponding to similar question if similarity score is above the threshold
#         if semantic_similarity(message, similar_question.text) > threshold:
#             return jsonify({'status': 'OK', 'answer': bot.get_response(similar_question.text).text})
#         else:
#             try:
#                 url = "https://en.wikipedia.org/wiki/" + message
#                 page = get(url).text
#                 soup = BeautifulSoup(page, "html.parser")
#                 p = soup.find_all("p")
#                 return jsonify({'status': 'OK', 'answer': p[1].text})
#
#             except IndexError as error:
#                 return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})
#
#
# if __name__ == "__main__":
#     app.run()

def ask():
    # Get user's message
    message = str(request.form['messageText'])

    # Get the threshold from request parameters or use the default value
    threshold = float(request.form.get('threshold', DEFAULT_THRESHOLD))

    # Find most similar question from training data
    similar_question = max(chatbot.storage.filter(), key=lambda x: semantic_similarity(message, x.text))

    # Get response corresponding to similar question if similarity score is above the threshold
    if semantic_similarity(message, similar_question.text) > threshold:
        bot_response = chatbot.get_response(similar_question.text).text
    else:
        try:
            url = "https://en.wikipedia.org/wiki/" + message
            page = get(url).text
            soup = BeautifulSoup(page, "html.parser")
            p = soup.find_all("p")
            bot_response = p[1].text
        except IndexError as error:
            bot_response = 'Sorry, I have no idea about that.'

    # Insert conversation into MongoDB collection
    conversation_entry = {
        'user_message': message,
        'bot_response': str(bot_response)
    }
    try:
        collection.insert_one(conversation_entry)
    except Exception as e:
        print("Error inserting conversation into MongoDB:", e)

    return jsonify({'status': 'OK', 'answer': bot_response})


if __name__ == "__main__":
    app.run()