
import os
import shutil

# The root directory where 'AllEnv' is located.
# You should change this to the actual path where 'AllEnv' is on your system.
root_dir = '/home/go/桌面/XLM/dsact_plot-master/AllEnv'

# The target directory where 'source_data_mdsacth25' will be created.
# You should change this to the actual path where you want 'source_data_mdsacth25' to be.
target_dir = '/home/go/桌面/XLM/gops_doc-master/source/plot_benchmark/source_data_mdsacth25'

# Function to create directory if it doesn't exist
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Create the target directory
create_dir(target_dir)

# List all the environments in the 'AllEnv' directory
env_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

# Iterate over each environment
for env in env_dirs:
    env_path = os.path.join(root_dir, env)
    # Create corresponding directory in target directory
    target_env_path = os.path.join(target_dir, env)
    create_dir(target_env_path)
    
    # List all algorithm directories in the current environment
    algo_dirs = [d for d in os.listdir(env_path) if os.path.isdir(os.path.join(env_path, d))]
    
    # Iterate over each algorithm directory
    for algo in algo_dirs:
        algo_path = os.path.join(env_path, algo)
        # Create corresponding algorithm directory in target environment directory
        target_algo_path = os.path.join(target_env_path, algo.split('_')[0])  # Assuming algo name is the prefix before the first '_'
        create_dir(target_algo_path)
        
        # Find the event.out file (assuming there is only one per algorithm directory)
        for file in os.listdir(algo_path):
            if file.startswith('events.out'):
                event_file_path = os.path.join(algo_path, file)
                # Copy the event.out file to the corresponding seed directory in the target algorithm directory
                shutil.copy(event_file_path, target_algo_path)

# Inform the user the process is complete
print('Files have been organized into the target structure.')
