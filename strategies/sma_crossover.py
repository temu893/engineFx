import backtrader as bt

class CustomStrategy(bt.Strategy):
    params = (
        ("short_period", 10),
        ("long_period", 20),
    )

    def __init__(self):
        self.sma_short = bt.ind.SMA(period=self.params.short_period)
        self.sma_long = bt.ind.SMA(period=self.params.long_period)
        self.crossover = bt.ind.CrossOver(self.sma_short, self.sma_long)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()
