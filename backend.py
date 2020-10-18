import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pyjokes
import wikipedia as wk


from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
#intents = json.loads(open('json/intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
intents = json.loads(open('json/intents.json').read())

with open('json/abbrevs.json') as f:
    data = json.load(f)

def reloadModel():
    global model, words, classes, intents
    model = load_model('chatbot_model.h5')
    words = pickle.load(open('words.pkl', 'rb'))
    classes = pickle.load(open('classes.pkl', 'rb'))
    intents = json.loads(open('json/intents.json').read())

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json, msg, varsDict):
    

    tag = ints[0]['intent']
    print(ints[0]['probability'])
    list_of_intents = intents_json['intents']
    result=""
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    #search up a joke
    if result == "//joke":
        result = pyjokes.get_joke()
    if result == "//help":
        result = "//help"
    #search wikepedia/google
    elif "search wiki" in msg:
        text = msg.replace("search wiki", "")
        result = wk.summary(text, sentences=3)
    #if msg isnt understood
    elif float(ints[0]['probability'])*100 < 88:
        result = "//confused"
    elif result == "":
        result = "oops im facing an error. tell danny about it please"
    

    #replace vars
    #example: %name%
    for key in varsDict:
        #print(key, varsDict[key])
        result = result.replace(key, varsDict[key])

    return result

def chatbot_response(msg, varsDict):
    #model = load_model('chatbot_model.h5')
#read json
    

#convert dict to list
    dictlist=[]
    for key, value in data.items():
        temp = [key,value]
        dictlist.append(temp)


    msg = msg.lower()

    # split the words based on whitespace
    sentence_list = msg.split()

    # make a place where we can build our new sentence
    new_sentence = []

    # look through each word 
    for word in sentence_list:
        # look for each candidate
        for candidate_replacements in dictlist:
            for candidate_replacement in candidate_replacements[1]:
            # if our candidate is there in the word
                if candidate_replacement == word:
                    # replace it 
                    word = word.replace(candidate_replacement, candidate_replacements[0])
                elif candidate_replacement == word[:len(candidate_replacement)] and word[len(candidate_replacement):] == word[len(candidate_replacement)]*len(word[len(candidate_replacement):]):
                    word = candidate_replacements[0]

        # and pop it onto a new list 
        new_sentence.append(word)


    msg = " ".join(new_sentence)


    ints = predict_class(msg, model)
    res = getResponse(ints, intents, msg, varsDict)
    return res

"""

#Creating GUI with tkinter
import tkinter
from tkinter import *


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("Hello")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()
"""
