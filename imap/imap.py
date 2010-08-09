#!/usr/bin/python

import imaplib


imapObj = imaplib.IMAP4_SSL( "imap.gmail.com" )

imapObj.login( "dsteele", "agendick" )

imapObj.select()

typ, data = imapObj.search(None, 'ALL')

#for num in data[0].split():
#	typ, data = imapObj.fetch(num, '(RFC822)')
#	print 'Message %s\n%s\n' % (num, data[0][1])

print imapObj.getannotation( "", "*", "/" )


imapObj.close()

imapObj.logout()
