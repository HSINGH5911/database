import socket

HOST = "127.0.0.1"
PORT = 6379

print("Connected to Redis-like socket server.")
print("Commands: PING, SET <key> <val>, GET <key>, DEL <key>, EXISTS <key>, INCR <key>, DECR <key>, APPEND <key> <val>")
print("Type 'exit' or 'quit' to close the client.\n")

while True:
    try:
        user_input = input("redis-cli> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        # The server closes the socket after each command, 
        # so we establish a new connection for each request.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        client.send(user_input.encode())
        
        response = client.recv(1024)
        print(response.decode())
        client.close()
    except KeyboardInterrupt:
        print("\nExiting.")
        break
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Make sure socket_server is running.")
    except Exception as e:
        print(f"Error: {e}")
