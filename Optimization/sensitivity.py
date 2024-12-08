import pandas as pd
from backtest.backtesting import StrategyBacktest

def sensitivity_analysis(data_1, data_2, buy_amount_range, sell_amount_range):
    """
    sensitivity_analysis and optimized parameters
    """
    results = []

    for s1_buy in buy_amount_range:
        for s1_sell in sell_amount_range:
            for s2_buy in buy_amount_range:
                for s2_sell in sell_amount_range:
                    backtest = StrategyBacktest(data_1, data_2,
                                                signal_1_buy_amount=s1_buy,
                                                signal_1_sell_amount=s1_sell,
                                                signal_2_buy_amount=s2_buy,
                                                signal_2_sell_amount=s2_sell)
                    performance_df = backtest.calculate_performance_metrics()
                    sharpe_ratio = performance_df.loc[0, 'Sharpe Ratio']
                    results.append((s1_buy, s1_sell, s2_buy, s2_sell, sharpe_ratio))

    results_df = pd.DataFrame(results, columns=['Signal_1_Buy', 'Signal_1_Sell', 'Signal_2_Buy', 'Signal_2_Sell',
                                                'Sharpe Ratio'])

    # best parameters
    best_row = results_df.loc[results_df['Sharpe Ratio'].idxmax()]
    best_params = best_row[['Signal_1_Buy', 'Signal_1_Sell', 'Signal_2_Buy', 'Signal_2_Sell']]
    best_sharpe_ratio = best_row['Sharpe Ratio']

    return results_df, best_sharpe_ratio, best_params
