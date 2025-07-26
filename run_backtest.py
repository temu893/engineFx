from backtest.engine import BacktestRunner

if __name__ == "__main__":
    runner = BacktestRunner(
        symbol="EURUSD=X",
        strategy_path="strategies/sma_crossover.py",
        start="2022-01-01",
        end="2023-01-01"
    )
    runner.run()
