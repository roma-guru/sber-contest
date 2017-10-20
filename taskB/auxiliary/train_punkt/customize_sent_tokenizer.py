from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
punkt_param = PunktParameters()
abbreviation = ['u.s.a', 'fig']
punkt_param.abbrev_types = set(abbreviation)
tokenizer = PunktSentenceTokenizer(punkt_param)
r = tokenizer.tokenize('Fig. 2 shows a U.S.A. map.')
print(r)