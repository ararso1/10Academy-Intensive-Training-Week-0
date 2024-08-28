import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

# Load the data
data_df = pd.read_csv('C:\\Users\\araso\\Documents\\10academy\\data\\data.csv')

def clean_data(df):
    # Fill missing values
    df['title'] = df['title'].fillna('')
    df['full_content'] = df['full_content'].fillna('')
    
    # Ensure correct data types
    df['title'] = df['title'].astype(str)
    df['full_content'] = df['full_content'].astype(str)
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['published_at'])
    
    return df

# Load and clean data
data_df = pd.read_csv('data.csv')
data_df = clean_data(data_df)


# Data cleaning function
def clean_text(text):
    text = str(text).lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    return text

# Apply cleaning
data_df['cleaned_title'] = data_df['title'].apply(clean_text)
data_df['cleaned_content'] = data_df['full_content'].apply(clean_text)

# Convert published_at to datetime
data_df['published_at'] = pd.to_datetime(data_df['published_at'], errors='coerce')


# Function to extract top n keywords using TF-IDF
def extract_keywords_tfidf(texts, n=5):
    vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    top_keywords = []

    for i in range(tfidf_matrix.shape[0]):
        tfidf_scores = tfidf_matrix[i].T.todense()
        sorted_indices = tfidf_scores.argsort(axis=0)[::-1]
        top_n = [feature_names[index[0, 0]] for index in sorted_indices[:n]]
        top_keywords.append(top_n)
    
    return top_keywords


# Function to calculate cosine similarity between two lists of keywords
def calculate_similarity(keywords1, keywords2):
    vectorizer = TfidfVectorizer().fit([' '.join(keywords1), ' '.join(keywords2)])
    tfidf_matrix = vectorizer.transform([' '.join(keywords1), ' '.join(keywords2)])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


# Topic modeling function
def perform_lda(text_data, n_topics=5):
    vectorizer = CountVectorizer(max_df=0.9, min_df=10, stop_words='english')
    dtm = vectorizer.fit_transform(text_data)
    lda_model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda_model.fit(dtm)
    return lda_model, vectorizer

