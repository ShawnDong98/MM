import pandas as pd
import ast
import json
import base64
import numpy as np
np.set_printoptions(suppress=True, precision=4)
from os.path import join as pjoin
from maskrcnn_benchmark.structures.tsv_file_ops import tsv_reader, tsv_writer
import yaml

# Output of test_sg_net.py from scene_graph_benchmark
# predictions.tsv -> img_id, features (dict)

# Input for run_retreival.py
# predictions.tsv (lets rename to labels.tsv to avoid confusion) -> img_id, label (dict)
# features.tsv -> img_id, num_boxes, base64encoding
# image_id2idx.json -> cap_id (for us = img_id) to image idx (row no in features.tsv) mapping 

def generate_additional_features(rect, h, w):
    mask = np.array([w, h, w, h], dtype=np.float32)
    rect = np.clip(rect / mask, 0, 1)
    res = np.hstack((rect, [rect[3]-rect[1], rect[2]-rect[0]]))
    return res.astype(np.float32)

def generate_features(x):
    idx, objects = x[0], x[1]['objects']
    num_boxes = len(objects)
    height, width = hw_df.loc[idx,1][0]['height'], hw_df.loc[idx,1][0]['width']
    features_arr = []
    for i in range(num_boxes):
        features = np.frombuffer(base64.b64decode(objects[i]['feature']), np.float32)
        pos_feat = generate_additional_features(objects[i]['rect'], height, width)
        x = np.hstack((features, pos_feat))
        features_arr.append(x.astype(np.float32))
    features = np.vstack(tuple(features_arr))
    features = base64.b64encode(features).decode("utf-8")
    return features

def generate_num_boxes(x):
    objects = x[1]['objects']
    return len(objects)

def generate_labels(x):
    idx, objects = x[0], x[1]['objects']
    height, width = hw_df.loc[idx,1][0]['height'], hw_df.loc[idx,1][0]['width']
    subset_of_objects = [{'class': obj['class'], 'rect': obj['rect']} for obj in objects] 
    results = {'image_h': height, 'image_w': width, 'objects': subset_of_objects}
    return results

if __name__ == '__main__':
    data_path = './VizWiz/test'
    output_path = './VizWiz/test_output/'
    image_id2idxfile = pjoin(output_path, 'image_id2idx.json')

    hw_tsv = pjoin(data_path, 'test.hw.tsv')
    hw_df = pd.read_csv(hw_tsv, sep='\t', header=None, converters={1:ast.literal_eval}, index_col=0)

    pred_tsv = pjoin(output_path, 'predictions.tsv')
    df = pd.read_csv(pred_tsv, sep='\t', header = None, converters={1:json.loads})

    df['feature'] = df.apply(generate_features, axis=1)
    df['num_boxes'] = df.apply(generate_num_boxes, axis=1)
    df['label'] = df.apply(generate_labels, axis=1)
    df['idx'] = np.arange(len(df))

    df['feature'] = df['feature'].apply(json.dumps)
    df['num_boxes'] = df['num_boxes'].apply(json.dumps)
    df['label'] = df['label'].apply(json.dumps)

    LABEL_FILE = pjoin(output_path,'labels.tsv')
    FEATURE_FILE = pjoin(output_path,'features.tsv')
    
    tsv_writer(df[[0, 'label']].values.tolist(), LABEL_FILE)
    tsv_writer(df[[0, 'num_boxes', 'feature']].values.tolist(), FEATURE_FILE)

    image_id2idx = dict(zip(df['idx'], df[0]))
    with open(image_id2idxfile, 'w') as wf:
        json.dump(image_id2idx, wf)
