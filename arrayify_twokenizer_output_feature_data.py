''' 
This script arranges the data from the previous CrowdFlower parsing scripts
into a numpy array of features and labels for every tweet that was scored on 
CrowdFlower. Later, we can feed this script into a classifier script, or 
just write the classifier in here.
'''
import numpy as np
import random
from sklearn.svm import SVC
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
	for feature in features:
		if feature in tokens:
			feature_vector[0][counter] = 1
		elif feature in POS:
			feature_vector[0][counter] = 1
		else:
			feature_vector[0][counter] = 0
		counter += 1
	data_set[i] = feature_vector

data.close()
# Let's try an SVM

# First, separate into training and test data. Test data will be a random 10% of the original data set.
training_data_indices = random.sample(xrange(len(data_set)), int(len(data_set) * 0.9))
training_data = np.empty([len(data_set) * 0.9, len(features) + 1.0])
test_data = np.empty([len(data_set) * 0.1, len(features) + 1.0])
counter = 0
test_counter = 0
for i in range(len(data_set)):
	if i in training_data_indices:
		training_data[counter] = data_set[i]
		counter += 1
	else:
		test_data[test_counter] = data_set[i]

training_X = training_data[:,1:(len(features) + 1.0)]
training_Y = training_data[:,0]
for point in range(len(training_Y)):
    if training_Y[point] > 3.0:
        training_Y[point] = 1.0
    else: 
        training_Y[point] = 0.0
test_X = test_data[:,1:(len(features) + 1.0)]
test_Y = test_data[:,0]
for point in range(len(test_Y)):
    if test_Y[point] > 3.0:
        test_Y[point] = 1.0
    else: 
        test_Y[point] = 0.0

# Train SVM
clf = SVC()
clf.fit(training_X, training_Y)
# Predict test data using trained SVM
predictions = clf.predict(test_X)
# Calculate error rate of trained SVM
error_counter = 0.0
for p in range(len(predictions)):
    if predictions[p] != test_Y[p]:
        error_counter += 1.0
out_of_sample_error = error_counter / len(test_Y)
print out_of_sample_error
# Calculate in-sample error rate of trained SVM, for shits and giggles
in_predictions = clf.predict(training_X)
in_error_counter = 0.0
for p in range(len(in_predictions)):
    if in_predictions[p] != training_Y[p]:
        in_error_counter += 1.0
in_of_sample_error = in_error_counter / len(training_Y)
print in_of_sample_error

print predictions
print test_Y

