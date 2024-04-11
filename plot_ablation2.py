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
plt_conf.legend_ncol = 2

plt_conf.smooth_alpha = 0.2

sns.set_style("darkgrid")

def process_data(data_df: pd.DataFrame, plt_conf):
    # moving exponential average smoothing and downsample note that the data should be sorted by algorithm, env, run_id and the step should be in order
    print('scale and smooth data!')

    data_df["step"] = data_df["step"] / 1e6
    # replace 'algorithm' with 'Algorithm'
    data_df = data_df.rename(columns={'algorithm':'Algorithm'})

    # smooth
    data_df["value"] = data_df.groupby(["Algorithm", "env", "run_id","Reward scale"])["value"].transform(
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
    filename = 'ablation_study_2',
):
    data = json.load(open(data_file, "r"))
    data_df = pd.DataFrame(data)
    plot_data = process_data(data_df, plt_conf)

    fig, ax = plt.subplots(figsize=plt_conf.fig_size, dpi=plt_conf.dpi, tight_layout=True, )
    # plot the data note do not plot the border of the shadow 
    sns.lineplot(
        x="step",
        y="value",
        hue="Reward scale",
        data=plot_data,
        style="Algorithm",
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
        legend_handles, labels = ax.get_legend_handles_labels()
        empty_patch = plt.plot([], [], marker="none", linestyle="none")[0]
        legend_handles = [empty_patch,empty_patch,legend_handles[5],legend_handles[6],legend_handles[7],legend_handles[0],legend_handles[1],legend_handles[2],legend_handles[3],legend_handles[4]]
        for idx, label in enumerate(labels[1:5]):
            labels[idx+1] = 'Scale = '+label+'x'

        labels = ['','',labels[5],labels[6],labels[7],labels[0],labels[1],labels[2],labels[3],labels[4]]

        legend = ax.legend(legend_handles,labels,loc=plt_conf.legend_loc,ncol=plt_conf.legend_ncol,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False, 
        handlelength=1.5,handletextpad=0.5,columnspacing=0.5)
        for line in legend.get_lines():
            line.set_linewidth(plt_conf.line_width)


        
        # lagend_handles2 = [legend_handles[5],legend_handles[6],legend_handles[7]]
        # labels2 = [labels[5],labels[6],labels[7]]
        
        # legend1= ax.legend(lagend_handles1,labels1,loc=(0.42,0.0),ncol=2,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
        # ax.add_artist(legend1)
      

        # legend2= ax.legend(lagend_handles2,labels2,loc=(0.42,0.25),ncol=1,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
        # ax.add_artist(legend2)



        # # legend =ax.legend(legend_handles,labels,loc=plt_conf.legend_loc,ncol=plt_conf.legend_ncol,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
        # # legend = ax.legend(loc=plt_conf.legend_loc,ncol=plt_conf.legend_ncol,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
        # for line in legend1.get_lines():
        #     line.set_linewidth(plt_conf.line_width)
        # for line in legend2.get_lines():
        #     line.set_linewidth(plt_conf.line_width)
    else:
        ax.get_legend().remove()
        

    fig.savefig(os.path.join(save_path,filename+'.'+plt_conf.save_format), bbox_inches="tight", pad_inches=plt_conf.pad)

    return


if __name__ == "__main__":
    data_file = "./data/ablation2_new/run_data.json"
    save_path = "./figures/candidate2"
    filename = 'ablation_study_2'

    plot_performance(data_file, plt_conf, save_path, filename= filename,label_on = True)


