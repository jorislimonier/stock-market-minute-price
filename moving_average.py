# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import datetime
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['figure.figsize'] = (16,8)


# %%
# Using Alpha Vantage to get data
ALPHAVANTAGE_API_KEY = "Y7V3FYWRASU4O4U7"

start = datetime.datetime(2014, 1, 1)
df = pdr.DataReader("TSLA", "av-daily-adjusted", api_key=ALPHAVANTAGE_API_KEY)


# %%
adj_close = df[["adjusted close"]]

mavg30 = adj_close.rolling(window=30).mean()
mavg100 = adj_close.rolling(window=100).mean()

mavg30.columns = ["mavg30"]
mavg100.columns = ["mavg100"]

mavg = adj_close.copy()
mavg = mavg.merge(mavg30, left_index=True, right_index=True)
mavg = mavg.merge(mavg100, left_index=True, right_index=True)

col = list(mavg.columns)
alphas = [0.1, 1, 1]


for i in range(3):
    c = col[i]
    a = alphas[i]
    mavg[c].plot(alpha=a)
plt.legend()


# %%
days = list(mavg.index)
mavg["action"] = np.nan
thresh = 1.05
position = "sell"
for i in range(len(days)):
    d0 = days[i]
#     d1 = days[i+1]
    
    d = d0
    short_term_value = mavg.loc[d]["mavg30"]
    long_term_value = mavg.loc[d]["mavg100"]
    
    if short_term_value > long_term_value * thresh:
        if position == "buy":
            continue
        else:
#             print(d, short_term_value, long_term_value)
            mavg.loc[[d], ["action"]] = "buy"
#             print(mavg.loc[d]["action"])
            position = "buy"

    if short_term_value <= long_term_value / thresh:
        if position == "sell":
            continue
        else:
#             print(d, short_term_value, long_term_value)
            mavg.loc[[d], ["action"]] = "sell"
#             print(mavg.loc[d]["action"])
            position = "sell"
    
            
mavg["buy_signal_price"] = np.nan
mavg["sell_signal_price"] = np.nan

mavg.loc[mavg["action"] == "buy", "buy_signal_price"] = mavg[mavg["action"] == "buy"].loc[:, "adjusted close"]
mavg.loc[mavg["action"] == "sell", "sell_signal_price"] = mavg[mavg["action"] == "sell"].loc[:, "adjusted close"]
    
# mavg.loc["2015-01-09"]["action"] = 42
mavg[mavg["action"].notna()]


# %%
col = list(mavg.columns)
alphas = [0.2, 0.4, 0.4]

for i in range(3):
    c = col[i]
    a = alphas[i]
    mavg[c].plot(alpha=a)

plt.scatter(mavg.index, mavg["buy_signal_price"], label="Buy", marker="^", color="green")
plt.scatter(mavg.index, mavg["sell_signal_price"], label="Sell", marker="v", color="red")

plt.legend()


# %%



