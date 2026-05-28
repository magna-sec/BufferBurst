import platform
from random import choice as rchoice
from ipaddress import ip_address as check_ip

from Utils.FancyPrint import fancy_print
from Utils.MsgEnums import MsgEnums

CURSOR_COLOURS = ["bg_black", "bg_blue", "bg_cyan", "bg_gray", "bg_green",
                  "bg_purple", "bg_red", "bg_yellow", "fg_black", "fg_blue",
                  "fg_cyan", "fg_gray", "fg_green", "fg_purple", "fg_red",
                  "fg_yellow"]
CURSOR_TYPE = ["bold", "italics", "standout", "underline"]
CONFIRM = ["yes", "no"]


def get_register(register:str) -> str:
    fancy_print(f"Please Provide the {register} value: ", msg_type=MsgEnums.QUESTION.value, endl="")
    return input()


def restart_service():
    fancy_print("Please restart the service, press enter when done!", msg_type=MsgEnums.QUESTION.value, endl="")
    input()


def confirmation() -> bool:
    choice = display_menu(CONFIRM)
    return choice == 0


def display_menu(menu:list) -> int:
    if platform.system() == "Linux":
        from simple_term_menu import TerminalMenu
        terminal_menu = TerminalMenu(menu, menu_cursor_style=(rchoice(CURSOR_COLOURS), rchoice(CURSOR_TYPE)))
        return terminal_menu.show()

    # Fallback for non-Linux platforms
    for i, item in enumerate(menu):
        print(f"  [{i}] {item}")
    fancy_print("Enter number: ", msg_type=MsgEnums.QUESTION.value, endl="")
    while True:
        try:
            idx = int(input())
            if 0 <= idx < len(menu):
                return idx
        except ValueError:
            pass
        fancy_print("Invalid choice, try again: ", msg_type=MsgEnums.QUESTION.value, endl="")


def get_ip() -> str:
    ip = ""
    while not ip:
        fancy_print("Enter LHOST IP for Reverse Shell: ", msg_type=MsgEnums.QUESTION.value)
        in_ip = input()
        try:
            check_ip(in_ip)
            ip = in_ip
        except ValueError:
            fancy_print("Incorrect Format! \nExpects X.X.X.X", msg_type=MsgEnums.WARNING.value)
    return ip


def get_port() -> int:
    while True:
        fancy_print("Enter LHOST Port for Reverse Shell: ", msg_type=MsgEnums.QUESTION.value)
        in_port = input()
        try:
            in_port = int(in_port)
            if 0 <= in_port <= 65535:
                return in_port
            fancy_print("Port number must be between 0 and 65535.", msg_type=MsgEnums.WARNING.value)
        except ValueError:
            fancy_print("Invalid input. Please enter a valid port number.", msg_type=MsgEnums.WARNING.value)
