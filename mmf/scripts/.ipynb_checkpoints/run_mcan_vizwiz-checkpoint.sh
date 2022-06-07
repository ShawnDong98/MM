mmf_run config=mmf_configs/mcan_vizwiz/defaults.yaml \
	model=movie_mcan \
	dataset=vqa2 \
	run_type=train \
	training.batch_size=16 \
    	training.log_interval=100 \
	training.checkpoint_interval=1000 \
    	training.evaluation_interval=1000
