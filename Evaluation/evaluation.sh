echo "%%%%%%%%%%% Deep Tau 2.1 evaluation"

python evaluate_performance.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=3664a0c81e43429bab18138309d17a05 \
       discriminator=DeepTau_v2p1 'path_to_input="/eos/user/o/olavoryk/roc_curve_files/{sample_alias}/*.root"' \
       path_to_pred=null 'path_to_target="${path_to_mlflow}/${experiment_id}/e1f3ddb3c4c94128a34a7635c56322eb/artifacts/predictions/{sample_alias}/*_pred.h5"' \
       vs_type=e dataset_alias=WToTauNu_M20_DY

echo "Deep Tau 2.1 evaluation is finished"

echo "%%%%%%%%%%% Deep Tau 2.5 evaluation"

python evaluate_performance.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=7b6d535b3d054540acb727c3f33d1a8f \
       discriminator=DeepTau_run3 'path_to_input="/eos/user/o/olavoryk/roc_curve_files/{sample_alias}/*.root"' \
       path_to_pred=null 'path_to_target="${path_to_mlflow}/${experiment_id}/e1f3ddb3c4c94128a34a7635c56322eb/artifacts/predictions/{sample_alias}/*_pred.h5"' \
       vs_type=e dataset_alias=WToTauNu_M20_DY

echo "Deep Tau 2.5 evaluation is finished"



