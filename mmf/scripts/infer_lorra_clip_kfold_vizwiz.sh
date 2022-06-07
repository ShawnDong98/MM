mmf_predict config=mmf_configs/lorra_clip_kfold_vizwiz/defaults.yaml \
	model=lorra \
	dataset=vqa2 \
	run_type=test \
	checkpoint.resume_file=save_lorra_fold0/best.ckpt
