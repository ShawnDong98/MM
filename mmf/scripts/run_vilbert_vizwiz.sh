mmf_run config=mmf_configs/vilbert_vizwiz/defaults.yaml \
	model=vilbert \
	dataset=vqa2 \
	run_type=train \
	training.batch_size=16 \
    	training.log_interval=100 \
	training.checkpoint_interval=1000 \
    	training.evaluation_interval=1000 \
	checkpoint.resume_pretrained=True \
	checkpoint.resume_zoo=vilbert.finetuned.vizwiz \
	training.find_unused_parameters=True