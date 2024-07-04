# Stock Data Analysis Script for AAPL using Polygon.io API

import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Replace with your actual API key from Polygon.io
API_KEY = 'ARc_ONsSnqUF9t3i9VZR7fyVrw2iHFEd'

# API endpoint URL for fetching AAPL stock data
BASE_URL = 'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2021-06-30/2024-06-01'

def fetch_stock_data(api_key, base_url):
    """
    Fetches historical stock price data for AAPL from Polygon.io API.

    Args:
    - api_key (str): Your Polygon.io API key.
    - base_url (str): Base URL for the API endpoint.

    Returns:
    - dict: JSON response containing stock price data.
    """
    url = f"{base_url}?adjusted=true&sort=asc&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        if 'results' not in data:
            raise ValueError("Unexpected response format or missing data")
        
        return data
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def process_stock_data(data):
    """
    Converts JSON stock data into a pandas DataFrame and processes it.

    Args:
    - data (dict): JSON data from Polygon.io API.

    Returns:
    - pd.DataFrame: Processed stock price data as a DataFrame.
    """
    df = pd.DataFrame(data['results'])
    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
    return df

def analyze_stock_data(df):
    """
    Analyzes stock price data and generates summary statistics.

    Args:
    - df (pd.DataFrame): DataFrame containing stock price data.

    Returns:
    - dict: Summary statistics such as start date, end date, average price,
            highest price, and lowest price.
    """
    summary = {
        'Start Date': df['timestamp'].min(),
        'End Date': df['timestamp'].max(),
        'Average Price': df['c'].mean(),
        'Highest Price': df['h'].max(),
        'Lowest Price': df['l'].min()
    }
    return summary

def visualize_stock_data(df):
    """
    Visualizes AAPL stock closing prices over time.

    Args:
    - df (pd.DataFrame): DataFrame containing stock price data.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['c'], label='Closing Price', color='b')
    plt.title('AAPL Stock Price (2021-2024)')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to orchestrate fetching, processing, and visualizing stock data.
    """
    # Fetch data from Polygon.io API
    stock_data = fetch_stock_data(API_KEY, BASE_URL)
    
    # Process data into DataFrame
    df = process_stock_data(stock_data)
    
    # Analyze and print summary statistics
    summary_stats = analyze_stock_data(df)
    print("Summary Statistics:")
    for key, value in summary_stats.items():
        print(f"{key}: {value}")
    
    # Visualize stock closing prices
    visualize_stock_data(df)

if __name__ == "__main__":
    main()
