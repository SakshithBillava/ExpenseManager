import streamlit as st
import streamlit_authenticator as stauth
import pymongo
import database as dbase
import updation as upd
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_custom_notification_box import custom_notification_box as scnb

st.markdown('''# ****EXPENSE MANAGER****
Manage all your Expenses here''')
login = Image.open("login.jpg")
names = ['sakshith','shaun','abcd']
usernames = ['sakshith2002','rds','abd17']
password = ['2002','2001','2003']

def update():
    print("Entered update")
    st.session_state.confirm_add_user = True
    if(st.session_state.confirm_add_user==True and len(st.session_state.l)==3):
        upd.update_user(st.session_state.l[0],st.session_state.l[1],st.session_state.l[2])
        st.sidebar.success("New user aded successfully")
        st.sidebar.warning("LOGIN TO CONTINUE")
        st.session_state.confirm_add_user = False
        


@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])
client = pymongo.MongoClient("mongodb+srv://sakshith2002:admin@cluster0.frpdmtc.mongodb.net/?retryWrites=true&w=majority")
    
db = client.Expenses
collecion2 = db.user_credentials
#st.session_state.get_cred = client.Expenses
st.session_state.get_cred_item = list(db.user_credentials.find())
#print(st.session_state.get_cred_item)
#update("rds","shaun","2001")
#print(hashed)
d = {}
d2 = {}
#for i in range(len(usernames)):
#    d1 = {}
#    d1["name"] = names[i]
#    d1["password"] = hashed[i]
#    d2[usernames[i]] = d1

#d["usernames"] = d2
#"$2b$12$G7dOhRBS4FP7g1cPYORbTuYtEm8TvKgr5bCOGVgJyfucpogEMSFHO"
#$2b$12$TErpIHkdK0k7B7JQS6dlMevhry4hduFo3rtTN6UW800B7wgRA8Xy6
#print(d)

if "login" not in st.session_state:
    st.session_state.login = True


credentials = {
        "usernames":{
            "sakshith2002":{
                "name":"sakshith",
                "password":"$2b$12$rbxvsBlUCM3JjGgxZ0gyIePWvd6i4oPZZVhuPQmcEsJQEF9NiCfuW"
                },
            "rds":{
                "name":"shaun",
                "password":"$2b$12$TErpIHkdK0k7B7JQS6dlMevhry4hduFo3rtTN6UW800B7wgRA8Xy6"
                },
            "abd17":{
                "name":"abcd",
                "password":"$2b$12$wVuLlVVrnaOzlffdgI5Tz.4TSjqs8hUdOAYNlSeWOj5V5mVXub3Rq"
            }            
            }
        }

authenticator = stauth.Authenticate(credentials,"expense_cookie","abcdef",cookie_expiry_days=1)
if "input_display" not in st.session_state:
    st.session_state.input_display = True
def add_new_user(): 
    if(st.session_state.display and st.session_state.input_display and st.session_state.isLogged==False):
        st.session_state.l = []
        st.session_state.name = st.text_input("Enter your Name",key = 1)
        st.session_state.username = st.text_input("Enter your Username",key = 2)
        st.session_state.password = st.text_input("Enter the Password",key = 3, type = "password")
        if(st.session_state.username!="" and st.session_state.name!="" and st.session_state.password!=""):
            st.session_state.l.append(st.session_state.username)
            st.session_state.l.append(st.session_state.name)
            st.session_state.l.append(st.session_state.password)
        if(st.button("SIGN UP") and len(st.session_state.l)==3):
            st.session_state.input_display = False
            update()
            #st.warning("LOGIN TO CONTINUE")
        
         
    
    #if(st.session_state.confirm_add):
    #    st.warning("LOGIN TO CONTINUE")
if "isLogged" not in st.session_state:
    st.session_state.isLogged = False
with st.sidebar:
    selected = option_menu("User Menu", ["Home","Login", 'Sign Up(New user)'], 
        icons=["house",'unlock', ' '], menu_icon="cast",default_index = 0)
    
    if "confirm_add_user" not in st.session_state:
        st.session_state.confirm_add_user = False
    if "display" not in st.session_state:
        st.session_state.display = False
    if(len(selected)!=0):
        st.session_state.display = True
    
    if(selected=="Sign Up(New user)" and st.session_state.display):
        #st.session_state.input_display = True
        if(st.session_state.isLogged == True):
            st.warning("PLEASE LOGOUT TO ADD NEW USER")
        if(st.session_state.input_display == False):
            st.success("LOGIN TO CONTINUE")
            st.warning("User already added")
        st.session_state.added = add_new_user()
    
    elif(selected=="Login"):
        #authenticator = stauth.Authenticate(credentials,"expense_cookie","abcdef",cookie_expiry_days=1)

        name,authentication_status,username = authenticator.login("login","main")
        if(authenticator.logout("LOGOUT","sidebar")):
            #print("yes")
            st.session_state.login = False
            st.session_state.isLogged = False
            #print("AU_ST: ", authentication_status)

        if(authentication_status):
            st.session_state.isLogged = True
            st.write("SUCCESSFULLY LOGGED IN")
        else:
            st.session_state.isLogged = False
            st.write("Logged Out")
        #@st.experimental_singleton  
        
        collecion1 = db.myexpense

print(st.session_state.isLogged)


