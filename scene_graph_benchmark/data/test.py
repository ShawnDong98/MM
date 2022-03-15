import torch
from maskrcnn_benchmark.structures.bounding_box import BoxList

pred_pt = torch.load("../output/X152C5_test/inference/vinvl_vg_x152c4/predictions.pth")
print(type(pred_pt))
print(pred_pt[1].fields())
print(dir(BoxList))
