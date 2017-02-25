# -*- coding: utf-8 -*-

import base64
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


def b64grep(str, text):
    try:
        b64tst = base64.b64encode(str.encode()) in text.encode()
    except UnicodeDecodeError:
        b64tst = False

    return b64tst or str in text


def spy_decorator(method_to_decorate):
    msgtxt = []
    def wrapper(self, *args, **kwargs):
        returnvalue = method_to_decorate(self, *args, **kwargs)
        msgtxt.append(self.message_text)
        return returnvalue
    wrapper.msgtxt = msgtxt
    return wrapper


@pytest.mark.parametrize('body', ("", "hi yä"))
@pytest.mark.parametrize('attach', ("", "/etc/resolv.conf"))
@pytest.mark.parametrize('cc', ("", 'cc@example.com', "cc@exämple.com" ))
# TODO - oddly, unicode in Bcc doesn't work, while cc works
@pytest.mark.parametrize('bcc', ("", 'bcc@example.com') )#,"bcc@exämple.com" ))
@pytest.mark.parametrize('su', ("", 'subject'))
@patch(
    'gnomegmail.getGoogleFromAddress',
    Mock(return_value="me@example.com"),
)
@patch('gnomegmail.browser', Mock())
@patch('gnomegmail.GMailAPI.send_mail', Mock(return_value='1'))
def test_main(default_mailer_fxt, config_fxt, keyring_fxt,
              notify_fxt, web_fxt, oauth_fxt,
              monkeypatch, su, bcc, cc, attach, body):

    rfc822txt = None

    args = ['body', 'cc', 'bcc', 'su', 'attach']
    argvals = locals()
    queries = ['='.join((x, argvals[x])) for x in args if argvals[x]]

    mailto = "mailto:joe@example.com"
    if queries:
        mailto += "?" + '&'.join(queries)

    monkeypatch.setattr('gnomegmail.sys.argv', ['prog', mailto])

    myform = spy_decorator(gnomegmail.GMailAPI.form_message)
    with patch.object(gnomegmail.GMailAPI, 'form_message', myform):
        gnomegmail.main()
        rfc822txt = gnomegmail.GMailAPI.form_message.msgtxt[0]

    assert gnomegmail.GMailAPI.send_mail.called

    assert "To: joe@example.com" in rfc822txt

    if body:
        assert b64grep(body, rfc822txt)

    if su:
        assert "Subject: " + su in rfc822txt
    elif attach:
        assert "Subject: Sending " in rfc822txt
    else:
        assert "Subject:" not in rfc822txt

    if attach:
        assert "Content-Disposition: attachment; " in rfc822txt
    else:
        assert "Content-Disposition: attachment; " not in rfc822txt

    if cc:
        assert b64grep(cc, rfc822txt)
    else:
        assert "Cc: " not in rfc822txt

    if bcc:
        assert b64grep(bcc, rfc822txt)
    else:
        assert "Bcc: " not in rfc822txt
