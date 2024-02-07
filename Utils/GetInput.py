from Utils.FancyPrint import fancy_print
from Utils.MsgEnums import MsgEnums


### Yeah... i was gonna make his more complex
def get_register(register:str) -> str:
    """
    """
    fancy_print(f"Please Provide the {register.upper()} value:", msg_type=MsgEnums.QUESTION.value, endl="")
    user_input = input()
    return user_input


def restart_service():
    fancy_print(f"Please restart the service, press enter when done!", msg_type=MsgEnums.QUESTION.value, endl="")
    input()
