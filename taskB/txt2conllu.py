import nltk
import sys
from pymorphy2 import MorphAnalyzer
from russian_tagsets import converters

m = MorphAnalyzer()
oc2ud = converters.converter('opencorpora-int','ud20')


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
            pos, feats = oc2ud(str(t.tag)).split(' ')
            print("{0}\t{1}\t{2}\t{3}\t_\t{4}\t_\t_\t_\t_".format(j+1, t.word, 
                                                       t.normal_form, pos,
                                                        feats))
        print()
