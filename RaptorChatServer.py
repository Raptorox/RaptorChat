import socket
from colorama import Fore, init
from threading import Thread

init()

SERVER_HOST = '0.0.0.0'
print(f'{Fore.YELLOW}[?] Enter the port to host the server on: {Fore.RESET}', end='')
SERVER_PORT = int(input())
separator_token = '<SEP>'

client_sockets = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'{Fore.YELLOW}[*] Listening as {SERVER_HOST}:{SERVER_PORT}{Fore.RESET}')

def listen_for_clients(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f'{Fore.RED}[!] Error: {e}{Fore.RESET}')
            for client_socket in client_sockets:
                client_socket.send(f'{Fore.RED}[!] Error: {e}{Fore.RESET}'.encode())
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ': ')
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_socket, client_address = s.accept()
    print(f'{Fore.LIGHTGREEN_EX}[+] {client_address} has connected{Fore.RESET}')
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_clients, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()
s.close()