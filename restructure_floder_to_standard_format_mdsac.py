# copy the floders and files from the source floders to the target floders and restruture the floders
# the source floders are in the form of: mujoco/alg_mlp/env_id_env_name/test_*_run_*/
# the target floders should be in the from of : gops_benchmark/env_name/alg_YYMMDD-HHMMSS/

import os
import shutil
import itertools
import string

source_path ="/home/go/桌面/XLM/xiaoliming-MDSAC/MDSAC10SAMPLE/results/transfer"
#source_path ="/home/go/桌面/GOPS-dsac-t/results/mujoco/transfer"
#source_path ="/home/go/桌面/xiaoliming-MDSAC/MDSACT_10/results/mujoco/transfer"
#source_path ="/home/go/桌面/GOPS-dsac-t/results/mujoco/transfer"
#target_path = "/home/go/桌面/dsact_plot-master/dsac22meanc_mlp"
target_path = "mdsacth25e"
os.makedirs(target_path,exist_ok=True)
#algs = ['dsact','dsac','sac','ppo','trpo','td3','ddpg']
algs = ['mdsacth25e']
apprfuncs = ['mlp']
#envs=["gym_humanoid",'gym_inverteddoublependulum','gym_reacher','gym_ant', "gym_halfcheetah","gym_walker2d","gym_bipedalwalker","gym_pusher",'gym_hopper','gym_swimmer']
#envs=["gym_bipedalwalker","gym_reacher","gym_pusher","gym_hopper","gym_swimmer"]
#envs=["gym_inverteddoublependulum","gym_halfcheetah"]
#envs = ["gym_ant", "gym_halfcheetah",  "gym_humanoid", "gym_inverteddoublependulum","gym_walker2d"]
envs = ["gym_ant","gym_walker2d","gym_halfcheetah",  "gym_humanoid"]
#envs = ["gym_inverteddoublependulum"]
#envs = ["gym_inverteddoublependulum","gym_halfcheetah"]
# find the source floders and copy the files starts with events to the target floders
for alg, appr, env in itertools.product(algs,apprfuncs,envs):
    source_dir = os.path.join(source_path,alg+"_"+appr)
    target_dir = os.path.join(target_path,env)
    for floder in os.listdir(source_dir):
        if  floder.startswith(env) and floder.endswith("0109_run0"): #houzui
            source_floder = os.path.join(source_dir,floder)
            target_floder = os.path.join(target_dir,alg.upper()+'_'+floder)
            # os.makedirs(target_floder,exist_ok=True)           
            shutil.copytree(source_floder,target_floder, dirs_exist_ok = True)
            print("copy {} to {}".format(source_floder,target_floder))