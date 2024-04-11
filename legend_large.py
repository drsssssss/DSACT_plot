import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the colors and labels for the requested algorithms
#colors_requested = ['#E41A1C','#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628']
colors_requested = ['#E41A1C', '#377EB8','#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628',]
#labels_requested = ['DSAC-T', 'DSAC-v1', 'SAC', 'TD3', 'DDPG', 'TRPO', 'PPO']
labels_requested = ['M-DSAC', 'DSAC', 'SAC', 'TD3', 'DDPG', 'TRPO', 'PPO']

# Create a figure with the requested figsize
fig = plt.figure(figsize=(8/3, 2))   #7,1
#fig = plt.figure(figsize=(9.5, 0.5))   #1,7


# Create a list of patches to add to the legend
patches_requested = [mpatches.Patch(color=color, label=label) for color, label in zip(colors_requested, labels_requested)]

# Create the legend without a frame
legend = plt.legend(loc="center left" ,ncol=1,handles=patches_requested, frameon=False)  #DSACT
#legend = plt.legend(loc="center" ,ncol=7,handles=patches_requested, frameon=False)  #DSACT

# Tight layout to minimize whitespace
plt.tight_layout()

# Remove axes for clarity
plt.gca().set_axis_off()

# Show the plot
#plt.show()
plt.savefig('algs_legend_mdsac.pdf', dpi=600, bbox_inches='tight')