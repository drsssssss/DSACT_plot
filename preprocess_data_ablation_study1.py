from read_tensorboard import TsboardReader
import logging

def get_logger(log_level,log_file):
    selflogger = logging.getLogger('Export Data Logger')
    logging.basicConfig(filename=log_file,
                        filemode= 'a',
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                        level=log_level)
    return selflogger


logger = get_logger(logging.INFO,'./data/ablation1/log.txt')


ts_reader = TsboardReader(
    source_folder = "/home/wangwenxuan/dsac2_exp_results/ablation1_new/",
    floder_surfix= '',
    save_floder= './data/ablation1_new',
    algorithms = ['DSAC22MEAN','DSAC22MEN','DSAC22MEANS'],
    envs =  ['gym_humanoid'],
    policy_num= 5,
    metrics =  ['Evaluation/1. TAR-RL iter'],
    downsample_ratio= 15000,
    step_trans_dict={},
    alg_tag_dict={"DSAC22MEAN": "DSAC-T", "DSAC22MEN": "DSAC-T  w/o critic gradient adjusting", "DSAC22MEANS": "DSAC-T w/ single value distribution"},
    logger = logger,
    max_record_points= 300,
    get_files_func=None,
    )

data_df = ts_reader.read_and_save_data()