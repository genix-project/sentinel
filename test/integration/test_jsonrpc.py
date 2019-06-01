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
    genesis_hash = u'00000354655ff039a51273fe61d3b493bd2897fe6c16f732dbc4ae19f04b789e'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000da63bd9478b655ef6bf1bf76cd9af05202ab68643f9091e049b2b5280ed'

    creds = GenixConfig.get_rpc_creds(config_text, network)
    genixd = GenixDaemon(**creds)
    assert genixd.rpc_command is not None

    assert hasattr(genixd, 'rpc_connection')

    # Genix testnet block 0 hash == 00000da63bd9478b655ef6bf1bf76cd9af05202ab68643f9091e049b2b5280ed
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
