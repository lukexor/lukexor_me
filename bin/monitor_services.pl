#!/usr/bin/env perl

use strict;
use warnings;

use IO::Socket;

my @downservice = ();
my @services = ( 'redis-server', 'apache2', 'mysql' );

print "Checking status of services: @services\n";

SERVICE: foreach my $service (@services) {
    my $status = `/bin/ps cax | /bin/grep $service`;

    if (!$status) {
        push (@downservice, $service);
    }
}

if ( scalar @downservice > 1 )
{
    print "The following services are down: @downservice\n";
    print "Sending email alert...\n";

    open my $MAIL, "|/usr/sbin/sendmail -t"
        or die "Failed to open sendmail: $!";

        print $MAIL "To: lukexor\@gmail.com\n";
        print $MAIL "From: noreply\@lukexor.me\n";
        print $MAIL "Subject: lukexor.me Service Alert\n";
        print $MAIL "The following services are down:\n";
        SERVICE: foreach my $service (@downservice)
        {
            print $MAIL "- $service\n";
        }

    close $MAIL
        or die "Failed to close sendmail: $!";
}

print "Done\n\n";
exit 0;
