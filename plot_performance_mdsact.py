import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy
from misc import cfg, cm2inch

plt_conf = deepcopy(cfg)
plt_conf.fig_size = cm2inch((8, 6))
plt_conf.legend_loc = "lower right"
plt_conf.legend_ncol = 2
plt_conf.smooth_alpha = 0.9
plt_conf.downsample = 1
plt_conf.tick_size = 6
plt_conf.line_width = 1
plt_conf.legend_font['size'] = 6
plt_conf.label_font['size'] = 6

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
    env_list,
    label_on = True,
):
    data = json.load(open(data_file, "r"))
    data_df = pd.DataFrame(data)
    data_df = process_data(data_df, plt_conf)

    for idx,env in enumerate(env_list):
        plot_data = data_df[data_df["env"] == env]
        fig, ax = plt.subplots(figsize=plt_conf.fig_size, dpi=plt_conf.dpi, tight_layout=True, )
        colors = ['#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628','#E41A1C']
        # plot the data note do not plot the border of the shadow 
        sns.lineplot(
            x="step",
            y="value",
            hue="algorithm",
            data=plot_data,
            ax=ax,
            errorbar= ('ci', 95),
            err_kws= {'alpha':0.3,'edgecolor':'none'},
            #palette=plt_conf.color,
            palette=colors,
            linewidth=plt_conf.line_width,
        )
        handles, labels = ax.get_legend_handles_labels()
        # 定义你想要的顺序
        #desired_order = ['DSAC-T', 'DSAC-v1', 'SAC', 'TD3', 'DDPG', 'TRPO', 'PPO']
        desired_order = ['M-DSAC', 'DSAC', 'SAC', 'TD3', 'DDPG', 'TRPO', 'PPO']
        # 重新排列句柄和标签以匹配所需的顺序
        ordered_handles = [next(h for h, l in zip(handles, labels) if l == label) for label in desired_order]
        ordered_labels = desired_order
        ax.set_xlabel("Million iterations", fontdict=plt_conf.label_font)
        ax.set_ylabel("Average return", fontdict=plt_conf.label_font)
        ax.set_xlim(0, 1.5)
        #ax.set_ylim(-20,)
        ax.set_xticks([0, 0.3, 0.6, 0.9, 1.2, 1.5])
        ax.tick_params(labelsize=plt_conf.tick_size)
        #ax.legend(ordered_handles, ordered_labels, loc=plt_conf.legend_loc, ncol=2, prop=plt_conf.legend_font)

        if label_on and idx == len(env_list)-1:
            legend = ax.legend(ordered_handles, ordered_labels,loc=plt_conf.legend_loc,ncol=plt_conf.legend_ncol,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
            #legend = ax.legend(loc=plt_conf.legend_loc,ncol=plt_conf.legend_ncol,prop=plt_conf.legend_font,fontsize=plt_conf.tick_size,markerscale=0.35, frameon=False)
            for line in legend.get_lines():
                line.set_linewidth(plt_conf.line_width)
            ax.get_legend().remove()
        else:
            ax.get_legend().remove()
            #ax.get_legend()



        #plt.show()

        #fig.savefig(os.path.join(save_path,'perf_of_'+env+'.'+plt_conf.save_format), bbox_inches="tight", pad_inches=plt_conf.pad)
        fig.savefig(os.path.join(save_path,env+'.pdf'), bbox_inches="tight", pad_inches=plt_conf.pad)

    return


if __name__ == "__main__":
    data_file = "./data/mdsacth25/run_data.json"
    #data_file = "./data/huamoid.json"
    save_path = "./figures/mdsact_paper_final"
    os.makedirs(save_path, exist_ok=True)
    #env_list = [ "gym_ant","gym_walker2d","gym_halfcheetah", "gym_humanoid"]
    #env_list = ["gym_halfcheetah",'gym_inverteddoublependulum', "gym_ant", "gym_humanoid","gym_bipedalwalker","gym_pusher","gym_hopper"]
    env_list = ["gym_halfcheetah", "gym_ant", "gym_humanoid", "gym_inverteddoublependulum","gym_bipedalwalker","gym_pusher","gym_hopper"]
    #env_list = ["gym_halfcheetah"]
    #env_list = ["gym_humanoid","gym_ant","gym_halfcheetah","gym_bipedalwalker","gym_pusher",'gym_walker2d',"gym_inverteddoublependulum",]
    #alg_list = ['DSAC-T', 'SAC', 'TD3', 'DDPG', 'TRPO', 'PPO']
    #env_list = ["gym_bipedalwalker","gym_reacher","gym_pusher","gym_hopper","gym_swimmer"]
    plot_performance(data_file, plt_conf, save_path, env_list, label_on = True)





