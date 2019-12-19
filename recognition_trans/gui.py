from tkinter import *
import logging
import getpass
from optparse import OptionParser
import threading
import sys
import speech_recognition as sr
import sleekxmpp
from google_speech import Speech
from  recognition_trans import recognition as re
fenetre=Tk()
fenetre.geometry("400x600")
label = Label(fenetre, text="EASY CHAT_VOICE_TEXT_APP")
label.pack()
#global xmpp
global isClicked
#####
class XMClient(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password,recipient):
        super(XMClient, self).__init__(jid, password)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data Forms
        self.message=" no message "
        self.recipient = recipient
        
        self.add_event_handler('session_start', self.start,threaded=True)
        self.add_event_handler('message', self.recv_message)
        #self.add_event_handler()
    def start(self, event):
        self.send_presence()
        self.get_roster()
        print("sessions started")
        fenetre.ecran.insert(INSERT,"###### starting Chatt #####\n")
        #x = threading.Thread(target=self.send_msg)
        #y= threading.Thread(target=recv_message)
        #x.start()
        #x.join()
        #y=start()
    def send_msg(self):
        print("###### starting Chatt ##### ")
        fenetre.ecran.insert(INSERT,"###### starting Chatt #####\n")
        while(True):
            valueInput = input("\r You said (in) :")
            fenetre.ecran.insert(INSERT, "You said: "+sendText.get()+"\n")
            #Trans_msg = re.LanguageDetect(msg_data)
            self.msg = sendText.get()
            self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')

    def recv_message(self, msg):
        
        print(msg['type'])
        if msg['type'] in ('chat'):
            print("recieving msg ... ")
            #print(radio.get())
            msg_tranlated = re.LanguageDetect(msg['body'],radio.get())
            #print (msg_tranlated)
            #print ("%s says: %s" % (msg['from'],msg_tranlated ))
            comefr = str(msg['from'])
            msgrec = "%s says: %s" % (comefr.split("/")[0],msg_tranlated+"\n")
            fenetre.ecran.insert(INSERT,msgrec)
        elif msg['type'] in ('normal'):
            print("voice talk ... ")
            msg_tranlated = re.LanguageDetect(msg['body'],radio.get())
            print(msg_tranlated)
            comefr = str(msg['from'])
            speech = Speech(msg_tranlated, radio.get())
            speech.play()
            #re.TextTospeech(msg_tranlated)


def OnclickVoice():
    ClickSendVoice()
#fenetre.bind('<enter>', func)
def onclick():
    SenderClick()
    #sys.stdout.write("test")
    #press.press_and_release('enter')
def Connect():
    jid=UsernameGUI.get()
    pwd=PasswordGUI.get()
    to= RecipientGUI.get()
    print(jid , " --- to ---",to)
    global xmpp
    xmpp = XMClient(jid, pwd, to)
    
    try:
        ConBtn.config(text="Connecting...",bg="white",fg='black')
        xmpp.connect(("a3.pm", 5222))
        print ("User "+ jid + " Connected " )
        xmpp.process(block=False)
        
        ConBtn.config(text="Connected !",bg="green",fg='white')
    except:
        ConBtn.config(text=" Not Connected ! ",bg="white",fg='black')
        print("Unable to connect.")
def ClickConnect():
    th1 = threading.Thread(target=Connect())
    th1.start()
def SenderClick():
    tmp = sendText.get()
    fenetre.ecran.insert(INSERT, "You said : "+tmp+"\n")
    th2 = threading.Thread(target=xmpp.send_message(mto=RecipientGUI.get(), mbody=sendText.get(), mtype='chat'))
    sendText.delete(0, "end")
    th2.start()
    #sendText.delete(0.0, END)
def ClickSendVoice():
    msg_data = RecognitionToText(radio.get())
    #msg_data=" Hi this frome recoding Talk "
    #ConBtnVoice.config(text="Recording Voice ...",fg="green")
    if(msg_data):
        th3 = threading.Thread(target=xmpp.send_message(mto=RecipientGUI.get(), mbody=msg_data, mtype='voice'))
        th3.start()
        ConBtnVoice.config(text=" Talk Again & send ",fg="green")
def selection():  
   
   switcher = {
        'en': "English",
        'fr': "Francais",
        'de': "Deutsch",
        'it': "Italien"
    }
   selection = " Selected Language: " + switcher.get(radio.get())
   label.config(text = selection)
def RecognitionToText(lang="DE"):
    #instance of recognizer class
    r = sr.Recognizer()
    ConBtnVoice.config(text="Recording Voice ...",fg="green")
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
        #LanguageDetect(text_recognitized)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text_recognitized
if __name__ == '__main__':
    ########## Input ####
    ####User1
    labelUsername = Label(fenetre, text="Username :")
    labelUsername.pack()
    labelUsername.place(bordermode=OUTSIDE, height=30, width=100, x=20, y=30)
    var_texte = StringVar()
    var_texte.set("user100@a3.pm")
    UsernameGUI = Entry(fenetre, textvariable=var_texte)
    UsernameGUI.pack()
    UsernameGUI.place(bordermode=OUTSIDE, height=30, width=150, x=110, y=30)
    #### Password
    labelPassword = Label(fenetre, text="Password :")
    labelPassword.pack()
    labelPassword.place(bordermode=OUTSIDE, height=30, width=100, x=20, y=70)
    var_pwd = StringVar()
    var_pwd.set("pass12345")
    PasswordGUI = Entry(fenetre, textvariable=var_pwd,show='*')
    PasswordGUI.pack()
    PasswordGUI.place(bordermode=OUTSIDE, height=30, width=100, x=110, y=70)
    ####Recipient
    labelRecipient = Label(fenetre, text="Recipient (to) :")
    labelRecipient.pack()
    labelRecipient.place(bordermode=OUTSIDE, height=30, width=100, x=20, y=110)
    var_recp = StringVar()
    var_recp.set("test100@a3.pm")
    RecipientGUI = Entry(fenetre, textvariable=var_recp)
    RecipientGUI.pack()
    RecipientGUI.place(bordermode=OUTSIDE, height=30, width=150, x=110, y=110)
    ########Button Event
    ConBtn = Button(fenetre, text="Connection", fg="red",command=ClickConnect)
    ConBtn.pack()
    ConBtn.place(bordermode=OUTSIDE, height=30, width=100, x=280, y=110)
    ##### Menu Language ###########
    radio = StringVar() 
    radio.set("en") 
    #lbl = Label(text = "Favourite programming language:")  
    #lbl.pack()  
    R1 = Radiobutton(fenetre, text="EN", variable=radio, value='en',  
                    command=selection)  
    R1.pack( anchor = W,side=LEFT )  
    R1.place(bordermode=OUTSIDE, x=10, y=150)
    R2 = Radiobutton(fenetre, text="FR", variable=radio, value='fr',  
                    command=selection)  
    R2.pack( anchor = W,side=LEFT )  
    R2.place(bordermode=OUTSIDE, x=60, y=150)
    
    R3 = Radiobutton(fenetre, text="DE", variable=radio, value='de',  
                    command=selection)  
    R3.pack( anchor = W,side=LEFT)
    R3.place(bordermode=OUTSIDE, x=110, y=150)
    R4 = Radiobutton(fenetre, text="IT", variable=radio, value="it" , 
                    command=selection)  
    R4.pack( anchor = W,side=LEFT) 
    R4.place(bordermode=OUTSIDE, x=160, y=150)
    
    label = Label(fenetre,text="Default Language: English")
    label.pack()     
    label.place(bordermode=OUTSIDE, height=30, width=180, x=200, y=150)
    ####### TExt Box
    fenetre.ecran = Text(fenetre, wrap=WORD, highlightcolor="green", insertbackground="white", fg="black", bg="white")
    s1 = Scrollbar(fenetre, orient=VERTICAL)
    s1.config(command=fenetre.ecran.yview)
    fenetre.ecran.config(yscrollcommand=s1.set)
    fenetre.ecran.pack()
    fenetre.ecran.place(bordermode=OUTSIDE, height=200, width=350, x=20, y=180)
    ###### Button Event Voice 
    ConBtnVoice = Button(fenetre, text="Talk with Voice", fg="red",command=OnclickVoice)
    ConBtnVoice.pack()
    ConBtnVoice.place( height=30, width=350, x=20, y=430)

    

    var_texte2 = StringVar()
    sendText = Entry(fenetre, textvariable=var_texte2)
    sendText.pack()
    sendText.place(bordermode=OUTSIDE, height=30, width=290, x=20, y=390)
    fenetre.boutonSend = Button(fenetre, text="Send",fg="Green",command=onclick)
    fenetre.boutonSend.pack()
    fenetre.boutonSend.place(bordermode=OUTSIDE, height=30, width=50, x=320, y=390)
    ################# XMPP Instance 
    
  
    

    fenetre.mainloop()
    fenetre.destroy()