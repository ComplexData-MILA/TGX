import tgx
from tgx.utils.plotting_utils import plot_for_snapshots
import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser('*** discretizing time steps of a TG dataset ***')
    parser.add_argument('-d', '--data', type=str, help='dataset name', default='tgbl-wiki')
    parser.add_argument('-t', '--time', type=str, help='time granularity', default='daily')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args, sys.argv 

args, _ = get_args()


# === load the datasets from tgb or built-in ===

# load a built-in dataset
# dataset = tgx.builtin.uci()

# load a TGB dataset
data_name = args.data  # args.name can be supported TGB datasets, such as: "tgbl-coin", "tgbl-review", "tgbl-wiki"
dataset = tgx.tgb_data(data_name)

# make a Graph object from loaded dataset
ctdg = tgx.Graph(dataset)
# ctdg.save2csv("ctdg") #! save the graph to csv files

time_scale = args.time  #choices are: "minutely", "monthly", "weekly", "daily", "hourly" 
dtdg = ctdg.discretize(time_scale=time_scale)[0]
print(f"INFO: Discretize {data_name} to `{time_scale}`")



# === plotting the statistics ===
tgx.degree_over_time(dtdg, network_name=dataset.name)
tgx.nodes_over_time(dtdg, network_name=dataset.name)
tgx.edges_over_time(dtdg, network_name=dataset.name)
tgx.nodes_and_edges_over_time(dtdg, network_name=dataset.name)

tgx.TET(dtdg, 
        network_name=dataset.name, 
        figsize = (9, 5),
        axis_title_font_size = 24,
        ticks_font_size = 24)


tgx.TEA(dtdg, 
        network_name=dataset.name)



# === compute statistics ===
test_ratio = 0.15
tgx.get_reoccurrence(ctdg, test_ratio=test_ratio)
tgx.get_surprise(ctdg, test_ratio=test_ratio)
tgx.get_novelty(dtdg)


# Number of Connected Components
tgx.connected_components_per_ts(dtdg, network_name=dataset.name)

# Degree Density
tgx.degree_density(dtdg, k=3, network_name=dataset.name)

# Size of Largest Connected Component
component_sizes = tgx.size_connected_components(dtdg)
largest_component_sizes = [max(inner_list) if inner_list else 0 for inner_list in component_sizes]
filename = f"{dataset.name}_largest_connected_component_size"
plot_for_snapshots(largest_component_sizes, y_title="Size of Largest Connected Component", filename="./"+filename)

# Average Node Engagement
engagements = tgx.get_avg_node_engagement(dtdg)
filename = f"{dataset.name}_average_node_engagement"
plot_for_snapshots(engagements, y_title="Average Engagement", filename="./"+filename)

