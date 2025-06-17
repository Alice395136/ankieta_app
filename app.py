import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport

# Ładuję dane
df = pd.read_csv("35__welcome_survey_cleaned_comma.csv", sep=";", encoding="utf-8-sig")

# Zastępuję wartości None w kolumnie gender
df['gender'] = df['gender'].fillna('Inne').replace({0: 'M', 1: 'K'})

# Tytuł aplikacji
st.title("📊 Ankieta powitalna - analiza")
st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

# Tworzę pasek boczny z filtrami
def sidebar_filters(df):
    with st.sidebar:
        st.title("Filtruj")

        # Filtr płci
        gender_options = ['Wszyscy'] + df['gender'].unique().tolist()
        selected_gender = st.radio("Wybierz płeć", gender_options)

        # Filtr wiekowy
        unique_ages = ['Wszyscy'] + sorted(df['age'].dropna().astype(str).unique().tolist())
        selected_age = st.selectbox("Wybierz wiek", unique_ages)

        # Filtr ulubionych zwierząt
        animal_options = ['Wszyscy'] + df['fav_animals'].dropna().unique().tolist()
        selected_animal = st.selectbox("Wybierz zwierzę", animal_options)

        # Filtr poziomu wykształcenia
        edu_level_options = ['Wszyscy'] + df['edu_level'].dropna().unique().tolist()
        selected_edu_level = st.radio("Wybierz poziom wykształcenia", edu_level_options)

        # Filtr lat doświadczenia
        experience_options = ['Wszyscy'] + sorted(df['years_of_experience'].dropna().unique().tolist())
        selected_experience = st.selectbox("Wybierz lata doświadczenia", experience_options)

        # Filtr branży
        industry_options = ['Wszyscy'] + df['industry'].dropna().unique().tolist()
        selected_industry = st.selectbox("Wybierz branżę", industry_options)

        # Filtr smaku
        taste_options = ['Wszyscy'] + df['sweet_or_salty'].dropna().unique().tolist()
        selected_taste = st.selectbox("Wybierz preferencję smakową", taste_options)

        # Przycisk resetujący
        if st.button("🔄 Resetuj filtry"):
             st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

        # Przycisk do generowania raportu
        if st.button("🧑‍🚀 Wykonaj analizę ankiety"):
            profile = ProfileReport(df, title="Profilowanie danych", explorative=True)
            profile.to_file("output.html")
            with open("output.html", "rb") as file:
                st.download_button(
                    label="Pobierz pełny raport jako HTML",
                    data=file,
                    file_name="report.html",
                    mime='text/html'
                )

    return selected_gender, selected_age, selected_animal, selected_edu_level, selected_experience, selected_industry, selected_taste

selected_gender, selected_age, selected_animal, selected_edu_level, selected_experience, selected_industry, selected_taste = sidebar_filters(df)

# Filtrowanie danych na podstawie wyborów
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

# Wyświetlenie przefiltrowanych danych
if df_filtered.empty:
    st.write("Brak danych do wyświetlenia po użyciu wybranych filtrów.")
else:
    st.write("Przefiltrowane dane:")
    st.dataframe(df_filtered, height=300)

    # Rozkład przedziałów wiekowych
    st.markdown("### 📈 **Rozkład przedziałów wiekowych**")
    fig, ax = plt.subplots()
    sns.countplot(x='age', data=df_filtered, order=sorted(df_filtered['age'].unique()), ax=ax)
    ax.set_title("Rozkład wiekowy")
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

    # Najpopularniejsze ulubione zwierzęta
    st.markdown("### 🐈 🐕 **Najpopularniejsze ulubione zwierzęta**")
    fig, ax = plt.subplots()
    df_filtered['fav_animals'].value_counts().plot(kind='bar', ax=ax, color='green')
    ax.set_title("Ulubione zwierzęta")
    ax.set_xlabel("Zwierzę")
    ax.set_ylabel("Liczba osób")
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

    # Korelacja między wiekiem a branżą
    st.markdown("### 👁️‍🗨️ **Korelacja między wiekiem a branżą**")
    fig, ax = plt.subplots()
    sns.boxplot(x='industry', y='age', data=df_filtered, ax=ax, color='yellow')
    ax.set_title("Wiek a branża")
    ax.set_xlabel("Branża")
    ax.set_ylabel("Wiek")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

    # Rozkład hobby w zależności od płci
    hobby_columns = ['hobby_art', 'hobby_books', 'hobby_movies', 'hobby_other', 'hobby_sport', 'hobby_video_games']
    st.markdown("### 🎾 **Rozkład hobby w zależności od płci**")
    fig, ax = plt.subplots()
    hobby_gender_distribution = df_filtered.groupby('gender')[hobby_columns].sum()
    hobby_gender_distribution.plot(kind='barh', stacked=True, ax=ax)
    ax.set_title('Hobby w zależności od płci')
    ax.set_xlabel('Płeć')
    ax.set_ylabel('Liczba osób')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Umieszczenie legendy na zewnątrz, po prawej stronie i u góry
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

    # Preferencje smakowe w zależności od wieku
    st.markdown("### 🥧 **Preferencje smakowe w zależności od wieku**")
    fig, ax = plt.subplots()
    taste_age_distribution = df_filtered.groupby('sweet_or_salty')['age'].value_counts().unstack().plot(kind='barh', stacked=True, ax=ax)
    ax.set_title("Preferencje smakowe a wiek")
    ax.set_xlabel("Preferencja smakowa")
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Umieszczenie legendy na zewnątrz, po prawej stronie i u góry
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

    # Wykres poziomu wykształcenia
    st.markdown("### 🎓 **Wykres poziomu wykształcenia**")
    fig, ax = plt.subplots()
    df_filtered['edu_level'].value_counts().plot(kind='bar', ax=ax, color='red')
    ax.set_title("Poziom wykształcenia")
    ax.set_xlabel("Poziom wykształcenia")
    ax.set_ylabel("Liczba osób")
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)  # Dodanie odstępu

    # Preferowane metody nauki
    learning_columns = [
        'learning_pref_books', 'learning_pref_chatgpt', 'learning_pref_offline_courses',
        'learning_pref_online_courses', 'learning_pref_personal_projects',
        'learning_pref_teaching', 'learning_pref_teamwork', 'learning_pref_workshops'
    ]
    st.markdown("### 📚 **Preferowane metody nauki**")
    fig, ax = plt.subplots()
    learning_preferences = df_filtered[learning_columns].mean().sort_values(ascending=False)
    learning_preferences.plot(kind='bar', ax=ax, color='brown')
    ax.set_title("Preferencje dotyczące nauki")
    ax.set_xlabel("Metoda nauki")
    ax.set_ylabel("Średni poziom zainteresowania")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)