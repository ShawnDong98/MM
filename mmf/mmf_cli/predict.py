#!/usr/bin/env python3 -u
# Copyright (c) Facebook, Inc. and its affiliates.
import os
import sys

from mmf_cli.run import run
os.environ['CUDA_VISIBLE_DEVICES'] = "0"


def predict(opts=None):
    if opts is None:
        sys.argv.extend(["evaluation.predict=true"])
    else:
        opts.extend(["evaluation.predict=true"])

    run(predict=True)


if __name__ == "__main__":
    predict()
