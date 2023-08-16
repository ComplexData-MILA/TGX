
def edgelist_discritizer(edgelist, 
                          unique_ts,
                          time_interval = None,
                          max_intervals = 200):
    print("intervals:", time_interval)
    print(unique_ts[0], unique_ts[-1])
    total_time = unique_ts[-1] - unique_ts[0]
    if time_interval is not None:
        if isinstance(time_interval, str):
            if time_interval == "daily":
                interval_size = 86400
            elif time_interval == "weekly":
                interval_size = 86400 * 7
            elif time_interval == "monthly":
                interval_size = 86400 * 30
            elif time_interval == "yearly":
                interval_size = 86400* 365
            if int(total_time / interval_size) > max_intervals:
                user_input = input("Too many timestamps, discretizing data to 200 timestamps, do you want to proceed?(y/n): ")
                if user_input.lower() == 'n':
                    print('Cannot proceed to TEA and TET plot')
                    exit()
                else:
                    interval_size = max_intervals
        elif isinstance(time_interval, int):
            if time_interval > max_intervals:
                raise ValueError(f"The maximum number of time intervals is {max_intervals}.")
            else:
                interval_size = int(total_time / (time_interval-1))
                print(total_time, interval_size)
                
        else:
            raise TypeError("Invalid time interval")
    else:
        user_input = input(f"discretizing data to {max_intervals} timestamps, do you want to proceed?(y/n): ")
        if user_input.lower() == 'n':
            print('Cannot proceed to TEA and TET plot')
            exit()
        else:
            interval_size = int(total_time / 100)
    print(interval_size)
    print(f'Discretizing data to {int(total_time/interval_size)} timestamps...')
    if int(total_time/interval_size) == 0:
        print("Warning! Only one timestamp exist in the data.")
    updated_edgelist = {}
    timestamps = {unique_ts[0] : 0}
    new_t = 0
    for ts, edge_data in edgelist.items():
        bin_ts = int(ts / interval_size)
        
        if bin_ts not in timestamps:
            timestamps[bin_ts] = new_t
            new_t += 1

        curr_t = timestamps[bin_ts]
        if curr_t not in updated_edgelist:
            updated_edgelist[curr_t] = {}

        for (u,v), n in edge_data.items():
            if (u, v) not in updated_edgelist[curr_t]:
                updated_edgelist[curr_t][(u, v)] = n
            else:
                updated_edgelist[curr_t][(u, v)] += n
    return updated_edgelist