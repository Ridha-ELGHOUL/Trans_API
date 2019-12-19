import speech_recognition as sr
from googletrans import Translator
import pyttsx3

#!flask/bin/python
from flask import Flask
app = Flask(__name__)
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

def translation(text, target):
    translator = Translator()
    #print(translator.detect(text))
    print ('fisrt '+str(text))
    trans= str(translator.translate(text, target))
    transText = trans.split(",")
    print(transText)
    #print ("********************************************");
    #print ("TRADUCTION :  "+ transText[2][6:])
    #print ("********************************************");
    return transText[2][6:]
    #TextTospeech(transText[2][6:])

@app.route('/trans_msg', methods=['POST'])
def post():
    res=jsonify({'data':''})
    if(request.is_json):
        content = request.get_json()
        ret = translation(content['message'], content['target'])
        print (ret)
        res = jsonify({'data': str(ret)})
    return res

app.run(host='0.0.0.0', port=5000)

