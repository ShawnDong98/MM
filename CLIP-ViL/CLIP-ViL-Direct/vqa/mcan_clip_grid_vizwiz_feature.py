import argparse
import os
import torch
import tqdm
from fvcore.common.file_io import PathManager

from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.engine import default_setup
from detectron2.evaluation import inference_context
from detectron2.modeling import build_model
import numpy as np
from clip.clip import load
import torch.nn as nn
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize

from grid_feats import (
    add_attribute_config,
    build_detection_test_loader_with_attributes,
)
from timm.models.vision_transformer import resize_pos_embed

# A simple mapper from object detection dataset to VQA dataset names
dataset_to_folder_mapper = {}
dataset_to_folder_mapper['vizwiz_train'] = 'train'
dataset_to_folder_mapper['vizwiz_val'] = 'val'
dataset_to_folder_mapper['vizwiz_train_val'] = 'train_val'
dataset_to_folder_mapper['vizwiz_test'] = 'test'


def extract_grid_feature_argument_parser():
    parser = argparse.ArgumentParser(description="Grid feature extraction")
    parser.add_argument("--config-file", default="configs/R-50-grid.yaml", metavar="FILE", help="path to config file")
    parser.add_argument("--dataset", help="name of the dataset", default="vizwiz_train_val")
    parser.add_argument('--model_type', default='RN50x4', type=str, help='RN50, RN101, RN50x4, ViT-B/32, vit_base_patch32_224_in21k')

    # parser.add_argument(
    #     "opts",
    #     help="Modify config options using the command-line",
    #     default=None,
    #     nargs=argparse.REMAINDER,
    # )
    return parser


def extract_grid_feature_on_dataset(model, data_loader, dump_folder):
    for idx, inputs in enumerate(tqdm.tqdm(data_loader)):
        with torch.no_grad():
            image_id = inputs[0]['image_id']
            file_name = '%d.pth' % image_id
            # compute features
            images = model.preprocess_image(inputs)
            features = model.backbone(images.tensor)
            outputs = model.roi_heads.get_conv5_features(features)
            # modify the filename
            file_name = inputs[0]['file_name'].split("/")[-1].replace("jpg", "npy")
            outputs = outputs.permute(0, 2, 3, 1) 
            exit()
            with PathManager.open(os.path.join(dump_folder, file_name), "wb") as f:
                np.save(f, outputs.cpu().numpy())

                
                
def do_feature_extraction(cfg, model, dataset_name, args):
    with inference_context(model):
        dump_folder = os.path.join(cfg.OUTPUT_DIR, "features", dataset_to_folder_mapper[dataset_name])
        PathManager.mkdirs(dump_folder)
        data_loader = build_detection_test_loader_with_attributes(cfg, dataset_name, model_type='clip')
        extract_clip_feature_on_dataset(model, data_loader, dump_folder, args)
        
        
def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    add_attribute_config(cfg)
    cfg.merge_from_file(args.config_file)
    # cfg.merge_from_list(args.opts)
    # force the final residual block to have dilations 1
    cfg.MODEL.RESNETS.RES5_DILATION = 1
    cfg.freeze()
    default_setup(cfg, args)
    return cfg


def extract_clip_feature_on_dataset(model, data_loader, dump_folder, args):
    model_type = args.model_type.split("-")[0]
    mean = torch.Tensor([0.48145466, 0.4578275, 0.40821073]).to("cuda").reshape(3, 1, 1)
    std = torch.Tensor([0.26862954, 0.26130258, 0.27577711]).to("cuda").reshape(3, 1, 1)
    dump_folder = f"clip/{model_type}/" + dump_folder.split("/")[-1]

    if args.model_type == "ViT-B/32":
        num_patches = 558 #600 * 1000 // 32 // 32
        print(num_patches)
        pos_embed = nn.Parameter(torch.zeros(num_patches + 1, 768,  device='cuda'),)
        resized_pos_embed_weight = resize_pos_embed(model.visual.attnpool.positional_embedding.unsqueeze(0), pos_embed)
        pos_embed = nn.Parameter(resized_pos_embed_weight.squeeze(0),)
        model.visual.positional_embedding = pos_embed
        print(model.visual.positional_embedding.device)
        # pass
    dump_folder = "/home/datasets/VizWiz/grid-feats-vqa/" + dump_folder
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)
    for idx, inputs in enumerate(tqdm.tqdm(data_loader)):
        with torch.no_grad():
            image_id = inputs[0]['image_id']
            # file_name = '%d.pth' % image_id
            file_name = inputs[0]['file_name'].split('/')[-1][:-4] + '.pth'
            # compute features
            image = inputs[0]['image'].to("cuda").float() / 255.0
            
            image = (image - mean) / std
            image = image.unsqueeze(0)
  
            outputs = model.encode_image(image)
            if "RN" in args.model_type:
                outputs = outputs.permute(0, 2, 3, 1)
            else:
                outputs = outputs[:, :, :].reshape(1, 13, 43, 768)
            # break
            with PathManager.open(os.path.join(dump_folder, file_name), "wb") as f:
                # save as CPU tensors
                torch.save(outputs.cpu(), f)
                
                
def main(args):
    cfg = setup(args)
    model, transform = load(args.model_type, jit=False)
  
    do_feature_extraction(cfg, model, args.dataset, args)
    
args = extract_grid_feature_argument_parser().parse_args()
print("Command Line Args:", args)
main(args)
