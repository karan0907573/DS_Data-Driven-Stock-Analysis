import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # For example data
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from helper.dbhelper import get_stock_data,get_sector_data

def volatility_view():
    stock_df = get_stock_data()

    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.sort_values(by=['Ticker', 'date'], inplace=True)

    # Daily return
    stock_df['Daily Return'] = stock_df.groupby('Ticker')['close'].pct_change()

    # Volatility (standard deviation of daily returns)
    volatility_df = (
        stock_df.dropna(subset=['Daily Return'])
                .groupby('Ticker')['Daily Return']
                .std()
                .reset_index()
    )

    volatility_df.columns = ['Ticker', 'Volatility']

    # Top 10 most volatile
    top_10_volatility = volatility_df.sort_values(by='Volatility', ascending=False).head(10)

    # Convert to percentage
    top_10_volatility['Volatility_Pct'] = top_10_volatility['Volatility'] * 100

    # ----- Plotly Bar Chart -----
    fig = px.bar(
        top_10_volatility,
        x="Ticker",
        y="Volatility_Pct",
        title="Top 10 Most Volatile Stocks (Standard Deviation of Daily Returns)",
        labels={"Ticker": "Stock Ticker", "Volatility_Pct": "Volatility (%)"},
        text=top_10_volatility['Volatility_Pct'].round(2),
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        template="plotly_white",
        height=500,
        yaxis=dict(showgrid=True)
    )
    return fig

def cumulative_return_view():
    stock_df=get_stock_data()

    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.sort_values(by=['Ticker', 'date'], inplace=True)
    stock_df.reset_index(drop=True, inplace=True)

    stock_df['Daily Return'] = stock_df.groupby('Ticker')['close'].pct_change()

    daily_return_series = stock_df.groupby('Ticker')['close'].pct_change()
    stock_df['Daily Return'] = daily_return_series

    cumulative_returns_series = daily_return_series.groupby(stock_df['Ticker']).apply(
        lambda x: (1 + x.fillna(0)).cumprod() - 1
    )

    stock_df['Cumulative Return'] = cumulative_returns_series.droplevel(0)

    final_returns = stock_df.drop_duplicates(subset=['Ticker'], keep='last').sort_values(
        by='Cumulative Return', ascending=False
    ).head(5)

    top_5_tickers = final_returns['Ticker'].tolist()

    top_5_df = stock_df[stock_df['Ticker'].isin(top_5_tickers)]

    fig=plt.figure(figsize=(12, 5))

    for ticker in top_5_tickers:
        ticker_data = top_5_df[top_5_df['Ticker'] == ticker]
        plt.plot(ticker_data['date'], ticker_data['Cumulative Return'] * 100, label=ticker)

    plt.title('Cumulative Return Over Time for Top 5 Performing Stocks', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.legend(title='Stock Ticker', loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig
    
def cumulative_return_plotly_view():
    stock_df = get_stock_data()

    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.sort_values(by=['Ticker', 'date'], inplace=True)

    # Daily return
    stock_df['Daily Return'] = stock_df.groupby('Ticker')['close'].pct_change()

    # Cumulative return
    stock_df['Cumulative Return'] = (
        stock_df
        .groupby('Ticker')['Daily Return']
        .apply(lambda x: (1 + x.fillna(0)).cumprod() - 1)
        .reset_index(level=0, drop=True)
    )

    # Final cumulative return per ticker
    final_returns = (
        stock_df.drop_duplicates(subset=['Ticker'], keep='last')
        .sort_values(by='Cumulative Return', ascending=False)
        .head(5)
    )

    top_5_tickers = final_returns['Ticker'].tolist()
    top_5_df = stock_df[stock_df['Ticker'].isin(top_5_tickers)]

    fig = go.Figure()

    for ticker in top_5_tickers:
        ticker_data = top_5_df[top_5_df['Ticker'] == ticker]

        fig.add_trace(go.Scatter(
            x=ticker_data['date'],
            y=ticker_data['Cumulative Return'] * 100,
            mode='lines',
            name=ticker
        ))

    fig.update_layout(
        title="Cumulative Return Over Time for Top 5 Performing Stocks",
        xaxis_title="Date",
        yaxis_title="Cumulative Return (%)",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    # Add grid lines for readability
    fig.update_yaxes(showgrid=True, gridwidth=0.3)
    fig.update_xaxes(showgrid=False)
    return fig

def stock_return_view():
    stock_df = get_stock_data()
    sector_df = get_sector_data()

    # Prepare stock data
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.sort_values(by=['Ticker', 'date'], inplace=True)

    # Total return per ticker
    total_returns_per_ticker = stock_df.groupby('Ticker')['close'].agg(
        start_price='first',
        end_price='last'
    ).reset_index()

    total_returns_per_ticker['Total Return'] = (
        (total_returns_per_ticker['end_price'] - total_returns_per_ticker['start_price']) /
        total_returns_per_ticker['start_price']
    )

    # Merge with sector data
    sector_map = sector_df[['Ticker', 'Sector']].drop_duplicates()

    merged_df = total_returns_per_ticker[['Ticker', 'Total Return']].merge(
        sector_map, on='Ticker', how='left'
    )

    merged_df = merged_df.dropna(subset=['Sector'])

    # Average sector performance
    sector_performance = (
        merged_df.groupby('Sector')['Total Return']
                .mean()
                .sort_values(ascending=False)
                .reset_index()
    )

    sector_performance.columns = ['Sector', 'Average Total Return']

    # Convert to percentage
    sector_performance['Average Return (%)'] = sector_performance['Average Total Return'] * 100

    # Color coding (green = positive, red = negative)
    sector_performance['Color'] = sector_performance['Average Return (%)'].apply(
        lambda x: 'green' if x >= 0 else 'red'
    )

    # -------- Plotly Bar Chart --------
    fig = px.bar(
        sector_performance,
        x="Sector",
        y="Average Return (%)",
        color="Color",
        color_discrete_map={"green": "green", "red": "red"},
        title="Average Total Return by Sector",
        text=sector_performance['Average Return (%)'].round(2),
    )

    fig.update_traces(textposition='outside')

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Average Total Return (%)",
        xaxis_tickangle=-45,
        template="plotly_white",
        showlegend=False,
        height=600,
    )
    return fig

def stock_correlation_view():
    stock_df = get_stock_data()

    # Pivot to wide format
    pivot_df = stock_df.pivot_table(index='date', columns='Ticker', values='close')

    # Correlation matrix
    correlation_matrix = pivot_df.corr()

    # Plotly heatmap
    fig = px.imshow(
        correlation_matrix,
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1,
        labels=dict(x="Ticker", y="Ticker", color="Correlation"),
        title="Stock Price Correlation Heatmap",
        text_auto=True,
    )

    # Improve layout
    fig.update_layout(
        xaxis=dict(tickangle=45),
        width=900,
        height=900,
    )
    return fig

def monthly_gainers_losers_view():
    stock_df = get_stock_data()
    print(stock_df)
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.sort_values(by=['Ticker', 'date'], inplace=True)

    monthly_prices = stock_df.groupby(['Ticker', 'month'])['close'].agg(
        start_price='first',
        end_price='last'
    ).reset_index()


    # Monthly return
    monthly_prices['Monthly Return'] = (
        (monthly_prices['end_price'] - monthly_prices['start_price']) /
        monthly_prices['start_price']
    )
   
    # Get list of unique months
    unique_months = sorted(monthly_prices['month'].unique())

    selected_month = st.selectbox("Select Month", unique_months,width=200)
    print(selected_month)
    month_data = monthly_prices[monthly_prices['month'] == selected_month] \
                .sort_values(by='Monthly Return', ascending=False)

    # Top 5 gainers & losers
    top_gainers = month_data.head(5)
    top_losers = month_data.tail(5)

    combined = pd.concat([top_gainers, top_losers]) \
                .sort_values(by='Monthly Return', ascending=False)

    # Convert to percentage
    combined['Return (%)'] = combined['Monthly Return'] * 100

    # Color coding
    combined['Color'] = combined['Return (%)'].apply(
        lambda x: 'green' if x > 0 else 'red'
    )

    # ---------- PLOTLY CHART ----------
    fig = px.bar(
        combined,
        x="Ticker",
        y="Return (%)",
        color="Color",
        color_discrete_map={"green": "green", "red": "red"},
        text=combined['Return (%)'].round(2),
        title=f"Top 5 Gainers & Losers — {selected_month}"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_tickangle=-45,
        height=600
    )
    return fig