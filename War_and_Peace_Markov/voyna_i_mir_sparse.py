# coding: utf-8
import numpy as np
from tqdm import tqdm
import scipy.sparse
import sys

f = open(r"warandpeace.utf8", "r")
s = f.read().split()


num_to_item_dict = sorted(set(s))
item_to_num_dict = { x: i for (i, x) in enumerate(num_to_item_dict)}
number_of_items = len(set(s))
arr = [item_to_num_dict[x] for x in s]


# Создаём двумерный массив вероятностей переходов
prob = scipy.sparse.lil_matrix((number_of_items, number_of_items), dtype="uint16")
print("Матрица переходов занимает", sys.getsizeof(prob))


for i in tqdm(range(0, len(s) - 1)): # last but one
    x = arr[i]
    y = arr[i + 1]
    prob[x, y] += 1

print("Теперь матрица переходов занимает", sys.getsizeof(prob))

# Теперь генерируем
print("\nНаиболее часты переходы")
current_word = "иногда"
current_number = item_to_num_dict[current_word]



for i in range(20):
    probs_for_current = prob[current_number].toarray()[0]
    max_arg = np.argmax(probs_for_current)
    
    current_word = num_to_item_dict[max_arg]
    current_number = max_arg
    print(current_word, end="·")
    
    



print("\nТеперь со случайными числами")
current_word = "иногда"
current_number = item_to_num_dict[current_word]

for i in range(200):
    probs_for_current = prob[current_number].toarray()[0]
    normalized_probs_for_current = probs_for_current / np.sum(probs_for_current)
    
    max_arg = np.argmax(probs_for_current)
    choice = np.random.choice(range(0, len(probs_for_current)), p=normalized_probs_for_current)
    
    current_word = num_to_item_dict[choice]
    current_number = choice
    print(current_word, end=" ")
    
    


# Теперь просто набор случайных слов для сравнения
print("\nДля сравнения - просто набор случайно выбранных слов")
for i in range(200):
    rnd = np.random.randint(0, len(s))
    print(s[rnd], end=" ")
