

from gi.repository import Gio
import webbrowser
import gnomegmail

def test_gio_set_default_mailer():
    gnomegmail.set_as_default_mailer()


def is_default_mailer():
    result = gnomegmail.is_default_mailer()
    assert result is True or result is False
