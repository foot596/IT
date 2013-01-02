#!/usr/bin/perl
use strict;

my $place = ".1.3.6.1.4.1.2021.3027";
my $req = $ARGV[1];
my $ret;
my $item;
my @data = `iptables -t mangle -vxnL | grep "MARK"`;
my @finalData;
my @finalDataUnsorted;


my $i = 0;
foreach $item (@data) {
  chomp $item;
  if ($item =~ /^\s*(\d+)\s+(\d+)\s+MARK\s+tcp\s+--\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+tcp\s+(\S+)\s+MARK\s+set\s+0xd(\d+)/) {
#    print $item."\n";
    push @finalDataUnsorted, {id => int($6), name => "$4_$5", count => ($2 % 4294967295)};
  }
}

my @finalData =  sort { $a->{id} <=> $b->{id} } @finalDataUnsorted;

#print join "\n", map {$_->{id}." - ".$_->{name}." - ".$_->{count}} @finalData;
#print "\nSize: ".($#finalData + 1)."\n";

if ($ARGV[0] eq "-n") {
  if ($req eq  "$place") {
    if (0 <= $#finalData) {
      $ret = "$place.1.1";
    } else {
      exit 0;
    }
  } elsif ($req =~ m/^$place\.(\d+)$/) {
    if ($1 > 0 && $1 <= 4) {
      $ret = "$place.$1.1";
    } else {
      exit 0;
    }
  } elsif ($req =~ m/^$place\.(\d+)\.(\d+)$/) {
    if ($1 > 0 && $1 <= 4 && $2 < $#finalData + 1) {
      $ret = "$place.$1.".($2 + 1);
    } elsif ($1 > 0 && $1 < 4 && $2 == $#finalData + 1) {
      $ret = "$place.".($1 + 1).".1";
    } else {
      exit 0;
    }
  } else {
    exit 0;
  }

} else {
  $ret = $req;
}

if ($ret =~ m/$place\.(\d+)\.(\d+)/) {
  if ($1 == 1 && $2 > 0 && $2 <= $#finalData+1 ) {
    printf ("%s\ninteger\n%s\n", $ret, $2);
    exit 0;
  } elsif ($1 == 2 && $2 > 0 && $2 <= $#finalData+1 ) {
    printf ("%s\nstring\n%s\n", $ret, $finalData[$2-1]->{name});
    exit 0;
  } elsif ($1 == 3 && $2 > 0 && $2 <= $#finalData+1 ) {
    printf ("%s\ncounter\n%s\n", $ret, $finalData[$2-1]->{count});
    exit 0;   
  } elsif ($1 == 4 && $2 > 0 && $2 <= $#finalData+1 ) {
    printf ("%s\ninteger\n%s\n", $ret, $finalData[$2-1]->{id});
    exit 0;
  } else {
    print "string\nack... $ret $req\n";
    exit 0;
  }
}

exit 0;

