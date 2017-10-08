import nltk
import sys
from pymorphy2 import MorphAnalyzer

m = MorphAnalyzer()
pos_oc2ud = {
    None: 'PUNCT',
    'NOUN': 'NOUN',
    'ADJF': 'ADJ',
    'ADJS': 'ADJ',
    'VERB': 'VERB',
    'COMP': 'ADV',
    'INFN': 'VERB',
    'PRTF': 'VERB',
    'PRTS': 'VERB',
    'GRND': 'VERB',
    'NUMR': 'NUM',
    'ADVB': 'ADV',
    'NPRO': 'PRON',
    'PRED': 'ADV',
    'PREP': 'ADP',
    'CONJ': 'CCONJ',
    'PRCL': 'PART',
    'INTJ': 'INTJ'
}


if __name__=='__main__':
    infile = sys.argv[1]
    with open(infile) as f:
        txt = f.read()

    sents = nltk.sent_tokenize(txt)
    for i,s in enumerate(sents):
        s = s.replace('\n','')
        tokens = nltk.word_tokenize(s)
        print("# sent: {}".format(i))
        print("# text: {}".format(s))
        for j,t in enumerate(tokens):
            t = m.parse(t)[0]
            print("{0}\t{1}\t{2}\t{3}\t_\t_\t_\t_\t_\t_".format(j+1, t.word, 
                                                       t.normal_form, 
                                                       pos_oc2ud[t.tag.POS]))
        print()
