
import gnomegmail
import pytest
import os

@pytest.mark.skipif(not os.path.exists("/usr/bin/xdg-settings"),
                    reason="Not in a true GUI environment")
def test_browser():
    browser = gnomegmail.browser()

    assert browser.name
