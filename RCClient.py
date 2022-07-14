import socket
import time
import json
import tkinter as tk
from colorama import Fore, init
from datetime import datetime
from threading import Thread

init()

with open('RCConfig.json', 'r') as f:
	config = json.load(f)
	srv_port = config['srv_port']
	srv_addr = config['srv_addr']

print(f'{Fore.YELLOW}[?] Use the default server data? [{srv_addr}:{srv_port}] [y/n]: {Fore.RESET}', end='')
yorn = input()
if yorn == 'y':
	SERVER_HOST = srv_addr
	SERVER_PORT = srv_port
elif yorn == 'n':
	try:
		print(f'{Fore.YELLOW}[?] Enter server\'s IP address or address and port [ip:port]: {Fore.RESET}', end='')
		HOST_PORT = [x for x in input().split(':')]
		SERVER_HOST, SERVER_PORT = HOST_PORT
		SERVER_PORT = int(SERVER_PORT)
	except ValueError:
		SERVER_HOST = HOST_PORT[0]
		print(f'{Fore.YELLOW}[?] Enter server\'s port: {Fore.RESET}', end='')
		SERVER_PORT = int(input())

s = socket.socket()
print(f'{Fore.YELLOW}[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...{Fore.RESET}')
s.connect((SERVER_HOST, SERVER_PORT))
print(f'{Fore.LIGHTGREEN_EX}[+] Connected!{Fore.RESET}')

print(f'{Fore.YELLOW}[?] Enter your name: {Fore.RESET}', end='')
client_name = input()
#print(f'''{Fore.BLUE}[1] Blue
#{Fore.GREEN}[2] Green
#{Fore.LIGHTBLUE_EX}[3] Light Blue
#{Fore.LIGHTBLACK_EX}[4] Light Black
#{Fore.CYAN}[5] Cyan
#{Fore.LIGHTCYAN_EX}[6] Light Cyan
#{Fore.LIGHTMAGENTA_EX}[7] Light Magenta
#{Fore.LIGHTRED_EX}[8] Light Red
#{Fore.LIGHTWHITE_EX}[9] Light White
#{Fore.WHITE}[10] White
#{Fore.MAGENTA}[11] Magenta
#{Fore.YELLOW}[?] Choose user color: {Fore.RESET}''',
#    end=''
#)

#colors = [Fore.BLUE, Fore.GREEN, Fore.LIGHTBLUE_EX, Fore.LIGHTBLACK_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX,
#		  Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.WHITE, Fore.MAGENTA]
#chosen_color = None
#client_color = None
#while client_color is None:
#	try:
#		chosen_color = int(input())
#		if not (chosen_color >= 1 and chosen_color <= 11): raise ValueError
#		client_color = colors[chosen_color-1]
#	except (ValueError, IndexError):
#		print(f'{Fore.RED}[!] Unknown color code, enter a number in the range 1-11: {Fore.RESET}', end='')

#s.send(f'{Fore.LIGHTGREEN_EX}[+] {client_color}{client_name}{Fore.LIGHTGREEN_EX} has connected{Fore.RESET}'.encode())
s.send(f'[+] {client_name} has connected'.encode())

def listenForMessages(chat):
	while True:
		try:
			chat.configure(state='disabled')
			msg = s.recv(1024).decode()
			if msg[0] == '[':
				chat.configure(state='normal')
				chat.insert('end', f'\n{msg}')
				if int(chat.index('end')) == 25:
					chat.delete('1.0', '2.0')
				chat.configure(state='disabled')
		except:
			pass

def sendText(event):
    to_send = entry.get()
    entry.delete(0, 'end')
    if to_send.lower() == '/exit':
        #s.send(f'{Fore.RED}[-] {client_color}{client_name}{Fore.RED} has disconnected{Fore.RESET}'.encode())
        s.send(f'/exit {client_name}'.encode())
        exit()
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #s.send(f'{client_color}[{date_now}] {client_name}: {to_send}{Fore.RESET}'.encode())
    s.send(f'[{date_now}] {client_name}: {to_send}'.encode())
        
root = tk.Tk()
chat = tk.Text(root, bg='black', fg='#ccc')
entry = tk.Entry(root, bg='black', fg='#ccc')
entry.bind('<Return>', sendText)
chat.bind('<1>', lambda event: entry.focus_force())
entry.pack(fill='x')
chat.pack()

t = Thread(target=listenForMessages, args=(chat,))
t.daemon = True
t.start()

root.focus_force()
entry.focus_force()
root.mainloop()