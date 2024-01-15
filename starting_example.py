import tgx
import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser('*** discretizing time steps from datasets ***')
    parser.add_argument('-d', '--data', type=str, help='Dataset name', default='tgbl-wiki')
    parser.add_argument('-t', '--time', type=str, help='time granularity', default='daily')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args, sys.argv 

args, _ = get_args()


#! load the datasets from tgb or builtin
# dataset = tgx.builtin.uci()

data_name = args.data #"tgbl-coin" #"tgbl-review" #"tgbl-wiki"
dataset = tgx.tgb_data(data_name)



ctdg = tgx.Graph(dataset)
# ctdg.save2csv("ctdg") #! save the graph to csv files

time_scale = args.time #"minutely"  #"monthly" #"weekly" #"daily"  #"hourly" 
dtdg = ctdg.discretize(time_scale=time_scale)
print ("discretize to ", time_scale)

