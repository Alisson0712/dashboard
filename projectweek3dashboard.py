# -*- coding: utf-8 -*-
"""Projectweek3Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fqMveO9tGn-LAAaB-YHbdN2N6yGhcRvX
"""

#Import Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk

def load_data():
    try:
        df = pd.read_csv('netflix_titles.csv')
        st.success("Data Visualization successfully!")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

#Page Configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🎬", # Clapperboard emoji
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#Add a sidebar for the selection of differents graphs
with st.sidebar:
    st.title('🎬 Netflix Data Visualization')

    graph_options = [
        "Release Year Distribution",
        "Distribution of Content Types",
        "Top 13 Countries with Most Content",
        "Trend of Releases Over Time",
        "Type vs Rating",
        "Filter Only Movies",
        "Multivariate Analysis",
        "Choropleth Map: Titles by Country",
        "Word Cloud: Most Common Words in Titles Descriptions",
        "Distribution of Genres in Canada"
    ]
    selected_graph = st.selectbox('Select a Graph', graph_options)

def clean_data(df):
    if df is None or df.empty:
        st.error("DataFrame is empty or not loaded properly.")
        return None

    required_columns = ['release_year', 'type', 'country', 'rating', 'duration', 'listed_in', 'description']
    for column in required_columns:
        if column not in df.columns:
            st.error(f"The column '{column}' is missing from the DataFrame")
            return None

    df = df.dropna(subset=required_columns)
    if df.empty:
        st.error("The DataFrame is empty after cleaning.")
        return None

    return df

# Load your data
df = load_data()

# Initialize df_cleaned as None first to avoid NameError
df_cleaned = None

if df is not None:
    df_cleaned = clean_data(df)

# Now this is safe
if df_cleaned is None:
    st.error("The data is not available for further processing.")

# Release Year Distribution
# Both movies and TV shows increased after 2010, peaking around 2018-2019.
def release_year_distribution(df):
    if df is None or df.empty:
        st.error("DataFrame is empty or not loaded properly.")
        return

    if 'release_year' not in df.columns:
        st.error("The column 'release_year' is missing from the DataFrame.")
        return

    fig, ax = plt.subplots(figsize=(10,6))

    sns.histplot(df['release_year'], color='r', kde=True, ax=ax)
    ax.set_title('Distribution of Release Years', size=18)
    ax.set_xlabel('Release Year', size=14)
    ax.set_ylabel('Density', size=14)

    st.pyplot(fig)

# Distribution of content types
# movies are dominated with more than 6000
def content_type_distribution(df):
    if df is None or df.empty:
        st.error("DataFrame is empty or not loaded properly.")
        return
    if 'type' not in df.columns:
        st.error("The column 'type' is missing from the DataFrame.")
        return
    fig, ax = plt.subplots(figsize=(10,6))
    sns.countplot(data=df, x='type', palette=['skyblue', 'orange'], ax=ax)
    ax.set_title('Count of Movies vs TV Shows on Netflix')
    st.pyplot(fig)

# Top 13 countries with most content
# we can notice that United States and India dominate both categories

def top_13_countries(df):
    if df is None or df.empty:
        return

    if 'country' not in df.columns:
        st.error("The column 'country' is missing from the DataFrame.")
        return

    fig, ax = plt.subplots(figsize=(10,6))
    top_countries = df['country'].value_counts().head(13)
    colors = ['skyblue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'gold', 'lime']
    top_countries.plot(kind='bar', title='Top 13 Content Producing Countries', color=colors, ax=ax)
    ax.set_ylabel('Number of Titles')
    st.pyplot(fig)

# Trend of releases over time
# Around 2018 and 2019 are the years with the mist numbers of titles released over the period
def trend_of_releases(df):
    if df is None or df.empty:
        return

    fig, ax = plt.subplots(figsize=(12,5))
    df['release_year'].value_counts().sort_index().plot(kind='line', ax=ax, title='Number of Titles Released per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Titles')
    st.pyplot(fig)

# Type vs Rating
# we can notice that Movies are dominate in almost all catgories
#TV-MA is the most common rating overall, especially for TV Shows.
def type_vs_rating(df):
    if df is None or df.empty:
        return

    fig, ax = plt.subplots(figsize=(12,6))
    sns.countplot(data=df, x='rating', hue='type', order=df['rating'].value_counts().index, ax=ax)
    ax.set_title('Distribution of Ratings by Content Type')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title='Type')
    st.pyplot(fig)

# Filter only Movies
#Most Netflix movies are 90–110 minutes long
def filter_only_movies(df):
    if df is None or df.empty:
        return

    fig, ax = plt.subplots(figsize=(10,6))
    movies_df = df[df['type'] == 'Movie'].copy()
    movies_df['duration_minutes'] = movies_df['duration'].str.extract('(\d+)').astype(float)
    sns.histplot(data=movies_df, x='duration_minutes', bins=30, kde=True, ax=ax)
    ax.set_title('Distribution of Movie Durations (in minutes)')
    ax.set_xlabel('Duration (minutes)')
    st.pyplot(fig)

# Multivariate Analysis
# release_year vs duration_minutes: Typically weak or no correlation expected.
# type_encoded vs duration_minutes: May show a negative correlation, since TV Shows don't usually have a numerical duration in minutes
# Ensure duration_minutes and type_encoded exist
def multivariate_analysis(df):
    if df is None or df.empty:
        return

    fig, ax = plt.subplots(figsize=(10,6))
    df['duration_minutes'] = df['duration'].str.extract('(\d+)').astype(float)
    df['type_encoded'] = df['type'].map({'Movie': 0, 'TV Show': 1})
    numerical_df = df[['release_year', 'duration_minutes', 'type_encoded']].dropna()

    sns.heatmap(numerical_df.corr(), annot=True, square=True, cmap='RdBu', vmin=-1, vmax=1, ax=ax)
    ax.set_title('Correlations Between Netflix Variables', size=18)
    ax.set_xticklabels(ax.get_xticklabels(), size=13)
    ax.set_yticklabels(ax.get_yticklabels(), size=13)
    st.pyplot(fig)

# Choropleth map function for the top 5 countries
def choropleth_map(df):
    if df is None or df.empty:
        return
    if 'country' not in df.columns:
        st.error("The column 'country' is missing from the DataFrame.")
        return

    # Get the top 5 countries with the most titles
    country_count = df['country'].value_counts().head(5).reset_index()
    country_count.columns = ['country', 'count']

    # Create the choropleth map for the top 5 countries
    fig = px.choropleth(country_count,
                        locations="country",
                        locationmode='country names',
                        color="count",
                        color_continuous_scale="Viridis",
                        labels={'count': 'Number of Titles'},
                        title="Top 5 Netflix Titles by Country")

    st.plotly_chart(fig)

# Distribution of genres by country (only for Canada and top 10 genres)
def genres_by_canada(df):
    if df is None or df.empty:
        return

    if 'country' not in df.columns or 'listed_in' not in df.columns:
        st.error("The columns 'country' or 'listed_in' are missing from the DataFrame.")
        return

    # Filter data for Canada only
    df_canada = df[df['country'].str.contains('Canada', na=False)]

    # Split genres from the 'listed_in' column and create a new column for genres
    df_canada['genres'] = df_canada['listed_in'].str.split(',').apply(lambda x: [i.strip() for i in x])  # Split genres

    # Explode the genres column so that each genre has its own row
    df_expanded = df_canada.explode('genres')

    # Count the top 10 genres in Canada
    top_genres = df_expanded['genres'].value_counts().head(10)

    # Plot the top 10 genres as a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_genres.index, y=top_genres.values, ax=ax, palette='viridis')
    ax.set_title('Top 10 Genres in Canada')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Number of Titles')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

# Word Cloud Function for Title Descriptions
def word_cloud(df):
    if df is None or df.empty:
        st.error("Data is empty or not loaded properly.")
        return

    if 'description' not in df.columns:
        st.error("The column 'description' is missing from the DataFrame.")
        return

    # Combine all descriptions into a single string
    text = ' '.join(df['description'].dropna())

    # Remove stopwords (commonly used words that are not useful for analysis)
    stop_words = set(stopwords.words('english'))
    wordcloud = WordCloud(stopwords=stop_words, background_color="white", width=800, height=400).generate(text)

    # Plotting the word cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')  # Turn off axis
    st.pyplot(plt)

if df_cleaned is not None:
    if selected_graph == "Release Year Distribution":
        release_year_distribution(df_cleaned)
    elif selected_graph == "Distribution of Content Types":
        content_type_distribution(df_cleaned)
    elif selected_graph == "Top 13 Countries with Most Content":
        top_13_countries(df_cleaned)
    elif selected_graph == "Trend of Releases Over Time":
        trend_of_releases(df_cleaned)
    elif selected_graph == "Type vs Rating":
        type_vs_rating(df_cleaned)
    elif selected_graph == "Filter Only Movies":
        filter_only_movies(df_cleaned)
    elif selected_graph == "Multivariate Analysis":
        multivariate_analysis(df_cleaned)
    elif selected_graph == "Choropleth Map: Titles by Country":
        choropleth_map(df_cleaned)
    elif selected_graph == "Distribution of Genres in Canada":
        genres_by_canada(df_cleaned)

# Ensure that df_cleaned is properly defined and not empty
if df_cleaned is None or df_cleaned.empty:
    st.error("The data is not available for further processing.")
else:
    # Create 3 columns layout in Streamlit (side-by-side layout)
    col1, col2, col3 = st.columns([2, 3, 3], gap ='medium') # Three equal columns

    # In the first column, show any content if needed (currently empty)
    with col1:
        st.empty()  # First column empty (sidebar already takes care of this)

    # In the second column, show the choropleth map
    with col2:
        if selected_graph == "Trend of Releases Over Time":
            trend_of_releases(df_cleaned)

    # In the third column, display the additional information (fixed text content)
    with col3:
        st.markdown("### Data Source")
        st.markdown("[Netflix Titles Data on Kaggle](https://www.kaggle.com/datasets/padmapriyatr/netflix-titles)")

        st.markdown("### Dashboard Creator")
        st.markdown("Created by: **Alisson Barreto**")

        st.markdown("### Dataset Description")
        st.markdown("""
            The **Netflix Titles Dataset** contains information about movies and TV shows available on Netflix.
            The data includes details such as:
            - Title of the movie or show
            - Type (Movie or TV Show)
            - Country of origin
            - Language
            - Genre(s)
            - Rating
            - Duration
            - Release Year
            - And more

            The dataset provides insights into the variety and availability of content on Netflix across different countries and genres.
        """)