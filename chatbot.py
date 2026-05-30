import random
import spacy
import nltk
import unidecode
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

nlp = spacy.load('en_core_web_sm')
nltk.download('punkt_tab')

knowledge_basis = [
    "Jesus Christ is the Son of God and the Savior of humanity.",
    "Jesus was born in Bethlehem and lived in Nazareth.",
    "The Bible is the inspired Word of God.",
    "The Old Testament contains the history of Israel.",
    "The New Testament focuses on the life and teachings of Jesus Christ.",
    "Salvation is received through faith in Jesus Christ.",
    "The Gospel means good news.",
    "Prayer is communication with God.",
    "Christians believe that Jesus died on the cross for the forgiveness of sins.",
    "Jesus rose from the dead on the third day.",
    "The Holy Spirit guides believers in their spiritual lives.",
    "God is eternal, holy, and all-powerful.",
    "The doctrine of the Trinity teaches that God is Father, Son, and Holy Spirit.",
    "The church is the community of believers in Christ.",
    "Baptism is an important Christian practice.",
    "The Lord's Supper commemorates the sacrifice of Jesus.",
    "Faith is trusting in God's promises.",
    "Grace is God's undeserved favor toward humanity.",
    "Sin separates humanity from God.",
    "Repentance involves turning away from sin and turning toward God.",
    "The Ten Commandments were given to Moses.",
    "Abraham is considered the father of faith.",
    "Moses led the Israelites out of Egypt.",
    "David was the king of Israel and defeated Goliath.",
    "Solomon was known for his wisdom.",
    "The Psalms contain songs and prayers.",
    "The book of Proverbs contains wisdom teachings.",
    "Isaiah was a major prophet in the Old Testament.",
    "John the Baptist prepared the way for Jesus.",
    "The apostle Paul wrote many letters in the New Testament.",
    "Peter was one of the twelve disciples of Jesus.",
    "The Great Commission instructs Christians to make disciples of all nations.",
    "The kingdom of God is a central theme in the teachings of Jesus.",
    "The resurrection of Jesus is central to Christian belief.",
    "Love God and love your neighbor are two of the greatest commandments.",
    "The Bible teaches forgiveness and reconciliation.",
    "Christians believe in eternal life through Jesus Christ.",
    "The book of Revelation speaks about the final victory of God.",
    "The fruit of the Spirit includes love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control.",
    "The Sermon on the Mount contains important teachings of Jesus.",
    "The parable of the Good Samaritan teaches compassion.",
    "The parable of the Prodigal Son teaches forgiveness and grace.",
    "God created the heavens and the earth.",
    "The first book of the Bible is Genesis.",
    "The last book of the Bible is Revelation.",
    "Christianity teaches that God is both just and merciful.",
    "The cross symbolizes the sacrifice of Jesus Christ.",
    "The empty tomb symbolizes the resurrection of Jesus.",
    "The mission of the church is to worship God and proclaim the Gospel.",
    "Jesus taught his followers to pray and trust in God."
]

sentiment_analyzer = SentimentIntensityAnalyzer()

def detect_sentiment(text):
    score = sentiment_analyzer.polarity_scores(text)

    compound = score["compound"]

    if compound >= 0.05:
        return "positive"

    if compound <= -0.05:
        return "negative"

    return "neutral"

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text():
    text = " ".join(
        knowledge_basis[:5]
    )

    summary = summarizer(
        text,
        min_length=20,
        max_length=80,
        do_sample=False
    )

    chat_area.insert(
        tk.END,
        "Summary: "
        + summary[0]["summary_text"]
        + "\n\n"
    )

user_greetings = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon"
]

bot_greetings = [
    "Hello!",
    "Hi!",
    "Welcome!",
    "Nice to meet you!"
]

def greeting(text):
    for word in text.split():
        if word.lower() in user_greetings:
            return random.choice(bot_greetings)

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
        and not token.like_num
    ]
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
        return "Sorry, I could not find an answer. Could you rephrase your question?"

    return knowledge_basis[index]

def send_message():
    user_input = entry.get()

    if user_input.strip() == "":
        return

    chat_area.insert(tk.END, "You: " + user_input + "\n")

    answer_greeting = greeting(user_input)

    if answer_greeting:
        answer = answer_greeting
    else:
        mood = detect_sentiment(user_input)

        answer = generate_response(user_input)

        if mood == "positive":
            answer = (
                "I'm glad to hear that. "
                + answer
            )

        elif mood == "negative":
            answer = (
                "I'm sorry you're feeling this way. "
                + answer
            )

    chat_area.insert(tk.END, "Theo: " + answer + "\n\n")

    entry.delete(0, tk.END)

# =========================
# JANELA PRINCIPAL
# =========================

window = tk.Tk()
window.title("Theo - Your Theological Chatbot")
window.geometry("950x700")
window.configure(bg="#1E1E2E")

# =========================
# CABEÇALHO
# =========================

header = tk.Frame(
    window,
    bg="#111827",
    height=90
)

header.pack(fill="x")

title = tk.Label(
    header,
    text="Theo",
    font=("Segoe UI", 26, "bold"),
    fg="white",
    bg="#111827"
)

title.pack(pady=(12, 0))

subtitle = tk.Label(
    header,
    text="Your Theological Chatbot",
    font=("Segoe UI", 11),
    fg="#9CA3AF",
    bg="#111827"
)

subtitle.pack()

# =========================
# CHAT
# =========================

chat_frame = tk.Frame(
    window,
    bg="#1E1E2E"
)

chat_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

chat_area = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="#27293D",
    fg="white",
    insertbackground="white",
    relief="flat",
    padx=15,
    pady=15
)

chat_area.pack(
    fill="both",
    expand=True
)

chat_area.tag_config(
    "user",
    foreground="#60A5FA"
)

chat_area.tag_config(
    "bot",
    foreground="#34D399"
)

chat_area.insert(
    tk.END,
    "Theo: Hello! Ask me anything about theology.\n\n",
    "bot"
)

# =========================
# ÁREA INFERIOR
# =========================

bottom_frame = tk.Frame(
    window,
    bg="#1E1E2E"
)

bottom_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

entry = tk.Entry(
    bottom_frame,
    font=("Segoe UI", 12),
    bg="#27293D",
    fg="white",
    insertbackground="white",
    relief="flat"
)

entry.pack(
    side=tk.LEFT,
    fill="x",
    expand=True,
    ipady=12,
    padx=(0, 10)
)

# =========================
# BOTÃO RESUMO
# =========================

summary_button = tk.Button(
    bottom_frame,
    text="📄 Summary",
    command=summarize_text,
    font=("Segoe UI", 10, "bold"),
    bg="#F59E0B",
    fg="white",
    relief="flat",
    padx=15
)

summary_button.pack(
    side=tk.LEFT,
    padx=(0, 10)
)

# =========================
# BOTÃO ENVIAR
# =========================

send_button = tk.Button(
    bottom_frame,
    text="➤ Send",
    command=send_message,
    font=("Segoe UI", 10, "bold"),
    bg="#2563EB",
    fg="white",
    relief="flat",
    padx=20
)

send_button.pack(side=tk.LEFT)

# =========================
# ENTER
# =========================

window.bind(
    "<Return>",
    lambda event: send_message()
)

window.mainloop()