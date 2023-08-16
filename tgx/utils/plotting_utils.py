import datetime
import pandas as pd


def create_ts_list(start, end, metric, interval=None):
    if metric == "Unix" or metric == "unix" or metric == "UNIX":
        start = datetime.datetime.fromtimestamp(start).date()
        end = datetime.datetime.fromtimestamp(end).date()
    print(start, end)
    if interval == "month":
        # start = start.strftime('%Y/%m')
        # end = end.strftime('%Y/%m')
        date_list = pd.date_range(start = start, end = end, freq="Y") 
    elif interval == "year":
        start = start.strftime('%Y')
        end = end.strftime('%Y')
        date_list = pd.date_range(start = start, end = end, freq="Y") 
    print(date_list)
    print(start)
    

if __name__ == "__main__":
    create_ts_list(86400, 86400*365, "unix", "month")