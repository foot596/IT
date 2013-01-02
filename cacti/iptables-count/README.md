Iptables Count
==============

Installation
------------

1. Add rules (with mark like `0xd01`,  `0xd02` and so on...)

    $ sudo iptables -t mangle -I OUTPUT 1 -p tcp -d <ip address> --dport <port> -j MARK --set-mark 0xd02

2. Copy `get-count-snmp.pl` to `/usr/local/bin`

3. Add pass string to `/etc/snmp/snmpd.conf`

    pass .1.3.6.1.4.1.2021.3027 /usr/local/bin/get-count-snmp.pl

4. Test

    $ snmpwalk -c <community> <hostname> .1.3.6.1.4.1.2021.3027
