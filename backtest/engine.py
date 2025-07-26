import backtrader as bt
import yfinance as yf
from datetime import datetime
import importlib.util
import pandas as pd
import sys

class BacktestRunner:
    def __init__(self, symbol, strategy_path, start, end):
        self.symbol = symbol
        self.strategy_path = strategy_path
        self.start = start
        self.end = end

    def load_strategy(self):
        spec = importlib.util.spec_from_file_location("strategies.sma_crossover", self.strategy_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["strategies.sma_crossover"] = module  # <-- Register manually
        spec.loader.exec_module(module)
        return module.CustomStrategy

    def run(self):
        cerebro = bt.Cerebro()
        cerebro.addsizer(bt.sizers.FixedSize, stake=100)

        print(f"Downloading data for {self.symbol}...")
        raw_data = yf.download(
            self.symbol,
            start=self.start,
            end=self.end,
            auto_adjust=False,
            progress=False,
            group_by='column'
        )

        print("Downloaded data type:", type(raw_data))

        # If MultiIndex (e.g., ('Adj Close', 'EURUSD=X')), flatten it
        if isinstance(raw_data.columns, pd.MultiIndex):
            raw_data.columns = raw_data.columns.get_level_values(0)

        # Rename columns to what Backtrader expects
        raw_data = raw_data.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })

        raw_data.dropna(inplace=True)  # Clean any bad rows

        # Feed into Backtrader
        data = bt.feeds.PandasData(dataname=raw_data)
        cerebro.adddata(data)

        strategy_class = self.load_strategy()
        cerebro.addstrategy(strategy_class)

        print("Running backtest...")
        results = cerebro.run()
        cerebro.plot()
        return results


if __name__ == "__main__":
    runner = BacktestRunner(
        symbol="EURUSD=X",
        strategy_path="strategies/sma_crossover.py",
        start="2022-01-01",
        end="2023-01-01"
    )
    runner.run()
