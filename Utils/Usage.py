import argparse
from collections import namedtuple

def parse_args():
    """
    """
    parser = argparse.ArgumentParser(description="Semi-Automate Stack based Overflows... atleast helps")
    parser.add_argument('-i', '--ip', metavar='IP', type=str, help='IP Address', required=True)
    parser.add_argument('-p', '--port', metavar='PORT', type=int, help='Port Number', required=True)
    parser.add_argument('-t', '--type', metavar='TYPE', type=str, choices=['http', 'socket'], help='Type (http or socket)', required=True)
    parser.add_argument('-pr', '--prefix', metavar='PREFIX', type=str, help='Prefix String', required=False)
    parser.add_argument('-f', '--fuzz', metavar='FUZZ', type=int, help='Fuzzing Amount', required=False)

    # Parse the arguments
    args = parser.parse_args()

    target_tuple = namedtuple("target", ["ip", "port", "type", "prefix", "fuzz_amount"])
    target = target_tuple(args.ip, args.port, args.port, args.prefix, args.fuzz)

    return target