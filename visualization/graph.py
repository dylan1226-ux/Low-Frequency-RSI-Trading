import matplotlib.pyplot as plt
import seaborn as sns

def graphing_RSI_signal(trade_data, tail_period=500, signal=1, RSI_graph=True):
    """
    This function plots buy/sell signal simulation chart and optionally the RSI.
    """
    recent_trade_data = trade_data.tail(tail_period)

    plt.figure(figsize=(14, 7))

    # Closing price and trade signals
    plt.subplot(2, 1, 1)
    plt.plot(recent_trade_data['CLOCK'], recent_trade_data['CLOSE'], label='Close Price')
    plt.scatter(recent_trade_data['CLOCK'][recent_trade_data['Buy'] == 1],
                recent_trade_data['CLOSE'][recent_trade_data['Buy'] == 1],
                marker='^', color='g', label='Buy Signal', s=100, alpha=1)
    plt.scatter(recent_trade_data['CLOCK'][recent_trade_data['Sell'] == 1],
                recent_trade_data['CLOSE'][recent_trade_data['Sell'] == 1],
                marker='v', color='r', label='Sell Signal', s=100, alpha=1)
    plt.scatter(recent_trade_data['CLOCK'][recent_trade_data['Exit'] == 1],
                recent_trade_data['CLOSE'][recent_trade_data['Exit'] == 1],
                marker='x', color='orange', label='Buy Exit', s=100, alpha=1)
    plt.legend()
    plt.title(f'Close Price and Trade Signal {signal}')

    if RSI_graph:
        # Plot RSI
        plt.subplot(2, 1, 2)
        plt.plot(recent_trade_data['CLOCK'], recent_trade_data['RSI'], label='RSI')
        plt.axhline(30, linestyle='--', alpha=0.5, color='red')
        plt.axhline(70, linestyle='--', alpha=0.5, color='red')
        plt.title('RSI')
        plt.legend()

    plt.tight_layout()
    plt.show()


def graphing_pnl(combined_data):
    """
    graph pnl and long/short positions
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    fig, ax1 = plt.subplots(figsize=(14, 8))
    ax2 = ax1.twinx()

    ax1.plot(combined_data['CLOCK'], combined_data['CLOSE'], label='Close Price', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Close Price')

    # Compute PnL and balance
    pnl_list = []
    for i in range(1, len(combined_data)):
        prev_balance = combined_data.iloc[i - 1]['Balance']
        current_balance = combined_data.iloc[i]['Balance']
        inter_pnl = current_balance - prev_balance
        pnl_list.append([combined_data.iloc[i]['CLOCK'], inter_pnl, current_balance])

    pnl_df = pd.DataFrame(pnl_list, columns=['time', 'interPNL', 'balance'])

    # Plot balance
    ax2.plot(pnl_df['time'], pnl_df['balance'], label='Balance', color='purple', alpha=0.6)
    ax2.set_ylabel('Balance')

    #  buy and sell signals
    buy_1 = combined_data[combined_data['Trade_1'] > 0]
    buy_2 = combined_data[combined_data['Trade_2'] > 0]
    sell_1 = combined_data[combined_data['Trade_1'] < 0]
    sell_2 = combined_data[combined_data['Trade_2'] < 0]

    ylim = ax1.get_ylim()
    height = ylim[1] - ylim[0]
    scale = 0.25 / max(buy_1['Trade_1'].max(), buy_2['Trade_2'].max(), abs(sell_1['Trade_1'].min()),
                       abs(sell_2['Trade_2'].min()))

    # Plot buy signals
    for _, row in buy_1.iterrows():
        ax1.axvline(x=row['CLOCK'], ymin=0.5, ymax=0.5 + (row['Trade_1'] * scale), color='green', alpha=0.5,
                    linewidth=2)
    for _, row in buy_2.iterrows():
        ax1.axvline(x=row['CLOCK'], ymin=0.5, ymax=0.5 + (row['Trade_2'] * scale), color='lightgreen', alpha=0.5,
                    linewidth=2)

    # Plot sell signals
    for _, row in sell_1.iterrows():
        ax1.axvline(x=row['CLOCK'], ymin=0.5 + (row['Trade_1'] * scale), ymax=0.5, color='red', alpha=0.5, linewidth=2)
    for _, row in sell_2.iterrows():
        ax1.axvline(x=row['CLOCK'], ymin=0.5 + (row['Trade_2'] * scale), ymax=0.5, color='lightcoral', alpha=0.5,
                    linewidth=2)


    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.title('Close Price, Balance and Trading Signals')
    plt.show()


def graphing_heatmap(results_df):
    """
    Plot a heatmap for the Sharpe ratio sensitivity analysis.
     """
    #   pivot table
    pivot_table = results_df.pivot_table(values='Sharpe Ratio',
                                        index=['Signal_1_Buy', 'Signal_1_Sell'],
                                        columns=['Signal_2_Buy', 'Signal_2_Sell'])

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, cmap='viridis')
    plt.title('Sharpe Ratio Sensitivity Analysis Heatmap')
    plt.xlabel('Signal 2 Buy/Sell Amount')
    plt.ylabel('Signal 1 Buy/Sell Amount')
    plt.show()