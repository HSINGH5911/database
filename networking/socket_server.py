import socket
import threading
import time

from core.database import Database
from core.connection import ConnectionManager
from commands.registry import execute
from protocol.protocol import Protocol

HOST = "127.0.0.1"
PORT = 6379

db = Database()
conn_manager = ConnectionManager(pool_size=500)
protocol = Protocol()

def handle_client(client_socket, address):
    conn_state = conn_manager.register(client_socket, address)
    print(f"[+] Client connected: {address} (Active: {conn_manager.active_count()})")

    buffer = ""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"[-] Client disconnected: {address}")
                break

            buffer += data.decode("utf-8", errors="replace")
            
            command, args = protocol.parse_request(buffer)
            buffer = ""

            if command:
                conn_state.last_active = time.time()
                result = execute(command, db, args, client_socket=client_socket)
                
                response_str = protocol.serialize_response(result)
                client_socket.sendall(response_str.encode("utf-8"))

    except (ConnectionResetError, BrokenPipeError):
        print(f"[-] Client connection reset: {address}")
    except Exception as e:
        print(f"[!] Exception handling client {address}: {e}")
    finally:
        db.unsubscribe(client_socket)
        conn_manager.unregister(client_socket)
        client_socket.close()
        print(f"[*] Cleaned up connection: {address} (Active: {conn_manager.active_count()})")

def start_server(host=HOST, port=PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(128)

    print(f"[*] Multi-Threaded RESP Database Server listening on {host}:{port}")

    while True:
        try:
            client_socket, address = server.accept()
            worker_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )
            worker_thread.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down server.")
            break
        except Exception as e:
            print(f"[!] Accept error: {e}")
            break

    server.close()

if __name__ == "__main__":
    start_server()