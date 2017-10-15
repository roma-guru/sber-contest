import sys, os, time
from flask import Flask, render_template_string, request
app = Flask(__name__)

import nltk
import pandas as pd
df = pd.read_csv('../train_task_b.csv')
from random import randint

from pymorphy2.analyzer import MorphAnalyzer
from russian_tagsets import converters
m = MorphAnalyzer()

class MaltParser:
    """
    Обертка для парсера.
    """
    def __init__(self, parser_jarname, model_filename, pymorphy_analyzer=None):
        """
        Конструктор. Принимает:
        - путь к джарнику
        - имя натренированной модели (без расширения)
        - объект анализатора pymorphy2 (ради экономии памяти)
        """
        self.parser_jarname = parser_jarname
        self.model_filename = model_filename
        if not pymorphy_analyzer:
            pymorphy_analyzer = MorphAnalyzer()
        self.pymorphy_analyzer = pymorphy_analyzer
        # конвертатор из формата OpenCorpora в Universal Dependencies
        self.oc2ud = converters.converter('opencorpora-int', 'ud20')

    def text_to_conllu(self, txt):
        """
        Преобразование текста в формат CONLLU.
        """
        sents = nltk.sent_tokenize(txt)
        out_text = []
        m = self.pymorphy_analyzer
        for i,s in enumerate(sents):
            s = s.replace('\\n', '')
            tokens = nltk.word_tokenize(s)
            # заголовок предложения
            out_text.append("\n# sent: {}".format(i))
            out_text.append("# text: {}".format(s))
            for j,t in enumerate(tokens):
                # парсинг pymorphy
                t = m.parse(t)[0]
                # перевод в формат ud
                pos, feats = self.oc2ud(str(t.tag)).split(' ')
                out_text.append("{0}\t{1}\t{2}\t{3}\t_\t{4}\t_\t_\t_\t".format(
                    j+1, t.word, t.normal_form, pos, feats))
        # удаление лишнего переноса в начале
        return '\n'.join(out_text)[1:]

    def process_output(self, lines):
        """
        Обработка вывода парсера.
        Возвращает список списков словарей со св-ми токенов.
        """
        # накопитель предложений
        res = []
        # накопитель токенов предложения
        curr_sent = []
        for i, l in enumerate(lines):
            l = l.strip()
            if not l:
                # начало след предл
                if curr_sent:
                    res.append(curr_sent)
                curr_sent = []
            elif l.startswith('#'):
                # коммент
                continue
            else:
                # токен предложения
                c = {}
                c['id'], c['token'], c['norm_form'], \
                    c['pos'], _, c['feats'], c['par'], c['deprel'], _, _ = l.split('\t')
                curr_sent.append(c)
        # Нужно добавить посл пр-е если его нет еще
        if len(curr_sent) and (len(res)==0 or res[-1] != curr_sent):
            res.append(curr_sent)
        return res

    def parse(self, txt):
        """
        Парсинг предложений.
        """
        text_filename = "param.tmp"
        result_filename = "out.tmp"
        txt_conllu = self.text_to_conllu(txt)
        with open(text_filename, "w") as f_txt:
            f_txt.write(txt_conllu)
        command_to_run = "java -jar {0} -c {1} -i {2} -m parse -o {3}".format(
            self.parser_jarname, self.model_filename, text_filename, result_filename)
        print("Running: {}".format(command_to_run))
        c = os.system(command_to_run)
        if c>0:
            print("Parser return code nonzero: " + c)
            return
        with open(result_filename, "r", encoding="utf8") as f_res:
            result_text = f_res.readlines()
        print("Ready!")
        return self.process_output(result_text)

def to_visjs(sentence):
    """
    Перевод формата списка словарей в формат VisJS.
    Возвращает JSON - узлы + ребра.
    """
    from json import dumps
    edges = []
    nodes = []
    for token_line in sentence:
        id = int(token_line["id"])
        par_id = int(token_line["par"])
        deprel = token_line["deprel"]
        if par_id:
            edges.append({"from": id, "to": par_id, "label": deprel})
        word = token_line["token"]
        pos = token_line["pos"]
        label = "{} ({})".format(word, pos)
        nodes.append({"id": id, "label": label})
    return dumps(nodes, ensure_ascii=False), dumps(edges, ensure_ascii=False)

@app.route("/")
def main():
    """
    Главный url обработчик.
    """
    start = time.perf_counter()
    # Считаем обновления шаблона
    with open('template.html') as f:
        template = f.read()

    # Параметр - id пары текст-вопрос
    i = request.args.get('i')
    if i:
        i = int(i)
    else:
        i = randint(0, len(df))

    text = df.paragraph[i]
    answer = df.answer[i].strip(' ').strip('.')
    question = df.question[i].strip(' ')
    # Найдем предложение с ответом
    answer_sent = find_answer_sent(text, answer)
    parser_result = malt_parser.parse("{} {}".format(answer_sent, question))

    # Подсветим нужные части
    text,question,answer = highlight(text, question, answer_sent, answer)
    # Генерим узлы графа
    q_nodes, q_edges = to_visjs(parser_result[-1])
    s_nodes, s_edges = to_visjs(parser_result[0])

    finish = time.perf_counter()
    ping = round(finish - start, 2)
    return render_template_string(template, i=i, ping=ping,
                                  paragraph=text, question=question,
                                  answer=answer,
                                  nodes2=q_nodes, edges2=q_edges,
                                  nodes1=s_nodes, edges1=s_edges)

def find_answer_sent(text, answer):
    try:
        answer = answer.lower()
        sentences = nltk.sent_tokenize(text)
        sent = next(filter(lambda s: answer in s.lower(), sentences))
        return sent
    except StopIteration:
        print("Answer not found in text! This means error in sentence tokenizer")
        return None

def wrap_tag(text, word, open_tag, close_tag):
    """
    Обертка текста в теги.
    """
    return text.replace(word, '{1}{0}{2}'.format(word, open_tag, close_tag))

def highlight(text, question, answer_sent, answer):
    """
    Подсветка важных частей текста.
    """
    orig = answer_sent
    sent = orig.lower()
    q_words = nltk.word_tokenize(question)
    # Выделим ответ жиром
    sent = wrap_tag(sent, answer, '<b>', '</b>')
    # Выделим цветом пр-е с ответом
    sent = '<span class=\'answer-sent\'>{}</span>'.format(sent)
    text = text.replace(orig, sent)
    # Выделим вопросительное слово
    question = wrap_tag(question, q_words[0].capitalize(), '<b>', '</b>')
    question = wrap_tag(question, q_words[0], '<b>', '</b>')
    return (text, question, answer)

if __name__=='__main__':
    malt_parser = MaltParser("maltparser-1.9.1.jar", "russian_syntags", m)
    app.run(host='0.0.0.0', port=5000, debug=True)
