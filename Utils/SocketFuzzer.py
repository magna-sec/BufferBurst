import socket
from time import sleep

from Utils.FancyPrint import fancy_print
from Utils.MsgEnums import MsgEnums


def socket_fuzz(ip:str, port:int, amount:int, pre_string:str) -> str:
	"""
	"""
	# Must be a better way to do this
	if(amount == None or amount == 0): amount = 100
	if(pre_string == None): pre_string = ""


	string = pre_string + "A" * amount
	timeout = 5

	while True:
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.settimeout(timeout)
				s.connect((ip, port))
				s.recv(1024)
				fancy_print("Fuzzing",  str(len(string) - len(pre_string)) + " bytes")
				s.send(bytes(string, "latin-1"))
				s.recv(1024)
		except:
			fancy_print("Fuzzing Crashed At", str(len(string) - len(pre_string)) + " bytes", MsgEnums.INFO.value)
			return str(len(string) - len(pre_string))
		string += amount * "A"
		sleep(1)