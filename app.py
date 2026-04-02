import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_cleaned.csv")

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year

    df["country"] = df["country"].apply(ast.literal_eval)
    df["listed_in"] = df["listed_in"].apply(ast.literal_eval)

    return df

df = load_data()

st.title("🎬 Netflix Content Strategy Dashboard")

st.sidebar.header("Filters")

years = sorted(df["year_added"].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years)

selected_type = st.sidebar.multiselect(
    "Content Type",
    df["type"].unique(),
    default=df["type"].unique()
)

search_title = st.sidebar.text_input("Search Title")

filtered_df = df[
    (df["year_added"] == selected_year) &
    (df["type"].isin(selected_type))
]

if search_title:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_title, case=False)
    ]

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df["type"] == "Movie"]))
col3.metric("TV Shows", len(filtered_df[filtered_df["type"] == "TV Show"]))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Content Type Distribution")
    type_counts = filtered_df["type"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%")
    st.pyplot(fig1)

with col2:
    st.subheader("Top Genres")
    df_genre = filtered_df.explode("listed_in")
    genre_counts = df_genre["listed_in"].value_counts().head(10)

    fig2, ax2 = plt.subplots()
    genre_counts.plot(kind="bar", ax=ax2)
    st.pyplot(fig2)

st.subheader("Top Countries")

df_country = filtered_df.explode("country")
country_counts = df_country["country"].value_counts().head(10)

fig3, ax3 = plt.subplots()
country_counts.plot(kind="bar", ax=ax3)
st.pyplot(fig3)

st.subheader("Content Growth Over Time")

growth = df.groupby("year_added").size()

fig4, ax4 = plt.subplots()
growth.plot(ax=ax4)
st.pyplot(fig4)