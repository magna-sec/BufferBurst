
from Utils.FancyPrint import fancy_print, show_target
from Utils.MsgEnums import MsgEnums
from Utils.Usage import parse_args
from Utils.SocketFuzzer import socket_fuzz

def main():
    target = parse_args()

    # Print the values
    show_target(target.ip, target.port, target.type)
    socket_fuzz(target.ip, target.port, target.fuzz_amount, target.prefix)

if __name__ == "__main__":
    main()