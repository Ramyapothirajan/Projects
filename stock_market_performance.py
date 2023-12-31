# pip install yfinance
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import seaborn as sns 
import matplotlib.pyplot as plt 

tickers = ['GOOGL', 'AMZN', 'AAPL', 'MSFT', 'JPM']
# tickers list remains the same, containing the desired stock symbols.
end_date = datetime.now()
start_date = end_date - timedelta(days = 100)
# start_date = datetime.now() - pd.DateOffset(months=3)
df = yf.download(tickers, start=start_date, end=end_date, group_by = 'ticker')
df = pd.concat([df[ticker] for ticker in tickers], keys = tickers, names = ['Ticker', 'Date'])
df = df.reset_index()
print(df.head())

# line chart to analyze the historical price movement of a stock or index, as explained in the previous response. 
# This will provide insights into trends, support/resistance levels, and potential entry or exit points.
sns.set(style = 'darkgrid')
plt.figure(figsize = (14,8))
sns.lineplot(data = df, x = 'Date', y = 'Close', hue = 'Ticker', linewidth = 2)
plt.title("Stock Market Performance for that last 100 days", fontweight = 'bold')
plt.xlabel('Date', fontweight = 'bold')
plt.ylabel('Closing Price', fontweight = 'bold')
plt.xticks(rotation = 45)
plt.legend(title = 'Ticker')
plt.show()

# Moving Averages: Add moving averages to your line chart to smooth out the price data and identify trends more easily.
df['MA_10'] = df.groupby('Ticker')['Close'].rolling(window = 10).mean().reset_index(0, drop = True)
df['MA_20'] = df.groupby('Ticker')['Close'].rolling(window = 20).mean().reset_index(level = 0, drop = True)
# Rolling means, also known as moving averages, are statistical calculations that provide a smoothed average value over a specified window or period of time. 
# It is commonly used to reduce noise or fluctuations in time series data.
sns.set(style = 'darkgrid')
fig, axes = plt.subplots(len(tickers), 1, figsize=(16, 14), sharex=True)
# sharex=True, the x-axis is shared among all subplots, and any changes made to the x-axis of one subplot will be reflected in all the other subplots.
for ticker, ax in zip(tickers, axes):
    group = df[df['Ticker'] == ticker]
    ax.plot(group['Date'], group['Close'], label='Stock Price')
    ax.plot(group['Date'], group['MA_10'], label='MA_10')
    ax.plot(group['Date'], group['MA_20'], label='MA_20')
    ax.set_title(f'{ticker} Moving Averages', fontweight = 'bold')
    ax.set_ylabel('Closing Price', fontweight = 'bold')
    ax.legend()
  
plt.xlabel('Date', fontweight = 'bold')
plt.tight_layout()
plt.show()

# Relative Strength Index (RSI): Incorporate the RSI indicator into your analysis. 
# RSI measures the speed and change of price movements, indicating overbought or oversold conditions. 
# A high RSI reading (above 70) suggests overbought conditions and a potential reversal, 
# while a low RSI reading (below 30) suggests oversold conditions and a possible bounce-back.
# Traders and analysts often use the RSI in conjunction with other technical indicators and chart patterns to confirm potential trend reversals, to identify divergences between the RSI and price movements, and to generate trading signals.
# It is important to note that the RSI is a momentum oscillator and should be used in conjunction with other forms of analysis for better decision-making
# The RSI is calculated based on the average gains and losses over a specified period of time, typically 14 periods.
# The average gain and average loss are typically calculated using the difference between the closing prices of consecutive periods.

def calculate_rsi(df, period = 14):
    price_diff = df['Close'].diff(1)
    up = price_diff.where(price_diff > 0, 0)
    down = -price_diff.where(price_diff < 0, 0)
    avg_gain = up.rolling(window = period).mean()
    avg_loss = down.rolling(window = period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
# rsi = calculate_rsi(df)
df['RSI'] = df.groupby('Ticker').apply(calculate_rsi).reset_index(level = 0, drop=True)

sns.set(style = 'darkgrid')
fig, axes = plt.subplots(len(tickers), 1, figsize=(20, 20))
# sharex=True, the x-axis is shared among all subplots, and any changes made to the x-axis of one subplot will be reflected in all the other subplots.
for i, ticker in enumerate(tickers):
    axes[i].plot(df[df['Ticker'] == ticker]['Date'], df[df['Ticker'] == ticker]['RSI'])
    axes[i].set_title(f'{ticker} RSI', fontweight = 'bold')
    axes[i].set_ylabel('RSI', fontweight = 'bold') 
    axes[i].set_xlabel('Date', fontweight = 'bold')

plt.tight_layout()
plt.show()
# Close.shift(1), we shift the closing prices one period back in time, so that we can calculate the price differences between the current period and the previous period. 

# Volume Comparison with respect to companies
plt.figure(figsize = (12,8))
plt.bar(df['Ticker'], df['Volume'], color='blue', label='Volume')
plt.title('Volume Comparison')
plt.xlabel('Company Ticker')
plt.ylabel('Volume')
plt.legend()
plt.tight_layout()
plt.show()

# Volume Analysis: Evaluate the trading volume alongside the price movement. 
# Volume can indicate the strength of a price trend. 
# Higher volume during price increases suggests buying pressure, 
# while higher volume during price decreases indicates selling pressure. 
# Analyzing volume can provide confirmation or divergence signals when compared to price movements.

df['Avg_volume'] = df.groupby('Ticker')['Volume'].transform(lambda x: x.rolling(window=10).mean())
# transform - calculates the rolling mean with a window size of 10 for each group defined by the groupby operation and returns the transformed values aligned with the original dataframe.
sns.set(style = 'darkgrid')
fig, axes = plt.subplots(len(tickers), 1, figsize=(16, 14))
# sharex=True, the x-axis is shared among all subplots, and any changes made to the x-axis of one subplot will be reflected in all the other subplots.
for i, ticker in enumerate(tickers):
    axes[i].plot(df[df['Ticker'] == ticker]['Date'], df[df['Ticker'] == ticker]['Avg_volume'], label = ticker)
    axes[i].set_title(f'{ticker}-Average Volume', fontweight = 'bold')
    axes[i].set_ylabel('Volume', fontweight = 'bold') 
    axes[i].set_xlabel('Date', fontweight = 'bold')
    axes[i].legend(loc='upper right') 

plt.tight_layout()
plt.show()
