import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

from dataclasses import dataclass
from datetime import timedelta
from functools import reduce
from scipy.stats import norm


@dataclass
class ReturnTicket:
    mean: float
    std: float
    weeks: str

    def __str__(self) -> str:
        return f"{self.mean:.2%} pm {self.std:.2%}"


def get_ticker_return(ticker_name: str = "^GSPC", weeks=10):
    WEEKS_IN_A_YEAR = 52
    TICKER = yf.Ticker(ticker_name)
    HIST = TICKER.history(period="max", interval="1wk")

    start_date = HIST["Close"].index[0].date() + timedelta(weeks=1)

    hist_pct_change = []
    while True:
        next_date = start_date + timedelta(weeks=weeks)
        date_values = HIST["Close"].pct_change().loc[start_date:start_date +
                                                     timedelta(
                                                         weeks=weeks)].values

        try:
            pct_change = reduce(lambda x, y: (x) * (1 + y), date_values[1:],
                                1 + date_values[0])

        except:
            break

        hist_pct_change.append(pct_change - 1)
        start_date = next_date

    return ReturnTicket(mean=np.mean(hist_pct_change) * WEEKS_IN_A_YEAR /
                        weeks,
                        std=np.std(hist_pct_change) * WEEKS_IN_A_YEAR / weeks,
                        weeks=weeks)


def get_success_probability(return_ticket: ReturnTicket, threshold=0):
    normal_aprox = norm(loc=return_ticket.mean, scale=return_ticket.std)

    return 1 - normal_aprox.cdf(threshold)


def plot_returns(tickers):
    returns = [100*ticker.mean for ticker in tickers]
    std = [100*ticker.std for ticker in tickers]
    weeks = [ticker.weeks for ticker in tickers]
    
    plt.errorbar(weeks, returns, yerr=std, fmt=".r")

    plt.title("Returns for the SP500 over different time periods")
    plt.xlabel("Investment time (in weeks)")
    plt.ylabel("Yearly return (%)")

    plt.savefig("test.png")


def plot_probability(tickers):
    weeks = [ticker.weeks for ticker in tickers]
    prob1 = [100*get_success_probability(ticker) for ticker in tickers]
    prob2 = [100*get_success_probability(ticker, threshold=0.028) for ticker in tickers]
    
    plt.plot(weeks, prob1, ".b")
    plt.plot(weeks, prob2, ".r")

    plt.xlabel("Investment time (in weeks)")
    plt.ylabel("Probability (%)")

    plt.legend(["Probability of obtaining net profit", "Probability of beating inflation"])

    plt.savefig("probability.png")

def main():
    with open("returns.txt", "w") as f:
        tickers = []
        for i in range(10, 101, 5):
            ticker_return = get_ticker_return(weeks=i)
            tickers.append(ticker_return)
            f.write(f"Interval {i} weeks\n\n")
            f.write(f"{ticker_return}\n")
            f.write(f"{get_success_probability(ticker_return):.2%}\n")
            f.write(f"---------------------------------------\n")
        
        plot_probability(tickers)


if __name__ == "__main__":
    main()
