#!/usr/bin/env python

import mcap_token
import argparse
import datetime
import functools
import sys
import quandl
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description='Compute the capitalization for content delivery stakeholders')
parser.add_argument("--start_year",
                    help="Year to start the serie", default="2013",
                    type=str)
parser.add_argument("--stdout",
                    help="output png to stdout", action="store_true",
                    )

args = parser.parse_args()

matplotlib.legend.numpoints = 2
matplotlib.style.use('ggplot')


def normalize_and_fix_name(dataframe):
    return pd.DataFrame(dataframe[1]["Open"].values / dataframe[1]["Open"][0] * 100, index=dataframe[1]["Open"].index,
                        columns=[dataframe[0]])


# data = Quandl.get("SF1/SFLX", authtoken="LMzEf9c9zyb_s9x47otT")
# data.head()

# Quandl.get('SF1/NWSA_MARKETCAP', authtoken='LMzEf9c9zyb_s9x47otT')
# sd_BgWPXJLPWxL-Cr35M

# definition of the market values for some stocks
input = {
    "Content Owners": {"Disney": "GOOG/NYSE_DIS", "News": "GOOG/NASDAQ_NWS",
                       "Time Warner": "GOOG/NYSE_TWX", "Electronic Arts": "GOOG/NASDAQ_EA"},
    "Content Providers": {"Amazon": "GOOG/NASDAQ_AMZN", "Google": "GOOG/NASDAQ_GOOG", "Netflix": "GOOG/NASDAQ_NFLX",
                          # "Facebook": "GOOG/NASDAQ_FB ",
                          "Twitter": "GOOG/NYSE_TWTR"},
    "Technical Enablers": {"Akamai": "GOOG/NASDAQ_AKAM", "LimeLight": "GOOG/NASDAQ_LLNW",
                           "Verisign": "GOOG/NASDAQ_VRSN"},
    "Connectivity Providers": {"Verizon": "GOOG/NYSE_VZ", "Level 3": "GOOG/NYSE_LVLT", "AT&T": "GOOG/NYSE_T",
                               "Sprint": "GOOG/NYSE_S"},
    # "Devices Producers MSFT, AAPL,Dell": {"Microsoft": "SF1/MSFT_MARKETCAP", "Apple": "SF1/AAPL_MARKETCAP",                          "Dell": "SF1/DELL_MARKETCAP"}
}

# get market data


input_data = {category[0]: {label: quandl.get(code, authtoken=mcap_token.auth_token, trim_start='%s-01-01'%args.start_year,
                                              trim_end=datetime.datetime.now().strftime("%Y-%m-%d")).resample("BQ") for
                            (label, code) in
                            category[1].items()} for category in input.items()}

# group them by category
input_data_agg = {
cat: functools.reduce(lambda x, y: x.add(y.reindex(x.index, method="bfill"), fill_value=0), ts.values()) for (cat, ts)
in input_data.items()}

# fix the sereies name, normalize and concat for plotting
data = pd.concat(map(normalize_and_fix_name, input_data_agg.items()), axis=1)

plt.clf()
plt.grid = True
p = data[input.keys()[0]].plot(marker="o", color='blue', legend=True)
p = data[input.keys()[1]].plot(marker=".", legend=True)
p = data[input.keys()[2]].plot(marker=",", color='green', legend=True)
p = data[input.keys()[3]].plot(marker="o", color='black', legend=True)
# p=data[input.keys()[4]].plot(marker="^",color='yellow',legend=True)
p.get_figure().savefig("output.png", format="png")
# p=data[input.keys()[4]].plot(marker="^",legend=True).get_figure().savefig("output.png")

if args.stdout:
    with open("output.png") as f:
        
        sys.stdout.write(f.read())
        sys.stdout.flush()

