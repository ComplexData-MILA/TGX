import datetime
import pandas as pd


def create_ts_list(start, end, metric=None, interval=None):
    if metric == "Unix" or metric == "unix" or metric == "UNIX":
        start = datetime.datetime.fromtimestamp(start).date()
        end = datetime.datetime.fromtimestamp(end).date()
        if interval == 'daily':
            date_list = pd.date_range(start = start, end = end, freq="D") 
        elif interval == "month":
            date_list = pd.date_range(start = start, end = end, freq="M")
        elif interval == "year":
            date_list = pd.date_range(start = start, end = end, freq="Y") 
        timelist = []
        for dates in date_list:
            timelist.append(dates.strftime("%Y/%m/%d"))
    else:
        timelist = list(range(start, end, interval))
    # print(timelist)
    return timelist

    

    

if __name__ == "__main__":
    create_ts_list(86400, 86400*365, "unix", "month")
    create_ts_list(2015, 2022, interval=2)