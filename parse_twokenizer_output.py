'''
This file takes in the output of the runTagger bash script and outputs a file of feature data
for every tweet from a CrowdFlower job. The next script to be run, on the output
of this one, is "arrayify_twokenizer_output_feature_data.py"
'''
# labels.txt is a file of the CrowdFlower-labelled scores 
# (averaged over CrowdFlower participants) in the same order as the other features.
# tweets2.txt is a file of just the content of the tweets from CrowdFlower.
# parsed_tweets.txt is a file of tokenized and POS labelled tweets, created by the bash script shown below.
f = open('feature_labelled_data.txt', 'w')
y = open('labels.txt', 'r')
t = open('tweets2.txt', 'r')
d = open('parsed_tweets.txt', 'r') # ./runTagger.sh tweets.txt > parsed_tweets.txt
lines = d.readlines()
labels = y.readlines()
tweets = t.readlines()
data = []
counter = 0
for i in range(len(lines)):
	line = lines[i].strip()
	counter += 1
	label = labels[i].strip()
	line = line.split('\t')
	tokens = line[0]
	POS = line[1]
	scores = line[2]
	content = line[3]
	f.write(tokens + '\t' + POS + '\t' + label)
	f.write('\n')

d.close()
t.close()
y.close()
f.close()