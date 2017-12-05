# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:22:35 2017

@author: avhadsa
"""
#01 Train the Model : NRE - intent and Entities 

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
import simplejson

training_data = load_data('./../data/Transaction_RevereseHugeData1.json')
trainer = Trainer(RasaNLUConfig("./../config_spacy.json"))
trainer.train(training_data)
model_directory = trainer.persist('./')  # Returns the directory the model is stored in


#02 Test the model
                                 
from rasa_nlu.model import Metadata, Interpreter
from pprint import pprint
# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_directory, RasaNLUConfig("./../config_spacy.json"))

Output = interpreter.parse(u"reverse buy transaction with activity id 6784") #reverse buy transaction with activity id 6784

simplejson.dumps(Output)
pprint(Output)

#print(Output["intent"]["name"])
#print(Output["entities"])
#print(len(Output["entities"]))
#print(Output["entities"][0]["entity"])
#print(Output["entities"][0]["value"])
#print(Output["entities"][1]["entity"])


#03 check for all the parameters and values and ask question if not provided
#04 Call service
#05 Final output from Service

from rasa_nlu.model import Metadata, Interpreter
interpreter = Interpreter.load(model_directory, RasaNLUConfig("./../config_spacy.json"))

global context_rev_tran
global context

def RevereseTransaction(predictions):
    
    if predictions["intent"] is None:
        return "I did not understand. Please tell me again."
    
    if predictions["intent"]["name"] == "reverse_transaction" and  predictions["intent"]["confidence"] > 0.75:
        context_rev_tran["intent"] = "reverse_transaction"
        context = True
        if len(predictions["entities"]) == 0:
            context = False
            return "Activity ID and Transaction type is not provided. Please resubmit the complete request."
        if len(predictions["entities"]) == 1:
            if predictions["entities"][0]["entity"] == "Activity_ID":
                context_rev_tran["Activity_ID"] = predictions["entities"][0]["value"]
                while(True):
                    print("Please provide Transaction type")
                    y=input("Enter the message:");
                    if y.lower() == "buy" or y.lower() == "sell" or y.lower() == "free receipt":
                        context_rev_tran["Transaction_type"] = y
                        response = confirmToServiceCall()
                        return response
                
            if predictions["entities"][0]["entity"] == "Transaction_type":
                context_rev_tran["Transaction_type"] = predictions["entities"][0]["value"]
                while(True):
                    print("Please provide Activity ID")
                    y=input("Enter the message:");
                    try:
                        val = int(y)
                    except ValueError:
                        continue
                    else:
                        context_rev_tran["Activity_ID"] = y
                        response = confirmToServiceCall()
                        return response
                    
        if len(predictions["entities"]) == 2:
            if predictions["entities"][0]["entity"] == "Activity_ID":
                context_rev_tran["Activity_ID"] = predictions["entities"][0]["value"]
                if predictions["entities"][1]["entity"] == "Transaction_type":
                    context_rev_tran["Transaction_type"] = predictions["entities"][1]["value"]
                else:
                    return "There are more than one activity ids are provided. Please tell me again."
            if predictions["entities"][0]["entity"] == "Transaction_type":
                context_rev_tran["Transaction_type"] = predictions["entities"][0]["value"]
                if predictions["entities"][1]["entity"] == "Activity_ID":
                    context_rev_tran["Activity_ID"] = predictions["entities"][1]["value"]
                else:
                    return "There are more than one transaction types are provided. Please tell me again."            
            response = confirmToServiceCall()
            return response
        
        else:
            return "There are more than one activity ids or transaction types are provided. Please tell me again."        
    else:
        return "I did not understand. Please tell me again."


def confirmToServiceCall():
    while(True):
        print("Are you sure to reverse Activity# " + context_rev_tran["Activity_ID"] + " for " + context_rev_tran["Transaction_type"] + " transaction?")
        y=input("Enter the message:")
        if y.lower() == "yes":
            response = "Activity# " + context_rev_tran["Activity_ID"] + " for " + context_rev_tran["Transaction_type"] + " transaction" + " is reversed with Reversal Activity ID as 99999"
            context_rev_tran.clear()
            context = False
            return response
        if y.lower() == "no":
            response = "Activity# " + context_rev_tran["Activity_ID"] + " for " + context_rev_tran["Transaction_type"] + " transaction" + " is not reversed!"
            context_rev_tran.clear()
            context = False
            return response    

context = False
context_rev_tran = {}
while(True):
    x=input("Enter the message:");
    predictions = interpreter.parse(x)
    pprint(predictions)
    response = RevereseTransaction(predictions)
    print(response)

#simplejson.dumps()
