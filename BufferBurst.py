
from Utils.FancyPrint import fancy_print, show_target
from Utils.MsgEnums import MsgEnums
from Utils.Usage import parse_args
from Utils.SocketFuzzer import socket_fuzz
from Utils.CreateExploit import CreateExploit


from Templates.Debuggers import windbg_bof

def main():
    target = parse_args()

    # Print the values
    show_target(target.ip, target.port, target.type)

    new_exploit = CreateExploit(target, windbg_bof)
    new_exploit.start()

   

if __name__ == "__main__":
    main()