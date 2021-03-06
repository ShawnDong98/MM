python3 oscar/run_vqa.py -j 4 \
	--img_feature_dim 2054 \
	--max_img_seq_length 50 \
	--data_label_type mask \
	--img_feature_type faster_r-cnn \
	--data_dir data/VizWiz \
	--model_type bert \
    	--model_name_or_path checkpoints/vqa/large/checkpoint-2000000 \
	--task_name vqa_text \
	--do_train \
	--do_lower_case \
	--max_seq_length 128 \
	--per_gpu_eval_batch_size 128 \
	--per_gpu_train_batch_size 16 \
	--learning_rate 2e-05 \
	--num_train_epochs 25 \
   	--output_dir results_large_20220216 \
	--label_file data/VizWiz/trainval_ans2label.pkl \
	--label2ans_file data/VizWiz/trainval_label2ans.pkl \
	--save_epoch 1 \
	--seed 88 \
	--evaluate_during_training \
	--logging_steps 4000 \
	--drop_out 0.3 \
	--weight_decay 0.05 \
	--warmup_steps 0 \
	--loss_type bce \
	--img_feat_format pt \
    	--classifier linear \
	--cls_hidden_scale 3 \
	--txt_data_dir data/VizWiz
