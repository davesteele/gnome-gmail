
from mock import patch, Mock
import os
import pytest

import viagee

@pytest.mark.skipif(not os.path.exists("/usr/bin/xdg-settings") or
                    not os.environ.get("DISPLAY"),
                    reason="Not in a true GUI environment")
@patch('viagee.config')
def test_browser(config):
    get_str = Mock(return_value='')
    config.get_str = get_str

    browser = viagee.browser()

    assert browser.name
