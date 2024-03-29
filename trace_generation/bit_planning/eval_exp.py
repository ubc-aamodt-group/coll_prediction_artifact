from eval_gnn import eval_gnn
from eval_next import eval_next
from eval_bit import eval_bit, eval_lazysp
from eval_rrt import eval_rrt
import numpy as np
from environment import MazeEnv, KukaEnv, Kuka2Env
import pickle
import sys

env_names = ['Maze_2D_Easy', 'Maze_2D_Normal', 'Maze_2D_Hard', 'Maze_3D', 'Kuka_7D', 'Kuka_13D', 'Kuka_14D']
envs = [
    MazeEnv(dim=2, map_file='maze_files/mazes_easy.npz'),
    MazeEnv(dim=2, map_file='maze_files/mazes_normal.npz'),
    MazeEnv(dim=2, map_file='maze_files/mazes_hard.npz'),
    MazeEnv(dim=3, map_file="maze_files/mazes_hard_3.npz"),
    KukaEnv(),
    KukaEnv(kuka_file="kuka_iiwa/model_3.urdf", map_file="maze_files/kukas_13_3000.pkl"),
    Kuka2Env()
    ]
indexeses = [np.arange(1000), np.arange(1000), np.arange(1000), np.arange(2000, 3000), np.arange(2000, 3000), np.arange(2000, 3000), np.arange(2000, 3000)]
innn=int(sys.argv[1])
indexeses = [np.arange(1000), np.arange(1000), np.arange(1000), np.arange(2000, 3000), np.arange(innn, innn+1), np.arange(innn, innn+1), np.arange(2000, 3000)]
seeds = [1234]#, 2341, 3412, 4123]
#methods = [eval_next, eval_bit, eval_rrt, eval_lazysp]
methods = [eval_gnn, eval_next, eval_bit, eval_rrt, eval_lazysp]
method_names = ['GNN', 'NEXT', 'BIT*', 'RRT*', 'LazySP']
#method_names = ['NEXT', 'BIT*', 'RRT*', 'LazySP']
result_total = {}

skim_env=['Maze_2D_Easy', 'Maze_2D_Normal','Kuka_13D', 'Kuka_14D','Maze_3D', 'Maze_2D_Hard']
skim_methods=['GNN', 'NEXT', 'LazySP', 'BIT*']
for env_name, env, indexes in zip(env_names, envs, indexeses):
    if env_name in skim_env:
        continue
    #if indexes[0]>10:
    #    break
    for method_name, method in zip(method_names, methods):
        if not(method_name==sys.argv[2]):
            #if method_name in skim_methods:
            continue
        results = []
        for seed in seeds:
            #print(env_name, method_name, seed)
            result = method(str=str(env), seed=seed, env=env, indexes=indexes, use_tqdm=False)
            results.append(result)
            result_total[env_name, method_name, str(seed)] = result

            pickle.dump(result_total, open("data/result.p", "wb"))
        if True:
            print(env_name, method_name, 'Avg')
            print('success rate:', np.mean([result[0] for result in results]))
            print('collision check: %.2f' % np.mean([result[1] for result in results]))
            print('running time: %.2f' % np.mean([result[2] for result in results]))
            print('path cost: %.2f' % np.mean([result[3] for result in results]))
            print('total time: %.2f' % np.mean([result[4] for result in results]))
            print('')
        result_total[env_name, method_name, 'Avg'] = tuple([np.mean([result[i] for result in results]) for i in range(5)])
        pickle.dump(result_total, open("data/result.p", "wb"))

#print(result_total)
