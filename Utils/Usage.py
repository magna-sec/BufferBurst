import argparse
from collections import namedtuple


def parse_args():
    parser = argparse.ArgumentParser(description="Semi-automate stack-based buffer overflows")
    parser.add_argument('-i', '--ip',       metavar='IP',       type=str, required=True,  help='Target IP address')
    parser.add_argument('-p', '--port',     metavar='PORT',     type=int, required=True,  help='Target port')
    parser.add_argument('-t', '--type',     metavar='TYPE',     type=str, required=True,  choices=['http', 'socket'], help='Protocol (http or socket)')
    parser.add_argument('-T', '--template', metavar='TEMPLATE', type=str, required=False, help='Path to HTTP request template (required for --type http). Use * as the payload placeholder.')
    parser.add_argument('-P', '--prefix',   metavar='PREFIX',   type=str, required=False, help='Socket prefix string prepended to each send')
    parser.add_argument('-f', '--fuzz',     metavar='FUZZ',     type=int, required=False, help='Bytes to increment per fuzz step (default 100)')
    parser.add_argument('-d', '--debugger', metavar='DEBUGGER', type=str, default='windbg', choices=['windbg'], help='Debugger to use (default: windbg)')
    parser.add_argument('-v', '--verbose',  action='store_true',          help='Verbose output')

    args = parser.parse_args()

    if args.type == 'http' and not args.template:
        parser.error("--template is required when using --type http")

    template_content = ""
    if args.template:
        try:
            with open(args.template, "r", encoding="utf-8") as f:
                raw = f.read()
            # Normalise line endings to CRLF for HTTP
            template_content = raw.replace("\r\n", "\n").replace("\n", "\r\n")
        except OSError as e:
            parser.error(f"Cannot read template file: {e}")

    if args.prefix is None:
        args.prefix = ""

    Target = namedtuple("target", ["ip", "port", "type", "prefix", "fuzz_amount", "verbose", "template", "debugger"])
    return Target(args.ip, args.port, args.type, args.prefix, args.fuzz, args.verbose, template_content, args.debugger)
