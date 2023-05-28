import streamlit as st
import pandas as pd
import numpy as np
from bokeh import plotting
from plotting import figure
import streamlit_authenticator as stauth
import pymongo
import database as dbase
import updation as upd
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_custom_notification_box import custom_notification_box as scnb
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 


original_title = '<p style="font-family:Bodoni MT Black; color:white; font-size: 60px;">EXPENSE MANAGER</p>'
st.markdown(original_title,unsafe_allow_html=True)

login = Image.open("login.jpg")
#names = ['sakshith','shaun','abcd']
#usernames = ['sakshith2002','rds','abd17']
#password = ['2002','2001','2003']

bckg_img = """
<style> 
[data-testid = "stAppViewContainer"] {
background-image: url("https://wallpaperaccess.com/full/2200497.jpg");
background-size = cover;
}

</style>
"""
#st.markdown(bckg_img, unsafe_allow_html=True)

def update():
    st.session_state.confirm_add_user = True
    if(st.session_state.confirm_add_user==True and len(st.session_state.l)==3):
        upd.update_user(st.session_state.l[0],st.session_state.l[1],st.session_state.l[2])
        st.sidebar.success("New user aded successfully")
        st.sidebar.warning("LOGIN TO CONTINUE")
        
        st.session_state.category_dict = {
                "Username": st.session_state.username,
                "Food": 0,
                "Rent": 0,
                "Lifestyle": 0,
                "Travel": 0
            }
        collection4.insert_one(st.session_state.category_dict)
        st.session_state.confirm_add_user = False
        


@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])
client = pymongo.MongoClient("mongodb+srv://sakshith2002:admin@cluster0.frpdmtc.mongodb.net/?retryWrites=true&w=majority")

db = client.Expenses
collection2 = db.user_credentials
st.session_state.get_cred_item = list(db.user_credentials.find())
collection3 = db.user_expenses
st.session_state.get_user_data = list(db.user_expenses.find())
collection4 = db.user_expense_data
st.session_state.get_user_portfolio = list(db.user_expense_data.find())

if "username" not in st.session_state:
    st.session_state.username = ""
st.session_state.current_user_portfolio = []
for i in st.session_state.get_user_portfolio:
    if(st.session_state.username==i['Username']):
        st.session_state.current_user_portfolio.append(i)

if "was_logged_in" not in st.session_state:
    st.session_state.was_logged_in = False



d = {}
d2 = {}
for i in st.session_state.get_cred_item:
    d1 = {}
    d1["name"] = i['names']
    d1["password"] = i['password']
    d2[i['username']] = d1

d["usernames"] = d2

st.session_state.list_of_usernames = []
for i in st.session_state.get_cred_item:
    st.session_state.list_of_usernames.append(i['username'])

#print(st.session_state.list_of_usernames)

if "login" not in st.session_state:
    st.session_state.login = True


credentials = {
        "usernames":{
            "sakshith2002":{
                "name":"sakshith",
                "password":"$2b$12$EsUyWrvHb.JUaz5L8G8x6uG5zi73ZhxS7Dhn61IwlQJqwGzJns.Ea"
                },
            "rds":{
                "name":"shaun",
                "password":"$2b$12$TErpIHkdK0k7B7JQS6dlMevhry4hduFo3rtTN6UW800B7wgRA8Xy6"
                },
            "hg":{
                "name":"abcd",
                "password":"$2b$12$CSi12pOLeLmDTeZZDitQYuY8tEGGpS85l5awPuDluYq5WPDUFkVRu"
            }            
            }
        }

st.session_state.authenticator = stauth.Authenticate(d,"expense_cookie","abcdef",cookie_expiry_days=10)
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
    st.session_state.selected = option_menu("User Menu", ["Home","Login", 'Sign Up(New user)',"About"], 
        icons=["house",'unlock', 'person',"info"], menu_icon="cast",default_index = 1)
    
    if "confirm_add_user" not in st.session_state:
        st.session_state.confirm_add_user = False
    if "display" not in st.session_state:
        st.session_state.display = False
    if(len(st.session_state.selected)!=0):
        st.session_state.display = True
    
    if(st.session_state.selected=="Sign Up(New user)" and st.session_state.display):
        #st.session_state.input_display = True
        if(st.session_state.isLogged == True):
            st.warning("PLEASE LOGOUT TO ADD NEW USER")
        if(st.session_state.input_display == False):
            st.success("LOGIN TO CONTINUE")
            st.warning("User already added")
        st.session_state.added = add_new_user()

    elif(st.session_state.selected == "About"):
        text = '<p style=" color:white; font-size: 15px;"><b>This is an Expenser Manager <br> where you can manage all your<br>expense in one place.</b></p>'
        st.markdown(text,unsafe_allow_html=True)
        
    
    elif(st.session_state.selected=="Login"):
        #authenticator = stauth.Authenticate(credentials,"expense_cookie","abcdef",cookie_expiry_days=1)

        st.session_state.name,st.session_state.authentication_status,st.session_state.username = st.session_state.authenticator.login("login","main")
        if(st.session_state.authenticator.logout("LOGOUT","sidebar")):
            st.session_state.login = False
            st.session_state.isLogged = False
            st.session_state.was_logged_in = False

        if(st.session_state.authentication_status):
            st.session_state.isLogged = True
            st.session_state.was_logged_in = True
            st.success("SUCCESSFULLY LOGGED IN")
            st._main.success("Welcome " + st.session_state.name)
            st.balloons()
        else:
            st.session_state.isLogged = False
            st.write("Logged Out")
        #@st.experimental_singleton  
        collection1 = db.myexpense

if(st.session_state.authentication_status and st.session_state.selected=="Login"):
    #login_success = Image.open("login_success.png")
    #st.image(login_success)
    bckg_img_for_login = """
    <style>
    [data-testid = "stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/9486675/pexels-photo-9486675.jpeg?cs=srgb&dl=pexels-rocketmann-team-9486675.jpg&fm=jpg");
    background-size: cover;
    }
    [data-testid = "stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    [data-testid = "stToolbar"]{
    right: 2rem;
    }
    </style>
    """
    st.markdown(bckg_img_for_login,unsafe_allow_html=True)
    
elif(st.session_state.isLogged==False and st.session_state.selected=="Login"):
    bckg_img_for_login = """
    <style>
    [data-testid = "stAppViewContainer"] {
    background-image: url("https://i.ibb.co/zS7XKNR/login-to-continue-1.png");
    background-size = cover;
    }
    [data-testid = "stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    [data-testid = "stToolbar"]{
    right: 2rem;
    }
    </style>
    """
    st.markdown(bckg_img_for_login, unsafe_allow_html=True)
elif(st.session_state.selected=="Sign Up(New user)"):
    #sign_up = Image.open("sign_up.png")
    #sign_up_text = Image.open("sign_up_text.jpg")
    #st.image(sign_up)
    #st.image(sign_up_text) 
    bckg_img_for_sign_up = """
    <style>
    [data-testid = "stAppViewContainer"] {
    background-image: url("https://i.ibb.co/b3KC8xG/PLEASE-SIGN-UP-1-1.png");
    background-size : cover;
    }
    [data-testid = "stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    [data-testid = "stToolbar"]{
    right: 2rem;
    }
    </style>
    """ 
    st.markdown(bckg_img_for_sign_up,unsafe_allow_html=True)
if(st.session_state.selected=="Home" and st.session_state.isLogged==False):
    bckg_img_for_home = """
    <style>
    [data-testid = "stAppViewContainer"] {
    background-image: url("https://img.freepik.com/premium-vector/success-money-motivational-quotes-white-black-background-vector-script-lettering-as-t-shirt-print-poster-banner-greeting-card-time-is-money-keep-calm-business-finance-concept_504907-329.jpg?w=2000");
    background-size : cover;
    }
    [data-testid = "stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    [data-testid = "stToolbar"]{
    right: 2rem;
    }
    </style>
    """ 
    st.markdown(bckg_img_for_home,unsafe_allow_html=True)

if "click" not in st.session_state:
    st.session_state.click = False

if "goOn" not in st.session_state:
    st.session_state.goOn = False

def callback():
    st.session_state.click = True


def Commit():
    st.session_state.click = False
    st.session_state.confirm = True
    if(st.session_state.confirm):
        collection3.insert_one(st.session_state.item)
        st.session_state.goOn = True
        st.session_state.confirm = False
        
def Commit_user_expense_data(case,updated_value):
    if(case==1):
        st.session_state.new_data = {"$set": {"Food": updated_value}}
        collection4.update_one(st.session_state.previous_query,st.session_state.new_data)
    elif(case==2):
        st.session_state.new_data = {"$set": {"Rent": updated_value}}
        collection4.update_one(st.session_state.previous_query,st.session_state.new_data)
    elif(case==3):
        st.session_state.new_data = {"$set": {"Lifestyle": updated_value}}
        collection4.update_one(st.session_state.previous_query,st.session_state.new_data)
    elif(case==4):
        st.session_state.new_data = {"$set": {"Travel": updated_value}}
        collection4.update_one(st.session_state.previous_query,st.session_state.new_data)

def cancel_clicked():
    st.session_state.click = False

if "proceed_with_user_expense_data" not in st.session_state:
    st.session_state.proceed_with_user_expense_data = False

if(st.session_state.authentication_status==True and st.session_state.selected =="Home" ):
    if(st.button("CLICK HERE TO ADD YOUR EXPENSE OR INCOME",on_click=callback) or st.session_state.click):
        st.button("CANCEL",on_click=cancel_clicked)
        options = ["Income","Expenditure"]
        def Income():
            st.session_state.option = 1
        def Expenditure():
            st.session_state.option = 0
        type = st.radio("Select the appropriate",options=options)
        if(type=="Income"):
            Income()
        else:
            Expenditure()
        if(st.session_state.option==0):
            category = ["Food","Rent","Lifestyle","Travel"]
            st.session_state.category_input = st.radio("Select the category",options=category)
        if(st.session_state.option==1):
            st.session_state.income = st.number_input("Enter the income amount")
        else:
            st.session_state.expense = st.number_input("Enter the expense amount")
        st.session_state.date = st.date_input("Date of transaction")
        st.session_state.date = st.session_state.date.strftime('%m/%d/%Y')

        if(st.session_state.option==1):
            st.session_state.item = {
                "Username": st.session_state.username,
                "Option": st.session_state.option,
                "Category": "NA",
                "Amount": st.session_state.income,
                "Date": st.session_state.date
            }
        elif(st.session_state.option==0): 
            st.session_state.item = {
                "Username": st.session_state.username,
                "Option": st.session_state.option,
                "Category": st.session_state.category_input,
                "Amount": st.session_state.expense,
                "Date": st.session_state.date
            }

        st.button("CONFIRM",on_click=Commit)

def done():
    if(st.session_state.option==0):
        if(st.session_state.category_input=="Food"):
            st.session_state.previous_query = {"Username": st.session_state.username,"Food": st.session_state.current_user_portfolio[0]["Food"]}
            st.session_state.updated_food_cost = st.session_state.current_user_portfolio[0]["Food"] + st.session_state.expense
            case=1
            Commit_user_expense_data(case,st.session_state.updated_food_cost)
            st.session_state.goOn=False
        elif(st.session_state.category_input=="Rent"):
            st.session_state.previous_query = {"Username": st.session_state.username,"Rent": st.session_state.current_user_portfolio[0]["Rent"]}
            st.session_state.updated_rent_cost = st.session_state.current_user_portfolio[0]["Rent"] + st.session_state.expense
            case=2
            Commit_user_expense_data(case,st.session_state.updated_rent_cost)
            st.session_state.goOn=False
        elif(st.session_state.category_input=="Lifestyle"):
            st.session_state.previous_query = {"Username": st.session_state.username,"Lifestyle": st.session_state.current_user_portfolio[0]["Lifestyle"]}
            st.session_state.updated_lifestyle_cost = st.session_state.current_user_portfolio[0]["Lifestyle"] + st.session_state.expense
            case=3
            Commit_user_expense_data(case,st.session_state.updated_lifestyle_cost)
            st.session_state.goOn=False
        elif(st.session_state.category_input=="Travel"):
            st.session_state.previous_query = {"Username": st.session_state.username,"Travel": st.session_state.current_user_portfolio[0]["Travel"]}
            st.session_state.updated_travel_cost = st.session_state.current_user_portfolio[0]["Travel"] + st.session_state.expense
            case=4
            Commit_user_expense_data(case,st.session_state.updated_travel_cost)
            st.session_state.goOn=False

if(st.session_state.goOn==True):
    done()
    


#print(st.session_state.username)
#print(st.session_state.get_user_data)
st.session_state.current_user_data = []
for i in st.session_state.get_user_data:
    if(i["Username"]==st.session_state.username):
        st.session_state.current_user_data.append(i)

#print(st.session_state.current_user_data)
st.session_state.user_budget = 0
for i in st.session_state.current_user_data:
    if(i['Option']==1):
        st.session_state.user_budget += i['Amount']
#print(st.session_state.user_budget)

st.session_state.category_dict = {}
st.session_state.user_dataframe = pd.DataFrame.from_dict(st.session_state.current_user_data)

for i in st.session_state.current_user_portfolio:
    st.session_state.category_dict["Food"] = i["Food"]
    st.session_state.category_dict["Rent"] = i["Rent"]
    st.session_state.category_dict["Lifestyle"] = i["Lifestyle"]
    st.session_state.category_dict["Trvel"] = i["Travel"]

        
st.session_state.users_expense_category = []
st.session_state.users_expense_amounts = []
sizes = st.session_state.users_expense_amounts
labels = st.session_state.users_expense_category 
for i,j in st.session_state.category_dict.items():
    st.session_state.users_expense_category.append(i)
    st.session_state.users_expense_amounts.append(j)

#print(st.session_state.users_expense_category)
#print(st.session_state.users_expense_amounts)
if(st.session_state.selected=="About"):
    bckg_img_for_about = """
    <style>
    [data-testid = "stAppViewContainer"] {
    background-image: url("https://w0.peakpx.com/wallpaper/730/772/HD-wallpaper-dollars-dark-money-us-dollars-us.jpg");
    background-size : auto;
    }
    [data-testid = "stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    [data-testid = "stToolbar"]{
    right: 2rem;
    }
    </style>
    """ 
    st.markdown(bckg_img_for_about,unsafe_allow_html=True)


try:
    if(len(st.session_state.users_expense_amounts)!=0 and st.session_state.selected=="Home"):
        col1,col2,col3 = st.columns(3)
        coll1,coll2,coll3 = st.columns(3)
        st.session_state.total_expense = sum(sizes)
        st.session_state.budget_left = st.session_state.user_budget-st.session_state.total_expense
        st.session_state.budget_percentage_left = f'{(st.session_state.budget_left*100)/st.session_state.user_budget}%'
        st.session_state.budget_percentage_spent = f'{(st.session_state.total_expense*100)/st.session_state.user_budget}%'
        col1.metric("TOTAL BUDGET",st.session_state.user_budget,'100%')
        col2.metric("TOTAL SPENT",st.session_state.total_expense,st.session_state.budget_percentage_spent)
        col3.metric("BUDGET LEFT",st.session_state.budget_left,st.session_state.budget_percentage_left)
        coll1.metric("BUDGET SPENT PERCENTAGE",st.session_state.budget_percentage_spent)
        coll2.metric("BUDGET LEFT PERCENTAGE",st.session_state.budget_percentage_left)
        if(st.session_state.total_expense>st.session_state.user_budget):
            """ALERT!! 
               Your budget has gone over limit"""
        
        cols = st.columns([1, 1])
        with cols[0]:
            fig1 = px.pie(values=sizes,names=labels,hover_name=labels)
            fig1.update_layout(margin = dict(l=1,r=1,b=1,t=1),width=400,height=400 ,font=dict(color='#383635',size=15))
            st.write(fig1)

        with cols[1]:
            ll = []
            ll.append(sizes)
            chart_data = pd.DataFrame(
            np.array(ll),
            columns=labels)

            st.bar_chart(chart_data)

        dict_of_items = {}
        dict_of_items['Category'] = labels
        dict_of_items['Amount Spent'] = sizes
        new_df = pd.DataFrame.from_dict(dict_of_items)
        new_df = new_df.set_index('Category')
        fig4 = st.bar_chart(new_df,height=400,width=100,)
            

        updated_df = st.session_state.user_dataframe.drop('_id',axis=1)
        st.table(updated_df)

except KeyError as e:
    pass    
except ZeroDivisionError as er:
    pass
    
        
 
        


