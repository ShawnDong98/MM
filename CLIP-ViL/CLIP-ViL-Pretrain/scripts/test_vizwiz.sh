bash scripts/finetune_vizwiz_noddp.bash 0,1 snap/vizwiz/test \
	--gradient_accumulation_steps 8 \
	--batchSize 8 \
	--lr 5e-5 \
	--loss_scale 500 \
	--warmup_ratio 0.05 \
	--report_step 400 \
	--use_separate_optimizer_for_visual \
	--sgd_lr 0.001 \
	--sgd_momentum 0.0 \
	--epoch 12 \
	--schedule 2 \
	--use_positional_embedding \
	--pos_num 25 \
	--clip_model_name RN50x4 \
	--load snap/vizwiz/vqa_clip_rn50x4/BEST \
	--test test

