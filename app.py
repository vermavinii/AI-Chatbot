import os
import yaml
from pymongo import MongoClient
from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Initializing the MongoDB client(connect kar raha hai connection string ko use karke.)
client = MongoClient('mongodb://localhost:27017')
db = client['data']  # Choose or create a database
collection = db['conversations']  # Choose or create a collection

# Initializing the ChatBot
bot = ChatBot('ChatBot')
trainer = ListTrainer(bot)

# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-distilroberta-base-v1')

THRESHOLD_SIMILARITY = 0.7


# yml files/dataset ko load kar raha hai
def load_yaml_data(directory):
    conversations = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.yml'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)
                if isinstance(data, list):
                    for pair in data:
                        if len(pair) == 2:
                            question = pair[0].strip('-').strip()
                            answer = pair[1].strip('-').strip()
                            conversations.append({'question': question, 'answer': answer})
                else:
                    print(f"Invalid YAML data in file: {file_path}")
    return conversations


# Directory containing Banasthali Vidyapith College specific data
banasthali_data_directory = 'C:\\Users\\charu\\PycharmProjects\\flaskProject1\\chatt\\data'
banasthali_conversations = load_yaml_data(banasthali_data_directory)

# Train chatbot with Banasthali Vidyapith College specific dataset
for conversation in banasthali_conversations:
    question = conversation.get('question')
    answer = conversation.get('answer')
    if question and answer:
        trainer.train([question, answer])



# text proccessing
def preprocess_text(text):
    text = text.lower()  # Convert text to lowercase
    tokens = word_tokenize(text)  # Tokenize the text
    stop_words = set(stopwords.words('english'))  # Get English stop words
    tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    return ' '.join(tokens)  # Join tokens back into a string


# similarities check karne ke liye 2 sentences mein
def calculate_similarity(question1, question2):
    embeddings = model.encode([question1, question2])
    return 1 - cosine(embeddings[0], embeddings[1])


# Function to search the database for a user question
def search_database(user_question):
    conversation = collection.find_one({'question': user_question})
    if conversation:
        return conversation['answer']
    return None


# Function to get the most similar question from a list of questions
def get_most_similar_question(user_question, questions):
    max_similarity = 0
    most_similar_question = None

    for question in questions:
        similarity = calculate_similarity(user_question, question)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = question

    return most_similar_question, max_similarity


# Function to handle Wikipedia queries(web scrapping)
def get_wikipedia_answer(query):
    try:
        url = "https://en.wikipedia.org/wiki/" + query
        page = get(url).text
        soup = BeautifulSoup(page, "html.parser")
        p = soup.find_all("p")
        return p[1].text if p else "No information found on Wikipedia."
    except Exception as error:
        return "Error fetching information from Wikipedia: {}".format(str(error))


# Function to search YAML data for a user question
def search_yaml_data(user_question, conversations):
    for conversation in conversations:
        question = conversation.get('question')
        answer = conversation.get('answer')
        if question and answer:
            similarity = calculate_similarity(user_question, preprocess_text(question))
            if similarity > THRESHOLD_SIMILARITY:
                return answer
    return None



@app.route("/ask", methods=['POST'])
def ask():
    message = request.json['message']
    processed_message = preprocess_text(message)

    # Search Banasthali Vidyapith College specific dataset first
    response = search_yaml_data(processed_message, banasthali_conversations)
    if response:
        return jsonify({'status': 'OK', 'answer': response})

    # Search the database
    database_answer = search_database(processed_message)
    if database_answer:
        return jsonify({'status': 'OK', 'answer': database_answer})

    # Chatbot's response
    bot_response = bot.get_response(message)

    # Insert conversation into MongoDB collection
    conversation_entry = {'question': processed_message, 'answer': str(bot_response)}
    try:
        collection.insert_one(conversation_entry)
    except Exception as e:
        print("Error inserting conversation into MongoDB:", e)

    if bot_response.confidence > 0.1:
        return jsonify({'status': 'OK', 'answer': str(bot_response)})
    elif message == "bye":
        return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
    else:
        wikipedia_answer = get_wikipedia_answer(processed_message)
        return jsonify({'status': 'OK', 'answer': wikipedia_answer})

if __name__ == "__main__":
    app.run(debug=True)








































# import os
# import yaml
# from pymongo import MongoClient
# from flask import Flask, request, jsonify
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# from requests import get
# from bs4 import BeautifulSoup
# from sentence_transformers import SentenceTransformer
# from scipy.spatial.distance import cosine
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)
#
# # Initializing the MongoDB client
# client = MongoClient('mongodb://localhost:27017')
# db = client['data']
# collection = db['conversations']
#
# # Initializing the ChatBot
# bot = ChatBot('ChatBot')
# trainer = ListTrainer(bot)
#
# # Load a pre-trained sentence transformer model
# model = SentenceTransformer('paraphrase-distilroberta-base-v1')
# # yml files/dataset ko load kar raha hai
# def load_yaml_data(directory):
#     conversations = []
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.yml'):
#             file_path = os.path.join(directory, file_name)
#             with open(file_path, 'r') as yaml_file:
#                 data = yaml.safe_load(yaml_file)
#                 if isinstance(data, list):
#                     for pair in data:
#                         if len(pair) == 2:
#                             question = pair[0].strip('-').strip()
#                             answer = pair[1].strip('-').strip()
#                             conversations.append({'question': question, 'answer': answer})
#                 else:
#                     print(f"Invalid YAML data in file: {file_path}")
#     return conversations
# # Directory containing Banasthali Vidyapith College specific data
# banasthali_data_directory = 'C:\\Users\\charu\\PycharmProjects\\flaskProject1\\chatt\\data'
# banasthali_conversations = load_yaml_data(banasthali_data_directory)
# banasthali_questions = [conversation['question'] for conversation in banasthali_conversations]
#
# # Train chatbot with Banasthali Vidyapith College specific dataset
# for conversation in banasthali_conversations:
#     question = conversation.get('question')
#     answer = conversation.get('answer')
#     if question and answer:
#         trainer.train([question, answer])
#
# # Function to preprocess text
# def preprocess_text(text):
#     # Add your text preprocessing logic here
#     return text.lower()
#
# # Function to calculate similarity between two sentences
# def calculate_similarity(question1, question2):
#     embeddings = model.encode([question1, question2])
#     return 1 - cosine(embeddings[0], embeddings[1])
#
# # Function to search Banasthali dataset for a user question
# def search_banasthali_dataset(user_question):
#     similarities = [calculate_similarity(user_question, preprocess_text(question)) for question in banasthali_questions]
#     max_similarity = max(similarities)
#     threshold_similarity = max_similarity * 0.7  # Set threshold to 70% of max similarity
#     most_similar_index = similarities.index(max_similarity)
#     if max_similarity >= threshold_similarity:
#         return banasthali_conversations[most_similar_index]['answer']
#     return None
# # Function to search Banasthali dataset for a user question
#
# # Function to search the database for a user question
# def search_database(user_question):
#     conversation = collection.find_one({'question': user_question})
#     if conversation:
#         return conversation['answer']
#     return None
#
# # Function to handle Wikipedia queries (web scraping)
# def get_wikipedia_answer(query):
#     try:
#         url = "https://en.wikipedia.org/wiki/" + query
#         page = get(url).text
#         soup = BeautifulSoup(page, "html.parser")
#         p = soup.find_all("p")
#         return p[1].text if p else "No information found on Wikipedia."
#     except Exception as error:
#         return "Error fetching information from Wikipedia: {}".format(str(error))
#
# @app.route("/ask", methods=['POST'])
# def ask():
#     message = request.json['message']
#
#     # Search Banasthali Vidyapith College specific dataset first
#     banasthali_response = search_banasthali_dataset(message)
#     if banasthali_response:
#         return jsonify({'status': 'OK', 'answer': banasthali_response})
#
#     # Search the database
#     database_answer = search_database(message)
#     if database_answer:
#         return jsonify({'status': 'OK', 'answer': database_answer})
#
#     # Chatbot's response
#     bot_response = bot.get_response(message)
#
#     # Insert conversation into MongoDB collection
#     conversation_entry = {'question': message, 'answer': str(bot_response)}
#     try:
#         collection.insert_one(conversation_entry)
#     except Exception as e:
#         print("Error inserting conversation into MongoDB:", e)
#
#     return jsonify({'status': 'OK', 'answer': str(bot_response)})
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
#
#
#
#
#
#
#
#
#
#
#
#
# # import os
# # import yaml
# # from pymongo import MongoClient
# # from flask import Flask, request, jsonify
# # from chatterbot import ChatBot
# # from chatterbot.trainers import ListTrainer
# # from requests import get
# # from bs4 import BeautifulSoup
# # from nltk.corpus import stopwords
# # from nltk.tokenize import word_tokenize
# # from sentence_transformers import SentenceTransformer
# # from scipy.spatial.distance import cosine
# # from flask_cors import CORS
# import requests
# import openai
#
# # charu-735
# app = Flask(__name__)
# CORS(app)
#
# # Initializing the MongoDB client
# client = MongoClient('mongodb://localhost:27017')
# db = client['data']
# collection = db['conversations']
#
# # Initializing the ChatBot
# bot = ChatBot('ChatBot')
# trainer = ListTrainer(bot)
#
# # Load a pre-trained sentence transformer model
# model = SentenceTransformer('paraphrase-distilroberta-base-v1')
#
# THRESHOLD_SIMILARITY = 0.7
#
#
# # Load Banasthali Vidyapith College specific dataset
# def load_banasthali_data(directory):
#     banasthali_conversations = []
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.yml'):
#             file_path = os.path.join(directory, file_name)
#             with open(file_path, 'r') as yaml_file:
#                 data = yaml.safe_load(yaml_file)
#                 if isinstance(data, list):
#                     for pair in data:
#                         if len(pair) == 2:
#                             question = pair[0].strip('-').strip()
#                             answer = pair[1].strip('-').strip()
#                             banasthali_conversations.append({'question': question, 'answer': answer})
#                 else:
#                     print(f"Invalid YAML data in file: {file_path}")
#     return banasthali_conversations
#
#
# # Directory containing Banasthali Vidyapith College specific data
# banasthali_data_directory = 'C:\\Users\\charu\\PycharmProjects\\flaskProject1\\chatt\\data'
# banasthali_conversations = load_banasthali_data(banasthali_data_directory)
#
# # Train chatbot with Banasthali Vidyapith College specific dataset
# for conversation in banasthali_conversations:
#     question = conversation.get('question')
#     answer = conversation.get('answer')
#     if question and answer:
#         trainer.train([question, answer])
#
#
# # Text processing
# def preprocess_text(text):
#     text = text.lower()  # Convert text to lowercase
#     tokens = word_tokenize(text)  # Tokenize the text
#     stop_words = set(stopwords.words('english'))  # Get English stop words
#     tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
#     return ' '.join(tokens)  # Join tokens back into a string
#
#
# # Similarity calculation between two questions
# def calculate_similarity(question1, question2):
#     embeddings = model.encode([question1, question2])
#     return 1 - cosine(embeddings[0], embeddings[1])
#
#
# # Function to search the database for a user question
# def search_database(user_question):
#     conversation = collection.find_one({'question': user_question})
#     if conversation:
#         return conversation['answer']
#     return None
#
#
# # Function to search YAML data for a user question
# def search_yaml_data(user_question, conversations):
#     for conversation in conversations:
#         question = conversation.get('question')
#         answer = conversation.get('answer')
#         if question and answer:
#             similarity = calculate_similarity(user_question, preprocess_text(question))
#             if similarity > THRESHOLD_SIMILARITY:
#                 return answer
#     return None
#
#
# openai.api_key = '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'
#
#
# # Function to perform web search
# def perform_web_search(query):
#     def perform_web_search(query):
#         response = openai.Completion.create(
#             engine="davinci",
#             prompt="I want to learn about " + query + ".",
#             max_tokens=150,
#             n=1,
#             stop=None
#         )
#         return response.choices[0].text.strip()
#
#
# # Route to handle user queries
# # @app.route("/ask", methods=['POST'])
# # def ask():
# #     message = request.json['message']
# #     processed_message = preprocess_text(message)
# #
# #     # Search Banasthali Vidyapith College specific dataset first
# #     response = search_yaml_data(processed_message, banasthali_conversations)
# #     if response:
# #         return jsonify({'status': 'OK', 'answer': response})
# #
# #     # Search the database
# #     database_answer = search_database(processed_message)
# #     if database_answer:
# #         return jsonify({'status': 'OK', 'answer': database_answer})
# #
# #     # Perform web search
# #     web_search_answer = perform_web_search(processed_message)
# #     if web_search_answer:
# #         return jsonify({'status': 'OK', 'answer': web_search_answer})
# #
# #     # Chatbot's response
# #     bot_response = bot.get_response(message)
# #
# #     # Insert conversation into MongoDB collection
# #     conversation_entry = {'question': processed_message, 'answer': str(bot_response)}
# #     try:
# #         collection.insert_one(conversation_entry)
# #     except Exception as e:
# #         print("Error inserting conversation into MongoDB:", e)
# #
# #     if bot_response.confidence > 0.1:
# #         return jsonify({'status': 'OK', 'answer': str(bot_response)})
# #     elif message == "bye":
# #         return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
# #     else:
# #         return jsonify({'status': 'OK', 'answer': 'Sorry, I could not find an answer.'})
#
# @app.route("/ask", methods=['POST'])
# def ask():
#     message = request.json['message']
#     processed_message = preprocess_text(message)
#
#     # Search Banasthali Vidyapith College specific dataset first
#     response = search_yaml_data(processed_message, banasthali_conversations)
#     if response:
#         return jsonify({'status': 'OK', 'answer': response})
#
#     # Search the database
#     database_answer = search_database(processed_message)
#     if database_answer:
#         return jsonify({'status': 'OK', 'answer': database_answer})
#
#     # Perform web search using GPT-3 API
#     web_search_answer = perform_web_search(processed_message)
#     if web_search_answer:
#         return jsonify({'status': 'OK', 'answer': web_search_answer})
#
#     # Chatbot's response
#     bot_response = bot.get_response(message)
#
#     # Insert conversation into MongoDB collection
#     conversation_entry = {'question': processed_message, 'answer': str(bot_response)}
#     try:
#         collection.insert_one(conversation_entry)
#     except Exception as e:
#         print("Error inserting conversation into MongoDB:", e)
#
#     if bot_response.confidence > 0.1:
#         return jsonify({'status': 'OK', 'answer': str(bot_response)})
#     elif message == "bye":
#         return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
#     else:
#         return jsonify({'status': 'OK', 'answer': 'Sorry, I could not find an answer.'})
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
