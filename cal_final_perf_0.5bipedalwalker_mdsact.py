import json
import os
import copy
import pandas as pd
from misc import cfg
from copy import deepcopy
import numpy as np
import xlsxwriter as xw

plt_conf = deepcopy(cfg)
plt_conf.smooth_alpha = 1
conut_start_step = 0.35 # Million iterations

def process_data(data_df: pd.DataFrame):
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



def cal_final_perf(data_file, save_path, env_list, alg_list):
    data = json.load(open(data_file, "r"))
    data_df = pd.DataFrame(data)
    cal_data = process_data(data_df)
    cal_data_max = copy.deepcopy(cal_data)


    # get the value mean and std of the last step of the data group by algorithm, env
    # get the last ten steps of the data group by algorithm, env, run_id
    cal_data = cal_data[cal_data["step"]>=conut_start_step]
    cal_data_max = cal_data_max[cal_data_max["step"]>=conut_start_step]
    cal_data = cal_data.groupby(["algorithm", "env","step"])["value"].agg([np.mean, np.std,np.max]).reset_index()
    cal_data_max = cal_data_max.groupby(["algorithm", "env","run_id"])["value"].agg([np.max]).reset_index()
    cal_data_max.columns = ["algorithm", "env","run_id","max"]
    cal_data.columns = ["algorithm", "env","step","mean","std","max"]
    final_df = pd.DataFrame(columns=["algorithm", "env","final_mean","final_std"])
    for alg in alg_list:
        for env in env_list:
            # get the data of the last step of the algorithm and env
            data = cal_data[(cal_data["algorithm"]==alg) & (cal_data["env"]==env)]
            max_data = cal_data_max[(cal_data_max["algorithm"]==alg) & (cal_data_max["env"]==env)]
            # get the mean and std of the last step
            # print("using max value to calculate the mean and std")
            # mean = data["max"].values[-10:].max()
            # std = data["std"].values[-10:].mean()
            mean = max_data["max"].values.mean()
            std = max_data["max"].values.std()
            # add the mean and std to the cal_data
            add_data = {"algorithm":alg, "env":env,"mean":mean,"std":std}
            add_data = pd.DataFrame(add_data, index=[0])
            final_df = pd.concat([final_df, add_data], ignore_index=True)


    # save the data to excel, the sheet names are mean and std, the index is algorithm and the columns are env, and add another sheet named mean+std which the content of it is str(mean+-std) rounded to  decimal places
    writer = pd.ExcelWriter(os.path.join(save_path, "final_perfmean.xlsx"), engine='xlsxwriter')
    df_mean = final_df.pivot(index='env', columns='algorithm', values='mean')

    df_mean.reindex(env_list)
    df_mean.to_excel(writer, columns=alg_list,sheet_name='mean')
    df_std = final_df.pivot(index='env', columns='algorithm', values='std')
    df_std.reindex(env_list)
    df_std.to_excel(writer, columns=alg_list, sheet_name='std')
    df_mean_std = df_mean.applymap(lambda x: int(x)).astype(str) + "±" + df_std.applymap(lambda x: int(x)).astype(str)
    #df_mean_std    = np.round(df_mean_std)
    df_mean_std.reindex(env_list)

    df_mean_std.to_excel(writer, columns=alg_list, sheet_name='mean+std')

    writer.close()

    return



# def cal_final_perf(data_file, save_path, env_list, alg_list):
#     data = json.load(open(data_file, "r"))
#     data_df = pd.DataFrame(data)
#     cal_data = process_data(data_df)


#     # get the value mean and std of the last step of the data group by algorithm, env
#     cal_data = cal_data.groupby(["algorithm", "env","step"])["value"].agg([np.mean, np.std]).reset_index()
#     cal_data.columns = ["algorithm", "env","step","mean","std"]
#     final_df = pd.DataFrame(columns=["algorithm", "env","final_mean","final_std"])
#     for alg in alg_list:
#         for env in env_list:
#             # get the data of the last step of the algorithm and env
#             data = cal_data[(cal_data["algorithm"]==alg) & (cal_data["env"]==env)]
#             # get the mean and std of the last step
#             mean = data["mean"].values[-10:].mean()
#             std = data["std"].values[-10:].mean()
#             # add the mean and std to the cal_data
#             add_data = {"algorithm":alg, "env":env,"mean":mean,"std":std}
#             add_data = pd.DataFrame(add_data, index=[0])
#             final_df = pd.concat([final_df, add_data], ignore_index=True)


#     # save the data to excel, the sheet names are mean and std the index is algorithm and the columns are env
#     writer = pd.ExcelWriter(os.path.join(save_path, "final_perf.xlsx"), engine='xlsxwriter')
#     df_mean = final_df.pivot(index='algorithm', columns='env', values='mean')
#     df_mean.to_excel(writer, sheet_name='mean')
#     df_std = final_df.pivot(index='algorithm', columns='env', values='std')
#     df_std.to_excel(writer, sheet_name='std')
#     writer.save()

#     return

    


if __name__ == "__main__":
    data_file = "./data/mdsacth25/run_data.json"
    save_path = "./figures/bipedalwalker-mdsact"
    env_list = ["gym_bipedalwalker"]
    #env_list = ["gym_halfcheetah", "gym_ant", "gym_humanoid", "gym_inverteddoublependulum","gym_walker2d","gym_bipedalwalker","gym_reacher","gym_pusher","gym_hopper","gym_swimmer"]
    #alg_list = ['DSAC-T','DSAC']
    alg_list = ['MDSACTH25','DSAC-T','DSAC-v1','SAC','TD3','DDPG','TRPO','PPO']
    #alg_list = ['DSAC-T','DSAC-v1','SAC','TD3','DDPG','TRPO','PPO']
    cal_final_perf(data_file, save_path, env_list, alg_list)
        