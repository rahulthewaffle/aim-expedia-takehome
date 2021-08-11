import boto3
import pandas as pd
import sys
import os
import logging
import argparse

def setup_logger(logdir, env):
    os.makedirs(logdir, exist_ok=True)

    abp = os.path.abspath(__file__)
    log_name = os.path.basename(abp)[:-3] + '_' + str(os.getpid()) + env + '.log'
    log_path = os.path.join(logdir, log_name)
    if os.path.exists(log_path):
        os.remove(log_path)

    if env == 'DEV':
        log_level = logging.DEBUG
    elif env == 'PROD':
        log_level = logging.INFO
    else:
    	raise new ValueError("Invalid environment value, please provide either DEV or PROD.")

    logging.basicConfig(filename=log_path,
                        filemode='w',
                        format='%(asctime)s|%(levelname)s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=log_level)

if __name__ == '__main__':
	logdir = os.path.join(os.getcwd(), 'tmp', 'logs')

    parser = argparse.ArgumentParser()
    parser.add_argument('--s3-bucket', action='store', type=str, dest='s3bucket')
    parser.add_argument('--env', action='store', type=str, dest='env')
    parser.add_argument('--logdir', action='store', type=str, dest='logdir')
    cmd_line_arg = parser.parse_args()

    
	pass
