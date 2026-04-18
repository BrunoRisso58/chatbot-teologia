import random
import spacy
import nltk
import unidecode
import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from goose3 import Goose

nlp = spacy.load('pt_core_news_sm')
nltk.download('punkt_tab')

g = Goose()
url = 'https://voltemosaoevangelho.com/blog/2017/04/quem-e-jesus-cristo/'
article = g.extract(url)

knowledge_basis = [sentence for sentence in nltk.sent_tokenize(article.cleaned_text)]

user_greetings = ["oi", "olá", "ola", "eai", "hey"]
bot_greetings = ["Olá!", "Oi!", "Seja bem-vindo!", "E aí!"]

def greeting(text):
    for word in text.split():
        if word.lower() in user_greetings:
            return random.choice(bot_greetings)

def preprocess(text):
    text = unidecode.unidecode(text)
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct and not token.is_space and not token.like_num]
    return " ".join(tokens)

def generate_response(user_input):
    processed_basis = [preprocess(phrase) for phrase in knowledge_basis]
    processed_input = preprocess(user_input)

    processed_basis.append(processed_input)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed_basis)

    similarity = cosine_similarity(vectors[-1], vectors)

    index = similarity.argsort()[0][-2]

    if similarity[0][index] <= 0.2:
        return "Desculpe, não entendi sua pergunta. Pode reformular?"

    return knowledge_basis[index]

def send_message():
    user_input = entry.get()

    if user_input.strip() == "":
        return

    chat_area.insert(tk.END, "Você: " + user_input + "\n")

    answer_greeting = greeting(user_input)

    if answer_greeting:
        answer = answer_greeting
    else:
        answer = generate_response(user_input)

    chat_area.insert(tk.END, "Chatbot: " + answer + "\n\n")

    entry.delete(0, tk.END)

window = tk.Tk()
window.title("Chatbot Teológico")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(window, width=50)
entry.pack(side=tk.LEFT, padx=10, pady=10)

send_button = tk.Button(window, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT)

window.bind('<Return>', lambda event: send_message())

window.mainloop()