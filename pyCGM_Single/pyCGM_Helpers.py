import os
from argparse import ArgumentParser


def parse_args():
    
    parser = ArgumentParser(description='File Names')
    # general
    parser.add_argument('--dynamic_trial', type=str, required=True)
    parser.add_argument('--static_trial', type=str, required=True)
    parser.add_argument('--vsk_file', type=str,required=True)
    parser.add_argument('--outputDir', type=str,default='./output/')
    parser.add_argument('--player',type=int,required=True)
    args = parser.parse_args()
    return args
    
    

#     scriptdir = os.path.dirname(os.path.abspath(__file__))
#     os.chdir( scriptdir )
#     os.chdir( ".." ) #move current path one up to the directory of pycgm_embed
    
#     if x == 1:
#         dir = '/storage/Trinity Data/mocap _data/lower_01/'
#         dynamic_trial = dir+'Lower02.c3d' 
#         static_trial =  dir+'Static.c3d' 
#         vsk_file =      dir+'Player.vsk'     
#         outputfile =    dir+'pycgm_results_lower2'
#         CoM_output =    dir+'CoM'
        
#     if x == 2:
#         dir = 'SampleData/ROM/'
#         dynamic_trial = dir+'Sample_Dynamic.c3d' 
#         static_trial =  dir+'Sample_Static.c3d' 
#         vsk_file =      dir+'Sample_SM.vsk'     
#         outputfile =    dir+'pycgm_results_8.csv'
#         CoM_output =    dir+'CoM'
        
#     if x == 3:
#         dir = 'SampleData/Sample_2/'
#         dynamic_trial = dir+'RoboWalk.c3d' 
#         static_trial =  dir+'RoboStatic.c3d' 
#         vsk_file =      dir+'RoboSM.vsk'     
#         outputfile =    dir+'pycgm_results.csv'
#         CoM_output =    dir+'CoM'

#     return dynamic_trial,static_trial,vsk_file,outputfile,CoM_output