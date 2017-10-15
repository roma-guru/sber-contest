import re


s = open("abramov.txt", "r", encoding="utf8").readlines()
synonyms = {}

for line in s:
	s = line[:-1].split("::")
	article_word = s[0].lower()
	words = s[1].split(", ")
	if article_word not in synonyms:
		synonyms[article_word] = words
	else:
		synonyms[article_word].extend(words)


def double_synonym(s):
	synonyms_1 = synonyms[s]
	res = []
	for word in synonyms_1:
		if word in synonyms:
			res.extend(synonyms[word])
	return list(set(synonyms_1 + res))


def words_are_synonyms(word_1, word_2):
	""" Checking if two given words are synonyms """
	if word_1 in synonyms and word_2 in synonyms[word_1]:
		return True

	if word_2 in synonyms and word_1 in synonyms[word_2]:
		return True

	return False

print(synonyms["удивлять"])
print(synonyms["собака"])
print(double_synonym("удовлетворительный"))
print(words_are_synonyms("царица", "королева"))





    