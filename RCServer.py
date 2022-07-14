import socket
import json
from colorama import Fore, init
from threading import Thread

init()

with open('RCConfig.json', 'r') as f:
	SERVER_PORT = json.load(f)['srv_port']

SERVER_HOST = '0.0.0.0'
#print(f'{Fore.YELLOW}[?] Enter the port to host the server on: {Fore.RESET}', end='')
#SERVER_PORT = int(input())

client_sockets = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'{Fore.YELLOW}[*] Listening as {SERVER_HOST}:{SERVER_PORT}{Fore.RESET}')

def listenForClients(cs, ca):
	pendExit = False
	while True:
		try:
			msg = cs.recv(1024).decode()
			if '/exit' in msg:
				print(f'{Fore.RED}[-] {msg.split()[1]} {ca} has disconnected{Fore.RESET}')
				msg = f'[-] {msg.split()[1]} has disconnected'
				client_sockets.remove(cs)
				cs.close()
				pendExit = True
		except Exception as e:
			print(f'{Fore.RED}[!] Error: {e}{Fore.RESET}')
			client_sockets.remove(cs)
		for client_socket in client_sockets:
			client_socket.send(msg.encode())
		if pendExit:
			exit()

while True:
	client_socket, client_address = s.accept()
	print(f'{Fore.LIGHTGREEN_EX}[+] {client_address} has connected{Fore.RESET}')
	client_sockets.add(client_socket)
	t = Thread(target=listenForClients, args=(client_socket,client_address,))
	t.daemon = True
	t.start()