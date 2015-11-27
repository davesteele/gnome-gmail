
import gnomegmail


def test_browser():
    browser = gnomegmail.browser()

    assert browser.name
