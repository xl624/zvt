# -*- coding: utf-8 -*-
from logging.handlers import RotatingFileHandler

import pandas as pd

from zvdata.contract import *
from zvt.settings import DATA_SAMPLE_ZIP_PATH, ZVT_TEST_HOME, ZVT_HOME


def init_log(file_name='zvt.log', log_dir=None):
    if not log_dir:
        log_dir = zvt_env['log_path']

    root_logger = logging.getLogger()

    # reset the handlers
    root_logger.handlers = []

    root_logger.setLevel(logging.INFO)

    file_name = os.path.join(log_dir, file_name)

    fh = RotatingFileHandler(file_name, maxBytes=524288000, backupCount=10)

    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(levelname)s  %(threadName)s  %(asctime)s  %(name)s:%(filename)s:%(lineno)s  %(funcName)s  %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    root_logger.addHandler(fh)
    root_logger.addHandler(ch)


pd.set_option('expand_frame_repr', False)
pd.set_option('mode.chained_assignment', 'raise')

zvt_env = {}


def init_env(zvt_home: str,
             jq_username: str = os.environ.get('JQ_USERNAME'),
             jq_password: str = os.environ.get('JQ_PASSWORD')) -> None:
    """

    :param zvt_home: home path for zvt
    :param jq_username: joinquant username
    :param jq_password: joinquant password
    """
    data_path = os.path.join(zvt_home, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    init_data_env(data_path=data_path, domain_module='zvt.domain')

    zvt_env['data_path'] = data_path
    zvt_env['domain_module'] = 'zvt.domain'

    # path for storing ui results
    zvt_env['ui_path'] = os.path.join(zvt_home, 'ui')
    if not os.path.exists(zvt_env['ui_path']):
        os.makedirs(zvt_env['ui_path'])

    # path for storing logs
    zvt_env['log_path'] = os.path.join(zvt_home, 'logs')
    if not os.path.exists(zvt_env['log_path']):
        os.makedirs(zvt_env['log_path'])

    # setting joinquant account
    zvt_env['jq_username'] = jq_username
    zvt_env['jq_password'] = jq_password

    init_log()

    from zvt.domain import init_schema

    init_schema()


if os.getenv('TESTING_ZVT'):
    init_env(zvt_home=ZVT_TEST_HOME)
else:
    init_env(zvt_home=ZVT_HOME)

    if not zvt_env.get('data_path'):
        print('please use init_env to set zvt data path at first')
