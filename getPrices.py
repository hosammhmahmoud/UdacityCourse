import requests
import pandas as pd
from tqdm import tqdm
import os


# GET CRYPTO DATA FROM TOP 20 ASSETS BY MARKET CAPITALIZATION

api_key = os.getenv("CCCDATA_API_KEY")


def get_asset_ohlcv(asset, toSymbol, freq, limit, api_key, exchange="CCCAGG"):
    """
    Function that gets an asset prices and volumes from an exchange

    Parameters
    ----------
    asset str: the asset you want price and volume to
    toSymbol str: the toSymbol you want the price and volumes in i.e. 'USD'
    frq str: frequency of data - choose between minute, hour or day
    limit: number of data points - max 2000
    exchange: exchange you want to retrive the data from - default CCCAGG

    Returns
    -------
    df Dataframe: OHLCV Data


    """
    url = (
        f"https://min-api.cryptocompare.com/data/v2/histo{freq}?"
        f"fsym={asset}&tsym={toSymbol}&limit={limit}&e={exchange}&"
        f"tryConversion=true&api_key={api_key}"
    )
    data = requests.get(url).json()
    df = pd.DataFrame(data["Data"]["Data"])
    df.time = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    df.rename(columns={"volumeto": "volume"}, inplace=True)
    df.volume = df.volume / 1000  # divide by 1000 to alighn with zipline requirments
    return df[["open", "high", "low", "close", "volume"]]


# DOWNLOAD FILES IN MY BUNDLE DIRECTORY

save_path = "/Users/hosammahmoud/Documents/zipline/my_bundle/"

tickers = [
    "BTC",
    "ETH",
    "LTC",
    "MATIC",
    "BNB",
    "ADA",
    "DOT",
    "XRP",
    "DOGE",
    "ETC",
    "SOL",
    "TRX",
    "SHIB",
    "BCH",
    "LINK",
    "XLM",
    "AVAX",
    "ATOM",
    "XMR",
    "UNI",
]

for ticker in tqdm(tickers):
    try:
        df = get_asset_ohlcv(ticker, "USDT", "day", 2000, api_key, exchange="Binance")
        df.to_csv(save_path + f"{ticker}.csv")
    except:
        print("error with", ticker)
