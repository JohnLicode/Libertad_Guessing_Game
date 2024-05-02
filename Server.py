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

try:
    s.bind((host, port))
    s.listen(5)
    print(f"Server is listening on port {port}")

    while True:
        conn = None
        while conn is None:
            try:
                print("Waiting for connection..")
                conn, addr = s.accept()
                print(f"New client: {addr[0]}")
                conn.sendall(banner.encode())

                client_input = conn.recv(1024)
                difficulty = client_input.decode().strip()
                if difficulty not in ['1', '2', '3']:
                    conn.sendall(b"Invalid difficulty selection. Please enter a valid option.\n" + banner.encode())
                    conn.close()
                    continue

                # Client user name input
                conn.sendall(b"Enter your name: ")
                name = conn.recv(1024).decode().strip()

                # Determine leaderboard filename based on difficulty level
                if difficulty == '1':
                    leaderboard_filename = "leaderboard_easy_lvl.txt"
                elif difficulty == '2':
                    leaderboard_filename = "leaderboard_moderate_lvl.txt"
                else:
                    leaderboard_filename = "leaderboard_hard_lvl.txt"

                conn.sendall(b"The game is starting! Hit Enter\n")

                while True:
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
                            with open(leaderboard_filename, "a") as leaderboard_file:
                                leaderboard_file.write(f"{name}: {attempt_count} attempts\n")
                            break
                        elif guess > guessme:
                            conn.sendall(b"Guess Lower!\nEnter guess: ")
                        elif guess < guessme:
                            conn.sendall(b"Guess Higher!\nEnter guess: ")

            except socket.error as e:
                print(f"Socket error: {e}")
                if conn:
                    conn.close()
                continue

except socket.error as e:
    print(f"Socket error: {e}")
finally:
    s.close()
