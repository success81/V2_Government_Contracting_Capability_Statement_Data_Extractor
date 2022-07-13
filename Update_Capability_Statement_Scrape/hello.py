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


    #Change to self-deleting file once processing is done
    #Code to create temp file directory \tmp is the temp file directory
    if request.method == 'POST':
        fname = request.files["myfile"]
        #fname.save(secure_filename(fname.filename))
    if fname:
        filename = secure_filename(fname.filename)
        file_path = os.path.join('tmp', filename)
        #file_path = os.path.join('temp_files', filename)
        fname.save(file_path)

    #Code to assign PDF
    #fname ='FDT.pdf'
    doc = fitz.open(file_path)  
    text = ''
    for page in doc:  
        text += page.get_text() 

    #Converted Capability Statement
    complete_text = text
    lower = text.lower()
    #Removed punctuation

    #Tokenized complete text
    tokens = word_tokenize(lower)
    normal_tokens = word_tokenize(complete_text)

    #####################################################
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
    ######################################################
    #SDVOB
    SDVOB_counter = 0
    """
    Search for Service Disabled Business (Detected but verify)
    Search "sdvob" in lower yes
    """

    if "sdvob" in lower:
        SDVOB_counter += 5

        
    else:
        pass
    #for x in lower:
        #if x == "service-disabled":
            #SDVOB_counter += 1
        
    #########################

    #######################################################
    #VOSB
    VOSB_counter = 0
    """
    Veteran-Owned Small Business
    """

    if "vosb" in lower:
        VOSB_counter += 5
    else:
        pass

    #######################################################
    #HUBZone
    HUBZone_counter = 0
    """
    Historically Underutilized Business Zone Small Business
    """
    if "HUBZone" in normal_tokens:
        HUBZone_counter += 5
    else:
        pass

    #######################################################

    #######################################################
    #SDB
    SDB_counter = 0
    """
    Small disadvantaged Business
    """
    if "sdb" in lower:
        SDB_counter += 5
    elif "small disadvantaged" in lower:
        SDB_counter += 1
    else:
        pass
    #######################################################

    #####################################
    #8A
    eight_a_counter = 0
    """
    Search in tokens for a string of 8 and a (Detected, but verify)
    Search "8(a)" in lower Yes
    """
    if "8(a)" in lower:
        eight_a_counter += 5
    elif "8(a)" in tokens:
        eight_a_counter += 1
    else:
        pass

    #######################################


    #################################################
    #EDWOSB
    edwosb_counter = 0
    """
    Economically Disadvanteged women owned small business
    Search for edwosb in lower Yes
    """
    if "edwosb" in lower:
        edwosb_counter += 5
    elif "Economically Disadvantaged" in lower:
        edwosb_counter += 1
    else:
        pass
    ################################################

    ################################################
    #WOSB
    wosb_counter = 0
    """
    Women-Owned Small Business
    add search for woman owned and women owned
    """
    if "wosb" in lower:
        wosb_counter += 5
    elif "women" in tokens:
        wosb_counter += 1
    else:
        pass
    #for x in tokens:
        #if x == "women-owned" or "woman-owned":
            #wosb_counter += 1
        
    ################################################

    ################################################
    #ANC
    anc_counter = 0
    """
    ANC
    Alaska Native Corporation
    """
    if "anc" in tokens:
        anc_counter += 5
    elif "alaska native" in lower:
        anc_counter += 1
    else:
        pass
    ################################################

    ####Grade Scores of Certifications####

    #edwosb
    if edwosb_counter >= 5:
        edwosb_answer= "Yes"
    elif edwosb_counter == 1:
        edwosb_answer= "Detected, but verify"
    elif edwosb_counter == 0:
        edwosb_answer = "Not detected"

    #wosb
    if wosb_counter >= 5:
        wosb_answer= "Yes"
    elif wosb_counter == 1:
        wosb_answer= "Detected, but verify"
    elif wosb_counter == 0:
        wosb_answer = "Not detected"

    #sdb
    if SDB_counter >= 5:
        SDB_answer= "Yes"
    elif SDB_counter == 1:
        SDB_answer= "Detected, but verify"
    elif SDB_counter == 0:
        SDB_answer = "Not detected"

    #8a
    if eight_a_counter >= 5:
        eight_a_answer= "Yes"
    elif eight_a_counter == 1:
        eight_a_answer= "Detected, but verify"
    elif eight_a_counter == 0:
        eight_a_answer = "Not detected"

    #HUBZone
    if HUBZone_counter >= 5:
        HUBZone_answer= "Yes"
    elif HUBZone_counter == 0:
        HUBZone_answer = "Not detected"

    #SDVOB
    if SDVOB_counter >= 5:
        SDVOB_answer= "Yes"
    elif SDVOB_counter == 1:
        SDVOB_answer= "Detected, but verify"
    elif SDVOB_counter == 0:
        SDVOB_answer = "Not detected"

    #VOSB
    if VOSB_counter >= 5:
        VOSB_answer= "Yes"
    elif VOSB_counter == 1:
        VOSB_answer= "Detected, but verify"
    elif VOSB_counter == 0:
        VOSB_answer = "Not detected"

    #ANC
    if anc_counter >= 5:
        anc_answer= "Yes"
    elif anc_counter == 1:
        anc_answer= "Detected, but verify"
    elif anc_counter == 0:
        anc_answer = "Not detected"


    #Index
    """
    0. edwosb_counter
    1. wosb_counter
    2. SDB_counter
    3. eight_a_counter
    4. HUBZone_counter
    5. SDVOB_counter
    6. VOSB_counter
    7. anc_counter 
    8. codes
    9. complete_text
    """
        
        #Combining all text and NACICS into one list
    output = []

    output.append(edwosb_answer)
    output.append(wosb_answer)
    output.append(SDB_answer)
    output.append(eight_a_answer)
    output.append(HUBZone_answer)
    output.append(SDVOB_answer)
    output.append(VOSB_answer)
    output.append(anc_answer)
    output.append(codes)
    output.append(complete_text)

    return render_template('after.html', data = output)

if __name__ == "__main__":
    app.run(debug=True)





    #print (output)
