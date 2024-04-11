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
    source_folder = "/home/go/桌面/XLM/dsact_plot-master/mdsacth25", #!
    floder_surfix= '',
    save_floder= './data/mdsacth25',
    #algorithms = ['DSAC22MEAN','DSAC22MEANNT','DSACSTD','SAC','TD3','DDPG','TRPO','PPO'],
    algorithms = ['MDSACTH25'],
    #envs =  ["gym_humanoid",'gym_inverteddoublependulum','gym_reacher','gym_ant',"gym_walker2d",'gym_halfcheetah',"gym_bipedalwalker","gym_pusher",'gym_hopper','gym_swimmer'],#,'gym_ant','gym_humanoid'],
    envs =  ["gym_halfcheetah", "gym_ant", "gym_humanoid", "gym_inverteddoublependulum","gym_bipedalwalker","gym_pusher","gym_hopper"],
    policy_num= 5,
    metrics =  ['Evaluation/1. TAR-RL iter'],
    downsample_ratio= 15000,
    step_trans_dict={'TRPO':50,'PPO':100},
    alg_tag_dict={"MDSACTH25": "M-DSAC"},
    logger = logger,
    max_record_points= 100,
    get_files_func=None,
    )

data_df = ts_reader.read_and_save_data()