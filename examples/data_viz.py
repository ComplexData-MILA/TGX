import tgx
from tgx.utils.plotting_utils import plot_for_snapshots

"""
master example to show all visualization in tgx
"""

#* load built in datasets
dataset = tgx.builtin.uci() #built in datasets 

#* load the tgb datasets
# data_name = "tgbl-wiki" #"tgbl-review" 
# dataset = tgx.tgb_data(data_name) #tgb datasets


ctdg = tgx.Graph(dataset)
time_scale = "weekly" #"daily"
dtdg = ctdg.discretize(time_scale=time_scale)[0]


#! plotting the statistics, works
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



#! compute statistics
test_ratio = 0.15
tgx.get_reoccurrence(ctdg, test_ratio=test_ratio)
tgx.get_surprise(ctdg, test_ratio=test_ratio)
tgx.get_avg_node_activity(dtdg)
tgx.get_novelty(dtdg)


# Number of Connected Components
tgx.connected_components_per_ts(dtdg, network_name=dataset.name, plot_path = plot_path)

# Size of Largest Connected Component
component_sizes = tgx.size_connected_components(dtdg)
largest_component_sizes = [max(inner_list) if inner_list else 0 for inner_list in component_sizes]
filename = f"{dataset.name}_largest_connected_component_size"
plot_for_snapshots(largest_component_sizes, filename, "Size of Largest Connected Component", plot_path = plot_path)

# Average Node Engagement
engagements = tgx.get_avg_node_engagement(dtdg)
filename = f"{dataset.name}_average_node_engagement"
plot_for_snapshots(engagements, filename, "Average Engagement", plot_path = plot_path)

# Degree Density
tgx.degree_density(dtdg, k=3, network_name=dataset.name, plot_path = plot_path)
