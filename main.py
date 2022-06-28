import re
import math

text = "says he has signed a decree saying foreign buyers must pay in rubles for Russian gas from April 1, and contracts would be halted if these payments are not made."

AFINN = "./words.txt"

f = open(AFINN, "r")
texto = f.readlines()
afinn = {}

for line in texto:
    l = line.split()
    if len(l) > 2:
        afinn[' '.join(l[:len(l) - 1])] = int(l[-1])
    else:
        afinn[l[0]] = l[-1]
        afinn[l[-1]] = int(l[-1])
f.close()


pattern_split = re.compile(r"\W+")
sentiments = []


def sentiment(text):
    words = pattern_split.split(text.lower())
    #sentiments = map(lambda word: afinn.get(word, 0), words)
    for word in words:
        if word in afinn:
            sentiments.append(int(afinn[word]))
        else:
            sentiments.append(0)
    if sentiments:
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
    else:
        sentiment = 0
    return sentiment


print(sentiment(text=text))
