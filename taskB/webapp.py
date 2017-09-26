from flask import Flask, render_template_string
app = Flask(__name__)

import pandas as pd
df = pd.read_csv('../train_task_b.csv')
from random import randint

template = """
<html>
<head>
    <title>Вопрос {{ i }} | Задача B</title>
</head>
<body>
    {% autoescape false %}
    <p>{{ paragraph }}</p>
    {% endautoescape %}
    <hr>
    <p>{{ question }}</p>
    <hr>
    <p>{{ answer }}</p>
</body>
"""

@app.route("/")
def taskB():
    i = randint(0, len(df))
    answer = df.answer[i].lower().strip(' ').strip('.')
    question = df.question[i].strip(' ').strip('?')
    text = highlight(df.paragraph[i], question, answer)
    return render_template_string(template, i=i, paragraph=text, question=df.question[i], answer=answer)

def find_sent_end(text, pos):
    for i in range(pos+1, len(text)):
        if text[i-1:i+1] == '. ' and text[i+1].isupper():
            return i
    # reach end of text
    return len(text)-1

def find_sent_start(text, pos):
    for i in range(pos-1, 0, -1):
        if text[i-1:i+1] == '. ' and text[i+1].isupper():
            return i
    # reach start of text
    return 0

def highlight(text, question, answer):
    try:
        answer_pos = text.lower().index(answer.lower())
    except ValueError:
        print("Answer not found in text!")
        return text
    sent_start = find_sent_start(text, answer_pos)
    sent_end = find_sent_end(text, answer_pos)
    sent = text[sent_start:sent_end]
    answer_pos_in_sent = answer_pos - sent_start
    sent = f"{sent[:answer_pos_in_sent]}<b>{answer}</b>{sent[answer_pos_in_sent+len(answer):]}"
    q_words = question.split(' ')
    for w in q_words:
        try:
            i = sent.index(w)
            j = i+len(w)
            sent = f"{sent[:i]}<span style='color:red'>{w}</span>{sent[j:]}"
        except ValueError:
            pass
    text = f"{text[:sent_start]}<span style='background-color:yellow'>{sent}</span>{text[sent_end:]}"
    return text

if __name__=='__main__':
    app.run(port=5000, debug=True)
