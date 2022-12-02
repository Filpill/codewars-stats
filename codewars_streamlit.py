import s3fs
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import altair as alt
import matplotlib.pyplot as plt

st.title('Codewars Stats - Filpill')
# @st.cache(allow_output_mutation=True)

def alt_bar_chart(data,x_label,y_label,x_size,y_size):
    st.write(alt.Chart(data).mark_bar().encode(
        x = alt.X(x_label,sort=None),
        y =y_label
        # ,
        # color=alt.Color('Rank',
        #                  scale=alt.Scale(
        #                  domain=data.sort_values(['Count'])['Rank'].tolist(),
        #                  range=['purple', 'blue', 'yellow', 'grey'])  
        #                    )
    ).properties(
        width = x_size,
        height = y_size
    ))

# Loading in Raw Data
date_str = date.today().strftime("%d-%b-%Y")
st.text(f'Data refreshed: {date_str}')
data_load_state = st.text('Loading data...')
raw_data_df = pd.read_csv(f"s3://codewarsdata/codewars_request.csv",index_col=0)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(raw_data_df)

# Creating Monthly Count
st.subheader('Monthly Count')
monthly = pd.read_csv(f"s3://codewarsdata/monthly.csv",index_col=0)
[x_label,y_label] = ['Completed Date','Count']
[x_size,y_size] = [800,300]
alt_bar_chart(monthly,x_label,y_label,x_size,y_size) 

# Rank Count
st.subheader('Rank Count')
rank = pd.read_csv(f"s3://codewarsdata/rank.csv",index_col=0)
[x_label,y_label] = ['Rank','Count']
[x_size,y_size] = [800,300]
st.write(alt.Chart(rank).mark_bar().encode(
    x = alt.X(x_label,sort=None),
    y =y_label
    ,
    color=alt.Color('Rank',
                     scale=alt.Scale(
                     domain=rank.sort_values(['Count'])['Rank'].tolist(),
                     range=['purple', 'blue', 'yellow', 'grey'])  
                       )
).properties(
    width = x_size,
    height = y_size
))

# Category Count
top = 20 #Taking top 20 categories
st.subheader(f'Category Count - Top {top}')
category = pd.read_csv(f"s3://codewarsdata/tags.csv",index_col=0)
category = category.iloc[::-1]
category = category.iloc[0:top] 
[x_label,y_label] = ['Tags','Count']
[x_size,y_size] = [800,400]
alt_bar_chart(category,x_label,y_label,x_size,y_size) 

# Language Count
st.subheader('Language Count')
language = pd.read_csv(f"s3://codewarsdata/language.csv",index_col=0)
[x_label,y_label] = ['Languages','Count']
[x_size,y_size] = [800,300]
alt_bar_chart(language,x_label,y_label,x_size,y_size) 