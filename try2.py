from pymongo import MongoClient
from flask import Flask, request, render_template, g, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import _app_ctx_stack
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Initialize the MongoDB client globally
client = MongoClient('mongodb://localhost:27017')
db = client['data']  # Choose or create a database
collection = db['conversations']  # Choose or create a collection

# Initialize the ChatBot
bot = ChatBot('ChatBot')
trainer = ListTrainer(bot)

# Train the chatbot with data
for file in os.listdir('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data'):
    chats = open('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data\\' + file, 'r').readlines()
    chats = [chat.lower() for chat in chats]
    trainer.train(chats)

THRESHOLD_SIMILARITY = 10
def get_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_tokens = [w.lower() for w in word_tokens if w.isalnum() and w.lower() not in stop_words]
    return filtered_tokens
def get_most_similar_question(user_question, questions):
    max_similarity = 0
    most_similar_question = None

    for question in questions:
        similarity = fuzz.ratio(user_question.lower(), question.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = question

    return most_similar_question


@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
# def ask():
#     # Get user's message
#     message = str(request.form['messageText'])
#
#     # Search for the question in the database
#     conversation = collection.find_one({'question': message})
#     if conversation:
#         # If the exact question exists in the database, respond with the corresponding answer
#         return jsonify({'status': 'OK', 'answer': conversation['answer']})
#     else:
#         # Search for similar questions in the dataset
#         similar_question = get_most_similar_question(message, collection.distinct('question'))
#
#         if similar_question:
#             similar_answer = collection.find_one({'question': similar_question})['answer']
#             return jsonify({'status': 'OK', 'answer': similar_answer})
#         else:
#             # Get chatbot's response
#             bot_response = bot.get_response(message)
#
#             # Insert conversation into MongoDB collection
#             conversation_entry = {
#                 'question': message,
#                 'answer': str(bot_response)
#             }
#             try:
#                 collection.insert_one(conversation_entry)
#             except Exception as e:
#                 print("Error inserting conversation into MongoDB:", e)
#
#             # Check chatbot's confidence
#             if bot_response.confidence > 0.1:
#                 return jsonify({'status': 'OK', 'answer': str(bot_response)})
#             elif message == "bye":
#                 return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
#             else:
#                 try:
#                     url = "https://en.wikipedia.org/wiki/" + message
#                     page = get(url).text
#                     soup = BeautifulSoup(page, "html.parser")
#                     p = soup.find_all("p")
#                     return jsonify({'status': 'OK', 'answer': p[1].text})
#
#                 except IndexError as error:
#                     return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})

    # if conversation:
    #     # If the question exists in the database, respond with the corresponding answer
    #     return jsonify({'status': 'OK', 'answer': conversation['answer']})
    # else:
    #     # Get chatbot's response
    #     bot_response = bot.get_response(message)
    #
    #     # Insert conversation into MongoDB collection
    #     conversation_entry = {
    #         'question': message,
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

# def ask():
#     # Get user's message
#     message = str(request.form['messageText'])
#
#     # Search for the question in the database
#     conversation = collection.find_one({'question': message})
#
#     if conversation:
#         # If the exact question exists in the database, respond with the corresponding answer
#         return jsonify({'status': 'OK', 'answer': conversation['answer']})
#     else:
#         # Search for similar questions in the dataset
#         similar_question = get_most_similar_question(message, collection.distinct('question'))
#
#         if similar_question:
#             similar_answer = collection.find_one({'question': similar_question})['answer']
#             return jsonify({'status': 'OK', 'answer': similar_answer})
#         else:
#             # Get chatbot's response
#             bot_response = bot.get_response(message)
#
#             # Insert conversation into MongoDB collection
#             conversation_entry = {
#                 'question': message,
#                 'answer': str(bot_response)
#             }
#             try:
#                 collection.insert_one(conversation_entry)
#             except Exception as e:
#                 print("Error inserting conversation into MongoDB:", e)
#
#             # Check chatbot's confidence
#             if bot_response.confidence > 0.1:
#                 return jsonify({'status': 'OK', 'answer': str(bot_response)})
#             elif message == "bye":
#                 return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
#             else:
#                 try:
#                     url = "https://en.wikipedia.org/wiki/" + message
#                     page = get(url).text
#                     soup = BeautifulSoup(page, "html.parser")
#                     p = soup.find_all("p")
#                     return jsonify({'status': 'OK', 'answer': p[1].text})
#
#                 except IndexError as error:
#                     return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})
def ask():
    # Get user's message
    message = str(request.form['messageText'])

    # Search for the question in the database
    conversation = collection.find_one({'question': message})

    if conversation:
        # If the exact question exists in the database, respond with the corresponding answer
        return jsonify({'status': 'OK', 'answer': conversation['answer']})
    else:
        # Search for similar questions in the dataset
        similar_question = get_most_similar_question(message, collection.distinct('question'))

        if similar_question:
            similar_answer = collection.find_one({'question': similar_question})['answer']
            return jsonify({'status': 'OK', 'answer': similar_answer})
        else:
            # Get chatbot's response
            bot_response = bot.get_response(message)

            # Insert conversation into MongoDB collection
            conversation_entry = {
                'question': message,
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


def teardown_appcontext(exception=None):
    ctx = _app_ctx_stack.top
    if hasattr(ctx, 'sqlalchemy_session'):
        ctx.sqlalchemy_session.close()

if __name__ == "__main__":
    app.run()
