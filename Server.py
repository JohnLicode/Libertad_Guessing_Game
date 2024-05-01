import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game ==
Difficulty Level
1. Easy (1-50)
2. Moderate (1-100)
3. Hard (1-500)
Enter the difficulty corresponding number:"""


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
leaderboard = {}  # Store total attempts for each client

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

        #Client user name input
        conn.sendall(b"Enter your name: ")
        name = conn.recv(1024).decode().strip()

        conn.sendall(b"The game is starting! Hit Enter\n")
        guessme = generate_random_int(difficulty)
        conn.sendall(b"Guess the number: ")
        attempt_count = 0
        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            attempt_count += 1
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                # Update leaderboard
                if name in leaderboard:
                    leaderboard[name] += attempt_count
                else:
                    leaderboard[name] = attempt_count
                with open("leaderboard.txt", "w") as leaderboard_file:
                    for name, attempts in leaderboard.items():
                        leaderboard_file.write(f"{name}: {attempts} attempts\n")
                conn.close()
                conn = None
                break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nEnter guess: ")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nEnter guess: ")
