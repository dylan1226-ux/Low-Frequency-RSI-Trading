import numpy as np
from data.data_preprocessing import load_and_preprocess
from RSI_calculator.calculator_rsi import RSICalculation
from backtest.backtesting import StrategyBacktest
from Optimization.sensitivity import sensitivity_analysis
from visualization.graph import graphing_RSI_signal, graphing_pnl, graphing_heatmap


def main():

    file_path = "/Users/dylanpan/Library/Mobile Documents/com~apple~CloudDocs/Desktop/DongXing Securities/2016.01.01-2024.10.16机器学习数据.csv"
    stock_id = 600020

    # Process Data
    data = load_and_preprocess(file_path, stock_id)


    # Signal1 and Signal2
    signal1_data = RSICalculation.trade_signal_1(data.copy())
    signal2_data = RSICalculation.trade_signal_2(data.copy())


    # visualization
    graphing_RSI_signal(signal1_data, tail_period=500, signal=1, RSI_graph=True)
    graphing_RSI_signal(signal2_data, tail_period=500, signal=2, RSI_graph=True)


    # a trading example
    signal_1_buy_amounts=1000000
    signal_1_sell_amounts=1000000
    signal_2_buy_amounts=100000
    signal_2_sell_amounts=200000
    backtest = StrategyBacktest(signal1_data, signal2_data,
                                signal_1_buy_amount=signal_1_buy_amounts,
                               signal_1_sell_amount= signal_1_sell_amounts,
                               signal_2_buy_amount=signal_2_buy_amounts,
                              signal_2_sell_amount=signal_2_sell_amounts)

    # plot pnl and long/short positions
    graphing_pnl(backtest.combined_data)

    # performance
    performance_df = backtest.calculate_performance_metrics()
    print(performance_df)

    # sensitivity and best parameters
    # GridSearch
    buy_amount_range = np.arange(1000000, 10000000, 5000000)
    sell_amount_range = np.arange(1000000, 10000000, 5000000)
    results_df, best_sharpe_ratio, best_params = sensitivity_analysis(signal1_data,
                                                                      signal2_data,
                                                                      buy_amount_range,
                                                                      sell_amount_range)


    # Best Parameters
    print("Best Sharpe Ratio:", best_sharpe_ratio)
    print("Best Parameters:\n", best_params)

    # graph heatmap
    graphing_heatmap(results_df)


if __name__ == '__main__':
    main()