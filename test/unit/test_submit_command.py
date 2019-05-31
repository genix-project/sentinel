import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))


@pytest.fixture
def superblock():
    from models import Superblock
    # NOTE: no governance_object_id is set
    sbobj = Superblock(
        event_block_height=62500,
        payment_addresses='gbQGzgjz9Wd2riuqYeD9XR9qLUdz9gtraP|gNEFpDobUEwM7ohmArQVTngKXWAoxBuzaA',
        payment_amounts='5|3',
        proposal_hashes='e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
    )

    return sbobj


def test_submit_command(superblock):
    cmd = superblock.get_submit_command()

    assert re.match(r'^gobject$', cmd[0]) is not None
    assert re.match(r'^submit$', cmd[1]) is not None
    assert re.match(r'^[\da-f]+$', cmd[2]) is not None
    assert re.match(r'^[\da-f]+$', cmd[3]) is not None
    assert re.match(r'^[\d]+$', cmd[4]) is not None
    assert re.match(r'^[\w-]+$', cmd[5]) is not None

    submit_time = cmd[4]

    gobject_command = ['gobject', 'submit', '0', '1', submit_time, '7b22656e645f65706f6368223a313539313536323036372c226e616d65223a2274657374222c227061796d656e745f61646472657373223a22676d5554504e42664539346961345274703755697455554e79374259775365393975222c227061796d656e745f616d6f756e74223a313230302c2273746172745f65706f6368223a313538383938363538372c2274797065223a312c2275726c223a2268747470733a2f2f746573742e74657374227d']
assert cmd == gobject_command