# these should be the only imports you need
import csv

import tweepy
import nltk
import json
import sys

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# write your code here
# usage should be python3 part1.py <username> <num_tweets>

print("Warning: Replies are also considered as tweets!")
print("Warning: CSV file use \\r\\n as line terminator!")

consumer_key = 'ero6eldSp2RvmBhAqMJVAdsgz'
consumer_secret = '3maLK8fD5my1BvUpi2omLPZesxHMyccgYOnyZvL2JSckWDtPtf'
access_token = '1010385768055898112-jGy60GS8V7WLrIcWMwcPqTgtluCBiy'
access_token_secret = 'Jm44E1uXaoRSbynQvgjGAsxtMGvSSNUd6NbKvHzBffILl'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

arg = sys.argv
if len(arg) != 3:
    raise AssertionError('Usage should be python3 part1.py <username> <num_tweets>')

user = arg[1]
tweet_analyzed = int(arg[2])
tweets = api.user_timeline(screen_name=user,
                           count=tweet_analyzed,
                           tweet_mode='extended')

original_tweets = 0
time_favorited = 0
time_retweeted = 0


def get_full_text(tweet):
    if 'retweeted_status' in tweet:
        return tweet["retweeted_status"]["full_text"]
    else:
        return tweet["full_text"]


stop_word = ['http', 'https', 'RT']
word_count = {}
for tweet in tweets:
    seg = [w for w in nltk.word_tokenize(get_full_text(tweet)) if w.isalpha() and w not in stop_word]

    for word, typ in nltk.pos_tag(seg):
        word_count[word] = word_count.setdefault(word, 0) + 1

    if 'retweeted_status' not in tweet:
        original_tweets = original_tweets + 1
        time_favorited = time_favorited + tweet['favorite_count']
        time_retweeted = time_retweeted + tweet['retweet_count']

verb = {}
noun = {}
adjective = {}
for key, value in sorted(word_count.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    tag = nltk.pos_tag([key])[0][1]
    if tag.startswith('VB'):
        if len(verb) < 5:
            verb[key] = value
    elif tag.startswith('NN'):
        if len(noun) < 5:
            noun[key] = value
    elif tag.startswith('JJ'):
        if len(adjective) < 5:
            adjective[key] = value
    if len(verb) == 5 and len(noun) == 5 and len(adjective) == 5:
        break


print("USER: ", user)
print("TWEETS ANALYZED: ", tweet_analyzed)
print("VERBS:", end=' ')
for key, value in sorted(verb.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    print(key+"("+str(value)+")", end=' ')
print()
print("NOUNS:", end=' ')
for key, value in sorted(noun.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    print(key+"("+str(value)+")", end=' ')
print()
print("ADJECTIVES:", end=' ')
for key, value in sorted(adjective.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    print(key+"("+str(value)+")", end=' ')
print("ORIGINAL TWEETS: ", original_tweets)
print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): ", time_favorited)
print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): ", time_retweeted)

with open('noun_data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', lineterminator='\r\n')
    writer.writerow(['Noun', 'Number'])
    for key, value in sorted(noun.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        writer.writerow([key, value])
    csvfile.close()
