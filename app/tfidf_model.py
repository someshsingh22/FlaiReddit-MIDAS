from flask import Flask, request, render_template
from werkzeug.datastructures import ImmutableMultiDict
from sklearn.feature_extraction.text import TfidfVectorizer as TF
from sklearn.naive_bayes import MultinomialNB as MNB
from scipy import sparse #Sparsed Vectorizers
from scipy.sparse import hstack
import scipy.stats as ss 
import re
from sklearn.utils import resample
import numpy as np
import requests
import pickle

def query(url):
	id=url[:-1].split('/')[-2]
	r=requests.get('https://api.pushshift.io/reddit/search/submission/?ids={}&fields=selftext,title'.format(id))
	data=r.json()['data'][0]
	return data['selftext'], data['title']

def multi_query(inp):
	urls=inp.split()
	ids=[url[:-1].split('/')[-2] for url in urls]
	data=[]
	for id in ids:
		r=requests.get('https://api.pushshift.io/reddit/search/submission/?ids={}&fields=selftext,title'.format(id))
		dat=r.json()['data'][0]
		data.append(dat['title']+' '+dat['selftext'])
	return urls,data

def clean(text):
	contracts={
	"n't" : " not",
	"'ll" : "will",
	"'ve" : "have",
	"'n" : "",
	"'ed" : "",
	"'l" : "will",
	"'re" : "are",
	"'r" : "are",
	"'a" : " is a",
	"'d" : "had",
	"'ing" : "ing",
	"r\/" : " subreddit ",
	"u\/" : " user ",
	"&amp;" : " ",
	"&gt;" : " ",
	"&lt;" : " ",
	"&gt" : "  ",
	"&lt" : " ",
	"#" : "#  ",}
	text=text.lower()
	text=text.replace('\n', ' ')
	for k,v in contracts.items():
		text=text.replace(k,v)
	text=re.sub('[(]?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])/)*', ' ', text)
	text=re.sub('[^a-z]', ' ', text)
	text=' '.join([word for word in text.split(' ') if not word== ''])
	return text