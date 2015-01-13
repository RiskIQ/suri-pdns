suri-pdns
=========

Parse suricata logs and output DNS data.

Usage::
    
    # Dump dns suricata json log into || delimited log (matches gamelinux format).
    $ suri-pdns eve-dns.json -x "^(.*\.)?riskiq(\.(com|net|org))?$" -o output.log
