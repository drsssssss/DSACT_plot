import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy
from misc import cfg, cm2inch

plt_conf = deepcopy(cfg)
plt_conf.fig_size = cm2inch((8, 5.5))
plt_conf.legend_loc = "lower right"
plt_conf.legend_ncol = 1
plt_conf.smooth_alpha = 0.9

sns.set_style("darkgrid")

def process_data(data_df: pd.DataFrame, plt_conf):
    # moving exponential average smoothing and downsample note that the data should be sorted by algorithm, env, run_id and the step should be in order
    print('scale and smooth data!')

    data_df["step"] = data_df["step"] / 1e6

    # smooth
    data_df["value"] = data_df.groupby(["algorithm", "env", "run_id"])["value"].transform(
        lambda x: x.ewm(alpha=plt_conf.smooth_alpha).mean()
    )
    # downsample
    data_df = data_df.iloc[::plt_conf.downsample, :]
    
    return data_df


def plot_performance(
    data_file,
    plt_conf,
    save_path,
    label_on = True,
):
    data = json.load(open(data_file, "r"))
    data_df = pd.DataFrame(data)
    plot_data = process_data(data_df, plt_conf)

    fig, ax = plt.subplots(figsize=plt_conf.fig_size, dpi=plt_conf.dpi, tight_layout=True, )
    # plot the data note do not plot the border of the shadow 
    sns.lineplot(
        x="step",
        y="value",
        hue="algorithm",
        data=plot_data,
        ax=ax,
        errorbar= ('ci', 95),
        err_kws= {'alpha':0.3,'edgecolor':'none'},
        palette=plt_conf.color,
        linewidth=plt_conf.line_width,
    )
    ax.set_xlabel("Million iterations", fontdict=plt_conf.label_font)
    ax.set_ylabel("Average return", fontdict=plt_conf.label_font)
    ax.set_xlim(0, 1.5)
    ax.set_xticks([0, 0.3, 0.6, 0.9, 1.2, 1.5])
    ax.tick_params(labelsize=plt_conf.tick_size)

    if label_on:
        legend = ax.legend(loc=plt_conf.legend_loc,ncol=plt_conf.legend_ncol,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
        for line in legend.get_lines():
            line.set_linewidth(plt_conf.line_width)
    else:
        ax.get_legend().remove()
        

    fig.savefig(os.path.join(save_path,'ablation_study_1''.'+plt_conf.save_format), bbox_inches="tight", pad_inches=plt_conf.pad)

    return


if __name__ == "__main__":
    data_file = "./data/ablation1_new/run_data.json"
    save_path = "./figures/candidate2"
    plot_performance(data_file, plt_conf, save_path, label_on = True)


