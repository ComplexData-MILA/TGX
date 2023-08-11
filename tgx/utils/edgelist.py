

def edgelist_discritizer(edgelist, 
                          unique_ts,
                          time_interval = None):
    
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
        elif isinstance(time_interval, int):
            if time_interval > 100:
                raise ValueError("The maximum number of time intervals can be set to 100.")
            else:
                total_time = len(edgelist.keys())
                interval_size = int(total_time / time_interval)
                if interval_size == 0:
                    print("Warning: only one timestamp in the plot.")
        else:
            raise TypeError("Invalid time interval")
    else:
        user_input = input("discretizing data to 100 timestamps, do you want to proceed?(y/n): ")
        if user_input.lower() == 'no':
            print('Cannot proceed to TEA and TET plot')
            exit()
        else:
            interval_size = 100

    print(f'Discretizing data to {interval_size} timestamps...')
