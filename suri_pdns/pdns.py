#!/usr/bin/env pypy
''' suri_eve_pdns
Parse eve-dns.json events into PDNS data files.
'''
import re
import csv
import json
from collections import Counter
from datetime import datetime
from calendar import timegm

from suri_logging import LOGGER, add_args, setup_logging

PDNS_COLUMNS = ('timestamp', 'dns-client', 'dns-server', 'RR class', 'Query', 
    'Query Type', 'Answer', 'TTL', 'Count')


def convert_ts(timestamp):
    ''' Much quicker than stdlib version for fixed length timestamp formats '''
    dt = datetime(
        year=int(timestamp[0:4]),
        month=int(timestamp[5:7]),
        day=int(timestamp[8:10]),
        hour=int(timestamp[11:13]),
        minute=int(timestamp[14:16]),
        second=int(timestamp[17:19]),
        microsecond=int(timestamp[20:26]),
    )
    secs = timegm(dt.utctimetuple())
    return '%d.%06d' % (secs, dt.microsecond)


def build_pdns_row(timestamp, data):
    row = []
    ts = convert_ts(timestamp)
    return (
        ts, '', '', '', 
        str(data.get('rrname', '')), str(data.get('rrtype', '')),
        str(data.get('rdata', '')), str(data.get('ttl', ''))
    )


def parse_f(f, re_exclude=None):
    logs = Counter()
    for full_line in f:
        # strip out 0x0a in case newline was not stripped correctly
        line = full_line.replace('\x0a', '').strip()
        try:
            line_data = json.loads(line)
        except ValueError as e:
            LOGGER.error('%s: %s\nLine: %s' % (e.__class__.__name__, e, line))
            continue
        data = line_data['dns']
        if data['type'] != 'answer':
            continue
        rrname = data.get('rrname')
        if re_exclude is not None and rrname and re_exclude.match(rrname):
            continue
        pdns_row = build_pdns_row(line_data['timestamp'], data)
        logs.update([pdns_row])
    return logs


def parse(path, exclude=None):
    if exclude is not None:
        re_exclude = exclude_regex(exclude)
        LOGGER.debug('Compiled exclusion regex')
    else:
        re_exclude = None
    with open(path) as f:
        return parse_f(f, re_exclude=re_exclude)


def exclude_regex(arg):
    LOGGER.debug('Compiling exclusion regex')
    return re.compile(arg)


def write_logs(output, logs):
    with open(output, 'w') as f:
        for row, ct in logs.items():
            writerow = row + (str(ct),)
            f.write('||'.join(writerow)+'\n')
    return output


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('suricata_log', help='suricata JSON log path')
    parser.add_argument('--output', '-o', default='eve-dns.log')
    parser.add_argument('--exclude', '-x', help='exclude certain rrnames '
        'based on regex. eg ^(.*\.)?mydomain(\.(com|net|org))?$')
    add_args(parser)
    args = parser.parse_args()
    setup_logging(args=args)
    logs = parse(args.suricata_log, exclude=args.exclude)
    log_path = write_logs(args.output, logs)
    LOGGER.info('Wrote DNS logs to %s' % log_path)


if __name__ == '__main__':
    main()
