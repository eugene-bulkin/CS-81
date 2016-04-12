''' 
This script should be run in the same directory as the JSON file of results 
from a CrowdFlower job. This script will create two text files, which will be used 
in the following command-line cmd: ./runTagger.sh tweets.txt > parsed_tweets.txt, 
and then the following script: parse_twokenizer_output.py
'''
import json

f = open('tweets2.txt', 'w')
y = open('labels.txt', 'w')
counter = 0
data_file =  open('job_894382.json') 
data = data_file.readlines()
for df in data:
	counter += 1
	d = json.loads(df)
	tweet = d['data']['content'].encode('utf-8')
	score = d['results']['how_sincere_or_sarcastic_is_this_tweet']['avg']
	tweet = tweet.strip()
	temp = tweet.split('\n')
	tweet = ' '.join(temp)
	y.write(str(score))
	y.write('\n')
	f.write(tweet)
	f.write('\n')

f.close()
y.close()