import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
from pandas_ta import rsi, cci, macd

def analyze_indicators(df):
    df['RSI'] = rsi(df['close'])
    df['CCI'] = cci(df['high'], df['low'], df['close'])
    macd_vals = macd(df['close'])
    df = pd.concat([df, macd_vals], axis=1)
    
    df['MACD_prev'] = df['MACD_12_26_9'].shift(1)
    df['MACDs_prev'] = df['MACDs_12_26_9'].shift(1)
    
    df['Prediction'] = df.apply(lambda row: interpret_signals(row), axis=1)
    return df

def interpret_signals(row):
    rsi_pred = "Ціна падатиме" if row['RSI'] < 30 else "Ціна зростатиме" if row['RSI'] > 70 else "Невідомо"
    cci_pred = "Ціна падатиме" if row['CCI'] > 100 else "Ціна зростатиме" if row['CCI'] < -100 else "Невідомо"
    macd_pred = "Ціна зростатиме" if row['MACD_12_26_9'] > row['MACDs_12_26_9'] and row['MACD_prev'] < row['MACDs_prev'] else "Ціна падатиме" if row['MACD_12_26_9'] < row['MACDs_12_26_9'] and row['MACD_prev'] > row['MACDs_prev'] else "Невідомо"
    
    return rsi_pred if rsi_pred != "Невідомо" else cci_pred if cci_pred != "Невідомо" else macd_pred

start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
klines = Client().get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, start_date, end_date)

df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
for col in ['open', 'high', 'low', 'close']:
    df[col] = df[col].astype(float)

analyzed_df = analyze_indicators(df)

analyzed_df[['RSI', 'CCI', 'MACD_12_26_9', 'MACDs_12_26_9', 'Prediction']].to_csv('analyzed_prediction.csv', index=False)
