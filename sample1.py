from yahoo_finance_api2 import share as yapi2
import datetime as dt
from datetime import date,timedelta
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import talib as ta
import pandas_datareader.data as pdr

def get_stock_data(code):
    df = pdr.DataReader("{}.JP".format(code), "stooq").sort_index()
    return df

print("Running sample1.py")

# 株価の取得
code = "9432"
name = "日本電信電話"
df = get_stock_data(code)

df.index = pd.to_datetime(df.index).strftime('%m-%d-%Y')

close = df['Close']
ma5, ma25 = ta.SMA(close, timeperiod=5), ta.SMA(close, timeperiod=25)
df['ma5'], df['ma25'] = ma5, ma25

layout = {
    "title"  : { "text": "{} {}".format(code, name), "x":0.5 }, 
    "xaxis" : { "title": "日付", "rangeslider": { "visible": False },  "type" : "category" },
    "yaxis" : { "title": "価格（円）", "side": "left", "tickformat": "," },
    "plot_bgcolor":"light blue"
}

data =  [
    # ローソク足
    go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], increasing_line_color="red", decreasing_line_color="gray"),
    # 5日移動平均線
    go.Scatter(x=df.index, y=df["ma5"], name="MA5", line={ "color": "royalblue", "width": 1.2 } ),
    # 25日移動平均線
    go.Scatter(x=df.index, y=df["ma25"], name="MA25", line={ "color": "lightseagreen", "width": 1.2 } )
]

# チャート表示
fig = go.Figure(layout = go.Layout(layout), data = data)
fig.show()