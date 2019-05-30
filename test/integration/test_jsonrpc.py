import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from genixd import GenixDaemon
from genix_config import GenixConfig


def test_genixd():
    config_text = GenixConfig.slurp_config_file(config.genix_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000038977617c01646209e33e354174ef916df8284346b29aecfbc98fa43dd0'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000006874678aa53f78b7676ced0f443cd22ae8917199b5ec14d0b7b7df7b93d'

    creds = GenixConfig.get_rpc_creds(config_text, network)
    genixd = GenixDaemon(**creds)
    assert genixd.rpc_command is not None

    assert hasattr(genixd, 'rpc_connection')

    # Genix testnet block 0 hash == 000006874678aa53f78b7676ced0f443cd22ae8917199b5ec14d0b7b7df7b93d
    # test commands without arguments
    info = genixd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert genixd.rpc_command('getblockhash', 0) == genesis_hash
