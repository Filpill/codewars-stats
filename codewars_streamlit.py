import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

st.title('Codewars Stats - Filpill')
# @st.cache(allow_output_mutation=True)

def alt_bar_chart(data,x_label,y_label,x_size,y_size):
    st.write(alt.Chart(data).mark_bar().encode(
        x = alt.X(x_label,sort=None),
        y =y_label
    ).properties(
        width = x_size,
        height = y_size
    ))
#---------------------------------------------------------------------------------------------

# Loading in Raw Data
date_str = date.today().strftime("%d-%b-%Y")
st.text(f'Data refreshed: {date_str}')
data_load_state = st.text('Loading data...')
raw_data_df = pd.read_csv(f"s3://codewarsdata/codewars_request.csv",index_col=0)
data_load_state.text("Done!")
# data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(raw_data_df)

#---------------------------------------------------------------------------------------------

# Creating Monthly Count
st.subheader('Monthly Aggregated Kata Completions')
monthly = pd.read_csv(f"s3://codewarsdata/monthly.csv",index_col=0)
[x_label,y_label] = ['Completed Date','Count']
[x_size,y_size] = [800,300]

monthly_chart = alt.Chart(monthly).mark_bar().encode(
        x = alt.X(x_label,sort=None,axis=alt.Axis(labelAngle=0)),
        y =y_label,
    ).properties(width = x_size, height = y_size, title = 'Monthly Kata Completions')

monthly_text = monthly_chart.mark_text(
            align='center',
            baseline='bottom',
            dx=0,
            ).encode(
                text=y_label
            )

st.write(
    monthly_chart + monthly_text
)

#---------------------------------------------------------------------------------------------

# Rank Count
st.subheader('Puzzle Difficulty Distribution')
rank = pd.read_csv(f"s3://codewarsdata/rank.csv",index_col=0)

# Creating Color Dictionary Based on Ranks
# Difficulty colors
white = '#e0e0de'
yellow = '#F4B831'
blue= '#3B7EBA'
purple= '#856DCC'

rank_colors ={
     '1 kyu' : purple
    ,'2 kyu' : purple
    ,'3 kyu' : blue
    ,'4 kyu' : blue
    ,'5 kyu' : yellow 
    ,'6 kyu' : yellow 
    ,'7 kyu' : white 
    ,'8 kyu' : white 
}
# Making color list for difficulties of Kata
rank_color_list =[]
unique_ranks = rank['Rank']
for r in unique_ranks:
    rank_color_list.append(rank_colors.get(r))

[x_label,y_label] = ['Rank','Count']
[x_size,y_size] = [800,300]

rank_chart = alt.Chart(rank).mark_bar().encode(
x = alt.X(x_label,sort=None,axis=alt.Axis(labelAngle=0)),
y =y_label,
color=alt.Color('Rank',
                scale=alt.Scale(
                domain=rank.sort_values(['Count'])['Rank'].tolist(),
                range=rank_color_list),
                legend=None
            )
    ).properties(width = x_size, height = y_size, title = 'Kata Rank Completion Distribution')

rank_text = rank_chart.mark_text(
            align='center',
            baseline='bottom',
            dx=0,
            ).encode(
                text=y_label
            )

st.write(
    rank_chart + rank_text
)

#---------------------------------------------------------------------------------------------

# Category Count
top = 15 #Taking top X categories
st.subheader(f'Top {top} - Categories of Kata Solved')
category = pd.read_csv(f"s3://codewarsdata/tags.csv",index_col=0)
category = category.iloc[::-1]
category = category.iloc[0:top] 
[x_label,y_label] = ['Tags','Count']
[x_size,y_size] = [800,400]

category_chart = alt.Chart(category).mark_bar().encode(
        x = alt.X(x_label,sort=None,axis=alt.Axis(labelAngle=-35)),
        y =y_label,
    ).properties(width = x_size, height = y_size, title = 'Categories of Kata')

category_text = category_chart.mark_text(
            align='center',
            baseline='bottom',
            dx=0,
            ).encode(
                text=y_label
            )

st.write(
    category_chart + category_text
)

#---------------------------------------------------------------------------------------------

# Language Count
st.subheader('Solved Kata Split by Programming Language')
language = pd.read_csv(f"s3://codewarsdata/language.csv",index_col=0)
col1,col2,col3 = st.columns(3)

base = alt.Chart(language).mark_arc().encode(
        theta=alt.Theta("Count",stack=True),
        color=alt.Color(field="Languages", type="nominal")
        ).properties(title = 'Programming Languages Utilised')

pie = base.mark_arc(outerRadius=150)
language_text = base.mark_text(
            radius = 175,
            size = 20
            ).encode(
                text=y_label
            )

with col1:
    st.write(' ')

with col2:
    st.write(
        pie + language_text
    )

with col3:
    st.write(' ')

#---------------------------------------------------------------------------------------------