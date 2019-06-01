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
        payment_addresses='qfvtZk8GYfeM37gwZiHPZgVJGnwREsXkoT|qaSQZnZyVz5CEwpFVJkAdByf6tKfu9ejTo',
        payment_amounts='50000|30000',
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

    gobject_command = ['gobject', 'submit', '0', '1', submit_time, '5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2036323530302c20227061796d656e745f616464726573736573223a2022716676745a6b38475966654d333767775a6948505a67564a476e77524573586b6f547c716153515a6e5a79567a354345777046564a6b416442796636744b667539656a546f222c20227061796d656e745f616d6f756e7473223a202235303030307c3330303030222c202270726f706f73616c5f686173686573223a2022653861303035373931346132653139363461653861393435633437323334393163616165323037376139306130306132616162656532326234303038316138377c64316365373335323764376364366632323138663863613839333939306263376435633662393333343739316365373937336266613232663135356638323665222c202274797065223a20327d5d5d']
    assert cmd == gobject_command
