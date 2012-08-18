#!/usr/bin/python -tt

import unittest
import re

import sys
sys.path.append( '.' )

import gnomegmail

baseGmailURL = "https://mail.google.com/mail?view=cm&tf=0&fs=1"

testCaseStrings = [
( "mailto:joe", "https://mail.google.com/mail?view=cm&tf=0&fs=1&to=joe" ),
( "Mailto:joe", "*&to=joe" ),
( "joe", "*&to=joe" ),
( "joe@example.com", "*&to=joe%40example.com" ),
( "mailto:Joe", "*&to=Joe" ),
( "mailto:joe,sue", "*&to=joe%2Csue" ),
( "mailto:joe@example.com,sue@example.com", "*&to=joe%40example.com%2Csue%40example.com" ),
( "mailto:joe%40example.com", "*&to=joe%40example.com" ),
( "mailto:joe@example.com,%20sue@example.com", "*&to=joe%40example.com%2C+sue%40example.com" ),
( "mailto:joe@example.com, sue@example.com", "*&to=joe%40example.com%2C+sue%40example.com" ),

( "mailto:joe?subject=test%20email", "*&to=joe&su=test+email" ),
( "mailto:joe@example.com?subject=test%20email", "*&to=joe%40example.com&su=test+email" ),
( "mailto:joe?subject=test+email", "*&to=joe&su=test+email" ),
( "mailto:joe?subject=test email", "*&to=joe&su=test+email" ),
( "mailto:joe?SUBJECT=test email", "*&to=joe&su=test+email" ),
( "mailto:joe?Subject=test email", "*&to=joe&su=test+email" ),

( "mailto:joe?cc=sue@example.com", "*&to=joe&cc=sue%40example.com" ),
( "mailto:joe?cc=sue@example.com,fred", "*&to=joe&cc=sue%40example.com%2Cfred" ),

( "mailto:joe?bcc=sue@example.com", "*&to=joe&bcc=sue%40example.com" ),
( "mailto:joe?bcc=sue@example.com,fred", "*&to=joe&bcc=sue%40example.com%2Cfred" ),

( "mailto:joe?body=test message", "*&to=joe&body=test+message" ),
( "mailto:joe?body=test+message", "*&to=joe&body=test+message" ),
( "mailto:joe?body=test%20message", "*&to=joe&body=test+message" ),
( "mailto:joe?body=test%0Amessage", "*&to=joe&body=test%0Amessage" ),
( "mailto:joe?body=test%0amessage", "*&to=joe&body=test%0Amessage" ),

( "mailto:joe?cc=sue&bcc=fred&body=the body&subject=the subject", "*&to=joe&su=the+subject&body=the+body&cc=sue&bcc=fred" ),
( "mailto:joe?bcc=fred&body=the body&subject=the subject&cc=sue", "*&to=joe&su=the+subject&body=the+body&cc=sue&bcc=fred" ),


( "", "https://mail.google.com/" ),

( "mailto:joe?attach=file.txt", "https://mail.google.com/mail/#drafts/" ),

( "mailto:joe", "*&to=joe" ),
( "mailto:joe", "*&to=joe" ),
 ]

class TestURLCase( unittest.TestCase ):
	def __init__( self, mailtoURL, gmailURL ):

		unittest.TestCase.__init__(self,'testRun')

		self.mailtoURL = mailtoURL
		self.gmailURL = gmailURL

	def testRun( self ):
		cfg = gnomegmail.ConfigInfo()
		gm = gnomegmail.GMailURL( self.mailtoURL, cfg, False )
		GmUrl = gm.gmail_url( )
		#GmDict = gnomegmail.mailto2dict( self.mailtoURL )
		#GmUrl = gnomegmail.simpledict2url( GmDict )
		self.assertEqual( GmUrl, self.gmailURL )

if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest( TestURLCase( "joe", "https://mail.google.com/mail?view=cm&tf=0&fs=1&to=joe" ) )

	for ( mto, gm ) in testCaseStrings:
		gmr = re.sub( '^\*', baseGmailURL, gm, 1 )
		suite.addTest( TestURLCase( mto, gmr ) )

	unittest.TextTestRunner().run(suite)

