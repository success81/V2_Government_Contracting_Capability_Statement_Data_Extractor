#Libraries
import sys
import fitz
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from flask import Flask, render_template, request
import tempfile
from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def home():


	#Code to take in document 
	if request.method == 'POST':
		fname = request.files["myfile"]
		#fname.save(secure_filename(fname.filename))
	if fname:
		filename = secure_filename(fname.filename)
		file_path = os.path.join('temp', filename)
		#file_path = os.path.join('temp_files', filename)
		fname.save(file_path)


	

	#output = "fish"
	#big_pdf = open(fname, 'rb')
	#my_pdf = PyPDF2.PDFFileReader(fname)

	doc = fitz.open(file_path)  
	text = ''
	for page in doc:  
	    text += page.get_text() 

	#Converted Capability Statement
	complete_text = text


	#Tokenized complete text
	tokens = word_tokenize(complete_text)

	#Logic to pull NACICS
	NACICS = []
	num_check = ["0","1","2","3","4","5","6","7","8","9"]
	for x in tokens:
	    if len(x) == 6:
	        if x[0] in num_check and x[1] in num_check and x[2] in num_check and x[3] in num_check and x[4] in num_check and x[5] in num_check:
	            NACICS.append(x)
	        else:
	            pass

	#Putting Nacics on string
	codes = ""

	for x in NACICS:
	    codes += x
	    codes += " "

	#Combining all text and NACICS into one list
	output = []

	output.append(codes)
	output.append(complete_text)
	
	
	return render_template('after.html', data = output)

if __name__ == "__main__":
	app.run(debug=True)



