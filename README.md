非必须步骤：删除(**opt.pkl, 1500000.pkl, config.json ,及events.out文件**）之外的所有无用文件： python delete_pkl.py
其中path/to/your/folder为下图的:your/path/results/gym_pendulum
![image](https://github.com/drsssssss/DSACT_plot/assets/109412594/7fab08dd-5886-4b14-8be8-008276366220)

delete之后再进行以下步骤，减少占用。


运行顺序：


python restructure_floder_to_standard_format.py **标准格式化folder**


python preprocess_data.py **标准格式folder产生标准格式json**


python plot_performance.py **json 2 pdf/png**


python cal_final_perf.py **json 2 perfmance table**


第一步的restructure_floder_to_standard_format.py的source_path
source_path ="/home/go/桌面/XLM/GOPS-dsac-t/results/mujoco/transfer" 组成如下：
![image](https://github.com/drsssssss/DSACT_plot/assets/109412594/9368eac5-802f-466c-b1e1-aa6b810c3cb3)
