#!/usr/bin/python2 -tt

import nose
import re

import gnomegmail
import sys
sys.path.append('.')


baseGmailURL = "https://mail.google.com/mail/b/me?view=cm&tf=0&fs=1"

testCaseStrings = [
    ("mailto:joe",
     "https://mail.google.com/mail/b/me?view=cm&tf=0&fs=1&to=joe"),
    ("Mailto:joe", "*&to=joe"),
    ("joe", "*&to=joe"),
    ("joe@example.com", "*&to=joe%40example.com"),
    ("mailto:Joe", "*&to=Joe"),
    ("mailto:joe,sue", "*&to=joe%2Csue"),
    ("mailto:joe@example.com,sue@example.com",
     "*&to=joe%40example.com%2Csue%40example.com"),
    ("mailto:joe%40example.com", "*&to=joe%40example.com"),
    ("mailto:joe@example.com,%20sue@example.com",
     "*&to=joe%40example.com%2C+sue%40example.com"),
    ("mailto:joe@example.com, sue@example.com",
     "*&to=joe%40example.com%2C+sue%40example.com"),

    ("mailto:joe?subject=test%20email", "*&to=joe&su=test+email"),
    ("mailto:joe@example.com?subject=test%20email",
     "*&to=joe%40example.com&su=test+email"),
    ("mailto:joe?subject=test+email", "*&to=joe&su=test+email"),
    ("mailto:joe?subject=test email", "*&to=joe&su=test+email"),
    ("mailto:joe?SUBJECT=test email", "*&to=joe&su=test+email"),
    ("mailto:joe?Subject=test email", "*&to=joe&su=test+email"),

    # allow pluses in user name
    ("mailto:joe+2?Subject=test email", "*&to=joe%2B2&su=test+email"),

    ("mailto:joe?cc=sue@example.com", "*&to=joe&cc=sue%40example.com"),
    ("mailto:joe?cc=sue@example.com,fred",
     "*&to=joe&cc=sue%40example.com%2Cfred"),

    ("mailto:joe?bcc=sue@example.com", "*&to=joe&bcc=sue%40example.com"),
    ("mailto:joe?bcc=sue@example.com,fred",
     "*&to=joe&bcc=sue%40example.com%2Cfred"),



    ("", "https://mail.google.com/mail/b/me"),

    ("mailto:joe?attach=file.txt",
     "https://mail.google.com/mail/b/me#drafts/"),

    ("mailto:joe", "*&to=joe"),
    ("mailto:joe", "*&to=joe"),
 ]


def check_urlgen(input, output):
        gm = gnomegmail.GMailURL(input, "me", False)
        GmUrl = gm.gmail_url()
        nose.tools.eq_(GmUrl, re.sub('^\*', baseGmailURL, output, 1))


def test_urlgen():
    for (sin, sout) in testCaseStrings:
        yield(check_urlgen, sin, sout)
