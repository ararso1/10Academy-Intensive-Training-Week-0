import sys
sys.path.append('../')

from src.models import *
from src.db_config import engine, Base, SessionLocal
import pandas as pd

# Create all tables
Base.metadata.create_all(bind=engine)
data_df = pd.read_csv('C:\\Users\\araso\\Documents\\10academy\\data\\data.csv')
print(data_df.head())
# Function to load data into the database
def load_data(data_df):
    session = SessionLocal()

    # Convert data to dictionaries for insertion
    articles_data = data_df[['article_id', 'source_name', 'published_at', 'title', 'full_content']].to_dict(orient='records')
    topics_data = [{'topic_keywords': ', '.join(topics[i]), 'article_id': row['article_id']} for i, row in data_df.iterrows()]
    events_data = [{'event_description': row['event_description'], 'article_id': row['article_id']} for i, row in data_df.iterrows()]
    features_data = [{'article_id': row['article_id'], 'tfidf_vector': str(tfidf_matrix[i].toarray()), 'topic': row['topic'], 'event_cluster': row['event_cluster']} for i, row in data_df.iterrows()]

    try:
        # Insert data into tables
        session.bulk_insert_mappings(Article, articles_data)
        session.bulk_insert_mappings(Topic, topics_data)
        session.bulk_insert_mappings(Event, events_data)
        session.bulk_insert_mappings(Feature, features_data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
