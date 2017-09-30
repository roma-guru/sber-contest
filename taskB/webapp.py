from flask import Flask, render_template_string
app = Flask(__name__)

import nltk
import pandas as pd
df = pd.read_csv('../train_task_b.csv')
from random import randint
from pymorphy2.analyzer import MorphAnalyzer
morph = MorphAnalyzer()

template = """
<html>
<head>
    <title>Вопрос {{ i }} | Задача B</title>
    <style>
        body {
            color: #ddd;
            background-color: #222;
        }
        .quest-word {
            color: red;
        }
        .answer-sent {
            background-color: yellow;
            color: grey;
        }
    </style>
</head>
<body>
    {% autoescape false %}
    <p>{{ paragraph }}</p>
    {% endautoescape %}
    <hr>
    <p>{{ question }}</p>
    <hr>
    <p><b>{{ answer }}</b></p>
</body>
"""

@app.route("/")
def taskB():
    i = randint(0, len(df))
    answer = df.answer[i].lower().strip(' ').strip('.')
    question = df.question[i].strip(' ').strip('?')
    text = highlight(df.paragraph[i], question, answer)
    return render_template_string(template, i=i, paragraph=text, question=df.question[i], answer=answer)

def wrap_tag(text, word, open_tag, close_tag):
    return text.replace(word, '{1}{0}{2}'.format(word, open_tag, close_tag))

def highlight(text, question, answer):
    try:
        answer = answer.lower()
        sentences = nltk.sent_tokenize(text)
        sent = next(filter(lambda s: answer in s.lower(), sentences))
    except StopIteration:
        print("Answer not found in text! This means error in sentence tokenizer")
        return text

    orig = sent
    sent = sent.lower()
    # TODO:here morphy
    sent = wrap_tag(sent, answer, '<b>', '</b>')
    q_words = nltk.wordpunct_tokenize(question)
    for w in q_words:
        if len(w)<3: continue
        sent = wrap_tag(sent, w, '<span class=\'quest-word\'>', '</span>')
    sent = '<span class=\'answer-sent\'>{}</span>'.format(sent)
    text = text.replace(orig, sent)
    return text

if __name__=='__main__':
    app.run(port=5000, debug=True)
