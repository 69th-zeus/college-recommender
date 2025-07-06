import pandas as pd
import streamlit as st
from math import ceil

st.set_page_config(layout="wide")
#load data frame
df = pd.read_csv('result.csv')

JEE_MAINS = df[df['Exam'] == 'JEE Mains']['Institute'].unique().tolist()
JEE_MAINS.sort()
JEE_MAINS.insert(0, 'Show Me All')

JEE_ADV = df[df['Exam'] == 'JEE Advanced']['Institute'].unique().tolist()
JEE_ADV.sort()
JEE_ADV.insert(0, 'Show Me All')

EXAM = ['JEE Mains', 'JEE Advanced']
GENDER = ['Show Me All', 'Gender-Neutral', 'Female-only', 'Female-only (including Supernumerary)']
TYPE = ['Show Me All', 'IIT','NIT', 'IIIT', 'GFTI']
SIDEBAR = ['JEE', 'NEET']
YEARS = [2024, 2023, 2022, 2021]
SEAT_TYPE = [ 'Show Me All', 'EWS', 'OBC-NCL', 'OPEN', 'OPEN (PwD)', 'SC', 'ST', 'OBC-NCL (PwD)', 'EWS (PwD)', 'ST (PwD)', 'SC (PwD)']
QUOTA = ['Show Me All', 'AI', 'HS', 'OS', 'GO', 'JK', 'LA']

def main():
    st.sidebar.title("Select Your Browsing Method")
    mode = st.sidebar.selectbox('Select Mode',SIDEBAR, placeholder = 'Choose an Option', label_visibility="collapsed")

    if mode == 'JEE':
        jee()
    elif mode == 'Rank Based Recommendation':
        # neet()
        pass

def jee():
    st.title('JEE College Recommender')

    # Initialize Page
    st.title("🎓 Browse Colleges")

    st.write('The Looking Around page lets users explore available colleges based on their preferences. You can select the exam type (JEE Mains or Advanced), quota, gender, and institute type to filter results. It also allows you to choose specific years to view past cutoffs. The results are displayed in organized tables for each selected year. This feature helps users understand seat distributions without needing to input a rank.')

    # Get Variables
    exam = st.selectbox('Select Exam (JEE Mains or JEE Advanced)', EXAM, placeholder='Choose An Option')
    seat_type = st.selectbox('Select Your Seat Type (You May Skip)', SEAT_TYPE)
    gender = st.selectbox('Select Gender Type of Seats You would like to see (You May Skip)', GENDER)
    institute_type = st.selectbox('Select The type Of Institute You Would Like to See', TYPE)
    quota = st.selectbox('Select Quota of Seat to be Shown', QUOTA, placeholder='Show Me All')
    if exam == 'JEE Mains':
        institute_name = st.selectbox('Select College To View Data (You May Skip)', JEE_MAINS,placeholder='Show Me All')
    elif exam == 'JEE Advanced':
        institute_name = st.selectbox('Select College To View Data (You May Skip)', JEE_ADV,placeholder='Show Me All')
    rank = st.number_input('Enter Your Rank (You May Skip by Entering 0)', min_value=0, step=1, placeholder=0)
    cutoff = st.number_input("Cutoff threshold (% of your rank) to widen or narrow the seats which you 'may' get.", min_value=0, step = 1, placeholder=10)
    st.write("Show Data For - ")
    year_checks = {year: st.checkbox(str(year)) for year in YEARS}

    #Process Data To Show
    temp = df[df['Exam'] == exam]
    if seat_type != 'Show Me All':
        temp = temp[temp['Seat Type'] == seat_type]
    if gender != 'Show Me All':
        temp = temp[temp['Gender'] == gender]
    if institute_type != 'Show Me All':
        temp = temp[temp['Type'] == institute_type]
    if quota != 'Show Me All':
        temp = temp[temp['Quota'] == quota]
    if rank != 0:
        temp = temp[temp['Closing Rank (Last Round)'] > (1 + ceil(cutoff/100) * rank)]
        temp.sort_values(by = 'Opening Rank (First Round)')

    if temp.shape[0] == 0:
        st.error("The Selected Variation has no Seats to Display")
    else:
        st.write("Below are the highly proable seats")
        for year, checked in year_checks.items():
            if checked:
                st.title(f"{year}'s Data")
                st.dataframe(temp[temp['Year'] == year].reset_index(drop=True), use_container_width=True)


main()