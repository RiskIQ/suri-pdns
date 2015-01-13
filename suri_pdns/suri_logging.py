''' suri_logging
Logging for suri scripts
'''

import sys
import logging

# Python stdlib loggers are generally global or used as instance attributes
global LOGGER
LOGGER = logging.getLogger('suri_eve')

def setup_logging(args=None, path=None, level='error', test_mode=False):
    if args is not None:
        return setup_logging(path=args.log_path, level=args.log_level, 
            test_mode=args.log_test)
    global LOGGER
    if path == '-':
        def log_stderr(error_level):
            ''' Custom logger to stderr '''
            def error_level_logger(msg):
                print >>sys.stderr, '[LOG] %s: %s' % (error_level, msg)
            return error_level_logger

        class Logger(object):
            pass
        LOGGER = Logger()
        LOGGER.error = log_stderr('ERROR')
        LOGGER.critical = log_stderr('CRITICAL')
        LOGGER.warning = log_stderr('WARNING')
        LOGGER.info = log_stderr('INFO')
        LOGGER.debug = log_stderr('DEBUG')
    else:
        if test_mode:
            path = './debug.log'
        log_level = getattr(logging, level.upper())
        LOGGER.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s]: %(message)s',
        )
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(log_level)
        LOGGER.addHandler(file_handler)
        LOGGER.addHandler(stream_handler)

def add_args(parser):
    parser.add_argument('--log-path', '-l', 
        default='./suri_pdns.log', 
        help='path to log file')
    parser.add_argument('--log-level', '-L',
        default='error', help='log level (default error)')
    parser.add_argument('--log-test', '-t', action='store_true',
        help='logging debug mode (output all to stdout)')
