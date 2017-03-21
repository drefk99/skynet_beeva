#Program to train the classifier
#Importing necessary libraries to classify
import pickle
import pandas as pd
import numpy as np
import nltk

#Load as a table de txt files
a=pd.read_table('tweets_pos_clean.txt')
b=pd.read_table('tweets_neg_clean.txt')

#Initiate the auxiliar arrays
aux1=[]
aux2=[]
auxiliar1=[]
auxiliar2=[]

#Getting just  the words that have more than 3 letters and either happy face or sad face
for element in a['Text']:
	for w in element.split():
		if (w==':)' or len(w)>3):
			auxiliar1.append(w)
	aux1.append((auxiliar1,'positive'))
	auxiliar1=[]

for element in b['text']:
	for w in element.split():
		if (w==':(' or len(w)>3):
			auxiliar2.append(w)
	aux2.append((auxiliar2,'negative'))
	auxiliar2=[]

#From the arrays just use the first 10000 values for the positive and 20000 for the negatives
aux1=aux1[:10000]
aux2=aux2[:20000]

#Convert to dataframe
pos_df=pd.DataFrame(aux1)
neg_df=pd.DataFrame(aux2)

#Naming the columns
pos_df.columns=['words','sentiment']
neg_df.columns=['words','sentiment']

#Concatenate positive and negative values
table_aux1=aux1+aux2

#Definition of functions
#Function for getting the single words and sentiments
def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

#Function for getting the frequency of the words in the tweets
def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

#Function to check if a tweet has a specific word
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

#Get the frequency of all the words in the dataset
word_features = get_word_features(get_words_in_tweets(table_aux1))

#Building the training set for the classifier
training_set = nltk.classify.apply_features(extract_features, table_aux1)

#Train the classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

#Save the classifier and the word_features in a pickle for external use
with open('objs.pickle','wb') as f:
	pickle.dump([classifier, word_features],f)


