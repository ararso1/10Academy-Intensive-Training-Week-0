
### Some of the functions available in the notebooks and codes in this repository

#### News Data Parsing Functions from helper.py
`analyze_country_article_counts`: Analyze the number of articles written about each country mentioned in the content.
    Parameters:
    - data_df (DataFrame): A DataFrame containing articles with a 'content' column.
    - domains_location_df (DataFrame): A DataFrame containing countries in a 'Country' column.

    Returns:
    - top_10_countries_articles (DataFrame): A DataFrame of the top 10 countries by article count.
    - bottom_10_countries_articles (DataFrame): A DataFrame of the bottom 10 countries by article count.

`analyze_region_article_counts`: Analyze the number of articles reporting about specific regions like Africa, US, China, EU, Russia, Ukraine, and Middle East.

    Parameters:
    - data_df (DataFrame): A DataFrame containing articles with a 'content' column.
    - domains_location_df (DataFrame): A DataFrame containing location data with 'location' and 'SourceCommonName' columns.

    Returns:
    - top_10_region_articles (DataFrame): A DataFrame of the top 10 regions by article count.
    - bottom_10_region_articles (DataFrame): A DataFrame of the bottom 10 regions by article count.

`analyze_sentiment_statistics`: 
    Convert sentiment to numeric values and calculate descriptive statistics by domain.
    Compare global sentiment distribution with the distribution for the top 10 domains by traffic.

`clean_data`: Clean the input DataFrame by filling missing values, ensuring correct data types, and handling invalid dates.
    
    Parameters:
    - df (DataFrame): The input DataFrame to clean.
    - date_columns (list of str, optional): List of column names to be parsed as dates.
    - fillna_strategy (str or dict, optional): Strategy to fill missing values. Options are 'mean', 'median', 'mode', or a dictionary of column-specific strategies.
    - dropna_threshold (float, optional): Threshold for dropping rows with missing values. Rows with missing values above this threshold will be dropped.
    - date_format (str, optional): Format to enforce for date columns. If None, pandas will infer the format.
    - custom_types (dict, optional): A dictionary specifying the desired data types for specific columns.
    
    Returns:
    - cleaned_df (DataFrame): The cleaned DataFrame.

#### News Data Parsing Functions from topic_and_event_modeling.py

1. **`extract_keywords_tfidf(texts, n=5)`**:
   - **Description**: This function extracts the top `n` keywords from a list of text documents using the TF-IDF (Term Frequency-Inverse Document Frequency) method. It returns a list of the most important keywords for each document, helping to identify the key topics or concepts in the text.

2. **`calculate_similarity(keywords1, keywords2)`**:
   - **Description**: This function calculates the cosine similarity between two lists of keywords. It converts the keyword lists into TF-IDF vectors and computes the similarity score between them, which indicates how similar the two sets of keywords are.

3. **`perform_topic_modeling_by_lda(df, n_topics=10, n_words=10)`**:
   - **Description**: This function performs topic modeling on a DataFrame of text data using Latent Dirichlet Allocation (LDA). It identifies `n_topics` topics within the text and returns the LDA model, a list of top words for each topic, and the vectorizer used for the analysis.

4. **`analyze_topic_diversity(df)`**:
   - **Description**: This function analyzes the diversity of topics reported by each website in the provided DataFrame. It calculates the number of unique topics covered by each news source and returns a sorted list of websites, ranked by the diversity of topics they report on.

These descriptions provide a concise explanation of what each function does, focusing on their purpose and the type of output they generate. If you need more details or further adjustments, feel free to ask!