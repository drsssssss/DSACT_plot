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
    source_folder = "/home/go/桌面/XLM/dsact_plot-master/CarRacing",
    floder_surfix= '',
    save_floder= './data/carracing',
    # algorithms = ['DSACSTD','SAC'],
    algorithms = ['DSAC','SAC','TD3','DDPG','TRPO','PPO','DSACT'],
    envs =  ['gym_carracingraw'],
    policy_num= 5,
    metrics =  ['Evaluation/1. TAR-RL iter'],
    downsample_ratio= 5000,
    step_trans_dict={'TRPO':1000,'PPO':1000},
    alg_tag_dict={"DSACT": "DSAC-T","DSAC":"DSAC-v1"},
    logger = logger,
    max_record_points= 100,
    get_files_func=None,
    truncated_alg_list = ['TD3','DDPG']
    )

data_df = ts_reader.read_and_save_data()