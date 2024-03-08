# from pymongo import MongoClient
# from flask import Flask, request, render_template, jsonify
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# from requests import get
# from bs4 import BeautifulSoup
# import os
# from fuzzywuzzy import process
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from scipy.spatial.distance import cosine
#
# app = Flask(__name__)
#
# # Initialize the MongoDB client globally
# client = MongoClient('mongodb://localhost:27017')
# db = client['data']  # Choose or create a database
# collection = db['conversations']  # Choose or create a collection
#
# # Initialize the ChatBot
# bot = ChatBot('ChatBot')
# trainer = ListTrainer(bot)
#
# # Train the chatbot with data
# for file in os.listdir('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data'):
#     chats = open('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data\\' + file, 'r').readlines()
#     chats = [chat.lower() for chat in chats]
#     trainer.train(chats)
#
# # Load a pre-trained sentence transformer model
# model = SentenceTransformer('paraphrase-distilroberta-base-v1')
#
# THRESHOLD_SIMILARITY = 0.7  # Adjust threshold as needed
#
#
# def preprocess_text(text):
#     # Convert text to lowercase
#     text = text.lower()
#     # Tokenize the text
#     tokens = word_tokenize(text)
#     # Remove stopwords
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words]
#     # Join tokens back into a string
#     preprocessed_text = ' '.join(tokens)
#     return preprocessed_text
#
#
# def calculate_similarity(question1, question2):
#     embeddings = model.encode([question1, question2])
#     return 1 - cosine(embeddings[0], embeddings[1])
#
#
# def search_database(user_question):
#     conversation = collection.find_one({'question': user_question})
#     if conversation:
#         return conversation['answer']
#     return None
#
#
# def get_most_similar_question(user_question, questions):
#     max_similarity = 0
#     most_similar_question = None
#
#     for question in questions:
#         similarity = calculate_similarity(user_question, question)
#         if similarity > max_similarity:
#             max_similarity = similarity
#             most_similar_question = question
#
#     return most_similar_question, max_similarity
#
#
# @app.route("/")
# def hello():
#     return render_template('chat.html')
#
#
# @app.route("/ask", methods=['POST'])
# def ask():
#     # Get user's message
#     message = str(request.form['messageText'])
#
#     # Preprocess user's message
#     processed_message = preprocess_text(message)
#
#     # Search in the database
#     database_answer = search_database(processed_message)
#     if database_answer:
#         return jsonify({'status': 'OK', 'answer': database_answer})
#
#     # Search in the dataset
#     similar_questions = collection.distinct('question')
#     most_similar_question, similarity_score = get_most_similar_question(processed_message, similar_questions)
#     if similarity_score > THRESHOLD_SIMILARITY:
#         similar_answer = collection.find_one({'question': most_similar_question})['answer']
#         return jsonify({'status': 'OK', 'answer': similar_answer})
#
#     # Get chatbot's response
#     bot_response = bot.get_response(message)
#
#     # Insert conversation into MongoDB collection
#     conversation_entry = {
#         'question': processed_message,
#         'answer': str(bot_response)
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
#         try:
#             url = "https://en.wikipedia.org/wiki/" + message
#             page = get(url).text
#             soup = BeautifulSoup(page, "html.parser")
#             p = soup.find_all("p")
#             return jsonify({'status': 'OK', 'answer': p[1].text})
#
#         except IndexError as error:
#             return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})
#
#
# if __name__ == "__main__":
#     app.run()

from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from fuzzywuzzy import process
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import cosine
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Initialize the MongoDB client globally
client = MongoClient('mongodb://localhost:27017/')
db = client['Chatbot']  # Choose or create a database
collection = db['convo']  # Choose or create a collection

# Initialize the ChatBot
bot = ChatBot('ChatBot')
trainer = ListTrainer(bot)

# Train the chatbot with data
for file in os.listdir('E:\\a\\chatt\\data'):
    chats = open('E:\\a\\chatt\\data\\' + file, 'r').readlines()
    chats = [chat.lower() for chat in chats]
    trainer.train(chats)

# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-distilroberta-base-v1')

THRESHOLD_SIMILARITY = 0.7  # Adjust threshold as needed


def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text


def calculate_similarity(question1, question2):
    embeddings = model.encode([question1, question2])
    return 1 - cosine(embeddings[0], embeddings[1])


def search_database(user_question):
    conversation = collection.find_one({'question': user_question})
    if conversation:
        return conversation['answer']
    return None


def get_most_similar_question(user_question, questions):
    max_similarity = 0
    most_similar_question = None

    for question in questions:
        similarity = calculate_similarity(user_question, question)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = question

    return most_similar_question, max_similarity



@app.route("/ask", methods=['POST'])
def ask():
    # Get user's message
    message = request.json['message']

    # Preprocess user's message
    processed_message = preprocess_text(message)

    # Search in the database
    database_answer = search_database(processed_message)
    if database_answer:
        return jsonify({'status': 'OK', 'answer': database_answer})

    # Search in the dataset
    similar_questions = collection.distinct('question')
    most_similar_question, similarity_score = get_most_similar_question(processed_message, similar_questions)
    if similarity_score > THRESHOLD_SIMILARITY:
        similar_answer = collection.find_one({'question': most_similar_question})['answer']
        return jsonify({'status': 'OK', 'answer': similar_answer})

    # Get chatbot's response
    bot_response = bot.get_response(message)

    # Insert conversation into MongoDB collection
    conversation_entry = {
        'question': processed_message,
        'answer': str(bot_response)
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
    app.run(debug=True)
