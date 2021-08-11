import sys
import os
import argparse
from meteor_aggs_utils import setup_logger
from meteor_aggs import final_aggregations

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', action='store', type=str, dest='bucket')
    parser.add_argument('--logdir', action='store', type=str, dest='logdir')
    args = parser.parse_args()

    bucket = args.bucket if args.bucket else 'majorly-meteoric'
    logdir = args.logdir if args.logdir else os.path.join(os.getcwd(), 'tmp', 'logs')

    logger = setup_logger(logdir)

    logger.debug(f'{sys.argv[0]} starting up, arguments: Bucket = {bucket}, logdir = {logdir}.')

    avg_mass, max_years = final_aggregations(bucket, logger)
    
    avg_string = 'Average meteorite mass is ' + avg_mass + '.'
    logger.debug(avg_string)
    print(avg_string)

    max_string = 'The year(s) with the highest meteorite counts are ' + max_years + '.'
    logger.debug(max_string)
    print(max_string)