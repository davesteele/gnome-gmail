#!/usr/bin/perl
#
    my $imap = new IMAP::Client();
    $imap->connect(PeerAddr => $server,
                  ConnectMethod => 'SSL STARTTLS PLAIN',
                  )
    or die "Unable to connect to [$server]: ".$imap->error();
