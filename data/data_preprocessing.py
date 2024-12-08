import pandas as pd

# please prepare your own data
def load_and_preprocess(file_path, symbol_filter):
    df = pd.read_csv(file_path)
    df = df[['trade_date', 'code', 'close']]
    df.rename(columns={'trade_date': "CLOCK", 'code': "SYMBOL", 'close': "CLOSE"}, inplace=True)
    df = df[df['SYMBOL'] == symbol_filter]
    df['CLOSE'] = df['CLOSE'].astype('float64')
    return df