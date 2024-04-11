import pandas as pd
import numpy as np

def read_xlsx(path):
    data = pd.read_excel(path, sheet_name=None)
    # get row name form the first sheet
    rowname = data['mean'].iloc[:,0].values
    # get colomn name from the first sheet
    colomnname = data['mean'].columns.values[1:]
    return data, rowname, colomnname


def name2index(name, name_list):
    return np.where(name_list==name)[0][0] + 1


def cal_improve(alg, env, algs, envs, data):
    improve_dict = {}
    for alg1 in algs:
        if alg1 == alg:
            continue
        else:
            alg1_index = name2index(alg1, algs)
            alg_index = name2index(alg, algs)
            env_index = name2index(env, envs) -1
            alg1_data = float(data.iloc[env_index, alg1_index])
            alg_data = float(data.iloc[env_index, alg_index])
            improve = (alg_data -alg1_data ) / alg1_data
            improve = round(improve, 3)*100
            print(f"{alg} improve {alg1} in {env} is {improve}%")
            improve_dict[alg1] = improve

    return improve_dict



path = "/home/go/桌面/dsact_plot-master/figures/main_exp_1022/final_perfmean.xlsx"

data, envs, algs = read_xlsx(path)

results = cal_improve("DSAC-T", "gym_inverteddoublependulum",algs,envs, data["mean"])
print(results)


