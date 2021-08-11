import os
import logging

def setup_logger(logdir):
    os.makedirs(logdir, exist_ok=True)

    abp = os.path.abspath(__file__)
    log_name = os.path.basename(abp)[:-3] + '_' + str(os.getpid()) + '.log'
    log_path = os.path.join(logdir, log_name)
    if os.path.exists(log_path):
        os.remove(log_path)

    logging.basicConfig(filename=log_path,
                        filemode='w',
                        format='%(asctime)s|%(levelname)s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    return logging.getLogger()