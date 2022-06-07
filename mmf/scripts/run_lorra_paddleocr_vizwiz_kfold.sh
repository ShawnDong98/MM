mmf_run config=mmf_configs/lorra_clip_kfold_vizwiz/defaults.yaml \
	model=lorra \
	dataset=vqa2 \
	run_type=train \
    	training.log_interval=10 \
	training.checkpoint_interval=100 \
    	training.evaluation_interval=100
