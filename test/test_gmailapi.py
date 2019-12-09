# -*- coding: utf-8 -*-

import pytest

from six.moves import urllib

import viagee

base_mail_dict = {
    'to': "to@exämple.com",
    'from': "from@exämple.com",
}


@pytest.mark.parametrize("body", (
    "",
    "simple body",
    "body with http://example.com/link",
))
@pytest.mark.parametrize("attach", (False, True))
@pytest.mark.parametrize("cc", ([], ["cc@example.com"]))
@pytest.mark.parametrize("bcc", ([], ["bcc@example.com"]))
@pytest.mark.parametrize("su", ([], ["subject"]))
def test_gmailapi(web_fxt, tmpfile, su, bcc, cc, attach, body):
    mail_dict = base_mail_dict.copy()

    if body:
        mail_dict['body'] = body

    if attach:
        mail_dict['attach'] = [urllib.request.pathname2url(tmpfile)]

    if cc:
        mail_dict['cc'] = cc

    if bcc:
        mail_dict['bcc'] = bcc

    if su:
        mail_dict['su'] = su

    gmailapi = viagee.GMailAPI(mail_dict)
    gmailapi.form_message()
    id = gmailapi.upload_mail('user', 'atoken')

    assert id == '1'
