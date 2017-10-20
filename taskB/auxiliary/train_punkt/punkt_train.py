#!/usr/bin/env python
import nltk.tokenize.punkt
import pickle
import codecs
import sys, gc, bz2

print("Training Punkt on text")
tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
if sys.argv[1].endswith('.bz2'):
    with bz2.open(sys.argv[1], 'rt', encoding='utf8') as wiki:
        tokenizer.train(wiki.read(),verbose=True)
else:
    with open(sys.argv[1], 'r', encoding='utf8') as wiki:
        tokenizer.train(wiki.read(),verbose=True)

print("Writing pickle")
with open("punkt_russian.pkl","wb") as out:
    pickle.dump(tokenizer, out)
