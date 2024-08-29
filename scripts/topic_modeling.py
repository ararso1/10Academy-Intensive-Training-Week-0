from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation

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
        topics.append(' '.join(topic_words))
    
    return lda, topics, vectorizer