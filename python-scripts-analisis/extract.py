#Libraries used for extrating tweets
import json
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import pandas as pd
import pickle
import sys
import os

#Get external arguments to search the tweets
arg=sys.argv
print(sys.argv)
name=arg[1]+'_'+arg[2]+'.json'
if arg[1]=='santander':
        req='banco santander'
else:
        req=arg[1]



if os.path.isfile(name):
	print('Data has been already downloaded')
else:
	print('GET ALL THE TWEETS!!!')
	consumer_key = 'w87sF4cjjFylzzyCd4mmTVfW3'
	consumer_secret = 'QSomS57CVwOZWHoK9Bl2yt2PdBImgxftulZeGSraq4n9vJzGFh'
	access_token = '293210492-tjb5kNx8Iupi4Yq4vTlk3vuXCTM3XWqxALnoyIak'
	access_secret = 'g6IjmWVWljTp9OjrFBZddiIyzjFC9251S7brov3RHT3hU'

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	#Accesing the api
	api = tweepy.API(auth)

	#Initializing the dictionary that will contain the information
	datos_tweets={}
	datos_tweets.setdefault('date',{})
	datos_tweets.setdefault('texts',{})
	datos_tweets.setdefault('user_id',{})
	datos_tweets.setdefault('retweet_count',{})
	i=1

	#Make the requests for the specified term in 'q', 'since' and 'until 
	for tweet in tweepy.Cursor(api.search, q=req, lang="es", since=arg[2], until=arg[3]).items():
		if not hasattr(tweet,'retweeted_status'):
			datos_tweets['date'].update({i:tweet.created_at.isoformat()})
			datos_tweets['texts'].update({i:tweet.text})
			datos_tweets['user_id'].update({i:tweet.user.id})
			datos_tweets['retweet_count'].update({i:tweet.retweet_count})
			i=i+1

	#DataFrame to display the data afterwards
	df_datos_tweets=pd.DataFrame(datos_tweets)

	#Saving the data and assigning a name realted to the given arguments
	with open(name, 'w') as fp:
	    json.dump(datos_tweets, fp)

	print(df_datos_tweets.to_json)
