
import pytest
from mock import patch
from ggfixtures import *

import gnomegmail


class MyTestException(Exception):
    pass


@patch('gnomegmail.sys.exit', side_effect=MyTestException)
def test_main_quick(default_mailer_fxt, config_fxt, monkeypatch):
    monkeypatch.setattr('gnomegmail.sys.argv', ['prog', '-q'])

    with pytest.raises(MyTestException):
        gnomegmail.main()

    assert gnomegmail.sys.exit.calledwith(0)


@pytest.mark.parametrize('mailto', (
        "mailto:joe@example.com",
        "mailto:joe@example.com?body=hi",
    )
)
@patch(
    'gnomegmail.getGoogleFromAddress',
    Mock(return_value="me@example.com"),
)
@patch('gnomegmail.browser', Mock())
def test_main(default_mailer_fxt, config_fxt, keyring_fxt,
              notify_fxt, web_fxt, oauth_fxt,
              monkeypatch, mailto):
    monkeypatch.setattr('gnomegmail.sys.argv', ['prog', mailto])

    gnomegmail.main()
