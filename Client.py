import socket

host = "192.168.0.105"
port = 7777


s = socket.socket()
s.connect((host, port))

# received the banner
data = s.recv(1024)
# print banner
print(data.decode().strip())

while True:
    #let get our input from the user
    user_input = input("").strip()

    s.sendall(user_input.encode())
    reply = s.recv(1024).decode().strip()
    if "Correct" in reply:
        print(reply)
        break
    print(reply)
    continue
s.close()
