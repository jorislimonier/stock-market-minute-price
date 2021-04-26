# Stock market per minute

This Jupyter Notebook computes the price of a company at each minute of the day for each of the last 14 days (10 working days + 2 weekends where the stock market is closed).
This allows to compare volatility and per-minute evolution to deduce general trends. In particular, applications in day-trading can be found.
One can easily use a for-loop to iter over companies and make comparisons.

## API key

To run this script, you need to input your Alpha Vantage API key at the place marked in the code. Your API key can be found [here](https://www.alphavantage.co/support/#api-key)