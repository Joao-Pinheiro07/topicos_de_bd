import re
import math
from pyspark import SparkContext
from pyspark import HiveContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="PythonSentimentAnalysis")
sqlCtx = HiveContext(sc)



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

tweets = sqlCtx.sql("select username, texto from tweets")

tweet_contents = tweets.select("texto").collect()

sentimentTuple = 0

for row in tweet_contents:       
    sentimentTuple += sentiment(text=row[0])


log4jLogger = sc._jvm.org.apache.log4j
LOGGER = log4jLogger.LogManager.getLogger(__name__)
LOGGER.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
LOGGER.info(str(sentimentTuple))
LOGGER.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

query = "INSERT INTO sentimental_score select current_timestamp(), " + str(sentimentTuple)

sqlCtx.sql(query)
