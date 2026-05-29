import streamlit as st
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "assignment_db"

@st.cache_resource
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def get_collection(name):
    return get_db()[name]
