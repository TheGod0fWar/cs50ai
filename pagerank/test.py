import random
from typing import ValuesView

DAMPING = 0.85
corpus = {
    "1.html": {"2.html", "3.html"},  # Normaler Fall: Verlinkt auf zwei andere Seiten
    "2.html": {"3.html"},  # Verlinkt nur auf eine einzige Seite
    "3.html": set(),  # Sackgasse (Sink): Verlinkt auf GAR NICHTS
}

page = "1.html"

#
# transition = {}
# if corpus[page]:
#     i = len(corpus[page])
#
#     d_factor = DAMPING / i
#     rest_factor = (1 - DAMPING) / len(corpus)
#
#     for site in corpus:
#         transition[site] = rest_factor
#
#     for obj in corpus[page]:
#         print("obj",obj)
#         transition[obj] += d_factor
# else:
#     factor = 1 / len(corpus)
#     for obj in corpus:
#         transition[obj] = factor


capital = random.choice(list(corpus.keys()))

dic = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

# for i, (key, value) in enumerate(dic.items()):
    
print(dic)
print(enumerate(dic.items()))
