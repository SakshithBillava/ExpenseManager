import pymongo
#import streamlit as st 

#@st.experimental_singleton  
#def init_connection():
#    return pymongo.MongoClient(**st.secrets["mongo"])
client = pymongo.MongoClient("mongodb+srv://sakshith2002:admin@cluster0.frpdmtc.mongodb.net/?retryWrites=true&w=majority")

db1 = client.Expenses
collections1 = db1.user_credentials

def addUser(username,name,password):
    if(len(username)!=0 and len(name)!=0 and len(password)!=0):
        item = {
            "names": name,
            "username": username,
            "password": password
        }
        collections1.insert_one(item)