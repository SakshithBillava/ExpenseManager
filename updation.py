import database as dbase
import streamlit_authenticator as stauth

def update_user(username,name,password):
    l = [password]
    hashed = stauth.Hasher(l).generate()
    if(username!=""and name!="" and password!=""):
        dbase.addUser(username,name,hashed[0])