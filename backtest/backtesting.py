import pandas as pd
import matplotlib.pyplot as plt

class StrategyBacktest:
    def __init__(self, data_1, data_2, initial_funds=10000000, allocation=1000000, min_tick=2, multiplier=5, slippage=1,
                 signal_1_buy_amount=700000, signal_1_sell_amount=100000,
                 signal_2_buy_amount=300000, signal_2_sell_amount=100000):
        self.data_1 = data_1.rename(columns={'Buy': "Signal_1_Buy", "Sell": "Signal_1_Sell", "Exit": "Signal_1_Exit"})
        self.data_2 = data_2.rename(columns={'Buy': "Signal_2_Buy", "Sell": "Signal_2_Sell", "Exit": "Signal_2_Exit"})
        self.combined_data = pd.concat([self.data_1, self.data_2], axis=1)
        self.combined_data = self.combined_data.loc[:, ~self.combined_data.columns.duplicated()]
        self.combined_data['CLOCK'] = pd.to_datetime(self.combined_data['CLOCK'])
        self.initial_funds = initial_funds
        self.allocation = allocation
        self.min_tick = min_tick
        self.multiplier = multiplier
        self.slippage = slippage
        self.signal_1_buy_amount = signal_1_buy_amount
        self.signal_1_sell_amount = signal_1_sell_amount
        self.signal_2_buy_amount = signal_2_buy_amount
        self.signal_2_sell_amount = signal_2_sell_amount
        self.prepare_data()

    def prepare_data(self):
        """
        Initialize Data
        """
        self.combined_data['Contract_Value'] = self.combined_data['CLOSE'] * self.multiplier
        self.combined_data['Position_1'] = 0.0
        self.combined_data['Position_2'] = 0.0
        self.combined_data['Trade_1'] = 0.0
        self.combined_data['Trade_2'] = 0.0
        self.combined_data['Balance'] = 0.0
        self.combined_data.iloc[0, self.combined_data.columns.get_loc('Balance')] = self.initial_funds
        self.calculate_positions()
        self.calculate_returns()

    def calculate_positions(self):
        """
        Calculate the positions based on buy, sell, and exit signals for both strategies.
        """
        for i in range(1, len(self.combined_data)):
            contract_value = self.combined_data.iloc[i]['Contract_Value']
            previous_balance = self.combined_data.iloc[i - 1]['Balance']
            current_balance = previous_balance

            # signal for strategy 1
            if self.combined_data.iloc[i]['Signal_1_Buy'] == 1:
                current_balance = self.buy_signal_1(i, contract_value, current_balance)
            if self.combined_data.iloc[i]['Signal_1_Sell'] == 1:
                current_balance = self.sell_signal_1(i, contract_value, current_balance)
            if self.combined_data.iloc[i]['Signal_1_Exit'] == 1:
                current_balance = self.exit_signal_1(i, contract_value, current_balance)
            # signal for strategy 2
            if self.combined_data.iloc[i]['Signal_2_Buy'] == 1:
                current_balance = self.buy_signal_2(i, contract_value, current_balance)
            if self.combined_data.iloc[i]['Signal_2_Sell'] == 1:
                current_balance = self.sell_signal_2(i, contract_value, current_balance)
            if self.combined_data.iloc[i]['Signal_2_Exit'] == 1:
                current_balance = self.exit_signal_2(i, contract_value, current_balance)

            self.combined_data.iloc[i, self.combined_data.columns.get_loc('Balance')] = current_balance

    def buy_signal_1(self, i, contract_value, current_balance):
        """
        Signal 1 Buy: Position P=signal_1_buy_amount/ single contract price
        """
        position = int(self.signal_1_buy_amount / contract_value)
        trade_cost = position * self.slippage * self.multiplier * self.min_tick
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Position_1')] += position
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Trade_1')] = position
        return current_balance - (position * contract_value + trade_cost)

    def sell_signal_1(self, i, contract_value, current_balance):
        """
        Signal 1 Sell: Position P=signal_1_sell_amount/ price
        """
        position = int(self.signal_1_sell_amount / contract_value)
        new_position = self.combined_data.iloc[i]['Position_1'] - position
        trade_cost = position * self.slippage * self.multiplier * self.min_tick
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Position_1')] = max(new_position, 0)
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Trade_1')] = -position
        return current_balance + (position * contract_value - trade_cost)

    def exit_signal_1(self, i, contract_value, current_balance):
        """
        Signal one exit: Sell half
        """
        position = self.combined_data.iloc[i]['Position_1'] // 2
        new_position = self.combined_data.iloc[i]['Position_1'] - position
        trade_cost = position * self.slippage * self.multiplier * self.min_tick
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Trade_1')] = -position
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Position_1')] = max(new_position, 0)
        return current_balance + (position * contract_value - trade_cost)

    def buy_signal_2(self, i, contract_value, current_balance):
        """
        Signal 2 Buy: Position P=signal_2_buy_amount/ price
        """
        position = int(self.signal_2_buy_amount / contract_value)
        trade_cost = position * self.slippage * self.multiplier * self.min_tick
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Position_2')] += position
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Trade_2')] = position
        return current_balance - (position * contract_value + trade_cost)

    def sell_signal_2(self, i, contract_value, current_balance):
        """
        Signal 2 Sell: Position P=signal_2_sell_amount/ price
        """
        position = int(self.signal_2_sell_amount / contract_value)
        new_position = self.combined_data.iloc[i]['Position_2'] - position
        trade_cost = position * self.slippage * self.multiplier * self.min_tick
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Position_2')] = max(new_position, 0)
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Trade_2')] = -position
        return current_balance + (position * contract_value - trade_cost)

    def exit_signal_2(self, i, contract_value, current_balance):
        """
        Signal 2 Exit: Sell half
        """
        position = self.combined_data.iloc[i]['Position_2'] // 2
        new_position = self.combined_data.iloc[i]['Position_2'] - position
        trade_cost = position * self.slippage * self.multiplier * self.min_tick
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Trade_2')] = -position
        self.combined_data.iloc[i, self.combined_data.columns.get_loc('Position_2')] = max(new_position, 0)
        return current_balance + (position * contract_value - trade_cost)

    def calculate_returns(self):
        """
        Calculate Return
        """
        self.combined_data['Daily_Return_1'] = (self.combined_data['Position_1'].shift(1) * self.combined_data[
            'CLOSE'].diff()) / self.combined_data['Balance'].shift(1)
        self.combined_data['Daily_Return_2'] = (self.combined_data['Position_2'].shift(1) * self.combined_data[
            'CLOSE'].diff()) / self.combined_data['Balance'].shift(1)
        self.combined_data['Daily_Return'] = self.combined_data['Daily_Return_1'] + self.combined_data['Daily_Return_2']
        self.combined_data['Cumulative_Return'] = self.combined_data['Daily_Return'].cumsum()

    def calculate_performance_metrics(self):
        """
        Calculate Performance Metrics
        """
        average_daily_return = self.combined_data['Daily_Return'].mean()
        annualized_return = (1 + average_daily_return) ** 252 - 1  # 假设一年有252个交易日
        annualized_volatility = self.combined_data['Daily_Return'].std() * (252 ** 0.5)

        # Calculate Sharpe
        sharpe_ratio = annualized_return / annualized_volatility

        # Calculate Max Drawndpwn
        rolling_max = self.combined_data['Cumulative_Return'].cummax()
        drawdown = self.combined_data['Cumulative_Return'] - rolling_max
        max_drawdown = drawdown.min()
        max_drawdown_date = self.combined_data.loc[drawdown == max_drawdown, 'CLOCK'].values[0]
        max_drawdown_date = pd.to_datetime(max_drawdown_date)

        end_of_drawdown = self.combined_data.loc[drawdown == max_drawdown, 'CLOCK'].values[0]
        end_of_drawdown = pd.to_datetime(end_of_drawdown)
        max_drawdown_recovery_date = self.combined_data.loc[(self.combined_data['Cumulative_Return'] >= rolling_max) & (
                    self.combined_data['CLOCK'] > end_of_drawdown), 'CLOCK'].values
        if len(max_drawdown_recovery_date) > 0:
            max_drawdown_recovery_date = pd.to_datetime(max_drawdown_recovery_date[0])
            max_drawdown_recovery_time = (max_drawdown_recovery_date - max_drawdown_date).days
        else:
            max_drawdown_recovery_time = None

        # calculate calmar
        calmar_ratio = annualized_return / abs(max_drawdown)

        # append as dic
        performance_metrics = {
            'Sharpe Ratio': sharpe_ratio,
            'Calmar Ratio': calmar_ratio,
            'Annualized Return': annualized_return,
            'Annualized Volatility': annualized_volatility,
            'Max Drawdown': max_drawdown,
            'Max Drawdown Date': max_drawdown_date,
            'Max Drawdown Recovery Data': max_drawdown_recovery_time}

        performance_df = pd.DataFrame(performance_metrics, index=[0])
        return performance_df

    # def get_trading_pnl(self):
    #
    #     """
    #     calculate trading pnl
    #     """
    #     pnl_list = []
    #     for i in range(1, len(self.combined_data)):
    #         prev_balance = self.combined_data.iloc[i - 1]['Balance']
    #         current_balance = self.combined_data.iloc[i]['Balance']
    #         inter_pnl = current_balance - prev_balance
    #         pnl_list.append([self.combined_data.iloc[i]['CLOCK'], inter_pnl, current_balance])
    #
    #     pnl_df = pd.DataFrame(pnl_list, columns=['time', 'interPNL', 'balance'])
    #     return pnl_df
    #
    # def plot_results(self):
    #     fig, ax1 = plt.subplots(figsize=(14, 8))
    #     ax2 = ax1.twinx()
    #
    #     # 绘制收盘价图
    #     ax1.plot(self.combined_data['CLOCK'], self.combined_data['CLOSE'], label='Close Price', color='blue')
    #     ax1.set_xlabel('Date')
    #     ax1.set_ylabel('Close Price')
    #     pnl_df = self.get_trading_pnl()
    #     # 绘制 balance 图
    #     ax2.plot(pnl_df['time'], pnl_df['balance'], label='Balance', color='purple', alpha=0.6)
    #     ax2.set_ylabel('Balance')
    #
    #     # 获取买入和卖出信号
    #     buy_1 = self.combined_data[self.combined_data['Trade_1'] > 0]
    #     buy_2 = self.combined_data[self.combined_data['Trade_2'] > 0]
    #     sell_1 = self.combined_data[self.combined_data['Trade_1'] < 0]
    #     sell_2 = self.combined_data[self.combined_data['Trade_2'] < 0]
    #
    #     ylim = ax1.get_ylim()
    #     height = ylim[1] - ylim[0]
    #     # 缩放比例
    #     scale = 0.25 / max(buy_1['Trade_1'].max(), buy_2['Trade_2'].max(), abs(sell_1['Trade_1'].min()),
    #                        abs(sell_2['Trade_2'].min()))
    #
    #     # 绘制买入信号
    #     for _, row in buy_1.iterrows():
    #         ax1.axvline(x=row['CLOCK'], ymin=0.5, ymax=0.5 + (row['Trade_1'] * scale), color='green', alpha=0.5,
    #                     linewidth=2)
    #     for _, row in buy_2.iterrows():
    #         ax1.axvline(x=row['CLOCK'], ymin=0.5, ymax=0.5 + (row['Trade_2'] * scale), color='lightgreen', alpha=0.5,
    #                     linewidth=2)
    #
    #     # 绘制卖出信号
    #     for _, row in sell_1.iterrows():
    #         ax1.axvline(x=row['CLOCK'], ymin=0.5 + (row['Trade_1'] * scale), ymax=0.5, color='red', alpha=0.5,
    #                     linewidth=2)
    #     for _, row in sell_2.iterrows():
    #         ax1.axvline(x=row['CLOCK'], ymin=0.5 + (row['Trade_2'] * scale), ymax=0.5, color='lightcoral', alpha=0.5,
    #                     linewidth=2)
    #
    #     fig.tight_layout()
    #     fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    #     plt.title('Close Price, Balance and Trading Signals')
    #     plt.show()