import streamlit as st
import pandas as pd
import pickle
import time
from preprocess import preprocess
from streamlit_extras.stylable_container import stylable_container

# PAGE CONFIGURATIONS
st.set_page_config(page_title="Titanic Survival Predictor", page_icon="🚢", layout="centered", initial_sidebar_state="collapsed")

top = """
        <style>
        .block-container {
                padding-top: 0rem;
                padding-bottom: 5rem;
                margin-top: 0rem;
        }
        </style>
        """
st.markdown(top, unsafe_allow_html=True)

btn = """
        <style>
        [data-testid="stBaseButton-secondaryFormSubmit"] {
                width: inherit;
        }
        a[class="st-emotion-cache-2fwri8 e16zdaao1"] {
                border: 1px solid white;
        }
        </style>
        """
st.markdown(btn, unsafe_allow_html=True)

hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide, unsafe_allow_html=True)

sidebar = """
        <style>
        [data-testid=stSidebar] {
                background-color: #243b48;
        }
        </style>
        """
st.markdown(sidebar, unsafe_allow_html=True)

toast = """
        <style>
        div[data-testid=stToast] {
                position: relative;
                width: 100%;
                background-color: #ffffff;
                box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
                padding-left: 25px;
        }

        [data-testid=toastContainer] {
                position: absolute;
                margin: 0 auto;
                margin-inline: auto;
                max-width: 350px;
                display: flex;
                justify-content: center;
        }
        [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                font-size: 16px;
                font-weight: 400;
                color: #24252d;
        }
        svg[data-baseweb="icon"] {
                color: #5d6164;
        }
        svg[data-baseweb="icon"]:hover {
                color: #5d6164;
        }
        </style>
        """
st.markdown(toast, unsafe_allow_html=True)

# TITLE
st.markdown("<h1 style='text-align: center; color: white;'>Can You Survive the Titanic?</h1>", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
        st.link_button("**Developer:** Ian Jure Macalisang", "https://github.com/ianjure", type="primary", use_container_width=True)
        b1_col, b2_col = st.columns(2)
        with b1_col:
                repo_button = st.link_button("SOURCE CODE", "https://github.com/ianjure/titanic-survivor-prediction", use_container_width=True)
        with b2_col:
                notebook_button = st.link_button("NOTEBOOK", "https://colab.research.google.com/github/ianjure/titanic-survivor-prediction/blob/master/Titanic_Survivor_Prediction_Notebook.ipynb", use_container_width=True)

# FORM
with stylable_container(
        key = "titanic_form",
        css_styles = """
        div[data-testid="stForm"] {
                background-color: #5c94af;
                box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
        }
        svg[title="open"] {
                color: white;
        }
        """
        ):
        with st.form("my_form"):
                name = st.text_input("NAME", "John Smith")
                class_col, status_col, sex_col = st.columns(3)
                with class_col:
                        pclass = st.selectbox("CLASS", ("1", "2", "3"))
                with status_col:
                        sp = st.selectbox("STATUS", ("Single", "Married"))
                with sex_col:
                        sex = st.selectbox("SEX", ("Male", "Female"))
                cabin_col, embarked_col = st.columns(2)
                with cabin_col:
                        cabin = st.selectbox("CABIN", ("A", "B", "C", "D", "E", "F", "G", "T"))
                with embarked_col:
                        embarked = st.selectbox("EMBARKED", ("Cherbourg", "Queenstown", "Southampton"))
                col1, col2 = st.columns(2)
                with col1:
                        age = st.slider("AGE", 0, 100, 18)
                        par = st.slider("PARENTS", 0, 2, 0)
                with col2:
                        sib = st.slider("SIBLINGS", 0, 15, 0)
                        ch = st.slider("CHILDREN", 0, 15, 0)
                        
                if sp == "Married":
                        sibsp = sib + 1
                else:
                        sibsp = sib
                parch = par + ch

                with stylable_container(
                        key = "form_button",
                        css_styles = """
                        button[data-testid="baseButton-secondaryFormSubmit"] {
                                    width: inherit;
                                    color: white;
                                    background-color: #716144;
                                    border-color: #736345;
                        }
                        """
                ):
                        submitted = st.form_submit_button("SUBMIT")
                
                if submitted:
                        input = {'PassengerId': [1],
                                    'Pclass': [pclass],
                                    'Name': [name],
                                    'Sex': [sex],
                                    'Age': [age],
                                    'SibSp': [sibsp],
                                    'Parch': [parch],
                                    'Ticket': ['A'],
                                    'Fare': [32.20],
                                    'Cabin': [cabin],
                                    'Embarked': [embarked[0]]
                                    }
                        input_df = pd.DataFrame(input)
                        input_final = preprocess(input_df)
                        
                        model = pickle.load(open('model.pkl', 'rb'))
                        pred = model.predict_proba(input_final)

                        if pred[0][1] > 0.6:
                                  st.toast(f"{name.split(" ")[0]}, you have a **{round(pred[0][1] * 100)}%** chance of survival!", icon="😄")
                                  time.sleep(10)
                        else:      
                                  st.toast(f"{name.split(" ")[0]}, you only have a **{round(pred[0][0] * 100)}%** chance of survival!", icon="😭")
                                  time.sleep(10)
