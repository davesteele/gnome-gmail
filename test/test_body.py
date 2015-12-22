#!/usr/bin/python2 -tt

import nose
import pytest
from six.moves import urllib

import gnomegmail


baseMailtoURL = "mailto:joe?body="

testCaseStrings = [
    ("x", "x"),
    ("x", "<html>"),
    ("x", "</html>"),
    ("x", "<head>"),
    ("x", "</head>"),
    ("x", "<body>"),
    ("x", "</body>"),

    ("http://example.com",
        "<a href=\"http://example.com\">http://example.com</a>"),
    ("http://example.com#1",
        "<a href=\"http://example.com#1\">http://example.com#1</a>"),
    # flake8: noqa
    ("http://example.com?a=b&c=d",
        "<a href=\"http://example.com?a=b&c=d\">http://example.com?a=b&c=d</a>"),
    ("(http://example.com/)",
        "<a href=\"http://example.com/\">http://example.com/</a>)"),
    ("(http://example.com/a)",
        "<a href=\"http://example.com/a\">http://example.com/a</a>)"),

    ("a http://example.com b",
        "<a href=\"http://example.com\">http://example.com</a>"),
    ("\"http://example.com\"",
        "<a href=\"http://example.com\">http://example.com</a>"),
    ("\'http://example.com\'",
        "<a href=\"http://example.com\">http://example.com</a>"),
    ("http://example.com.",
        "<a href=\"http://example.com\">http://example.com</a>."),
    ("http://example.com,",
        "<a href=\"http://example.com\">http://example.com</a>,"),
    ("(http://example.com)",
        "<a href=\"http://example.com\">http://example.com</a>)"),

    ("http://aa.com http://example.com",
        "<a href=\"http://example.com\">http://example.com</a>"),
    ("http://aa.com http://example.com",
        "<a href=\"http://aa.com\">http://aa.com</a>"),

    ("https://example.com",
        "<a href=\"https://example.com\">https://example.com</a>"),
    ("ftp://example.com",
        "<a href=\"ftp://example.com\">ftp://example.com</a>"),

    ("mailto:joe@example.com",
        "<a href=\"mailto:joe@example.com\">mailto:joe@example.com</a>"),

    ("a b", "a b"),
    ("a  b", "a&nbsp; b"),
    ("a   b", "a&nbsp;&nbsp; b"),
    ("a    b", "a&nbsp;&nbsp;&nbsp; b"),
    ("a\tb", "a&emsp;b"),

    ("a>b", "a&gt;b"),
    ("a<b", "a&lt;b"),

    ("a\nb", "a<br>\nb"),
    ("a\nb\nc", "a<br>\nb<br>\nc"),
 ]


def get_gmapi(input):
        gm = gnomegmail.GMailURL(input, "me")
        mail_dict = gm.mail_dict

        gmapi = gnomegmail.GMailAPI(mail_dict)

        return gmapi


def check_needs_api(mailto, result):

        gmapi = get_gmapi(mailto)

        nose.tools.assert_true(gmapi.needs_api() is result)


@pytest.mark.parametrize("body, result", testCaseStrings)
def test_needs_api_yes(body, result):
    gmapi = get_gmapi(baseMailtoURL + body)

    assert gmapi.needs_api() is True


@pytest.mark.parametrize("body, result", testCaseStrings)
@pytest.mark.parametrize("encbody", (False, True))
def test_body2html(encbody, body, result):

    if encbody:
        body = urllib.parse.quote(body)
    elif '&' in body or '#' in body:
        pytest.skip("Don't test unencoded bodies with URL special chars")

    gmapi = get_gmapi(baseMailtoURL + body)

    html_body = gmapi.body2html()

    assert result in html_body


@pytest.mark.parametrize("mailto, needs_api", (
    ("mailto:joe", False),
    ("mailto:joe?subject=hi", False),
    ("mailto:joe?body=%20", True),
    ("mailto:joe?attach=file", True),
    ("mailto:joe?attachment=file", True),
))
def test_needs_api(mailto, needs_api):
    gmapi = get_gmapi(mailto)

    assert gmapi.needs_api() == needs_api
