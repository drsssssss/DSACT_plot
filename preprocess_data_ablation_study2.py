from read_tensorboard import TsboardReader
import logging

def get_logger(log_level,log_file):
    selflogger = logging.getLogger('Export Data Logger')
    logging.basicConfig(filename=log_file,
                        filemode= 'a',
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                        level=log_level)
    return selflogger


logger = get_logger(logging.INFO,'./data/log.txt')


ts_reader = TsboardReader(
    source_folder = "/home/go/桌面/dsact_plot-master/dsactb20/",
    floder_surfix= '',
    save_floder= './data/ablation_bound/tb20_cheetah_011',
    #algorithms = ['DSAC22MEAN','DSAC22MEANB10'],
    algorithms = ['DSACTB20'],
    envs =  ["gym_halfcheetah"],
    configs = ['0.1','1.0'],
    config_name= 'Reward scale',
    policy_num= 5,
    metrics =  ['Evaluation/1. TAR-RL iter'],
    downsample_ratio= 15000,
    step_trans_dict={},
    #alg_tag_dict={"DSAC22MEAN": "DSAC-T", "DSAC22MEANB10": "DSAC-T w/ fixed bound",},
    alg_tag_dict={ "DSACTB20": "DSAC-T w/ fixed bound",},
    #alg_tag_dict={ "DSAC": "DSAC-v1",},
    logger = logger,
    max_record_points= 100,
    get_files_func=None,
    )

data_df = ts_reader.read_and_save_data()