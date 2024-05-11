from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, time, asset, quantity, side, entry, take_profit, stop_loss, result=None):
        self.time = time
        self.asset = asset
        self.quantity = quantity
        self.side = side
        self.entry = entry
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.result = result

def calculate_signals(data):
    signals = []
    for index, row in data.iterrows():
        signal = "No signal"
        take_profit_price = None
        stop_loss_price = None
        current_price = row['close']

        if row['rsi'] > 65 and row['adx'] > 25:
            signal = 'sell'
        elif row['rsi'] < 35 and row['adx'] > 25:
            signal = 'buy'

        if signal == "buy":
            stop_loss_price = round((1 - 0.02) * current_price, 1)
            take_profit_price = round((1 + 0.1) * current_price, 1)
        elif signal == "sell":
            stop_loss_price = round((1 + 0.02) * current_price, 1)
            take_profit_price = round((1 - 0.1) * current_price, 1)

        signals.append(Signal(
            row['time'],
            'BTCUSDT',
            100,
            signal,
            current_price,
            take_profit_price,
            stop_loss_price,
            None  
        ))

    return signals

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')



    data = pd.DataFrame({
        'time': pd.date_range(start=yesterday, end=today, periods=100),
        'close': np.random.randn(100),
        'rsi': np.random.randint(30, 80, 100),
        'adx': np.random.randint(20, 40, 100)
    })

    signals = calculate_signals(data)

  
    plt.figure(figsize=(12, 6))
    plt.plot(data['time'], data['close'], label='BTCUSDT price')

    for signal in signals:
        if signal.side == 'buy':
            plt.scatter(signal.time, signal.entry, color='green', label='Buy signal', marker='^', s=100)
        elif signal.side == 'sell':
            plt.scatter(signal.time, signal.entry, color='red', label='Sell signal', marker='v', s=100)

    plt.title('BTCUSDT price and signals')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()


