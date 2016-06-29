
import gnomegmail
import pytest
import os
from mock import patch, Mock


@pytest.mark.skipif(not os.path.exists("/usr/bin/xdg-settings") or
                    not os.environ.get("DISPLAY"),
                    reason="Not in a true GUI environment")
@patch('gnomegmail.config')
def test_browser(config):
    get_str = Mock(return_value='')
    config.get_str = get_str

    browser = gnomegmail.browser()

    assert browser.name
