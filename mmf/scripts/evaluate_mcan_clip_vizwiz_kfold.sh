mmf_run config=mmf_configs/mcan_clip_kfold_vizwiz/defaults.yaml \
	model=movie_mcan \
	dataset=vqa2 \
	run_type=val \
	checkpoint.resume_file=save_mcan_clip_fold4/best.ckpt
