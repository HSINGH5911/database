import time
import queue

class ConnectionState:
    """Encapsulates per-client connection state."""
    def __init__(self, conn_id=0):
        self.conn_id = conn_id
        self.client_socket = None
        self.address = None
        self.name = ""
        self.db_index = 0
        self.authenticated = False
        self.connected_at = 0
        self.last_active = 0
        self.subscriptions = set()

    def reset(self):
        """Resets connection state before returning to pool."""
        self.client_socket = None
        self.address = None
        self.name = ""
        self.db_index = 0
        self.authenticated = False
        self.connected_at = 0
        self.last_active = 0
        self.subscriptions.clear()


class ConnectionPool:
    """Pool for recycling ConnectionState objects."""
    def __init__(self, max_size=500):
        self.pool = queue.Queue(maxsize=max_size)
        for i in range(max_size):
            self.pool.put(ConnectionState(conn_id=i + 1))

    def acquire(self, client_socket, address):
        """Checks out a state object from the pool."""
        try:
            state = self.pool.get_nowait()
        except queue.Empty:
            state = ConnectionState()

        state.client_socket = client_socket
        state.address = address
        state.connected_at = time.time()
        state.last_active = time.time()
        return state

    def release(self, state):
        """Resets and returns state object to pool."""
        if state:
            state.reset()
            try:
                self.pool.put_nowait(state)
            except queue.Full:
                pass


class ConnectionManager:
    """Manages active connections and pooled states."""
    def __init__(self, pool_size=500):
        self.active_connections = {}  
        self.pool = ConnectionPool(max_size=pool_size)

    def register(self, client_socket, address):
        state = self.pool.acquire(client_socket, address)
        self.active_connections[client_socket] = state
        return state

    def unregister(self, client_socket):
        state = self.active_connections.pop(client_socket, None)
        if state:
            self.pool.release(state)
        return state

    def get_state(self, client_socket):
        return self.active_connections.get(client_socket)

    def active_count(self):
        return len(self.active_connections)