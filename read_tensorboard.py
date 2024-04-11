
import json
import pandas as pd
import numpy as np
import os
import glob
import itertools
from tensorboard.backend.event_processing import event_accumulator
from operator import itemgetter

# tensorboard.backend.application.logger.setLevel("ERROR")

# Define the path to the events.out files

class TsboardReader:
    def __init__(self, source_folder, save_floder,algorithms,policy_num, envs,floder_surfix, metrics, 
                 downsample_ratio, step_trans_dict, alg_tag_dict, max_record_points,logger, get_files_func = None,configs =['',],config_name = 'default',truncated_alg_list = []):
        self.source_folder = source_folder
        self.save_floder = save_floder
        self.algorithms = algorithms
        self.envs = envs
        self.metrics = metrics
        self.downsample_ratio = downsample_ratio
        self.step_trans_dict = step_trans_dict
        self.alg_tag_dict = alg_tag_dict  
        self.max_record_points = max_record_points
        self.floder_surfix = floder_surfix
        self.get_files_func = get_files_func
        self.configs = configs
        self.config_name = config_name
        self.logger = logger
        self.policy_num = policy_num
        self.truncated_alg_list = truncated_alg_list

        if not os.path.exists(self.save_floder):
            os.makedirs(self.save_floder)


    def __default_get_files_path(self, algorithm:str,env:str,config:str):
        # get all the path of the files whose name begin with 'events.out' in the algorithm folder
        target_file_list = []
        alg_folder = os.path.join(self.source_folder, env)
        if os.path.exists(alg_folder):
            # get the floders in the algorithm folder that start with the "algorithm name"+_ and end with the floder_surfix
            if config == '':
                floders = glob.glob(os.path.join(alg_folder,algorithm.upper()+'_*'+self.floder_surfix))
            else:
                floders = glob.glob(os.path.join(alg_folder,algorithm.upper()+'_'+env+'_'+config+'_*'+self.floder_surfix))
            num_floders = len(floders)
            if num_floders == 0:
                self.logger.error("No floder found for algorithm: {} in env: {}".format(algorithm,env))
                raise RuntimeError("No floder found for algorithm: {} in env: {}".format(algorithm,env))
            if num_floders < self.policy_num:
                self.logger.warning("Only {} floders found for algorithm: {} in env: {}".format(num_floders,algorithm,env))
            if num_floders > self.policy_num:
                self.logger.warning("More than {} floders found for algorithm: {} in env: {}, only use the latest floders".format(num_floders,algorithm,env))
                floders.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                floders = floders[:self.policy_num]
            for floder in floders:
                candidate_file_list = []
                for file in os.listdir(floder):
                    if file.startswith('events.out'):
                        candidate_file_list.append(os.path.join(floder,file))
                events_num = len(candidate_file_list)
                if events_num == 0:
                    self.logger.error("No event file found in floder: {}".format(floder))
                    raise RuntimeError("No event file found in floder: {}".format(floder))
                if events_num > 1:
                    self.logger.warning("More than one event file found in floder: {}, only use the one with largest size".format(floder))
                    candidate_file_list.sort(key=lambda x: os.path.getsize(x), reverse=True)
                    candidate_file_list = candidate_file_list[:1]
                target_file_list.append(candidate_file_list[0])      
        else:
            self.logger.error("The target folder does not exist!")
            raise RuntimeError('The target folder does not exist!') 
        self.logger.info("Get {} event files for algorithm: {} in env: {}".format(len(target_file_list),algorithm,env))
        self.logger.info("The event files are: {}".format(target_file_list))
        return target_file_list
    
    def get_files_path(self, algorithm,env,config):
        if self.get_files_func is None:
            return self.__default_get_files_path(algorithm,env,config)
        else:
            return self.get_files_func(algorithm,env)
        
    def read_tensorboard(self, path):
        """
        Input dir of tensorboard log.
        """
        ea = event_accumulator.EventAccumulator(path)
        ea.Reload()
        valid_key_list = ea.scalars.Keys()

        event_dict ={key:ea.scalars.Items(key) for key in valid_key_list}
        return event_dict
    
    def reformate_data(self, event_dict:dict, metrics:list, algorithm:str, env:str, config:str, run_id:int):
        data_list = []
        # FIXME: only support equal length of metrics
        metric = metrics[0]
        if algorithm in self.truncated_alg_list:
            max_record_points = int(0.4*self.max_record_points)
        else:
            max_record_points = self.max_record_points

        data_length = len(event_dict[metric])
        if algorithm in self.alg_tag_dict.keys():
            alg_tag = self.alg_tag_dict[algorithm]
        else:
            alg_tag = algorithm
        record_points_num = 0
        data_list = []
        for id in range(data_length):
            e = event_dict[metric][id]
            if record_points_num>= max_record_points:
                break
            if algorithm in self.step_trans_dict.keys():
                step = e.step*self.step_trans_dict[algorithm]
            else:
                step = e.step
            # Add the data to the list
            if step >= record_points_num*self.downsample_ratio:                
                data_list.append({'algorithm': alg_tag,'env':env, 'run': id, 'step': step, 'value': e.value, 'metric': metric, 'run_id': run_id, self.config_name:config})
                record_points_num += 1

        return data_list
    
    def convert_to_df(self, data_list:list):
        # FIXME: only support equal length of metrics
        metric = self.metrics[0]
        data_summary = pd.DataFrame(data_list)
        # data_summary = data_df.groupby(['algorithm', 'step','env'])['value'].agg([np.mean, np.std]).reset_index()
        # data_summary.columns = ['algorithm', 'step', 'env', 'value_mean', 'value_std']
        # data_summary['value_std'] = data_summary['value_std'].fillna(0)
        return data_summary


    
    def read_and_save_data(self):
        total_data_list = []
        for algorithm, env, config in itertools.product(self.algorithms, self.envs,self.configs):
            file_list = self.get_files_path(algorithm,env,config)
            for idx, file in enumerate(file_list):
                event_dict = self.read_tensorboard(file)
                data_list = self.reformate_data(event_dict, self.metrics, algorithm, env,config, idx)
                total_data_list.extend(data_list)
        data_summary = self.convert_to_df(total_data_list)
        data_json = json.loads(data_summary.reset_index().to_json(orient='records'))
        filename = os.path.join(self.save_floder, 'run_data.json')
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)
        self.logger.info("Data saved to {}".format(filename))
        return data_summary       


                 


        

        

        


# events_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'source_data_run3')

# # Define the names of the algorithms (which are the names of the folders)
# algorithms = ['DSAC2','SAC','TD3','DDPG','TRPO','PPO']
# on_policy_algorithms = ['PPO','TRPO']
# envs = ['gym_ant', 'gym_halfcheetah', 'gym_hopper', 'gym_humanoid', 'gym_inverteddoublependulum','gym_invertedpendulum','gym_reacher', 'gym_swimmer', 'gym_walker2d']
# # envs = ['gym_swimmer']
# # Define the metrics you want to visusalize
# metrics = ['Evaluation/1. TAR-RL iter']
# sample_interval = 15_000 # 0.3M
# step_fix_factor = 250  # match the step of the on-policy algorithms since they repeat network updates in the same step
# max_record_points = 100 # max_record_points * sample_interval = max RL steps(1.5M)
# # Create a list to hold the data

