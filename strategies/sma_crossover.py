import backtrader as bt

class SmaCross(bt.SignalStrategy):
    params = dict(period=20)

    def __init__(self):
        sma = bt.ind.SMA(period=self.p.period)
        crossover = bt.ind.CrossOver(self.data.close, sma)
        self.signal_add(bt.SIGNAL_LONG, crossover)
