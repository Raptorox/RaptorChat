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

client_names = []
client_sockets = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'{Fore.YELLOW}[*] Listening as {SERVER_HOST}:{SERVER_PORT}{Fore.RESET}')

def listenForClients(client_sock, client_addr):
    pend_exit = False
    while not pend_exit:
        msg = ''
        try:
            msg = client_sock.recv(1024).decode()
            if msg.startswith('/exit'):
                client_names.remove(msg.split()[-1])
                print(f'{Fore.RED}[-] {msg.split()[-1]} {client_addr} has disconnected{Fore.RESET}')
                msg = f'[-] {msg.split()[-1]} has disconnected'
                client_sockets.remove(client_sock)
                client_sock.close()
                pend_exit = True
            elif msg.startswith('[NAME_REQ]'):
                name = msg.split()[-1]
                msg = ''
                if name in client_names:
                    client_sock.send('NAME_TAKEN'.encode())
                else:
                    client_sock.send('OK'.encode())
                    client_names.append(name)
                    print(f'{Fore.LIGHTGREEN_EX}[+] {client_addr} has acquired name "{name}"{Fore.RESET}')
        except Exception as e:
            print(f'{Fore.RED}[!] Error: {e}{Fore.RESET}')
            client_sockets.remove(client_sock)
        for client_socket in client_sockets:
            if msg != '':
                client_socket.send(msg.encode())

while True:
    try:
        client_socket, client_address = s.accept()
        print(f'{Fore.LIGHTGREEN_EX}[+] New connection from {client_address}{Fore.RESET}')
        client_sockets.add(client_socket)
        t = Thread(target=listenForClients, args=(client_socket,client_address,))
        t.daemon = True
        t.start()
    except KeyboardInterrupt:
        print(f'{Fore.RED}[!] Exiting...{Fore.RESET}')
        for client_sock in client_sockets:
            client_sock.send(f'[!!!] Server stopped, connection lost'.encode())
            client_sock.close()
        break
