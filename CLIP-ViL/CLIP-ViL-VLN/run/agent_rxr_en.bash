name=agent_rxr_en_maxinput160_ml04
flag="--attn soft --train listener 
      --featdropout 0.3
      --angleFeatSize 128
      --language en
      --maxInput 160
      --features img_features/ResNet-152-imagenet.tsv
      --feature_size 2048
      --feedback sample
      --mlWeight 0.4
      --subout max --dropout 0.5 --optim rms --lr 1e-4 --iters 150000 --maxAction 35"
mkdir -p snap/$name
CUDA_VISIBLE_DEVICES=$1 python rxr_src/train.py $flag --name $name 

# Try this with file logging:
# CUDA_VISIBLE_DEVICES=$1 unbuffer python r2r_src/train.py $flag --name $name | tee snap/$name/log
