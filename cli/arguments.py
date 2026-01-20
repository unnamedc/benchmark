import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='HTTP Server Availability Tester',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python bench.py -H https://ya.ru,https://google.com -C 5
  python bench.py -F hosts.txt -C 10 -O results.txt
        '''
    )
    
    hosts_group = parser.add_mutually_exclusive_group(required=True)
    hosts_group.add_argument(
        '-H', '--hosts',
        help='Comma-separated list of hosts (e.g., https://ya.ru,https://google.com)'
    )
    hosts_group.add_argument(
        '-F', '--file',
        help='Path to file with list of hosts (one per line)'
    )
    
    parser.add_argument(
        '-C', '--count',
        type=str,
        default='1',
        help='Number of requests per host (default: 1)'
    )
    parser.add_argument(
        '-O', '--output',
        help='Path to output file (default: console)'
    )
    
    return parser.parse_args()