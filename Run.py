import ccxt
import pandas as pd

# Initialize the exchange object
exchange = ccxt.binance({
    'rateLimit': 2000,
    'enableRateLimit': True,
})

# Define the symbol and time interval for the data
symbol = 'BTC/USDT'
time_interval = '1d'

# Fetch historical OHLCV data
ohlcv = exchange.fetch_ohlcv(symbol, time_interval)

# Convert the data to a pandas dataframe
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Calculate the 20-day simple moving average
df['sma20'] = df['close'].rolling(window=20).mean()

# Calculate the 40-day simple moving average
df['sma40'] = df['close'].rolling(window=40).mean()

# Initialize the buying and selling flags
df['buy'] = 0
df['sell'] = 0

# Set the buying flag when the close price is above the 20-day SMA
df.loc[df['close'] > df['sma20'], 'buy'] = 1

# Set the selling flag when the close price drops below the 40-day SMA
df.loc[df['close'] < df['sma40'], 'sell'] = 1

# Define the holding period (in days)
hold_period = 5

# Initialize the current holding status
df['hold'] = 0
df.loc[df['buy'] == 1, 'hold'] = 1

# Loop through the dataframe and check for selling conditions
for i in range(hold_period, len(df)):
    if df.iloc[i]['hold'] == 1:
        if df.iloc[i]['sell'] == 1:
            df.at[i, 'hold'] = 0

# Print the final dataframe
print(df)
