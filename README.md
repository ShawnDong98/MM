# 提取特征

```
cd scene_graph_benchmark
```

创建 tsv

```
python3 tools/mini_tsv/tsv_create.py
```

提取特征

```
bash scripts/extract_features.sh
```

将特征转换为 Oscar 的输入

```
bash data/prepare_vinvl_input.py
```

# 