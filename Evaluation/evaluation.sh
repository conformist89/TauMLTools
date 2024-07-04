
# python evaluate_performance.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=cf155e681fda4432bb8f2c72670912a4 \
#        discriminator=DeepTau_v2p1 'path_to_input="/eos/user/o/olavoryk/roc_curve_files/{sample_alias}/*.root"' \
#        path_to_pred=null 'path_to_target="${path_to_mlflow}/${experiment_id}/e1f3ddb3c4c94128a34a7635c56322eb/artifacts/predictions/{sample_alias}/*_pred.h5"' \
#        vs_type=e dataset_alias=ggH_DY 


# python evaluate_performance.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=080f8be3b57545d3ab1bdddc1038c82c \
#        discriminator=DeepTau_v2p1 'path_to_input="/eos/user/o/olavoryk/roc_curve_files/{sample_alias}/*.root"' \
#        path_to_pred=null 'path_to_target="${path_to_mlflow}/${experiment_id}/e1f3ddb3c4c94128a34a7635c56322eb/artifacts/predictions/{sample_alias}/*_pred.h5"' \
#        vs_type=e dataset_alias=ggH_DY 

# discriminator either DeepTau_v2p1 or DeepTau_run3

echo "%%%%%%%%%%% Deep Tau 2.1 evaluation"

python evaluate_performance.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=4e14f6ee063443cb8b21b17694a4b839 \
       discriminator=DeepTau_v2p1 'path_to_input="/eos/user/o/olavoryk/roc_curve_files/{sample_alias}/*.root"' \
       path_to_pred=null 'path_to_target="${path_to_mlflow}/${experiment_id}/e1f3ddb3c4c94128a34a7635c56322eb/artifacts/predictions/{sample_alias}/*_pred.h5"' \
       vs_type=jet dataset_alias=ggH_WJets

echo "Deep Tau 2.1 evaluation is finished"

# echo "%%%%%%%%%%% Deep Tau 2.5 evaluation"

# python evaluate_performance.py path_to_mlflow=../Training/python/2018v1/mlruns experiment_id=4 run_id=85ea216dcd1b4c978b94e708a4fff411 \
#        discriminator=DeepTau_run3 'path_to_input="/eos/user/o/olavoryk/roc_curve_files/{sample_alias}/*.root"' \
#        path_to_pred=null 'path_to_target="${path_to_mlflow}/${experiment_id}/e1f3ddb3c4c94128a34a7635c56322eb/artifacts/predictions/{sample_alias}/*_pred.h5"' \
#        vs_type=jet dataset_alias=WToTauNu_M20_wjets_jets

# echo "Deep Tau 2.5 evaluation is finished"

# 0143479d108a4c118fef42c21636184a DT 2.1 // 7284229487034782ba2cf58d33e41961 DT 2.5 WToTauNu_M-20_v3 vs tt jets
# d27378003ff146b1a16b7d2f4090b32c DT 2.1 // 6aeec0ad3dd94f938744f99b7f405d90 DT 2.5 WToTauNu_M-20_v3 vs w jets
# 3664a0c81e43429bab18138309d17a05 DT 2.1 // 7b6d535b3d054540acb727c3f33d1a8f DT 2.5 WToTauNu_M-20_v3 vs DY e

# 7900ee5116664d75950537d662134438 // 990437b6990f45019c7f6b4e8eab351b WToTauNu_M-20_v3 vs tt jets
# 65eef74f9fe44499807978b51fbd9fbe // 85ea216dcd1b4c978b94e708a4fff411 WToTauNu_M-20_v3 vs wjets 


