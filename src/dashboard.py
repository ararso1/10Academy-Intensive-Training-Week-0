import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import *  # Import your data loader functions
import psycopg2
from sqlalchemy import create_engine
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts import helper

# Database connection setup (replace with your credentials)
# DB_URL = "postgresql://username:password@localhost:5432/your_database"
# engine = create_engine(DB_URL)

data_df = helper.clean_data(pd.read_csv('docs\\data\\data.csv'))
domains_location_df = helper.clean_data(pd.read_csv('docs\\data\\domains_location.csv'))
traffic_data_df = helper.clean_data(pd.read_csv('docs\\data\\traffic.csv'))
rating_df = helper.clean_data(pd.read_csv('docs\\data\\rating.csv'))

# # Function to fetch data from your PostgreSQL database
# def fetch_data(query):
#     with engine.connect() as conn:
#         result = pd.read_sql(query, conn)
#     return result

# Title of the Dashboard
st.title("News Analysis Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Tabular", "Graphical", "Correlation Analysis"])

# Home Page
if options == "Tabular":
    st.write("## Tabular Analysis")

    top_articles = get_top_articles(data_df)
    top_traffic = get_top_traffic(traffic_data_df)
    top_coutries, x = helper.analyze_country_article_counts(data_df, domains_location_df)
    top_region, y = helper.analyze_region_article_counts(data_df, domains_location_df)

    country_domain_counts = domains_location_df['Country'].value_counts()
    top_10_countries_domains = country_domain_counts.head(10)
    
    # Layout to display data side by side
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    
    with col1:
        st.write("### 1. Top 10 Websites by Article Count")
        st.table(top_articles)
    with col2:
        st.write("### 2. Top 10 Websites by Visitor Traffic")
        st.table(top_traffic)

    with col3:
        st.write("### 3. Top 10 Countries by Article Count:")
        st.table(top_coutries)
    with col4:
        st.write("### 4. Top 10 Regions by Article Count:")
        st.table(top_region)

    with col5:
        st.write("### 5. Top 10 Countries by Article Count:")
        st.table(top_coutries)
    with col6:
        st.write("### 6. Top 10 Regions by Article Count:")
        st.table(top_region)


# Graphical/Plot Page
elif options == "Graphical":
    st.write("## Graphical Analysis")
    
    st.write("### 1. Distribution of Content Length Across Websites")
    fig_content_length = plot_content_length_distribution(data_df)
    st.plotly_chart(fig_content_length)
    
    st.write("### 2. Distribution of Title Word Count Across Websites")
    fig_title_word_count = plot_title_word_count_distribution(data_df)
    st.plotly_chart(fig_title_word_count)

    # Prepare data for scatter plots
    # Convert sentiment to numeric values for descriptive statistics
    sentiment_mapping = {'Negative': -1, 'Neutral': 0, 'Positive': 1}
    rating_df['title_sentiment_numeric'] = rating_df['title_sentiment'].map(sentiment_mapping)
    rating_df['title_sentiment_numeric'] = pd.to_numeric(rating_df['title_sentiment_numeric'])

    report_counts = rating_df.groupby('source_name').size().reset_index(name='total_reports')  # type: ignore
    sentiment_agg = rating_df.groupby('source_name')['title_sentiment_numeric'].agg(
        avg_sentiment='mean',
        median_sentiment='median'
    ).reset_index()
    merged_data = pd.merge(report_counts, sentiment_agg, on='source_name')
    merged_data = pd.merge(merged_data, traffic_data_df[['Domain', 'GlobalRank']], left_on='source_name', right_on='Domain')

    st.write("### 3. Impact of News Reporting and Average Sentiment on Global Ranking")
    fig_avg_sentiment = plot_scatter_avg_sentiment(merged_data)
    st.plotly_chart(fig_avg_sentiment)
    
    st.write("### 4. Impact of News Reporting and Median Sentiment on Global Ranking")
    fig_median_sentiment = plot_scatter_median_sentiment(merged_data)
    st.plotly_chart(fig_median_sentiment)

    st.write("### 5. Topic Trends Over Time")
    fig_topic_trends = plot_topic_trends(data_df, n_topics=10)
    st.plotly_chart(fig_topic_trends)

# Correlation Analysis Page
elif options == "Correlation Analysis":
    st.write("## Correlation Analysis")

    # Data preprocessing and vectorization for event clustering
    data_df['text'] = data_df['title'] + " " + data_df['full_content']
    vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english', max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(data_df['text'])

    # Apply K-Means clustering to group articles into events
    num_clusters = 10
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    data_df['event_cluster'] = kmeans.labels_

    sentiment_mapping = {'Negative': -1, 'Neutral': 0, 'Positive': 1}
    rating_df['title_sentiment_numeric'] = rating_df['title_sentiment'].map(sentiment_mapping)
    rating_df['title_sentiment_numeric'] = pd.to_numeric(rating_df['title_sentiment_numeric'])

    data_df = pd.merge(data_df, rating_df[['article_id', 'title_sentiment_numeric']], on='article_id', how='left')

    # 1. Number of events covered in the data
    num_events = data_df['event_cluster'].nunique()
    st.write(f"### 1. Number of Events Covered in the Data: {num_events}")

    # 2. Earliest reporting news sites per event
    data_df['published_at'] = pd.to_datetime(data_df['published_at'], errors='coerce')
    data_df = data_df.dropna(subset=['event_cluster', 'published_at', 'source_name'])
    earliest_reports = data_df.groupby(['event_cluster', 'source_name'])['published_at'].min().reset_index()
    earliest_site_per_event = earliest_reports.loc[earliest_reports.groupby('event_cluster')['published_at'].idxmin()]
    st.write("### 2.  Earliest Reporting News Sites Per Event")
    st.dataframe(earliest_site_per_event)

    # 3. Events with the highest reporting
    event_reporting = data_df['event_cluster'].value_counts().reset_index()
    event_reporting.columns = ['event_cluster', 'num_articles']
    st.write("### 3. Events with the Highest Reporting")
    st.dataframe(event_reporting.head(10))

    # 4. Correlation between news sites reporting events
    pivot_table = pd.pivot_table(data_df, index='event_cluster', columns='source_name', aggfunc='size', fill_value=0) # type: ignore
    correlation_matrix = pivot_table.corr()
    st.write("### 4.  Correlation Matrix Between News Sites Reporting Events")
    st.dataframe(correlation_matrix)

    # Additional Correlation Analyses:

    # Correlation Between Sentiment and Event Reporting
    sentiment_event_correlation = data_df.groupby('event_cluster')['title_sentiment_numeric'].mean().reset_index()
    sentiment_event_correlation = sentiment_event_correlation.merge(event_reporting, on='event_cluster')
    correlation_sent_event = sentiment_event_correlation['title_sentiment_numeric'].corr(sentiment_event_correlation['num_articles'])
    st.write("### 5. Correlation Between Sentiment and Event Reporting")
    st.write(f"Correlation between sentiment and number of articles per event: {correlation_sent_event}")

    # Correlation Between Global Rank and Reporting Volume
    site_article_count = data_df['source_name'].value_counts().reset_index()
    site_article_count.columns = ['source_name', 'num_articles']
    rank_article_correlation = site_article_count.merge(traffic_data_df[['Domain', 'GlobalRank']], left_on='source_name', right_on='Domain')
    correlation_rank_volume = rank_article_correlation['GlobalRank'].corr(rank_article_correlation['num_articles'])
    st.write("### 6. Correlation Between Global Rank and Reporting Volume")
    st.write(f"Correlation between global rank and number of articles: {correlation_rank_volume}")

    # Correlation Between Different News Categories and Sentiment
    category_sentiment = data_df.groupby('category')['title_sentiment_numeric'].mean().reset_index()
    st.write("### 7. Average Sentiment by News Category")
    st.dataframe(category_sentiment)

    # Correlation Between Site Location and Reporting Volume
    site_location_correlation = data_df.groupby('source_name').size().reset_index(name='num_articles') # type: ignore
    site_location_correlation = site_location_correlation.merge(domains_location_df, left_on='source_name', right_on='SourceCommonName')
    location_reporting_correlation = site_location_correlation.groupby('Country')['num_articles'].sum().reset_index()
    st.write("### Reporting Volume by Country")
    st.dataframe(location_reporting_correlation)

    # Correlation Between Reporting Timeliness and Sentiment
    earliest_sentiment = earliest_site_per_event.merge(data_df[['event_cluster', 'source_name', 'title_sentiment_numeric']], on=['event_cluster', 'source_name'])
    earliest_sentiment_correlation = earliest_sentiment.groupby('event_cluster')['title_sentiment_numeric'].mean().corr(sentiment_event_correlation['title_sentiment_numeric'])
    st.write("### Correlation Between Reporting Timeliness and Sentiment")
    st.write(f"Correlation between reporting timeliness and sentiment: {earliest_sentiment_correlation}")
