mmf_predict config=mmf_configs/mcan_clip_kfold_vizwiz/defaults.yaml \
	model=movie_mcan \
	dataset=vqa2 \
	run_type=test \
	checkpoint.resume_file=save_mcan_clip_fold1/best.ckpt
