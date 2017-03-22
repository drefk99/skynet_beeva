import json                                                                                                     
import tweepy                                                      
from tweepy import Stream                                             
from tweepy.streaming import StreamListener                           
from tweepy import OAuthHandler                                       
import pandas as pd                                                   
import pickle                                                                                                                                
import sys

from elasticsearch import Elasticsearch                                    
                                    
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#Variables para poner las credenciales para la API
consumer_key = ''                            
consumer_secret = ''                                          
access_token = ''
access_secret = ''  
                                                                                                                 
auth = OAuthHandler(consumer_key, consumer_secret)                                                              
auth.set_access_token(access_token, access_secret)                                                              
                                                                                                                 
api = tweepy.API(auth)
datos_tweets={}                                                       
datos_tweets.setdefault('date',[])                                    
datos_tweets.setdefault('texts',[])                                   
datos_tweets.setdefault('user_id',[])                                 
datos_tweets.setdefault('retweet_count',[])                           

args=sys.argv

                                                                          
#print(place_id)                                                      
for tweet in tweepy.Cursor(api.search, q=args[1], lang="es", since=args[2], until=args[3]).items():
     if not hasattr(tweet,'retweeted_status'):                      
         datos_tweets['date'].append(tweet.created_at.isoformat())
         datos_tweets['texts'].append(tweet.text)                                                                
         datos_tweets['user_id'].append(tweet.user.id)                                                           
         datos_tweets['retweet_count'].append(tweet.retweet_count)                  


es.index(index='skynet_beeva', doc_type=args[1], id=args[2], body= datos_tweets) 
es.get(index='skynet_beeva', doc_type=args[1], id=args[2])

ela_bancomer = es.get(index='skynet_beeva', doc_type=args[1], id=args[2])
#Añadir la ruta absoluta a datoJ para ejecutar con el cron
with open('datoJ/'+args[1]+args[2]+'.json', 'w') as fp:                                                                     
         json.dump(ela_bancomer, fp)
