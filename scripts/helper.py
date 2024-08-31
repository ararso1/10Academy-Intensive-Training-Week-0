import pandas as pd
import numpy as np

def clean_data(df, date_columns=None, fillna_strategy='mean', dropna_threshold=0.5, date_format=None, custom_types=None): # type: ignore
    
    # Fill missing values for specific columns if provided
    if 'title' in df.columns:
        df['title'] = df['title'].fillna('')
    if 'full_content' in df.columns:
        df['full_content'] = df['full_content'].fillna('')
    if 'published_at' in df.columns:
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    
    # Ensure correct data types for specific columns if custom_types is provided
    if custom_types:
        for col, dtype in custom_types.items():
            if col in df.columns:
                if pd.api.types.is_integer_dtype(dtype):
                    # Remove or convert non-numeric values to NaN before converting to integer
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    df[col] = df[col].astype(pd.Int64Dtype())
                else:
                    df[col] = df[col].astype(dtype)
    
    # General data type conversion
    df = df.convert_dtypes()
    
    # Handle missing values based on general strategy
    if isinstance(fillna_strategy, dict):
        df = df.fillna(value=fillna_strategy)
    elif fillna_strategy == 'mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif fillna_strategy == 'median':
        df = df.fillna(df.median(numeric_only=True))
    elif fillna_strategy == 'mode':
        df = df.fillna(df.mode().iloc[0])
    else:
        raise ValueError("Invalid fillna_strategy. Choose from 'mean', 'median', 'mode', or provide a dictionary.")
    
    # Drop rows with missing values based on threshold
    df = df.dropna(thresh=int(dropna_threshold * len(df.columns)))
    
    # Convert specified columns to datetime
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
    
    # Drop rows with invalid dates in any specified date columns
    if date_columns:
        df = df.dropna(subset=date_columns)
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Remove whitespace from string columns
    for col in df.select_dtypes(include='string').columns:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

def analyze_country_article_counts(data_df, domains_location_df):
    """
    Analyze the number of articles written about each country mentioned in the content.

    Parameters:
    - data_df (DataFrame): A DataFrame containing articles with a 'content' column.
    - domains_location_df (DataFrame): A DataFrame containing countries in a 'Country' column.

    Returns:
    - top_10_countries_articles (DataFrame): A DataFrame of the top 10 countries by article count.
    - bottom_10_countries_articles (DataFrame): A DataFrame of the bottom 10 countries by article count.
    """

    # List of countries to check in the content
    countries_list = domains_location_df['Country'].unique()

    # Initialize a dictionary to count articles per country
    country_article_count = {country: 0 for country in countries_list}

    # Count occurrences of each country in the article content
    for country in countries_list:
        country = str(country)
        country_article_count[country] = data_df['content'].str.contains(country, case=False, na=False).sum()

    # Convert dictionary to DataFrame
    country_article_count_df = pd.DataFrame(list(country_article_count.items()), columns=['Country', 'ArticleCount']).dropna()

    # Sort by ArticleCount to find the top and bottom 10 countries
    top_10_countries_articles = country_article_count_df.sort_values(by='ArticleCount', ascending=False).head(10)
    bottom_10_countries_articles = country_article_count_df.sort_values(by='ArticleCount', ascending=True).tail(10)

    return top_10_countries_articles, bottom_10_countries_articles


def analyze_region_article_counts(data_df, domains_location_df):
    """
    Analyze the number of articles reporting about specific regions like Africa, US, China, EU, Russia, Ukraine, and Middle East.

    Parameters:
    - data_df (DataFrame): A DataFrame containing articles with a 'content' column.
    - domains_location_df (DataFrame): A DataFrame containing location data with 'location' and 'SourceCommonName' columns.

    Returns:
    - top_10_region_articles (DataFrame): A DataFrame of the top 10 regions by article count.
    - bottom_10_region_articles (DataFrame): A DataFrame of the bottom 10 regions by article count.
    """

    # Define country groups for each region
    african_countries = domains_location_df[domains_location_df['location'].isin([
        'DZ', 'AO', 'BJ', 'BW', 'BF', 'BI', 'CV', 'CM', 'CF', 'TD', 'KM', 'CG', 'CD',
        'DJ', 'EG', 'GQ', 'ER', 'SZ', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'KE', 'LS',
        'LR', 'LY', 'MG', 'MW', 'ML', 'MR', 'MU', 'YT', 'MA', 'MZ', 'NA', 'NE', 'NG',
        'RE', 'RW', 'SH', 'ST', 'SN', 'SC', 'SL', 'SO', 'ZA', 'SS', 'SD', 'TZ', 'TG',
        'TN', 'UG', 'EH', 'ZM', 'ZW'])]['SourceCommonName'].unique()

    eu_countries = domains_location_df[domains_location_df['location'].isin([
        'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU',
        'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES',
        'SE'])]['SourceCommonName'].unique()

    middle_east_countries = domains_location_df[domains_location_df['location'].isin([
        'BH', 'EG', 'IR', 'IQ', 'IL', 'JO', 'KW', 'LB', 'OM', 'PS', 'QA', 'SA', 'SY',
        'AE', 'YE'])]['SourceCommonName'].unique()

    # Initialize dictionaries for each region
    africa_article_count = data_df['content'].apply(lambda x: any(country in x for country in african_countries)).sum()
    us_article_count = data_df['content'].str.contains('US', case=False, na=False).sum()
    china_article_count = data_df['content'].str.contains('China', case=False, na=False).sum()
    eu_article_count = data_df['content'].apply(lambda x: any(country in x for country in eu_countries)).sum()
    russia_article_count = data_df['content'].str.contains('Russia', case=False, na=False).sum()
    ukraine_article_count = data_df['content'].str.contains('Ukraine', case=False, na=False).sum()
    middle_east_article_count = data_df['content'].apply(lambda x: any(country in x for country in middle_east_countries)).sum()

    # Aggregate the article counts for each region
    region_article_count = {
        'Africa': africa_article_count,
        'US': us_article_count,
        'China': china_article_count,
        'EU': eu_article_count,
        'Russia': russia_article_count,
        'Ukraine': ukraine_article_count,
        'Middle East': middle_east_article_count
    }

    region_article_count_df = pd.DataFrame(list(region_article_count.items()), columns=['Region', 'ArticleCount'])

    # Sort and display the top and bottom 10 regions by article count
    top_10_region_articles = region_article_count_df.sort_values(by='ArticleCount', ascending=False).head(10)
    bottom_10_region_articles = region_article_count_df.sort_values(by='ArticleCount', ascending=True).head(10)

    return top_10_region_articles, bottom_10_region_articles


def analyze_sentiment_statistics(rating_df, traffic_data_df):
    """
    Convert sentiment to numeric values and calculate descriptive statistics by domain.
    Compare global sentiment distribution with the distribution for the top 10 domains by traffic.
    """

    # Convert sentiment to numeric values for descriptive statistics
    sentiment_mapping = {'Negative': -1, 'Neutral': 0, 'Positive': 1}
    rating_df['title_sentiment_numeric'] = rating_df['title_sentiment'].map(sentiment_mapping)
    rating_df['title_sentiment_numeric'] = pd.to_numeric(rating_df['title_sentiment_numeric'])

    # Group by domain and calculate descriptive statistics
    sentiment_stats = rating_df.groupby('source_name')['title_sentiment_numeric'].agg(
        mean_sentiment=np.mean,
        median_sentiment=np.median,
        variance_sentiment=np.var,
        count='count'
    ).reset_index()

    # Identify top 10 domains by visitor traffic
    top_10_traffic_domains = traffic_data_df.sort_values(by='GlobalRank').head(10)['Domain']

    # Filter sentiment statistics for these top 10 domains
    top_10_sentiment_stats = sentiment_stats[sentiment_stats['source_name'].isin(top_10_traffic_domains)]

    # Global sentiment distribution
    global_sentiment_distribution = rating_df['title_sentiment'].value_counts(normalize=True)

    # Sentiment distribution for top 10 domains
    top_10_domains_sentiment_distribution = rating_df[rating_df['source_name'].isin(top_10_traffic_domains)]['title_sentiment'].value_counts(normalize=True)

    return sentiment_stats, global_sentiment_distribution, top_10_domains_sentiment_distribution, top_10_sentiment_stats


