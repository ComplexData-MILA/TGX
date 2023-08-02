# Load the data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler


sns.set_style('darkgrid', {
    'font.size': 60,
    'font.family': 'serif',
    'dpi': 300,
})
df = pd.read_csv('data/ml_enron.csv', index_col=0)
# preprocessings
df.columns = ['src', 'dst', 't', 'label', 'idx']

# Scale all the times such that they are between 0 and 1
# The original times can be recovered using lambda t : t * (max_time - min_time) + min_time
scaler = MinMaxScaler()

df['t'] = scaler.fit_transform(df['t'].values.reshape(-1, 1))

# Calculate TEA plot
src = df['src'].values
dst = df['dst'].values
t = df['t'].values
edge_events = np.stack([src, dst])
# We start by calculating a unique id for each appearing edge in the network
edge_index, edge_hash, edge_count = np.unique(
    edge_events,
    return_inverse=True,
    return_counts=True,
    axis=1,
)
# The edge indices (src,dst) can be retrieved by indexing into the edge_index matrix
assert np.all(edge_index[:, edge_hash] == edge_events)

# Train test split
t_split = 0.8
df.loc[df['t'] < t_split, 'split'] = 'train'
df.loc[df['t'] >= t_split, 'split'] = 'test'

# Bin the time stamps into small intervals
# This can be used to reduce the number of points to plot
class BinTime(object):

    def __init__(self, n_intervals):
        self.n_intervals = n_intervals

    def __call__(self, t):
        step_size = 1 / self.n_intervals
        time_norm = (t - min(t)) / (max(t) - min(t))
        time_index = time_norm // step_size
        return time_index


n_bins = 50
bin_time = BinTime(n_bins)
time_index = bin_time(t)


past_edge_hash = set()
edge_counts = []
new_edge_counts = []

for i in tqdm(np.unique(time_index)):
    mask = time_index == i
    ei = edge_hash[mask]
    ei_unique = np.unique(ei)
    edge_counts.append(len(ei_unique))
    n_old = len(past_edge_hash)
    past_edge_hash.update(set(ei_unique))
    new_edge_counts.append(len(past_edge_hash) - n_old)


bar_plot = pd.DataFrame(
    {
        'Repeated Edges': np.array(edge_counts) - np.array(new_edge_counts),
        'New edges': new_edge_counts,
        'Time Interval': np.unique(time_index)
    },)


fig, ax = plt.subplots(figsize=(20, 10))
bar_plot.plot(kind='bar', stacked=True, x='Time Interval', ax=ax)
ticks = np.arange(0, len(np.unique(time_index)), 10)
plt.xticks(ticks=ticks, labels=ticks)
plt.ylabel('Number of edges')
plt.title('Tea Plot of the ENRON dataset')
plt.savefig("./plots/enron")