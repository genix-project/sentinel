import pytest
import sys
import os
import time
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../lib')))
import misc
import config
from models import GovernanceObject, Proposal, Superblock, Vote
import pprint


# clear DB tables before each execution
def setup():
    # clear tables first...
    Vote.delete().execute()
    Proposal.delete().execute()
    Superblock.delete().execute()
    GovernanceObject.delete().execute()


def teardown():
    pass


# list of proposal govobjs to import for testing
@pytest.fixture
def go_list_proposals():
    items = [
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 7,
         u'CollateralHash': u'acb67ec3f3566c9b94a26b70b36c1f74a010a37c0950c22d683cc50da324fdca',
         u'DataHex': u'5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20323132323532303430302c20226e616d65223a202253757065722d70697a7a61222c20227061796d656e745f61646472657373223a2022716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f54222c20227061796d656e745f616d6f756e74223a2032353030302e37352c202273746172745f65706f6368223a20313437343236313038362c202274797065223a20312c202275726c223a2022687474703a2f2f706163636f696e2e696f2f70697a7a61227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "Super-pizza", "payment_address": "qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT", "payment_amount": 25000.75, "start_epoch": 1474261086, "type": 1, "url": "http://genix.io/pizza"}]]',
         u'Hash': u'dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c',
         u'IsValidReason': u'',
         u'NoCount': 25,
         u'YesCount': 1025,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 29,
         u'CollateralHash': u'3efd23283aa98c2c33f80e4d9ed6f277d195b72547b6491f43280380f6aac810',
         u'DataHex': u'5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20323132323532303430302c20226e616d65223a20225461636f732d636f6e2d6361726e65222c20227061796d656e745f61646472657373223a2022716153515a6e5a79567a354345777046564a6b416442796636744b667539656a546f222c20227061796d656e745f616d6f756e74223a2033323030302e30312c202273746172745f65706f6368223a20313437343236313038362c202274797065223a20312c202275726c223a2022687474703a2f2f706163636f696e2e696f2f7461636f73227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "Tacos-con-carne", "payment_address": "qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo", "payment_amount": 32000.01, "start_epoch": 1474261086, "type": 1, "url": "http://genix.io/tacos"}]]',
         u'Hash': u'0523445762025b2e01a2cd34f1d10f4816cf26ee1796167e5b029901e5873630',
         u'IsValidReason': u'',
         u'NoCount': 56,
         u'YesCount': 1056,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


# list of superblock govobjs to import for testing
@pytest.fixture
def go_list_superblocks():
    items = [
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f547c716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f54222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e37353735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT", "payment_amounts": "25.75000000|25.7575000000", "type": 2}]]',
         u'Hash': u'667c4a53eb81ba14d02860fdb4779e830eb8e98306f9145f3789d347cbeb0721',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f547c716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f54222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'8f91ffb105739ec7d5b6c0b12000210fcfcc0837d3bb8ca6333ba93ab5fc0bdf',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f547c716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f54222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


@pytest.fixture
def superblock():
    sb = Superblock(
        event_block_height=62500,
        payment_addresses='qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo',
        payment_amounts='50000|30000',
        proposal_hashes='e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
    )
    return sb


def test_superblock_is_valid(superblock):
    from genixd import GenixDaemon
    genixd = GenixDaemon.from_genix_conf(config.genix_conf)

    orig = Superblock(**superblock.get_dict())  # make a copy

    # original as-is should be valid
    assert orig.is_valid() is True

    # mess with payment amounts
    superblock.payment_amounts = '7|yyzx'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7,|yzx'
    assert superblock.is_valid() is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True

    # mess with payment addresses
    superblock.payment_addresses = 'qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo|1234 Anywhere ST, Chicago, USA'
    assert superblock.is_valid() is False

    # single payment addr/amt is ok
    superblock.payment_addresses = 'qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is True

    # ensure number of payment addresses matches number of payments
    superblock.payment_addresses = 'qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo'
    superblock.payment_amounts = '37.00|23.24'
    assert superblock.is_valid() is False

    superblock.payment_addresses = 'qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo'
    superblock.payment_amounts = '37.00'
    assert superblock.is_valid() is False

    # ensure amounts greater than zero
    superblock.payment_addresses = 'qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo'
    superblock.payment_amounts = '-37.00'
    assert superblock.is_valid() is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True

    # mess with proposal hashes
    superblock.proposal_hashes = '7|yyzx'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '7,|yyzx'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '0|1'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '0000000000000000000000000000000000000000000000000000000000000000|1111111111111111111111111111111111111111111111111111111111111111'
    assert superblock.is_valid() is True

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True


def test_superblock_is_deletable(superblock):
    # now = misc.now()
    # assert superblock.is_deletable() is False

    # superblock.end_epoch = now - (86400 * 29)
    # assert superblock.is_deletable() is False

    # add a couple seconds for time variance
    # superblock.end_epoch = now - ((86400 * 30) + 2)
    # assert superblock.is_deletable() is True
    pass


def test_serialisable_fields():
    s1 = ['event_block_height', 'payment_addresses', 'payment_amounts', 'proposal_hashes']
    s2 = Superblock.serialisable_fields()

    s1.sort()
    s2.sort()

    assert s2 == s1


def test_deterministic_superblock_creation(go_list_proposals):
    import genixlib
    import misc
    from genixd import GenixDaemon
    genixd = GenixDaemon.from_genix_conf(config.genix_conf)
    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_genixd(genixd, item)

    max_budget = 600000
    prop_list = Proposal.approved_and_ranked(proposal_quorum=1, next_superblock_max_budget=max_budget)
    sb = genixlib.create_superblock(prop_list, 72000, budget_max=max_budget, sb_epoch_time=misc.now())

    assert sb.event_block_height == 72000
    assert sb.payment_addresses == 'qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo'
    assert sb.payment_amounts == '25000.75000000|32000.01000000'
    assert sb.proposal_hashes == 'dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c|0523445762025b2e01a2cd34f1d10f4816cf26ee1796167e5b029901e5873630'

    assert sb.hex_hash() == '9acf934c982b2f4411d22caf32a59dad5c2d301f9383af2e031cf49262379a49'


def test_deterministic_superblock_selection(go_list_superblocks):
    from genixd import GenixDaemon
    genixd = GenixDaemon.from_genix_conf(config.genix_conf)

    for item in go_list_superblocks:
        (go, subobj) = GovernanceObject.import_gobject_from_genixd(genixd, item)

    # highest hash wins if same -- so just order by hash
    sb = Superblock.find_highest_deterministic('14d34a90db210c7158ee9d80852f15bf37234b8d298ff95c78b86f1c787489f5')

    assert sb.object_hash == 'bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36'
