# app.py
from flask import Flask, request, render_template, jsonify
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
from tfidf_model import *

tfidf=pickle.load(open("tfidf.pickle","rb"))
model=pickle.load(open('model.pickle','rb'))

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def form():
	if request.method=='POST':
		link = request.form['link']
		text, title = query(link)
		data = tfidf.transform([title +' '+ text])
		return render_template('output.html', flair=str(model.predict(data)[0]))
	else:
	    return render_template('index.html')
@app.route('/auto',methods=['POST'])
def post():
	link = request.files['upload_file'].read().decode("utf-8")
	urls,data = multi_query(link)
	data = tfidf.transform(data)
	out=model.predict(data).tolist()
	json={k:v for k,v in zip(urls,out)}
	return jsonify(json)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000) 
