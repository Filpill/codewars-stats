import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Codewars Stats - Filpill')

@st.cache(allow_output_mutation=True)
def load_data(filename,nrows):
    data = pd.read_csv(filename, nrows=nrows)
    return data

# Loading in Raw Data
data_load_state = st.text('Loading data...')
raw_data = load_data('csv/codewars_request.csv',10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(raw_data)

# Creating Monthly Count
st.subheader('Monthly Count')
monthly = load_data('csv/monthly.csv',100)
st.bar_chart(monthly,x='Completed Date',y='Count')

# Rank Count
st.subheader('Rank Count')
rank = load_data('csv/rank.csv',100)
st.bar_chart(rank,x='Rank',y='Count')

# Category Count
st.subheader('Category Count')
category = load_data('csv/tags.csv',100)
st.bar_chart(category,x='Tags',y='Count')

# Language Count
st.subheader('Language Count')
language = load_data('csv/language.csv',100)
st.bar_chart(language,x='Languages',y='Count')