# src/dashboard.py
import sys
sys.path.append('../')

import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import *  # Import your data loader functions
# from topic_modeling import get_topic_data  # Import your topic modeling functions
# from event_modeling import get_event_data  # Import your event modeling functions
import psycopg2
from sqlalchemy import create_engine

# Database connection setup (replace with your credentials)
DB_URL = "postgresql://username:password@localhost:5432/your_database"
engine = create_engine(DB_URL)

# Function to fetch data from your PostgreSQL database
def fetch_data(query):
    with engine.connect() as conn:
        result = pd.read_sql(query, conn)
    return result

# Title of the Dashboard
st.title("News Analysis Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Home", "Topic Modeling", "Event Analysis", "Correlation Analysis"])

# Home Page
if options == "Home":
    st.write("## Welcome to the News Analysis Dashboard")
    st.write("Use the sidebar to navigate through different sections of the analysis.")

# Topic Modeling Page
elif options == "Topic Modeling":
    st.write("## Topic Modeling Insights")
    
    # Load topic modeling data
    topic_data = get_topic_data() # type: ignore
    
    # Display Topic Distribution Pie Chart
    st.write("### Topic Distribution")
    fig = px.pie(topic_data, names='topic', values='count', title='Distribution of Topics')
    st.plotly_chart(fig)

    # Display Keywords Bar Chart
    st.write("### Top Keywords by Topic")
    fig = px.bar(topic_data, x='keywords', y='importance', color='topic', title='Top Keywords by Topic')
    st.plotly_chart(fig)

# Event Analysis Page
elif options == "Event Analysis":
    st.write("## Event Clustering Insights")

    # Load event data
    event_data = get_event_data() # type: ignore
    
    # Display Event Distribution Bar Chart
    st.write("### Event Distribution")
    fig = px.bar(event_data, x='event', y='count', title='Number of Articles per Event')
    st.plotly_chart(fig)

    # Display Event Timeline
    st.write("### Event Timeline")
    fig = px.line(event_data, x='date', y='count', color='event', title='Event Timeline')
    st.plotly_chart(fig)

# Correlation Analysis Page
elif options == "Correlation Analysis":
    st.write("## News Sites Correlation")

    # Example correlation data
    correlation_query = "SELECT * FROM correlation_table"
    correlation_data = fetch_data(correlation_query)
    
    # Display Correlation Heatmap
    fig = px.imshow(correlation_data.corr(), text_auto=True, title='Correlation Heatmap of News Sites')
    st.plotly_chart(fig)

