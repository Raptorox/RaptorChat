import sys
import socket
import tkinter as tk
from colorama import Fore, init
from datetime import datetime
from threading import Thread

init()

print(f'{Fore.YELLOW}[?] Enter server\'s IP address: {Fore.RESET}', end='')
SERVER_HOST = input()
print(f'{Fore.YELLOW}[?] Enter server\'s port: {Fore.RESET}', end='')
SERVER_PORT = int(input())
separator_token = '<SEP>'

s = socket.socket()
print(f'{Fore.YELLOW}[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...{Fore.RESET}')
s.connect((SERVER_HOST, SERVER_PORT))
print(f'{Fore.LIGHTGREEN_EX}[+] Connected!{Fore.RESET}')

print(f'{Fore.YELLOW}[?] Enter your name: {Fore.RESET}', end='')
name = input()
print(
    f'{Fore.YELLOW}[1] Blue{Fore.RESET}',
    f'{Fore.YELLOW}[2] Green{Fore.RESET}',
    f'{Fore.YELLOW}[3] Light Blue{Fore.RESET}',
    f'{Fore.YELLOW}[4] Light Black ???{Fore.RESET}',
    f'{Fore.YELLOW}[5] Cyan {Fore.RESET}',
    f'{Fore.YELLOW}[6] Light Cyan{Fore.RESET}',
    f'{Fore.YELLOW}[7] Light Magenta{Fore.RESET}',
    f'{Fore.YELLOW}[8] Light Red{Fore.RESET}',
    f'{Fore.YELLOW}[9] Light White ???{Fore.RESET}',
    f'{Fore.YELLOW}[10] White{Fore.RESET}',
    f'{Fore.YELLOW}[11] Magenta{Fore.RESET}',
    f'{Fore.YELLOW}[?] Choose user color: {Fore.RESET}',
    sep='\n',
    end=''
)

chosen_color = int(input())
client_color = None
if chosen_color == 1:
    client_color = Fore.BLUE
elif chosen_color == 2:
    client_color = Fore.GREEN
elif chosen_color == 3:
    client_color = Fore.LIGHTBLUE_EX
elif chosen_color == 4:
    client_color = Fore.LIGHTBLACK_EX
elif chosen_color == 5:
    client_color = Fore.CYAN
elif chosen_color == 6:
    client_color = Fore.LIGHTCYAN_EX
elif chosen_color == 7:
    client_color = Fore.LIGHTMAGENTA_EX
elif chosen_color == 8:
    client_color = Fore.LIGHTRED_EX
elif chosen_color == 9:
    client_color = Fore.LIGHTWHITE_EX
elif chosen_color == 10:
    client_color = Fore.WHITE
elif chosen_color == 11:
    client_color = Fore.MAGENTA
else:
    print('Unknown color code, restart the client')
    sys.exit()
s.send(f'{Fore.LIGHTGREEN_EX}[+] {client_color}{name}{Fore.LIGHTGREEN_EX} has connected{Fore.RESET}'.encode())

def listen_for_messages():
    while True:
        msg = s.recv(1024).decode()
        print('\n' + msg)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()


def sendText(event):
    to_send = entry.get()
    entry.delete(0, 'end')
    if to_send.lower() == '/exit':
        s.send(f'{Fore.RED}[-] {client_color}{name}{Fore.RED} has disconnected{Fore.RESET}'.encode())
        s.close()
        sys.exit()
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f'{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}'
    s.send(to_send.encode())
        
root = tk.Tk()
entry = tk.Entry()
entry.bind('<Return>', sendText)
entry.pack()
root.mainloop()