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
    text = highlight(df.paragraph[i],df.answer[i])
    return render_template_string(template, i=i, paragraph=text, question=df.question[i], answer=df.answer[i])

def highlight(text, answer):
    try:
        start = text.index(answer)
    except ValueError:
        print("Answer not found in text!")
        return text
    end = start + len(answer)
    text = f"{text[:start]}<b>{text[start:end]}</b>{text[end:]}"
    return text
