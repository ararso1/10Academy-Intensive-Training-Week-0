from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation

# Function to extract top n keywords using TF-IDF
def extract_keywords_tfidf(texts, n=5):
    vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    top_keywords = []

    for i in range(tfidf_matrix.shape[0]):
        tfidf_scores = tfidf_matrix[i].T.todense() # type: ignore
        sorted_indices = tfidf_scores.argsort(axis=0)[::-1]
        top_n = [feature_names[index[0, 0]] for index in sorted_indices[:n]]
        top_keywords.append(top_n)
    
    return top_keywords

# Function to calculate cosine similarity between two lists of keywords
def calculate_similarity(keywords1, keywords2):
    vectorizer = TfidfVectorizer().fit([' '.join(keywords1), ' '.join(keywords2)])
    tfidf_matrix = vectorizer.transform([' '.join(keywords1), ' '.join(keywords2)])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] # type: ignore


def perform_topic_modeling_by_lda(df, n_topics=10, n_words=10):
    # Combine title and full content for topic modeling
    df['text'] = df['title'] + ' ' + df['full_content']
    
    # Vectorize the text
    vectorizer = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(df['text'])
    
    # Apply LDA
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    
    # Get the topics and their top words
    topics = []
    for index, topic in enumerate(lda.components_):
        topic_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-n_words:]]
        topics.append(' '.join(topic_words)) # type: ignore
    
    return lda, topics, vectorizer


def analyze_topic_diversity(df):
    # Calculate the number of unique topics reported by each website
    diversity = df.groupby('source_name')['topic'].nunique().reset_index()
    diversity.columns = ['source_name', 'unique_topics']
    
    # Sort by most diverse topics
    most_diverse_sites = diversity.sort_values(by='unique_topics', ascending=False)
    
    return most_diverse_sites