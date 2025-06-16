import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport

df = pd.read_csv("35__welcome_survey_cleaned_comma.csv", index=False)
# df.to_csv("35__welcome_survey_cleaned_comma.csv", index=False)  # zapis z przecinkiem
df['gender'] = df['gender'].fillna('Inne').replace({0: 'M', 1: 'K'})

st.title("📊 Ankieta powitalna - analiza")
st.markdown("<br>", unsafe_allow_html=True)

def sidebar_filters(df):
    with st.sidebar:
        st.title("Filtruj")
        gender_options = ['Wszyscy'] + df['gender'].unique().tolist()
        selected_gender = st.radio("Wybierz płeć", gender_options)
        unique_ages = ['Wszyscy'] + sorted(df['age'].dropna().astype(str).unique().tolist())
        selected_age = st.selectbox("Wybierz wiek", unique_ages)
        animal_options = ['Wszyscy'] + df['fav_animals'].dropna().unique().tolist()
        selected_animal = st.selectbox("Wybierz zwierzę", animal_options)
        edu_level_options = ['Wszyscy'] + df['edu_level'].dropna().unique().tolist()
        selected_edu_level = st.radio("Wybierz poziom wykształcenia", edu_level_options)
        experience_options = ['Wszyscy'] + sorted(df['years_of_experience'].dropna().unique().tolist())
        selected_experience = st.selectbox("Wybierz lata doświadczenia", experience_options)
        industry_options = ['Wszyscy'] + df['industry'].dropna().unique().tolist()
        selected_industry = st.selectbox("Wybierz branżę", industry_options)
        taste_options = ['Wszyscy'] + df['sweet_or_salty'].dropna().unique().tolist()
        selected_taste = st.selectbox("Wybierz preferencję smakową", taste_options)
        if st.button("🔄 Resetuj filtry"):
            st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
        if st.button("🧑‍🚀 Wykonaj analizę ankiety"):
            profile = ProfileReport(df, title="Profilowanie danych", explorative=True)
            profile.to_file("output.html")
            with open("output.html", "rb") as file:
                st.download_button(label="Pobierz pełny raport jako HTML", data=file, file_name="report.html", mime='text/html')
    return selected_gender, selected_age, selected_animal, selected_edu_level, selected_experience, selected_industry, selected_taste

selected_gender, selected_age, selected_animal, selected_edu_level, selected_experience, selected_industry, selected_taste = sidebar_filters(df)

def filter_data(df, gender, age, animal, edu_level, experience, industry, taste):
    if gender != 'Wszyscy':
        df = df[df['gender'].astype(str) == gender]
    if age != 'Wszyscy':
        df = df[df['age'].astype(str) == age]
    if animal != 'Wszyscy':
        df = df[df['fav_animals'].astype(str) == animal]
    if edu_level != 'Wszyscy':
        df = df[df['edu_level'].astype(str) == edu_level]
    if experience != 'Wszyscy':
        df = df[df['years_of_experience'].astype(str) == experience]
    if industry != 'Wszyscy':
        df = df[df['industry'].astype(str) == industry]
    if taste != 'Wszyscy':
        df = df[df['sweet_or_salty'].astype(str) == taste]
    return df

df_filtered = filter_data(df, selected_gender, selected_age, selected_animal, selected_edu_level, selected_experience, selected_industry, selected_taste)

if df_filtered.empty:
    st.write("Brak danych do wyświetlenia po użyciu wybranych filtrów.")
else:
    st.write("Przefiltrowane dane:")
    st.dataframe(df_filtered, height=300)
