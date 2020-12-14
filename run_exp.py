import os
import sys
import torch
import logging
import traceback
import numpy as np
from pprint import pprint

from run import *
from utils.logger import setup_logging
from utils.arg_helper import parse_arguments, get_config
torch.set_printoptions(profile='full')
torch.set_printoptions(precision=4,linewidth=200)
np.set_printoptions(precision=4,linewidth=150)

def main():
  args = parse_arguments()
  config = get_config(args.config_file)
  # config = get_config("./config/train.yaml")
  np.random.seed(config.seed)
  torch.manual_seed(config.seed)
  torch.cuda.manual_seed_all(config.seed)
  config.use_gpu = config.use_gpu and torch.cuda.is_available()

  # log info
  log_file = os.path.join(config.save_dir,
                          "log_exp_{}.txt".format(config.run_id))
  logger = setup_logging(args.log_level, log_file)
  logger.info("Writing log file to {}".format(log_file))
  logger.info("Exp instance id = {}".format(config.run_id))
  logger.info("Exp comment = {}".format(args.comment))
  logger.info("Config =")
  print(">" * 80)
  pprint(config)
  print("<" * 80)

  # Run the experiment
  try:
    runner = eval(config.runner)(config)
    if args.test:
      runner.test()
    elif args.val:
      runner.validate()
    elif args.opt:
      runner.mll_opt()
    else:
      runner.train()

  except:
    logger.error(traceback.format_exc())

  sys.exit(0)


if __name__ == "__main__":
  main()