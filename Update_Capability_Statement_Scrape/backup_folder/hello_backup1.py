#Libraries
import sys
import fitz
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from flask import Flask, render_template, request
import tempfile


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def home():


	#Code to take in document
	output =request.files['myfile']
	

	


	return render_template('after.html', data = output)
  	
if __name__ == "__main__":
    app.run(debug=True)



