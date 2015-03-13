#!/usr/bin/perl
use strict;
use warnings;
use Math::BigFloat;
use Data::Dumper;
$Data::Dumper::Indent = 1;
$Data::Dumper::Sortkeys = 1;

# TODO: Use Sys::Info::Device::CPU to get CPU count.
my $cpu_count = 1;

my @groups = (
    {name => 'oracle', regexp => qr/(ora.*|\/home\/app\/oracle\/product\/11.2.0\/db_1)/i},
    {name => 'firefox', regexp => qr/firefox/},
    {name => 'opera', regexp => qr/opera/}
);

for(my $i = 0; $i <= $#groups; $i++) {
    $groups[$i]{cpu} =  Math::BigFloat->new(0);
}

my $group_other =  Math::BigFloat->new(0);

#print Dumper(@groups);

sub trim { my $s = shift; $s =~ s/^\s+|\s+$//g; return $s };

my @process_command = `/bin/ps axwwwho command:100,pcpu`;

for my $el (@process_command) {

    my $comm = trim(substr($el, 0, 100));
    my $cpu = Math::BigFloat->new(trim(substr($el, 101, 110)));

    my $found_flag = 0;

    for(my $i = 0; $i <= $#groups; $i++) {
        if($comm =~ $groups[$i]{regexp} && $found_flag == 0) {
#            printf($groups[$i]{name} . " \t: adding " . $cpu . " \tcommand " . $comm . "\n");
            $groups[$i]{cpu} += $cpu;
            $found_flag = 1;
        }
    }

    if($found_flag == 0) {
#        printf("other \t: adding " . $cpu . " \tcommand " . $comm . "\n");
        $group_other += $cpu;
    }
}
#print Dumper(@groups);

for(my $i = 0; $i <= $#groups; $i++) {
    printf($groups[$i]{name} . ":%.2f ", $groups[$i]{cpu} / $cpu_count);
}

printf("other:%.2f\n", $group_other / $cpu_count);

exit(0);

