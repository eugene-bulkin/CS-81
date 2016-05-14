import os
import sqlite3
import json
import re

url_regex = re.compile("https?:\/\/t\.co\/([^\b]+)")

def strip_urls(tweet):
    text = tweet['text']
    for url in tweet['urls']:
        text = text.replace(url['url'], '')
    text = re.sub(url_regex, "", text)
    tweet['text'] = text.strip()
    return tweet

def create_table(con):
    con.execute("CREATE TABLE IF NOT EXISTS tweets (id PRIMARY KEY, username, text UNIQUE, original_text, hashtag_json, symbol_json, url_json);")

def save_tweets(con):
    json_files = [fn for fn in os.listdir("results") if fn.endswith(".json")]

    all_tweets = []
    
    cur = con.cursor()

    i = 0
    for fn in json_files:
        j = json.load(open("results/" + fn))

        for tweet in j:
            old_text = tweet['text']
            tweet = strip_urls(tweet)

            all_tweets.append((tweet['id'], tweet['username'], tweet['text'], old_text, json.dumps(tweet['hashtags']),json.dumps(tweet['symbols']), json.dumps(tweet['urls'])))
            i += 1
            if i % 50 == 0:
                print "Processed tweet #%d..." % i
    print "Done. %d tweets processed." % i

    # ignore handles duplicates
    try:
        cur.executemany("INSERT OR IGNORE INTO tweets(id, username, text, original_text, hashtag_json, symbol_json, url_json) VALUES (?, ?, ?, ?, ?, ?, ?)", all_tweets)
        print "Successfully saved %d unique tweets." % cur.rowcount
    except Exception as e:
        print "Unable to successfully save tweets: %s" % e

if __name__ == '__main__':
    
    with sqlite3.connect("tweets.db") as con:
        create_table(con)

        save_tweets(con)
