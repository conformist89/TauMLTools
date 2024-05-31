import os

for i in range(0,22):
    os.system("python apply_training.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=e1f3ddb3c4c94128a34a7635c56322eb \
        path_to_input_dir=/eos/user/o/olavoryk/roc_curve_files/WToTauNu_M-20/ input_filename=nano_"+str(i)+"_0 sample_alias=WToTauNu_M-20_v3")