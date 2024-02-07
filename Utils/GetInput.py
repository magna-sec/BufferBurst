from simple_term_menu import TerminalMenu
from random import choice as rchoice


from Utils.FancyPrint import fancy_print
from Utils.MsgEnums import MsgEnums

CURSOR_COLOURS = ["bg_black", "bg_blue" ,"bg_cyan", "bg_gray", "bg_green"
                  , "bg_purple", "bg_red", "bg_yellow", "fg_black", "fg_blue"
                  , "fg_cyan" , "fg_gray", "fg_green", "fg_purple", "fg_red"
                  , "fg_yellow" 
                  ]
CURSOR_TYPE = ["bold", "italics", "standout", "underline"]
CONFIRM = ["yes", "no"]

### Yeah... i was gonna make his more complex
def get_register(register:str) -> str:
    """
    """
    fancy_print(f"Please Provide the {register} value: ", msg_type=MsgEnums.QUESTION.value, endl="")
    user_input = input()
    return user_input


def restart_service():
    # WILL BE MORE TO THIS WHEN MORE DEBUGGERS ARE ADDED
    fancy_print("Please restart the service, press enter when done!", msg_type=MsgEnums.QUESTION.value, endl="")
    input()


def confirmation():
    """
    """
    choice = display_menu(CONFIRM)
    # 0 = yes, 1 = no
    if(choice == 0): return True
    else: return False


# Literally just displaying, don't need to look at it.
def display_menu(menu:list) -> str:
    """
    """
    # Constructor for the TerminalMenu class is given random item for colour and type
    terminalMenu = TerminalMenu(menu, menu_cursor_style=(rchoice(CURSOR_COLOURS), rchoice(CURSOR_TYPE)))
    menuEntryIndex = terminalMenu.show()

    return menuEntryIndex