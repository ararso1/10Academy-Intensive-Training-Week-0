
### Some of the functions available in the notebooks and codes in this repository

#### News Data Parsing Functions
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

`clean_data`:     Clean the input DataFrame by filling missing values, ensuring correct data types, and handling invalid dates.
    
    Parameters:
    - df (DataFrame): The input DataFrame to clean.
    - date_columns (list of str, optional): List of column names to be parsed as dates.
    - fillna_strategy (str or dict, optional): Strategy to fill missing values. Options are 'mean', 'median', 'mode', or a dictionary of column-specific strategies.
    - dropna_threshold (float, optional): Threshold for dropping rows with missing values. Rows with missing values above this threshold will be dropped.
    - date_format (str, optional): Format to enforce for date columns. If None, pandas will infer the format.
    - custom_types (dict, optional): A dictionary specifying the desired data types for specific columns.
    
    Returns:
    - cleaned_df (DataFrame): The cleaned DataFrame.