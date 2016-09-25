# -*- coding: utf-8 -*-

import pytest
from mock import patch, Mock

import gnomegmail


class MyTestException(Exception):
    pass


@patch('gnomegmail.sys.exit', side_effect=MyTestException)
def test_main_quick(default_mailer_fxt, config_fxt, monkeypatch):
    monkeypatch.setattr('gnomegmail.sys.argv', ['prog', '-q'])

    with pytest.raises(MyTestException):
        gnomegmail.main()

    assert gnomegmail.sys.exit.calledwith(0)


@pytest.mark.parametrize('body', ("", "hi yä"))
@pytest.mark.parametrize('attach', ("", "/etc/resolv.conf"))
@pytest.mark.parametrize('cc', ("", 'cc@example.com'))
@pytest.mark.parametrize('bcc', ("", 'bcc@example.com'))
@pytest.mark.parametrize('su', ("", 'subject'))
@patch(
    'gnomegmail.getGoogleFromAddress',
    Mock(return_value="me@example.com"),
)
@patch('gnomegmail.browser', Mock())
def test_main(default_mailer_fxt, config_fxt, keyring_fxt,
              notify_fxt, web_fxt, oauth_fxt,
              monkeypatch, su, bcc, cc, attach, body):

    args = ['body', 'cc', 'bcc', 'su', 'attach']
    argvals = locals()
    queries = ['='.join((x, argvals[x])) for x in args if argvals[x]]

    mailto = "mailto:joe@example.com"
    if queries:
        mailto += "?" + '&'.join(queries)

    monkeypatch.setattr('gnomegmail.sys.argv', ['prog', mailto])

    gnomegmail.main()
