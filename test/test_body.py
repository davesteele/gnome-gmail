#!/usr/bin/python2 -tt

import nose
import re
from six.moves import urllib


import sys
sys.path.append( '.' )

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
#    ("a&b", "a&amp;b"),


    ("a\nb", "a<br>\nb"),
    ("a\nb\nc", "a<br>\nb<br>\nc"),
 ]

def get_gmapi(input):
        gm = gnomegmail.GMailURL(input, "me", False)
        mail_dict = gm.mail_dict

        gmapi = gnomegmail.GMailAPI(mail_dict)

        return gmapi

def check_body2html(input, output):
        input = baseMailtoURL + input

        gmapi = get_gmapi(input)

        html_body = gmapi.body2html()

        nose.tools.assert_in(output, html_body)

def check_needs_api(mailto, result):

        gmapi = get_gmapi(mailto)

        nose.tools.assert_true(gmapi.needs_api() is result)

def test_urlgen():
    for (sin, sout) in testCaseStrings:
        yield(check_needs_api, baseMailtoURL + sin, True)
        if not '&' in sin and not '#' in sin:
            yield(check_body2html, sin, sout)
        yield(check_body2html, urllib.parse.quote(sin), sout)

def test_null_needs_api():
        check_needs_api("mailto:joe", False)
        check_needs_api("mailto:joe?subject=hi", False)

def test_body_needs_api():
        check_needs_api("mailto:joe?body=%20", True)

def test_attach_needs_api():
        check_needs_api("mailto:joe?attach=file", True)
        check_needs_api("mailto:joe?attachment=file", True)





