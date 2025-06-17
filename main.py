import numpy as np
import pandas as pd
import streamlit as st
from data import *

st.set_page_config(layout="wide")
st.title('JEE College Predictor')

#load data frame
df = pd.read_csv('result.csv')

#Select variables from the user
exam = st.selectbox('Select Exam (JEE Mains or JEE Advanced)', EXAM, placeholder='Choose An Option')

quota = st.selectbox('Select Your Quota (You May Skip)', QUOTA)

rank = st.number_input('Enter Rank', value = 0, step = 1)
relaxation = st.number_input('Enter Relaxtion (Up what Percent out of your rank would you want the results to be)', value = 5.00, step = 0.001)
relaxed_rank = rank * (1 - relaxation)

gender = st.selectbox('Select Gender Type of Seats You would like to see (You May Skip)', GENDER)

institute_type = st.selectbox('Select The type Of Institute You Would Like to See', TYPE)

temp = df[df['Exam'] == exam]
if quota != 'Show Me All':
    temp = temp[temp['Seat Type'] == quota]
if gender != 'Show Me All':
    temp = temp[temp['Gender'] == gender]
if institute_type != 'Show Me All':
    temp = temp[temp['Type'] == institute_type]

temp = temp[pd.to_numeric(temp['Closing Rank (Last Round)'], errors='coerce') > rank]
temp.sort_values(by = 'Closing Rank (Last Round)', inplace=True)

if temp.shape[0] == 0:
    st.error("The Selected Variation has no Seats to Display")
else:
    st.dataframe(temp, use_container_width=True)
    


# #get all the category and gender divisions
# category = list(df[df['Institute'].str.contains('Indian Institute of Technology')]['Seat Type'].value_counts().index)
# selected_category = st.selectbox("Select Category Of Seat To be Shown", category)

# gender = list(df[df['Institute'].str.contains('Indian Institute of Technology')]['Gender'].value_counts().index)
# selected_gender = st.selectbox("Select Gender Category Of Seat To be Shown", gender)

# rank = st.number_input('Enter your JEE Advanced Rank')
# data_points= st.number_input('Enter number of Considerable Options you would like to see (Above 100 Ideally)', value = 100, min_value= 100, max_value= 99999, step = 1)

# # process data and show results
# temp = df[(df['Institute'].str.contains('Indian Institute of Technology'))]
# temp['Closing Rank'] = pd.to_numeric(temp['Closing Rank'], errors='coerce')
# temp.dropna(subset=['Closing Rank'], inplace=True)
# temp = temp[temp['Seat Type'] == selected_category]
# temp = temp[temp['Gender'] == selected_gender]
# temp = temp[temp['Closing Rank'] > 0.95 * rank]
# temp = temp.sort_values(by = 'Closing Rank')
# st.dataframe(temp.head(data_points))