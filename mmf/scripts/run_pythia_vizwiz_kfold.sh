mmf_run config=mmf_configs/pythia_clip_kfold_vizwiz/defaults.yaml \
	model=pythia \
	dataset=vqa2 \
	run_type=train \
	training.batch_size=16 \
    	training.log_interval=100 \
	training.checkpoint_interval=1000 \
    	training.evaluation_interval=500
