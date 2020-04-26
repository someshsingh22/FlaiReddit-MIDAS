from flask import Flask, request
from werkzeug.datastructures import ImmutableMultiDict
import model

app=Flask(__name__)

@app.route("/") 
def home_view(): 
        return "<h1>Welcome to Geeks for FlaiReddit</h1>"

@app.route('/classifier',methods=['GET','POST'])
def main():
	if request.method=='POST':
		text = request.files['upload_file'].read()
		return model.classify(text)
	else:
		return "GET"+ model.classify("POST")

if __name__=="__main__":
    app.run() 
