python3 tools/demo/demo_image.py --config_file sgg_configs/vgattr/vinvl_x152c4.yaml \
				 --img_file demo/woman_fish.jpg \
				 --save_file output/woman_fish_x152c4.obj.jpg \
				 MODEL.WEIGHT models/vinvl/vinvl_vg_x152c4.pth \
				 MODEL.ROI_HEADS.NMS_FILTER 1 \
				 MODEL.ROI_HEADS.SCORE_THRESH 0.2 \
				 TEST.IGNORE_BOX_REGRESSION False

