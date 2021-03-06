# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under a Microsoft Research License.

from __future__ import absolute_import

import os
import procdata
import numpy as np
from src.run_xval_icml import run_on_split, create_parser
from src.xval import XvalMerge
from src.utils import Trainer, load_config_file

def main():
    parser = create_parser(False)
    args = parser.parse_args()
    spec = load_config_file(args.yaml)  # spec is a dict of dicts of dicts
    data_settings = spec["data"]
    trainer = Trainer(args, args.yaml, add_timestamp=True)
    data = procdata.ProcData(data_settings)
    
    xval_merge = XvalMerge(args, data_settings, trainer)
    for split_idx in range(1, args.folds + 1):
        print("---------------------------------------------------------------------------")
        print("    FOLD %d of %d"%(split_idx, args.folds))
        print("---------------------------------------------------------------------------")
        data_pair, val_results = run_on_split(args, split_idx, xval_merge.trainer)
        xval_merge.add(split_idx, data_pair, val_results)
    xval_merge.finalize()
    xval_merge.save(xval_merge.trainer.tb_log_dir)
    if args.no_figures is False:
        xval_merge.make_writer(xval_merge.trainer.tb_log_dir)
        xval_merge.prepare_treatment()
        xval_merge.make_images(data)
        xval_merge.close_writer()
    #xval_merge.load(xval_merge.trainer.tb_log_dir)
    print('Completed')

if __name__ == "__main__":
    main()