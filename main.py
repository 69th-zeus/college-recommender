import numpy as np
import pandas as pd
import streamlit as st

st.title('JEE College Predictor')
#load data frame
df = pd.read_excel('2024Round5.xlsx')

#get all the category and gender divisions
category = list(df[df['Institute'].str.contains('Indian Institute of Technology')]['Seat Type'].value_counts().index)
selected_category = st.selectbox("Select Category Of Seat To be Shown", category)

gender = list(df[df['Institute'].str.contains('Indian Institute of Technology')]['Gender'].value_counts().index)
selected_gender = st.selectbox("Select Gender Category Of Seat To be Shown", gender)

rank = st.number_input('Enter your JEE Advanced Rank')
data_points= st.number_input('Enter number of Considerable Options you would like to see (Above 100 Ideally)', value = 100, min_value= 100, max_value= 99999, step = 1)

# process data and show results
temp = df[(df['Institute'].str.contains('Indian Institute of Technology'))]
temp['Closing Rank'] = pd.to_numeric(temp['Closing Rank'], errors='coerce')
temp.dropna(subset=['Closing Rank'], inplace=True)
temp = temp[temp['Seat Type'] == selected_category]
temp = temp[temp['Gender'] == selected_gender]
temp = temp[temp['Closing Rank'] > 0.95 * rank]
temp = temp.sort_values(by = 'Closing Rank')
st.dataframe(temp.head(data_points))