import subprocess

import trimesh
import slam.plot as splt

param = ['--in',  # 0
         '--out',  # 1
         '--outT',  # 2
         '--outG',  # 3
         '--mesh',  # 4
         '--fill',  # 5
         '--iters',  # 6
         '--stepSize',  # 7
         '--cutOff',  # 8
         '--degree',  # 9
         '--aSteps',  # 10
         '--aStepSize',  # 11
         '--res',  # 12
         '--smooth',  # 13
         '--c2i',  # 14
         '--gssTolerance',  # 15
         '--poincareMaxNorm',  # 16
         '--random',  # 17
         '--noCenter',  # 18
         '--ascii',  # 19
         '--collapse',  # 20
         '--noOrient',  # 21
         '--noGridScale',  # 22
         '--spherical',  # 23
         '--lump',  # 24
         '--verbose',  # 25
         '--fullVerbose'    # 26
         ]

args1 = ['model_in/foetus1.ply',  # 0
         'ResultSphereMap/brain',  # 1
         '',  # 2
         '',  # 3
         '',  # 4
         '',  # 5
         '100',  # 6
         '',  # 7
         '',  # 8
         '',  # 9
         '',  # 10
         '',  # 11
         '',  # 12
         '',  # 13
         '',  # 14
         '',  # 15
         '',  # 16
         ' ',  # 17
         ' ',  # 18
         ' ',  # 19
         ' ',  # 20
         ' ',  # 21
         ' ',  # 22
         ' ',  # 23
         ' ',  # 24
         ]

for i in range(2, len(args1)):
    if args1[i] != '':
        if args1[i] != ' ':
            subprocess.call(['./SphereMap',
                             param[0],
                             args1[0],
                             param[1],
                             str(args1[1])+'_'+str(i)+'_args.cmcf.ply',
                             param[23],
                             param[i],
                             args1[i]])
        else:
            subprocess.call(['./SphereMap',
                             param[0],
                             args1[0],
                             param[1],
                             str(args1[1])+'_'+str(i)+'_args.cmcf.ply',
                             param[23],
                             param[i]])

        model_path = str(args1[1])+'_'+str(i)+'_args.cmcf.ply'
        print(model_path)
        model = trimesh.load(model_path)
        splt.pyglet_plot(model)

