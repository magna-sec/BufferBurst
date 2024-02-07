from termcolor import cprint

from Utils.MsgEnums import MsgEnums


def show_target(ip:str, port:str, trgt_type:str):
    cprint("#### ", "green", end="")
    cprint("Target Details", "yellow", end="")
    cprint(" ####", "green")

    cprint("IP Address", "blue", end="")
    cprint(": ", "white", end="")
    cprint(ip, "yellow")

    cprint("Port", "blue", end="")
    cprint(": ", "white", end="")
    cprint(port, "yellow")
    
    cprint("Target Type", "blue", end="")
    cprint(": ", "white", end="")
    cprint(trgt_type, "yellow")

def fancy_print(pre_text:str, post_text:str="", msg_type:int=0, endl:str="\n"):
    """
    """
    # CHANGE THESE TO ENUM
    match msg_type:
        case MsgEnums.NORMAL.value:
            cprint("[+] ", "white", end="")
            cprint(pre_text, "blue", end="")
        case MsgEnums.WARNING.value:
            cprint("[!] ", "white", end="")
            cprint(pre_text, "red", end="")
        case MsgEnums.INFO.value:
            cprint("[I] ", "white", end="")
            cprint(pre_text, "green", end="")
        case MsgEnums.QUESTION.value:
            cprint("[?] ", "white", end="")
            cprint(pre_text, "yellow", end="")
        case default:
            cprint("[+] ", "white", end="")
            cprint(pre_text, "blue", end="")

    if(post_text):
        cprint(": ", "white", end="")      
        cprint(post_text, "yellow", end=endl)
    else:
        print()
      