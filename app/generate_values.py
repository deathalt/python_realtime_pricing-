from random import random
from threading import Thread, Lock
import time

from settings import TICKER_COUNT

mutex = Lock()

Ticker_type = list[dict[str, list[int]]]


def create_items_list() -> list[str]:
    tickers_list = []
    for x in range(TICKER_COUNT):
        tickers_list.append("item_{0:0=2d}".format(x))
    return tickers_list


def init_ticker_data(tickers_list: list[str]) -> Ticker_type:
    ticker_data: Ticker_type = []
    for ticker in tickers_list:
        ticker_data.append({ticker: [0]})
    return ticker_data


def generate_movement() -> int:
    movement = -1 if random() < 0.5 else 1
    return movement


def increment_ticker_data(
    ticker_data: Ticker_type, tickers_list: list[str]
) -> Ticker_type:
    for ticker in tickers_list:
        index = tickers_list.index(ticker)
        ticker_data[index][ticker].append(
            ticker_data[index][ticker][-1] + generate_movement()
        )
    return ticker_data


def append_price(ticker_data: Ticker_type, tickers_list: list[str]) -> None:
    while True:
        with mutex:
            increment_ticker_data(ticker_data=ticker_data, tickers_list=tickers_list)
        time.sleep(1)


def run_generator():
    tickers_list = create_items_list()
    ticker_data = init_ticker_data(tickers_list=tickers_list)
    thread = Thread(target=append_price, args=(ticker_data, tickers_list))
    thread.daemon = True
    thread.start()
    return ticker_data
