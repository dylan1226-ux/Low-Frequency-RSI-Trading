import pandas as pd

class RSICalculation:

    @staticmethod
    def calculate_RSI(data, window=14):
        """
        Calculate the RSI indicator based on the formula
        """
        delta = data['CLOSE'].diff(1)
        AU = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        AD = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        RS = AU / AD
        RSI = 100 - (100 / (1 + RS))
        return RSI

    @staticmethod
    def trade_signal_1(data, window=14, n=40):
        """
        Signal 1: Overbought/Oversold Strategy
        """
        data['RSI'] = RSICalculation.calculate_RSI(data, window)
        data['Buy'] = 0
        data['Sell'] = 0
        data['Exit'] = 0

        # Buy signal - when RSI crosses above 30
        buy_signals = (data['RSI'] > 30) & (data['RSI'].shift(1) <= 30)
        data.loc[buy_signals, 'Buy'] = 1

        # Sell signal - when RSI crosses below 70
        sell_signals = (data['RSI'] < 70) & (data['RSI'].shift(1) >= 70)
        data.loc[sell_signals, 'Sell'] = 1

        # Generate exit signals: RSI returns to neutral or after n days
        for i in range(len(data)):
            if data['Buy'].iloc[i] == 1:
                for j in range(1, n + 1):
                    if i + j < len(data):
                        if data['RSI'].iloc[i + j] > 50 or j == n:
                            if i + n < len(data):
                                data.iloc[i + n, data.columns.get_loc('Exit')] = 1
                            break

        return data

    @staticmethod
    def trade_signal_2(data, window=14, n=40, k=5, a=10, threshold=1):
        """
        信号二：Counter-Trend Strategy
        """
        data['RSI'] = RSICalculation.calculate_RSI(data, window)
        data['Buy'] = 0
        data['Sell'] = 0
        data['Exit'] = 0

        # 计算 RSI_t - RSI_{t-k}
        data['RSI_diff'] = data['RSI'] - data['RSI'].shift(k)

        # 买入信号 - 当 RSI_t - RSI_{t-k} < -a
        buy_signals = data['RSI_diff'] < -a
        data.loc[buy_signals, 'Buy'] = 1
        # 卖出信号 - 当 RSI_t - RSI_{t-k} > a
        sell_signals = data['RSI_diff'] > a
        data.loc[sell_signals, 'Sell'] = 1

        # 生成退出信号：动量回归到接近零或 n 天后
        for i in range(len(data)):
            if data['Buy'].iloc[i] == 1:
                for j in range(1, n + 1):
                    if i + j < len(data):
                        if abs(data['RSI_diff'].iloc[i + j]) < threshold or j == n:
                            if i + j < len(data):
                                data.iloc[i + j, data.columns.get_loc('Exit')] = 1
                            break
        return data
