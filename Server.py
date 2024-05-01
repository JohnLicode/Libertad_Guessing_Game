import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
Choose your difficulty:
1. Easy (1-50)
2. Moderate (1-100)
3. Hard (1-500)
Enter your difficulty number:"""

def generate_random_int(difficulty):
    if difficulty == '1':
        return random.randint(1, 50)
    elif difficulty == '2':
        return random.randint(1, 100)
    elif difficulty == '3':
        return random.randint(1, 500)
    else:
        return random.randint(1, 100)  # Default to moderate difficulty

# Initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")
guessme = 0
conn = None

while True:
    if conn is None:
        print("Waiting for connection..")
        conn, addr = s.accept()
        print(f"New client: {addr[0]}")
        conn.sendall(banner.encode())
    else:
        client_input = conn.recv(1024)
        difficulty = client_input.decode().strip()
        if difficulty not in ['1', '2', '3']:
            conn.sendall(b"Invalid difficulty selection. Please enter a valid option.\n" + banner.encode())
            continue
        guessme = generate_random_int(difficulty)
        conn.sendall(banner.encode())
        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                with open("Lead board attempt.txt", "a") as record_file:
                    record_file.write(f"User's guess: {guess}, Result: Correct\n")
                conn.close()
                conn = None
                break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nenter guess: ")
                with open("Lead board attempt.txt", "a") as record_file:
                    record_file.write(f"User's guess: {guess}, Result: Lower\n")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nenter guess: ")
                with open("attempt_record.txt", "a") as record_file:
                    record_file.write(f"User's guess: {guess}, Result: Higher\n")