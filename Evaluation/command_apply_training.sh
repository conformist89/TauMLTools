# python apply_training.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=e1f3ddb3c4c94128a34a7635c56322eb \
#         path_to_input_dir=/eos/user/o/olavoryk/roc_curve_files/WToTauNu_M-20 \
#          input_filename=nano sample_alias=WToTauNu_M-20_v3


for i in {0..22}
do
   python apply_training.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=e1f3ddb3c4c94128a34a7635c56322eb \
        path_to_input_dir=/eos/user/o/olavoryk/roc_curve_files/WToTauNu_M-20/ input_filename=nano_$i sample_alias=WToTauNu_M-20_v3
done


