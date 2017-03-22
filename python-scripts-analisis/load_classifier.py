#Program to classify the texts of the tweets with the name of the json as argument
#Importing necesasary libraries
import pickle
import pandas as pd
import numpy as np
import nltk
import json
import sys
import os

#Getting the external arguments and builiding strings for later use
arg=sys.argv
name1=arg[1]+'_analisis.json'
name2=arg[1]+'_resultados.json'

#Loading the classifier and the word features
with open('objs.pickle', "rb") as f:
        classifier, word_features=pickle.load(f)


#Defined function for extract the features given the text and the word features
def extract_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
                features['contains(%s)' % word] = (word in document_words)
        return features

if os.path.isfile(name1) and os.path.isfile(name2):
	print('Data has been already analized')
else:
	print('Analizing...')
	
	#Loading the file specified in the argument
	with open(arg[1]+'.json', 'r') as fp:
		data = json.load(fp)


	#Declaration of auxiliar variables
	load=[]

	#Get the text of the json file
	for i in range(1,len(data['texts'])):
		load.append(data['texts'][str(i)])

	#Converting to dataframe for data manipulation
	a=pd.DataFrame(load)
	a.columns=['text']

	#Declaration of more auxiliar variables
	aux=[]
	p=0
	n=0
	ne=0
	values={}
	values.setdefault('text',[])
	values.setdefault('sentiment',[])

	sentiments={}
	sentiments.setdefault('positivos',[])
	sentiments.setdefault('negativos',[])
	sentiments.setdefault('neutros',[])

	#Classifying each tweet
	for element in a['text']:
		values['text'].append(element)
		aux=element.split()
		prob1=classifier.prob_classify(extract_features(aux))
		dist1=prob1.samples()
		prob_pos=prob1.prob("positive")
		print(prob_pos)
	#The classifier gives us the probability that a tweet is positive, with this probability we define from what to another is positive negative or  neutral
		if prob_pos < 0.25 and prob_pos > 0.2:
			values['sentiment'].append('neutral')
		elif prob_pos < 0.2:
			values['sentiment'].append('malo')
		else:
			values['sentiment'].append('bueno')

	#Count the positives, negatives and neutrals
	for sen in values['sentiment']:
		if sen =='bueno':
			p=p+1
		elif sen == 'malo':
			n=n+1
		else:		
			ne=ne+1 

	#Assign values into dict
	sentiments['positivos'].append(p)
	sentiments['negativos'].append(n)
	sentiments['neutros'].append(ne)

	print(values)

	#Save the file of the tweets with their evaluation
	with open(name1, 'w') as fp1:
	    json.dump(values, fp1)

	#Save the file with the final results
	with open(name2, 'w') as fp2:
	    json.dump(sentiments, fp2)

	print(p)
	print(n)
	print(ne)
