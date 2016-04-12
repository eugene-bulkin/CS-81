''' 
This script arranges the data from the previous CrowdFlower parsing scripts
into a numpy array of features and labels for every tweet that was scored on 
CrowdFlower. Later, we can feed this script into a classifier script, or 
just write the classifier in here.
'''
import numpy as np
from collections import defaultdict

data = open('feature_labelled_data.txt', 'r')
f = data.readlines()
token_dict = defaultdict(int)
POS_dict = defaultdict(int)
training_data = []
for i in range(len(f)):
	line = f[i]
	line = line.strip()
	tokens, POS, score = line.split('\t')
	line_list = []
	line_list.append(tokens)
	line_list.append(POS)
	line_list.append(score)
	training_data.append(line_list)
	# split tokens on ' ' and add to dictionary of all tokens
	score = score.split()
	POS = POS.split()
	tokens = tokens.split()
	for i in range(len(tokens)):
		token_dict[tokens[i]] += 1
	# same for POS
	for k in range(len(POS)):
		POS_dict[POS[k]] += 1
	# score is Y

# features consist of all tokens (unigrams), all POS, and is an indicator (0 for feature is not present,
# 1 if the feature is present in a given tweet).
features = []
for key in token_dict.keys():
	features.append(key)
for key in POS_dict.keys():
	features.append(key)

# data_set will be an np.array of N data points (one for each tweet), represented by vectors,
# where the first element of the vector will be the CrowdFlower score of that tweet, and the rest 
# will be indicators (1 or 0) of whether or not the given feature in that position (associated with
# the same position in the 'features' vector) is present in that given tweet.
data_set = np.empty([len(training_data), len(features) + 1])
for i in range(len(training_data)):
	# Each "point" is a list of the tokens, POS, and score, separated by ' ' from each other
	feature_vector = np.empty([1, len(features) + 1])
	counter = 1
	point = training_data[i]
	tokens = point[0]
	POS = point[1]
	score = point[2]
	# The feature vector has the following structure: feature_vector[0] is the score, decided by CrowdFlower.
	# every subsequent element of the feature_vector vector is an indicator of whether or not the feature
	# at that position was present in the tweet in question.
	feature_vector[0][0] = score
	print feature_vector
	for feature in features:
		print feature
		if feature in tokens:
			feature_vector[0][counter] = 1
		elif feature in POS:
			feature_vector[0][counter] = 1
		else:
			feature_vector[0][counter] = 0
		counter += 1
	data_set[i] = feature_vector

data.close()