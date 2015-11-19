
import pytest
from ggfixtures import *

import urllib

import gnomegmail

base_mail_dict = {
    'to': "to@example.com",
    'from': "from@example.com",

}


@pytest.mark.parametrize("body", (
        "",
        "simple body",
        "body with http://example.com/link",
    )
)
@pytest.mark.parametrize("attach", (False, True))
def test_gmailapi(web_fxt, tmpfile, attach, body):

    print tmpfile

    mail_dict = base_mail_dict.copy()

    if body:
        mail_dict['body'] = body

    if attach:
        mail_dict['attach'] = [urllib.pathname2url(tmpfile)]

    gmailapi = gnomegmail.GMailAPI(mail_dict)
    gmailapi.form_message()
    id = gmailapi.send_mail('user', 'atoken')

    assert id == '1'
