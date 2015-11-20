
import pytest
from ggfixtures import *        # flake8: noqa

import gnomegmail


def test_oauth_get_code(oauth_fxt):
    oauth = gnomegmail.GMOauth()
    code = oauth.get_code('hint')
    assert code == "thecode"


def test_oauth_generate_tokens(oauth_fxt):
    oauth = gnomegmail.GMOauth()
    access, refresh = oauth.generate_tokens('login')


@pytest.mark.parametrize("access, refresh", (
        (None, None),
        (None, 'refresh'),
        ('access', 'refresh'),
    )
)
def test_oauth_access_iter(oauth_fxt, access, refresh):
    oauth = gnomegmail.GMOauth()
    for aout, rout in oauth.access_iter(access, refresh, 'login'):
        pass
