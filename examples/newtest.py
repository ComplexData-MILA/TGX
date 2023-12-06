import tgx
import tgx.utils.newstat as newstat
from tgx.utils.plotting_utils import plot_for_snapshots


plot_path = "/home/mila/e/elahe.kooshafar/projects/TGX_results"

dataset = tgx.builtin.uci()
G = tgx.Graph(dataset)
new_G = G.discretize(time_scale="weekly")

# Number of Connected Components
newstat.connected_components_per_ts(new_G, network_name=dataset.name, plot_path = plot_path)

# Size of Largest Connected Component
component_sizes = newstat.size_connected_components(new_G)
largest_component_sizes = [max(inner_list) if inner_list else 0 for inner_list in component_sizes]
filename = f"{dataset.name}_largest_connected_component_size"
plot_for_snapshots(largest_component_sizes, filename, "Size of Largest Connected Component", plot_path = plot_path)

# Average Node Engagement
engagements = newstat.get_avg_node_engagement(new_G)
filename = f"{dataset.name}_average_node_engagement"
plot_for_snapshots(engagements, filename, "Average Engagement", plot_path = plot_path)

# Degree Density
newstat.degree_density(new_G, k=3, network_name=dataset.name, plot_path = plot_path)