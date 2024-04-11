from read_tensorboard import TsboardReader
import logging

def get_logger(log_level,log_file):
    selflogger = logging.getLogger('Export Data Logger')
    logging.basicConfig(filename=log_file,
                        filemode= 'a',
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                        level=log_level)
    return selflogger


logger = get_logger(logging.INFO,'./data/ablation3/log_ant.txt')


ts_reader = TsboardReader(
    source_folder = "/home/wangwenxuan/dsac2_exp_results/ablation3/",
    floder_surfix= '',
    save_floder= './data/ablation3',
    algorithms = ['DSAC2W2MEAN','DSAC22MEAN'],
    envs =  ['gym_ant'],
    configs = ['1.0','2.0','3.0'],
    config_name= 'Reward scale',
    policy_num= 5,
    metrics =  ['Evaluation/1. TAR-RL iter'],
    downsample_ratio= 15000,
    step_trans_dict={},
    alg_tag_dict={"DSAC2W2MEAN": "DSAC-T", "DSAC2W2MEANB10": "DSAC-T w/ fixed bound", "DSAC22MEAN": "DSAC-T w/o gradient scale"},
    logger = logger,
    max_record_points= 100,
    get_files_func=None,
    )

data_df = ts_reader.read_and_save_data()