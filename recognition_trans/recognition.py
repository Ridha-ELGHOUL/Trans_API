import speech_recognition as sr
from googletrans import Translator
import pyttsx3
def RecognitionToText(lang="DE"):
    #instance of recognizer class
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ("RECOGNITON STARTED ... Tell something");
        print ("---------------- Recording  -----------");
        audio = r.listen(source)
        print ("FINISH RECORDING ... ")

    # Speech recognition using Google Speech Recognition
    try:
        text_recognitized = r.recognize_google(audio,language = lang)
        #print ("********************************************");
        #print("YOU SAID : ")
        #print( text_recognitized)
        #print ("********************************************");
        LanguageDetect(text_recognitized)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text_recognitized

def LanguageDetect(text,l='en'):
    translator = Translator()
    #print(translator.detect(text))
    trans= str(translator.translate(text,dest=l))
    transText = trans.split(",")
    #print ("********************************************");
    #print ("TRADUCTION :  "+ transText[2][6:])
    #print ("********************************************");
    return transText[2][6:]
    #TextTospeech(transText[2][6:])

def TextTospeech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()