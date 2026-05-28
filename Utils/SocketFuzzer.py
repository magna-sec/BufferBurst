import socket
from time import sleep
from subprocess import check_output

from Utils.FancyPrint import fancy_print
from Utils.MsgEnums import MsgEnums


def socket_fuzz(ip:str, port:int, fuzz_amount:int, pre_string:str) -> int:
    timeout = 5

    if fuzz_amount is None or fuzz_amount == 0:
        fuzz_amount = 100
    amount = fuzz_amount

    while True:
        pattern = check_output(f"msf-pattern_create -l {amount}", shell=True).decode()
        string = pre_string + pattern
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.recv(1024)
                fancy_print("Fuzzing", str(amount) + " bytes")
                s.send(bytes(string, "latin-1"))
                s.recv(1024)
        except:
            fancy_print("Fuzzing Crashed At", str(amount) + " bytes", MsgEnums.INFO.value)
            return amount

        amount += fuzz_amount
        sleep(1)
