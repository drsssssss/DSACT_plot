from read_tensorboard import TsboardReader
import logging

def get_logger(log_level,log_file):
    selflogger = logging.getLogger('Export Data Logger')
    logging.basicConfig(filename=log_file,
                        filemode= 'a',
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                        level=log_level)

    selflogger.addHandler(logging.StreamHandler())
    selflogger.info("new logger")
    selflogger.info("log level: {}".format(log_level))
    selflogger.info("log file: {}".format(log_file))
    selflogger.info("log format: {}".format('%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s'))
    return selflogger


logger = get_logger(logging.INFO,'./data/log.txt')


ts_reader = TsboardReader(
    source_folder = "/home/go/桌面/XLM/dsact_plot-master/AllEnv", #!
    floder_surfix= '',
    save_floder= './data/AllEnv_NOdsacV1', #!
    #algorithms = ['DSAC22MEAN','DSAC22MEANNT','DSACSTD','SAC','TD3','DDPG','TRPO','PPO'],
    #algorithms = ['DSACT','SAC','PPO','TRPO','TD3','DDPG'],
    algorithms = ['DSACT','SAC','TD3','DDPG','TRPO','PPO'],
    #algorithms = ['DSACT','SAC','TD3','DDPG','TRPO','PPO'],
    #envs =  ["gym_bipedalwalker","gym_reacher","gym_pusher","gym_hopper","gym_swimmer"],
    #envs =  ["gym_bipedalwalkerhardcore"],
    envs=["gym_halfcheetah", "gym_ant", "gym_humanoid", "gym_inverteddoublependulum", "gym_reacher", "gym_bipedalwalker", "gym_pusher", "gym_hopper", "gym_swimmer", "gym_walker2d"],
#envs =  ["gym_halfcheetah", "gym_ant", "gym_humanoid", "gym_inverteddoublependulum","gym_bipedalwalker","gym_pusher","gym_hopper"],
    policy_num= 5,
    metrics =  ['Evaluation/1. TAR-RL iter'],
    downsample_ratio= 15000,
    step_trans_dict={'TRPO':50,'PPO':100},
    alg_tag_dict={"DSACT": "DSAC"},
    #$alg_tag_dict={"DSACT": "DSAC-T","DSAC":"DSAC-v1"},
    logger = logger,
    max_record_points= 100,
    get_files_func=None,
    )

data_df = ts_reader.read_and_save_data()