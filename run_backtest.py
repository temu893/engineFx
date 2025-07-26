# forex_backtest_engine/run_backtest.py
import backtrader as bt
from strategies.sma_crossover import SmaCross
import yfinance as yf

class ForexData(bt.feeds.PandasData):
    params = (('datetime', None),)

def run():
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0.0002)

    df = yf.download('EURUSD=X', start='2022-01-01', end='2023-01-01', interval='1h')
    df.dropna(inplace=True)
    data = ForexData(dataname=df)
    
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    cerebro.run()
    cerebro.plot()

if __name__ == '__main__':
    run()
