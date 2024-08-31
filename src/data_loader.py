import sys
import os
# sys.path.append('../')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import plotly.graph_objs as go
from plotly import express as px
import pandas as pd
from scripts import helper, topic_and_event_modeling

# Function to get the top ten websites by news article count
def get_top_articles(data_df):
    top_articles = data_df['source_name'].value_counts().head(10).reset_index()
    top_articles.columns = ['Website', 'Article Count']
    return top_articles

# Function to get the top ten websites by visitor traffic
def get_top_traffic(traffic_data_df):
    # Assuming traffic_data_df has 'Domain' and 'GlobalRank' columns
    top_traffic = traffic_data_df.sort_values(by='GlobalRank').head(10)
    top_traffic = top_traffic[['Domain', 'GlobalRank']]
    top_traffic.columns = ['Website', 'Visitor Traffic Rank']
    return top_traffic

# Define plotting functions
def plot_content_length_distribution(data_df):
    data_df['content_length'] = data_df['full_content'].apply(lambda x: len(x) if x else 0)
    fig = px.box(data_df, x='source_name', y='content_length')
    fig.update_layout(xaxis_title='Website', yaxis_title='Content Length (Characters)', xaxis_tickangle=90)
    return fig

def plot_title_word_count_distribution(data_df):
    data_df['title_word_count'] = data_df['title'].apply(lambda x: len(x.split()) if x else 0)
    fig = px.box(data_df, x='source_name', y='title_word_count')
    fig.update_layout(xaxis_title='Website', yaxis_title='Title Word Count', xaxis_tickangle=90)
    return fig


def plot_scatter_avg_sentiment(merged_data):
    fig = px.scatter(
        merged_data,
        x='total_reports',
        y='GlobalRank',
        color='avg_sentiment',
        color_continuous_scale='RdBu',
        size='total_reports',
        hover_name='source_name'
    )
    fig.update_yaxes(autorange='reversed')  # GlobalRank (lower is better)
    return fig

def plot_scatter_median_sentiment(merged_data):
    fig = px.scatter(
        merged_data,
        x='total_reports',
        y='GlobalRank',
        color='median_sentiment',
        color_continuous_scale='RdBu',
        size='total_reports',
        hover_name='source_name',
    )
    fig.update_yaxes(autorange='reversed')  # GlobalRank (lower is better)
    return fig


def plot_topic_trends(df, n_topics):
    # Perform topic modeling
    n_topics = 10  # Number of topics to identify
    lda, topics, vectorizer = topic_and_event_modeling.perform_topic_modeling_by_lda(df, n_topics=n_topics)

    # Assign the most likely topic to each article
    topic_assignments = lda.transform(vectorizer.transform(df['text'])).argmax(axis=1)
    df['topic'] = topic_assignments

    # Group by date and topic, then count the occurrences
    trend_data = df.groupby([df['published_at'].dt.date, 'topic']).size().reset_index(name='count')
    
    # Create a scatter plot using Plotly
    fig = px.scatter(
        trend_data,
        x='published_at',
        y='topic',
        size='count',
        color='count',
        color_continuous_scale='Viridis',
        labels={
            'published_at': 'Date',
            'topic': 'Topic',
            'count': 'Number of Articles'
        },
        size_max=60,
        hover_name='count'
    )

    fig.update_yaxes(
        tickvals=list(range(n_topics)),
        ticktext=[f'Topic {i+1}' for i in range(n_topics)]
    )

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Topic',
        coloraxis_colorbar=dict(
            title='Number of Articles'
        )
    )

    return fig

